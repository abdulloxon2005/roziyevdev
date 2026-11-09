"""
Python kodini bajarish uchun yagona integratsiya nuqtasi (Django tomoni).

Backend ``settings.CODE_RUNNER['BACKEND']`` orqali tanlanadi:

* ``subprocess`` — ``code_sandbox.executor`` orqali alohida, cheklangan jarayonda (lokal/dev);
* ``http``       — alohida sandbox konteyneriga HTTP so'rov (production uchun tavsiya etiladi);
* ``disabled``   — kod bajarish o'chirilgan; foydalanuvchiga halol xabar ko'rsatiladi
                   (hech qachon soxta natija qaytarilmaydi).

Bu modul web-server jarayonida hech qachon foydalanuvchi kodini ``exec()`` qilmaydi.
"""
import json
import logging
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class RunStatus:
    OK = 'ok'
    ERROR = 'error'
    SYNTAX_ERROR = 'syntax_error'
    TIMEOUT = 'timeout'
    MEMORY = 'memory'
    OUTPUT_LIMIT = 'output_limit'
    BUSY = 'busy'
    INVALID = 'invalid'
    UNAVAILABLE = 'unavailable'


STATUS_LABELS = {
    RunStatus.OK: "Dastur muvaffaqiyatli bajarildi",
    RunStatus.ERROR: "Dastur bajarilishida xato yuz berdi",
    RunStatus.SYNTAX_ERROR: "Sintaksis xatosi",
    RunStatus.TIMEOUT: "Vaqt chegarasidan oshib ketdi",
    RunStatus.MEMORY: "Xotira chegarasidan oshib ketdi",
    RunStatus.OUTPUT_LIMIT: "Chiqish hajmi juda katta",
    RunStatus.BUSY: "Server band",
    RunStatus.INVALID: "So'rov noto'g'ri",
    RunStatus.UNAVAILABLE: "Kod bajarish xizmati mavjud emas",
}


@dataclass
class RunResult:
    status: str
    stdout: str = ''
    stderr: str = ''
    error: dict | None = None
    elapsed_ms: int = 0
    truncated: bool = False
    friendly_error: str = ''
    extra: dict = field(default_factory=dict)

    @property
    def ok(self):
        return self.status == RunStatus.OK

    @property
    def is_infrastructure_problem(self):
        """Talaba kodi emas, platforma tomonidagi muammo (natija hisoblanmasligi kerak)."""
        return self.status in (RunStatus.BUSY, RunStatus.UNAVAILABLE, RunStatus.INVALID)

    def to_dict(self):
        return {
            'status': self.status,
            'status_label': STATUS_LABELS.get(self.status, self.status),
            'ok': self.ok,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'error': self.error,
            'error_line': (self.error or {}).get('line'),
            'friendly_error': self.friendly_error,
            'elapsed_ms': self.elapsed_ms,
            'truncated': self.truncated,
        }


def _config():
    defaults = {
        'BACKEND': 'subprocess',
        'URL': '',
        'TOKEN': '',
        'TIMEOUT_SECONDS': 5,
        'CPU_SECONDS': 3,
        'MEMORY_MB': 256,
        'MAX_OUTPUT_CHARS': 20000,
        'RATE_LIMIT_PER_MINUTE': 40,
    }
    return {**defaults, **getattr(settings, 'CODE_RUNNER', {})}


# ==============================================================================
# Xatolarni yangi boshlovchiga tushunarli tilda izohlash
# ==============================================================================

_ERROR_EXPLANATIONS = {
    'SyntaxError': "Python kodni o'qiy olmadi — yozilish qoidasi (sintaksis) buzilgan. "
                   "Qavslar, qo'shtirnoqlar va vergullar to'g'ri yopilganini tekshiring.",
    'IndentationError': "Satr boshidagi bo'shliqlar (chekinish) noto'g'ri. Python'da chekinish muhim: "
                        "bir blokdagi satrlar bir xil miqdorda surilgan bo'lishi kerak.",
    'TabError': "Chekinishda Tab va bo'sh joy aralashib ketgan. Faqat bo'sh joy (4 ta) ishlating.",
    'NameError': "Python bu nomni tanimadi. Ehtimol, nom xato yozilgan (masalan, print o'rniga Print), "
                 "matn qo'shtirnoqqa olinmagan yoki o'zgaruvchi hali yaratilmagan.",
    'TypeError': "Qiymat turi mos kelmadi. Masalan, matn va sonni + bilan qo'shib bo'lmaydi.",
    'ValueError': "Qiymat turi to'g'ri, lekin qiymatning o'zi mos emas (masalan, int(\"salom\")).",
    'ZeroDivisionError': "Nolga bo'lish mumkin emas. Bo'luvchi 0 bo'lmasligini tekshiring.",
    'IndexError': "Ro'yxatda bunday tartib raqamli element yo'q.",
    'KeyError': "Lug'atda bunday kalit yo'q.",
    'AttributeError': "Bu turdagi qiymatda bunday xususiyat yoki metod yo'q.",
    'RecursionError': "Funksiya o'zini o'zi juda ko'p marta chaqirdi (cheksiz rekursiya).",
    'EOFError': "Dastur input() orqali ma'lumot kutdi, lekin kiritish (stdin) bo'sh edi.",
    'PermissionError': "Bu amal o'quv muhitida xavfsizlik sababli taqiqlangan "
                       "(fayl, tarmoq yoki tizim buyruqlari).",
    'ModuleNotFoundError': "Bunday modul topilmadi yoki o'quv muhitida mavjud emas.",
    'ImportError': "Modulni import qilib bo'lmadi.",
    'UnicodeError': "Matn kodlashda muammo yuz berdi.",
    'AssertionError': "assert sharti bajarilmadi.",
    'SystemExit': "Dastur nolga teng bo'lmagan kod bilan yakunlandi.",
}

_SYNTAX_HINTS = [
    (re.compile(r"was never closed"), "Ochilgan qavs yopilmagan. Har bir ( uchun ) bo'lishi kerak."),
    (re.compile(r"unterminated string literal"), "Matn qo'shtirnog'i yopilmagan. Matn \"...\" yoki '...' ichida bo'lishi kerak."),
    (re.compile(r"unmatched '\)'"), "Ortiqcha yopuvchi qavs ) bor."),
    (re.compile(r"invalid syntax\. Perhaps you forgot a comma"), "Qiymatlar orasida vergul tushib qolgan bo'lishi mumkin."),
    (re.compile(r"Missing parentheses in call to 'print'"), "Python 3 da print qavs bilan yoziladi: print(\"...\")."),
    (re.compile(r"invalid character"), "Kodda Python tushunmaydigan belgi bor (masalan, “ ” kabi chiroyli qo'shtirnoqlar). Oddiy \" belgisini ishlating."),
    (re.compile(r"expected ':'"), "Satr oxirida ikki nuqta (:) tushib qolgan."),
    (re.compile(r"unexpected indent"), "Bu satr keraksiz surilgan (oldida ortiqcha bo'sh joy bor)."),
    (re.compile(r"expected an indented block"), "Bu satr surilishi (oldiga 4 ta bo'sh joy qo'yilishi) kerak edi."),
]


def explain_error(status, error):
    if status == RunStatus.TIMEOUT:
        return ("Dastur ajratilgan vaqt ichida tugamadi. Kodda cheksiz sikl bo'lishi mumkin "
                "yoki dastur input() orqali ma'lumot kutib qolgan.")
    if status == RunStatus.MEMORY:
        return "Dastur juda ko'p xotira ishlatdi. Juda katta ro'yxat yoki cheksiz o'sish bo'lishi mumkin."
    if status == RunStatus.OUTPUT_LIMIT:
        return "Dastur ekranga juda ko'p ma'lumot chiqardi, natija qisqartirildi. Cheksiz sikl bo'lishi mumkin."
    if status in (RunStatus.BUSY, RunStatus.UNAVAILABLE, RunStatus.INVALID):
        return ''
    if not error:
        return ''
    err_type = error.get('type') or ''
    message = error.get('message') or ''
    parts = []
    line = error.get('line')
    if line:
        parts.append(f"{line}-qatorda xato.")
    base = _ERROR_EXPLANATIONS.get(err_type)
    if base:
        parts.append(base)
    if err_type in ('SyntaxError', 'IndentationError'):
        for pattern, hint in _SYNTAX_HINTS:
            if pattern.search(message):
                parts.append(hint)
                break
    if err_type == 'NameError':
        m = re.search(r"name '(\w+)' is not defined", message)
        if m:
            name = m.group(1)
            if name.lower() == 'print' and name != 'print':
                parts.append(f"«{name}» emas, «print» deb kichik harflarda yozing.")
            else:
                parts.append(f"«{name}» nomi aniqlanmagan. Agar bu matn bo'lsa, uni qo'shtirnoqqa oling: \"{name}\".")
    return ' '.join(parts)


# ==============================================================================
# Backendlar
# ==============================================================================

def _run_subprocess(cfg, code, files, entry, stdin):
    from code_sandbox.executor import run_python
    return run_python(
        code,
        files=files,
        entry=entry,
        stdin=stdin,
        limits={
            'timeout_seconds': float(cfg['TIMEOUT_SECONDS']),
            'cpu_seconds': int(cfg['CPU_SECONDS']),
            'memory_mb': int(cfg['MEMORY_MB']),
            'max_output_chars': int(cfg['MAX_OUTPUT_CHARS']),
        },
    )


def _run_http(cfg, code, files, entry, stdin):
    url = (cfg['URL'] or '').rstrip('/')
    if not url:
        return {'status': RunStatus.UNAVAILABLE, 'stderr': 'CODE_RUNNER_URL sozlanmagan.'}
    body = json.dumps({'code': code, 'files': files, 'entry': entry, 'stdin': stdin}).encode('utf-8')
    req = urllib.request.Request(
        f'{url}/run',
        data=body,
        method='POST',
        headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {cfg['TOKEN']}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=float(cfg['TIMEOUT_SECONDS']) + 5) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        logger.warning('Code sandbox HTTP error: %s', exc.code)
        return {'status': RunStatus.UNAVAILABLE, 'stderr': f'Sandbox xizmati xatosi ({exc.code}).'}
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        logger.warning('Code sandbox unreachable: %s', exc)
        return {'status': RunStatus.UNAVAILABLE, 'stderr': 'Sandbox xizmatiga ulanib bo\'lmadi.'}


def run_python(code=None, *, files=None, entry='main.py', stdin=''):
    """Python kodini sozlangan sandbox backend'ida bajaradi va ``RunResult`` qaytaradi."""
    cfg = _config()
    backend = (cfg['BACKEND'] or 'subprocess').lower()
    if backend == 'subprocess':
        raw = _run_subprocess(cfg, code, files, entry, stdin)
    elif backend == 'http':
        raw = _run_http(cfg, code, files, entry, stdin)
    else:
        raw = {
            'status': RunStatus.UNAVAILABLE,
            'stderr': "Kod bajarish xizmati hozircha yoqilmagan. Administrator CODE_RUNNER_BACKEND sozlamasini o'rnatishi kerak.",
        }

    status = raw.get('status') or RunStatus.UNAVAILABLE
    error = raw.get('error')
    res = RunResult(
        status=status,
        stdout=raw.get('stdout') or '',
        stderr=raw.get('stderr') or '',
        error=error,
        elapsed_ms=int(raw.get('elapsed_ms') or 0),
        truncated=bool(raw.get('truncated')),
    )
    res.friendly_error = explain_error(status, error)
    return res


def check_rate_limit(user_id, scope='run'):
    """Foydalanuvchi bo'yicha daqiqasiga ishga tushirishlar sonini cheklaydi. True — ruxsat."""
    limit = int(_config()['RATE_LIMIT_PER_MINUTE'])
    if limit <= 0:
        return True
    key = f'code-runner:{scope}:{user_id}'
    try:
        added = cache.add(key, 1, timeout=60)
        if added:
            return True
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=60)
        return True
    return count <= limit
