"""1-kursning 2–11-modullari kontent fayllari ro'yxati (tartib bo'yicha)."""
import importlib

MODULE_FILES = [
    'python_m02', 'python_m03', 'python_m04', 'python_m05', 'python_m06',
    'python_m07', 'python_m08', 'python_m09', 'python_m10', 'python_m11',
]


def load_modules():
    mods = []
    for name in MODULE_FILES:
        try:
            mods.append(importlib.import_module(f'apps.interactive.content.{name}'))
        except ModuleNotFoundError as exc:
            if exc.name != f'apps.interactive.content.{name}':
                raise
    return mods


# Kursning to'liq (11 modul) tavsifi — yangi modullar qo'shilganda kurs kartochkasini yangilash uchun
COURSE_FULL = {
    'title': "Python dasturlash asoslari — Boshlang'ich kurs",
    'short_description': "Python'ni noldan boshlayotganlar uchun to'liq kurs: 11 modul, 74 ta qisqa interaktiv dars, "
                         "brauzerning o'zida kod yozish va avtomatik tekshiriladigan topshiriqlar hamda mini-loyihalar.",
    'description': """
**Python dasturlash asoslari** — dasturlashni mutlaqo noldan boshlayotgan o'quvchini mustaqil ravishda kichik dasturlar yaratish darajasiga olib chiqadigan interaktiv kurs.

**Kurs tarkibi:** 11 modul, 74 ta dars (har biri 10–15 daqiqa), har modul oxirida nazorat va mini-loyiha, 3 ta takrorlash (Review) hamda yakuniy baholash.

Nazariyani o'qiysiz, shu sahifaning o'zida kod yozib ishga tushirasiz, mashqlar va testlarni bajarasiz, topshiriqlar esa haqiqiy kod bajarilishi orqali avtomatik tekshiriladi.
Kompyuteringizga hech narsa o'rnatish shart emas — barcha kodlar xavfsiz serverda bajariladi; kurs oxirida esa Python va VS Code'ni o'z kompyuteringizga o'rnatishni ham o'rganasiz.
""".strip(),
    'duration_hours': 40,
    'what_you_will_learn': "\n".join([
        "Algoritmik fikrlash va Python tilida birinchi dasturlarni yozish",
        "O'zgaruvchilar, ma'lumot turlari, matnlar va input()",
        "Shartlar (if/elif/else) va sikllar (for/while)",
        "List, tuple, set va dictionary bilan ishlash",
        "Funksiyalar yozish va kodni qayta ishlatish",
        "Xatolarni topish va boshqarish (try/except)",
        "Fayllar va JSON bilan ishlash, modullar",
        "Python va VS Code'ni o'rnatib, mustaqil dastur yaratish",
    ]),
}
