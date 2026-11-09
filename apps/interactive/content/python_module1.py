"""
«Python — 0 dan boshlash» kursi va uning 1-moduli («Birinchi qadamlar») uchun dastlabki kontent.

Bu fayl faqat boshlang'ich ma'lumot: `manage.py seed_python_course` uni bazaga yozadi.
Keyingi barcha tahrirlar (yangi modullar, darslar, topshiriqlar) admin panel orqali qilinadi —
kodni o'zgartirish shart emas.
"""
from .python_m1_lessons_1_2 import LESSON_1, LESSON_2
from .python_m1_lessons_3_4 import LESSON_3, LESSON_4
from .python_m1_lessons_5_6 import ASSESSMENT, LESSON_5, LESSON_6

COURSE = {
    'slug': 'python-0-dan-boshlash',
    'title': "Python — 0 dan boshlash",
    'category': "Backend & Python",
    'short_description': "Dasturlashni hech qachon o'rganmaganlar uchun Python kursi: qisqa interaktiv darslar, "
                         "brauzerning o'zida kod yozish va avtomatik tekshiriladigan topshiriqlar.",
    'description': """
**Python — 0 dan boshlash** — dasturlashni noldan o'rganmoqchi bo'lganlar uchun interaktiv kurs.

Har bir dars 10–15 daqiqalik bo'lib, bitta asosiy tushunchani o'rgatadi. Nazariyani o'qiysiz,
shu sahifaning o'zida kod yozib ishga tushirasiz, mashqlar va testlarni bajarasiz, dars oxirida esa
mustaqil vazifani avtomatik tekshiruvdan o'tkazasiz.

Kompyuteringizga hech narsa o'rnatish shart emas — barcha kodlar xavfsiz serverda bajariladi.
""".strip(),
    'level': 'beginner',
    'duration_hours': 20,
    'what_you_will_learn': "\n".join([
        "Algoritmik fikrlash: masalani qadamlarga ajratish",
        "Python tilida birinchi dasturlarni yozish",
        "print() ning barcha asosiy imkoniyatlari: sep, end, \\n, \\t",
        "Xato xabarlarini o'qish va xatolarni mustaqil tuzatish",
        "Izohlar va toza kod yozish odatlari (PEP 8)",
    ]),
    'requirements': "\n".join([
        "Hech qanday dasturlash tajribasi talab qilinmaydi",
        "Internetga ulangan kompyuter yoki telefon",
    ]),
}

MODULE = {
    'order': 1,
    'title': "Birinchi qadamlar",
    'description': "Dasturlash va algoritm tushunchasi, Python bilan tanishuv, print() funksiyasi, "
                   "xato xabarlarini o'qish va toza kod yozish odati.",
}

LESSONS = [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5, LESSON_6]

__all__ = ['COURSE', 'MODULE', 'LESSONS', 'ASSESSMENT']
