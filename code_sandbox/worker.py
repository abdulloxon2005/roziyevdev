"""
Sandbox ishchi jarayoni (child process).

Ushbu fayl ``python -I -S -X utf8 worker.py`` ko'rinishida, ota jarayon tomonidan
toza muhit (bo'sh env, vaqtinchalik ishchi papka, resurs limitlari) bilan ishga
tushiriladi. Vazifa (JSON) stdin orqali keladi:

    {"files": {"main.py": "..."}, "entry": "main.py", "stdin": "...", "max_output": 65536}

Ishchi:
  * foydalanuvchi modullarini diskka yozmasdan, xotiradan import qiladi;
  * audit-hook orqali tarmoq, yangi jarayon, fayl yozish, ctypes va boshqa xavfli
    amallarni bloklaydi (bu OS darajasidagi cheklovlarga QO'SHIMCHA himoya qatlami);
  * stdout/stderr hajmini cheklaydi;
  * kutilmagan xatoni foydalanuvchi fayllari bo'yicha filtrlangan traceback va
    tuzilgan (JSON) xato ma'lumoti bilan stderr oxiriga yozadi.

Bu modul atayin faqat standart kutubxonadan foydalanadi va loyiha kodini import qilmaydi.
"""
import builtins
import importlib.abc
import importlib.util
import io
import json
import linecache
import os
import sys
import traceback

ERROR_MARKER = "\x00__SANDBOX_ERROR__\x00"

# Foydalanuvchi kodi import qila olmaydigan modullar (audit "import" hodisasi orqali)
BLOCKED_MODULES = {
    'ctypes', '_ctypes', 'socket', '_socket', 'ssl', '_ssl', 'select', 'selectors',
    'subprocess', '_posixsubprocess', 'multiprocessing', '_multiprocessing',
    'mmap', 'signal', 'resource', 'pty', 'fcntl', 'termios', 'winreg', '_winapi',
    'msvcrt', '_winreg', 'asyncio', 'faulthandler', 'tracemalloc', 'gc', 'zipimport',
    'webbrowser', 'urllib', 'http', 'ftplib', 'smtplib', 'telnetlib', 'xmlrpc',
    'sqlite3', '_sqlite3', 'shutil', 'tempfile', 'pickle', '_pickle', 'marshal',
}

# Har doim bloklanadigan audit hodisalari (prefiks bo'yicha)
BLOCKED_EVENT_PREFIXES = (
    'socket.', 'subprocess.', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn',
    'os.fork', 'os.forkpty', 'os.startfile', 'os.kill', 'os.killpg', 'os.remove',
    'os.unlink', 'os.rename', 'os.replace', 'os.rmdir', 'os.mkdir', 'os.makedirs',
    'os.chmod', 'os.chown', 'os.chflags', 'os.link', 'os.symlink', 'os.truncate',
    'os.utime', 'os.chdir', 'os.putenv', 'os.unsetenv', 'os.setxattr',
    'os.removexattr', 'os.add_dll_directory', 'os.mkfifo', 'os.mknod',
    'shutil.', 'ctypes.', 'pty.', 'winreg.', '_winapi.', 'msvcrt.',
    'gc.get_objects', 'gc.get_referrers', 'gc.get_referents', 'sys._current_frames',
    'code.__new__', 'function.__new__', 'pickle.', 'mmap.',
    'sqlite3.', 'webbrowser.', 'urllib.', 'http.', 'ftplib.', 'smtplib.',
    'resource.setrlimit', 'resource.prlimit', 'sys.setprofile', 'sys.settrace',
)

PATH_EVENTS = {'os.listdir', 'os.scandir', 'glob.glob', 'glob.glob/2', 'os.walk'}


class OutputLimitExceeded(Exception):
    pass


class LimitedWriter(io.TextIOBase):
    """Chiqish hajmini cheklaydigan stdout/stderr o'rami."""

    def __init__(self, target, limit, shared):
        self._target = target
        self._limit = limit
        self._shared = shared  # ikkala oqim uchun umumiy hisoblagich

    @property
    def encoding(self):
        return 'utf-8'

    def writable(self):
        return True

    def write(self, text):
        if not isinstance(text, str):
            raise TypeError(f"write() argument must be str, not {type(text).__name__}")
        remaining = self._limit - self._shared['written']
        if remaining <= 0:
            raise OutputLimitExceeded()
        chunk = text[:remaining]
        self._shared['written'] += len(chunk)
        self._target.write(chunk)
        if len(chunk) < len(text):
            self._target.flush()
            raise OutputLimitExceeded()
        return len(text)

    def flush(self):
        self._target.flush()


class MemoryModuleFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Loyiha fayllarini (utils.py va h.k.) diskka yozmasdan xotiradan import qiladi."""

    def __init__(self, modules):
        # {"utils": ("utils.py", source)}
        self._modules = modules

    def find_spec(self, fullname, path=None, target=None):
        if fullname in self._modules:
            filename = self._modules[fullname][0]
            return importlib.util.spec_from_loader(fullname, self, origin=filename)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        filename, source = self._modules[module.__name__]
        module.__file__ = filename
        code = compile(source, filename, 'exec')
        exec(code, module.__dict__)


def _norm(path):
    try:
        return os.path.normcase(os.path.realpath(os.fspath(path)))
    except Exception:
        return None


def _allowed_read_roots():
    roots = set()
    for p in (sys.prefix, sys.base_prefix, sys.exec_prefix, sys.base_exec_prefix):
        n = _norm(p)
        if n:
            roots.add(n.rstrip(os.sep) + os.sep)
    return tuple(roots)


def install_audit_hook():
    read_roots = _allowed_read_roots()

    def deny(what):
        raise PermissionError(f"Xavfsizlik cheklovi: «{what}» amaliga ruxsat berilmagan.")

    def path_allowed(path):
        if isinstance(path, int):
            return False
        n = _norm(path)
        return bool(n) and (n.rstrip(os.sep) + os.sep).startswith(read_roots)

    def hook(event, args):
        if event == 'open':
            path, mode, flags = (list(args) + [None, None, None])[:3]
            mode = mode or 'r'
            if isinstance(mode, str) and any(c in mode for c in 'wax+'):
                deny("faylga yozish")
            if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC):
                deny("faylga yozish")
            if path is None or not path_allowed(path):
                deny("fayl tizimiga kirish")
            return
        if event in PATH_EVENTS:
            path = args[0] if args else None
            if path is None or path == '' or path == '.':
                deny("papkalarni ko'rish")
            if not path_allowed(path):
                deny("papkalarni ko'rish")
            return
        if event == 'import':
            name = args[0] if args else ''
            if isinstance(name, str):
                root = name.split('.')[0]
                if name in BLOCKED_MODULES or root in BLOCKED_MODULES:
                    deny(f"import {name}")
            return
        if event.startswith(BLOCKED_EVENT_PREFIXES):
            deny(event)

    sys.addaudithook(hook)


def _safe_exit(code=None):
    raise SystemExit(code)


def _report_error(exc, user_files):
    """Filtrlangan traceback'ni va tuzilgan xato ma'lumotini stderr'ga yozadi."""
    tb_exc = traceback.TracebackException.from_exception(exc)
    tb_exc.stack = traceback.StackSummary.from_list(
        [frame for frame in tb_exc.stack if frame.filename in user_files]
    )
    text = ''.join(tb_exc.format())
    line = None
    filename = None
    if isinstance(exc, SyntaxError):
        line = exc.lineno
        filename = exc.filename
    elif tb_exc.stack:
        line = tb_exc.stack[-1].lineno
        filename = tb_exc.stack[-1].filename
    info = {
        'type': type(exc).__name__,
        'message': str(exc) if not isinstance(exc, SyntaxError) else (exc.msg or ''),
        'line': line,
        'file': filename,
    }
    err = sys.stderr
    try:
        err.write(text)
    except OutputLimitExceeded:
        pass
    # Tuzilgan xato ma'lumoti chiqish limitidan qat'i nazar asl oqimga yoziladi
    sys.__stderr__.write(ERROR_MARKER + json.dumps(info, ensure_ascii=False) + "\n")
    sys.__stderr__.flush()


def main():
    raw = sys.stdin.buffer.read()
    job = json.loads(raw.decode('utf-8'))

    files = job.get('files') or {}
    entry = job.get('entry') or 'main.py'
    if entry not in files:
        files[entry] = job.get('code', '')
    max_output = int(job.get('max_output') or 65536)

    # Foydalanuvchi fayllarining manba matnini linecache'ga joylash (traceback uchun)
    for name, source in files.items():
        linecache.cache[name] = (len(source), None, source.splitlines(True), name)

    modules = {}
    for name, source in files.items():
        if name != entry and name.endswith('.py'):
            mod_name = name[:-3].replace('/', '.')
            if mod_name.isidentifier() or all(p.isidentifier() for p in mod_name.split('.')):
                modules[mod_name] = (name, source)
    if modules:
        sys.meta_path.insert(0, MemoryModuleFinder(modules))

    # Windows'da ham satr oxiri LF bo'lishi uchun (natijalarni solishtirish platformaga bog'liq bo'lmasin)
    for stream in (sys.__stdout__, sys.__stderr__):
        try:
            stream.reconfigure(newline='\n', encoding='utf-8')
        except (AttributeError, ValueError):
            pass

    shared = {'written': 0}
    sys.stdout = LimitedWriter(sys.__stdout__, max_output, shared)
    sys.stderr = LimitedWriter(sys.__stderr__, max_output, shared)
    sys.stdin = io.StringIO(job.get('stdin') or '')

    # -S rejimida site moduli yuklanmaydi; yangi boshlovchilar ishlatadigan exit()/quit() ni qo'shamiz
    builtins.exit = _safe_exit
    builtins.quit = _safe_exit

    user_globals = {'__name__': '__main__', '__builtins__': builtins, '__file__': entry}
    source = files[entry]
    user_files = set(files.keys())

    exit_code = 0
    try:
        code = compile(source, entry, 'exec')
    except (SyntaxError, ValueError) as exc:
        _report_error(exc, user_files)
        sys.__stdout__.flush()
        os._exit(1)

    # Traceback chiqarishda ishchi faylining o'zini o'qish kerak bo'lmasligi uchun oldindan keshlaymiz
    linecache.getline(__file__, 1)
    install_audit_hook()
    try:
        exec(code, user_globals)
    except SystemExit as exc:
        if exc.code not in (None, 0):
            exit_code = exc.code if isinstance(exc.code, int) else 1
            if not isinstance(exc.code, int):
                try:
                    sys.stderr.write(str(exc.code) + "\n")
                except OutputLimitExceeded:
                    pass
    except OutputLimitExceeded:
        sys.__stderr__.write(ERROR_MARKER + json.dumps({'type': 'OutputLimitExceeded', 'message': '', 'line': None, 'file': None}) + "\n")
        exit_code = 3
    except BaseException as exc:  # noqa: BLE001 — foydalanuvchi xatosi har qanday turda bo'lishi mumkin
        _report_error(exc, user_files)
        exit_code = 1
    finally:
        try:
            sys.__stdout__.flush()
            sys.__stderr__.flush()
        except Exception:
            pass
    os._exit(exit_code if isinstance(exit_code, int) and 0 <= exit_code < 256 else 1)


if __name__ == '__main__':
    main()
