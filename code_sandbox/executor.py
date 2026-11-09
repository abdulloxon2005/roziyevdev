"""
Python kodini alohida, resurslari cheklangan jarayonda bajaruvchi executor.

Himoya qatlamlari:
  1. Har bir ishga tushirish — yangi ``python -I -S -X utf8`` jarayoni (web-server
     jarayonida ``exec()`` yo'q). ``-I`` muhit o'zgaruvchilari, user-site va joriy
     papkani e'tiborsiz qoldiradi.
  2. Bo'sh muhit o'zgaruvchilari (SECRET_KEY, DB parollari va h.k. bola jarayonga o'tmaydi).
  3. Vaqtinchalik bo'sh ishchi papka (har ishga tushirishdan keyin o'chiriladi).
  4. Linux'da ``setrlimit``: CPU vaqti, virtual xotira, fayl hajmi, jarayonlar soni,
     ochiq fayllar soni; alohida sessiya (timeout'da butun guruh o'ldiriladi).
  5. Devor soati bo'yicha timeout (barcha platformalarda).
  6. Ishchi ichida audit-hook: tarmoq, yangi jarayon, fayl yozish, ctypes va h.k. taqiqlangan.
  7. Bir vaqtdagi ishga tushirishlar soni semafor bilan cheklangan.

Production'da bu executor alohida konteynerda (``code_sandbox/server.py``) ishlatilishi
tavsiya etiladi: tarmoqdan uzilgan, read-only fayl tizimi, ``no-new-privileges``,
cgroup xotira/CPU/PID limitlari bilan.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

from .worker import ERROR_MARKER

WORKER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'worker.py')

DEFAULT_LIMITS = {
    'timeout_seconds': 5.0,       # devor soati bo'yicha
    'cpu_seconds': 3,             # sof CPU vaqti (Linux)
    'memory_mb': 256,             # virtual xotira (Linux)
    'max_output_chars': 20_000,   # foydalanuvchiga qaytariladigan chiqish
    'max_file_bytes': 2 * 1024 * 1024,  # stdout/stderr fayllari uchun qattiq chegara (Linux)
    'max_source_chars': 100_000,
    'max_files': 30,
}

MAX_CONCURRENT_RUNS = int(os.environ.get('CODE_SANDBOX_MAX_CONCURRENT', '4'))
_slots = threading.BoundedSemaphore(MAX_CONCURRENT_RUNS)

IS_POSIX = os.name == 'posix'


class Status:
    OK = 'ok'                      # dastur xatosiz yakunlandi
    ERROR = 'error'                # dastur ishlash vaqtida xato berdi (exception)
    SYNTAX_ERROR = 'syntax_error'  # kod kompilyatsiya bo'lmadi
    TIMEOUT = 'timeout'            # vaqt chegarasi
    MEMORY = 'memory'              # xotira chegarasi
    OUTPUT_LIMIT = 'output_limit'  # chiqish hajmi chegarasi
    BUSY = 'busy'                  # bir vaqtda juda ko'p ishga tushirish
    INVALID = 'invalid'            # noto'g'ri so'rov (juda katta kod va h.k.)
    UNAVAILABLE = 'unavailable'    # sandbox ishlamayapti


def _make_preexec(limits):
    def preexec():  # pragma: no cover - faqat Linux'da bola jarayon ichida ishlaydi
        import resource
        os.setsid()
        cpu = int(limits['cpu_seconds'])
        mem = int(limits['memory_mb']) * 1024 * 1024
        fsize = int(limits['max_file_bytes'])
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 1))
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        resource.setrlimit(resource.RLIMIT_FSIZE, (fsize, fsize))
        resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        try:
            resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
        except (ValueError, OSError):
            pass
    return preexec


def _clean_env():
    env = {'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
    if os.name == 'nt':
        # Windows'da Python ishga tushishi uchun SYSTEMROOT zarur
        for key in ('SYSTEMROOT', 'SystemRoot'):
            if key in os.environ:
                env['SYSTEMROOT'] = os.environ[key]
                break
    return env


def _read_limited(fileobj, limit):
    fileobj.seek(0)
    data = fileobj.read(limit * 4 + 4)
    text = data.decode('utf-8', errors='replace')
    truncated = len(text) > limit
    return text[:limit], truncated


def _extract_error(stderr_text):
    if ERROR_MARKER not in stderr_text:
        return stderr_text, None
    head, _, tail = stderr_text.rpartition(ERROR_MARKER)
    line = tail.split('\n', 1)[0]
    try:
        info = json.loads(line)
    except ValueError:
        info = None
    return head, info


def result(status, stdout='', stderr='', error=None, elapsed_ms=0, truncated=False, exit_code=None):
    return {
        'status': status,
        'stdout': stdout,
        'stderr': stderr,
        'error': error,
        'elapsed_ms': elapsed_ms,
        'truncated': truncated,
        'exit_code': exit_code,
    }


def validate_job(code=None, files=None, entry='main.py', stdin='', limits=None):
    limits = {**DEFAULT_LIMITS, **(limits or {})}
    files = dict(files or {})
    if code is not None:
        files[entry] = code
    if entry not in files:
        return None, "Ishga tushiriladigan fayl topilmadi."
    if len(files) > limits['max_files']:
        return None, "Fayllar soni juda ko'p."
    total = sum(len(v or '') for v in files.values()) + len(stdin or '')
    if total > limits['max_source_chars']:
        return None, "Kod hajmi ruxsat etilgan chegaradan katta."
    for name, content in files.items():
        if not isinstance(name, str) or not isinstance(content, str):
            return None, "Fayl nomi yoki mazmuni noto'g'ri."
    return {'files': files, 'entry': entry, 'stdin': stdin or '', 'limits': limits}, None


def run_python(code=None, *, files=None, entry='main.py', stdin='', limits=None, python_executable=None):
    """
    Python kodini izolyatsiyalangan jarayonda bajaradi.

    Qaytaradi: dict(status, stdout, stderr, error{type,message,line,file}, elapsed_ms, truncated, exit_code)
    """
    job, problem = validate_job(code, files, entry, stdin, limits)
    if problem:
        return result(Status.INVALID, stderr=problem)
    limits = job['limits']

    if not _slots.acquire(timeout=3):
        return result(Status.BUSY, stderr="Server hozir band. Bir necha soniyadan so'ng qayta urinib ko'ring.")
    workdir = tempfile.mkdtemp(prefix='sbx-')
    started = time.monotonic()
    try:
        payload = json.dumps({
            'files': job['files'],
            'entry': job['entry'],
            'stdin': job['stdin'],
            'max_output': limits['max_output_chars'] + 1,
        }).encode('utf-8')

        cmd = [python_executable or sys.executable, '-I', '-S', '-X', 'utf8', '-B', WORKER_PATH]
        popen_kwargs = dict(
            cwd=workdir,
            env=_clean_env(),
            stdin=subprocess.PIPE,
            close_fds=True,
        )
        if IS_POSIX:
            popen_kwargs['preexec_fn'] = _make_preexec(limits)
        else:
            popen_kwargs['creationflags'] = getattr(subprocess, 'CREATE_NO_WINDOW', 0)

        with tempfile.TemporaryFile(dir=workdir) as out_f, tempfile.TemporaryFile(dir=workdir) as err_f:
            try:
                proc = subprocess.Popen(cmd, stdout=out_f, stderr=err_f, **popen_kwargs)
            except OSError as exc:
                return result(Status.UNAVAILABLE, stderr=f"Sandbox jarayonini ishga tushirib bo'lmadi: {exc}")

            timed_out = False
            try:
                proc.communicate(input=payload, timeout=limits['timeout_seconds'])
            except subprocess.TimeoutExpired:
                timed_out = True
                _kill(proc)
                proc.communicate()
            elapsed_ms = int((time.monotonic() - started) * 1000)

            limit = limits['max_output_chars']
            stdout, out_trunc = _read_limited(out_f, limit)
            stderr_raw, err_trunc = _read_limited(err_f, limit + 2000)
            stderr, error = _extract_error(stderr_raw)
            stderr = stderr[:limit]
            truncated = out_trunc or err_trunc
            rc = proc.returncode

        if timed_out:
            return result(Status.TIMEOUT, stdout, stderr, None, elapsed_ms, truncated, rc)
        if error and error.get('type') == 'OutputLimitExceeded':
            return result(Status.OUTPUT_LIMIT, stdout, stderr, None, elapsed_ms, True, rc)
        if error and error.get('type') == 'MemoryError':
            return result(Status.MEMORY, stdout, stderr, error, elapsed_ms, truncated, rc)
        if error and error.get('type') in ('SyntaxError', 'IndentationError', 'TabError'):
            return result(Status.SYNTAX_ERROR, stdout, stderr, error, elapsed_ms, truncated, rc)
        if error:
            return result(Status.ERROR, stdout, stderr, error, elapsed_ms, truncated, rc)
        if rc is not None and rc < 0:
            # Signal bilan o'ldirilgan: SIGXCPU (CPU limiti), SIGKILL/SIGSEGV (xotira) va h.k.
            import signal as _signal
            if rc in (-getattr(_signal, 'SIGXCPU', 24),):
                return result(Status.TIMEOUT, stdout, stderr, None, elapsed_ms, truncated, rc)
            if rc in (-getattr(_signal, 'SIGXFSZ', 25),):
                return result(Status.OUTPUT_LIMIT, stdout, stderr, None, elapsed_ms, True, rc)
            return result(Status.MEMORY, stdout, stderr, None, elapsed_ms, truncated, rc)
        if truncated:
            return result(Status.OUTPUT_LIMIT, stdout, stderr, None, elapsed_ms, True, rc)
        if rc not in (0, None):
            return result(Status.ERROR, stdout, stderr, {'type': 'SystemExit', 'message': f"exit code {rc}", 'line': None, 'file': None}, elapsed_ms, truncated, rc)
        return result(Status.OK, stdout, stderr, None, elapsed_ms, truncated, rc)
    finally:
        _slots.release()
        shutil.rmtree(workdir, ignore_errors=True)


def _kill(proc):
    try:
        if IS_POSIX:
            import signal as _signal
            os.killpg(proc.pid, _signal.SIGKILL)
        else:
            proc.kill()
    except (ProcessLookupError, PermissionError, OSError):
        try:
            proc.kill()
        except OSError:
            pass
