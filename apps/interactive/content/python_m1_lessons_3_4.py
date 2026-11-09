"""Python — 0 dan boshlash · 1-modul · 3–4-darslar."""
from .builders import T, callout, code_task, example, exercise, fill, multiple, opt, predict, single, text

# ==============================================================================
# 3-DARS. Birinchi dastur: print("Salom, dunyo!")
# ==============================================================================
LESSON_3 = {
    'order': 3,
    'title': 'Birinchi dastur: print("Salom, dunyo!")',
    'duration': 13,
    'objective': "print() funksiyasi yordamida ekranga matn va sonlarni chiqarish, matnni qo'shtirnoqqa olish "
                 "qoidalarini bilish va birinchi to'liq dasturni mustaqil yozish.",
    'concepts': ["print() funksiyasi", "Matn (string) va qo'shtirnoqlar", "Sonlarni chiqarish", "Katta-kichik harf farqi", "Bo'sh print()"],
    'blocks': [
        text(r"""
Dasturlash olamida an'ana bor: yangi tilni o'rganishda birinchi dastur ekranga
**"Salom, dunyo!"** (inglizcha *Hello, World!*) yozadi. Python'da bu bitta qator:

```python
print("Salom, dunyo!")
```

Natija:

```text
Salom, dunyo!
```
""", title="An'anaviy birinchi dastur"),
        example(r'''
print("Salom, dunyo!")
''', title="Birinchi dasturingiz", body=r"""
«Ishga tushirish»ni bosing. Natija oynasida `Salom, dunyo!` chiqishi kerak.
Endi qo'shtirnoq ichidagi matnni o'z ismingiz bilan almashtiring: `print("Salom, Aziza!")`.
"""),
        text(r"""
`print("Salom, dunyo!")` qatorini qismlarga ajratamiz:

| Qism | Nomi | Vazifasi |
|---|---|---|
| `print` | funksiya nomi | "ekranga chiqar" buyrug'i |
| `(` `)` | qavslar | funksiyaga nima berilayotganini o'raydi |
| `"Salom, dunyo!"` | matn (string) | ekranga chiqadigan ma'lumot |

**Funksiya** — tayyor buyruq. Uni chaqirish uchun nomini yozib, qavs ochamiz. Qavs ichidagi narsa
funksiyaga beriladigan ma'lumot (**argument**) deyiladi.
""", title="Kod qanday tuzilgan?"),
        callout('analogy', r"""
`print` — bu **ovoz kuchaytirgich (karnay)**. Qavs ichiga nima bersangiz, u shuni hammaga e'lon qiladi.
Qo'shtirnoqlar esa "bu so'zma-so'z aytiladigan matn" degan belgi — xuddi kitobdagi iqtibos kabi.
""", title="Hayotiy o'xshatish"),
        text(r"""
Python'da matn **qo'shtirnoq** ichida yoziladi. Ikki xil qo'shtirnoq bor va ikkalasi ham to'g'ri:

```python
print("Salom")   # qo'sh qo'shtirnoq
print('Salom')   # birlik qo'shtirnoq
```

Muhim qoida: qaysi qo'shtirnoq bilan **ochsangiz**, o'shasi bilan **yoping**.

Matn ichida apostrof (`'`) bo'lsa — masalan **o'zbek** so'zlarida — matnni qo'sh qo'shtirnoqqa oling:

```python
print("Men o'zbekman")    # to'g'ri
```

Agar `'Men o'zbekman'` deb yozsangiz, Python matn `'Men o'` da tugadi deb o'ylaydi va xato beradi.
""", title="Qo'shtirnoqlar qoidasi"),
        callout('warning', r"""
Python **katta-kichik harfni farqlaydi**: `print` to'g'ri, `Print` yoki `PRINT` — xato!
Shuningdek, Word yoki Telegram'dan nusxalangan “chiroyli” qo'shtirnoqlar ham ishlamaydi —
faqat klaviaturadagi oddiy `"` yoki `'` belgisini ishlating.
""", title="Diqqat: ko'p uchraydigan xatolar"),
        text(r"""
Sonlarni qo'shtirnoqsiz ham chiqarish mumkin. Bunda Python ularni **son** sifatida tushunadi va
hatto hisoblay oladi:

```python
print(2026)
print(7 + 3)      # 10 chiqadi — Python hisoblaydi
print("7 + 3")    # 7 + 3 chiqadi — bu shunchaki matn
```

Qavs ichi bo'sh `print()` esa **bo'sh qator** chiqaradi.
""", title="Sonlar va bo'sh print()"),
        example(r'''
print("Hisob-kitob:")
print(7 + 3)
print("7 + 3")
print()
print("Yuqorida bo'sh qator bor")
''', title="Son va matn farqi", body=r"""
Ishga tushiring: `7 + 3` qo'shtirnoqsiz bo'lsa — natija `10`, qo'shtirnoq ichida bo'lsa — aynan `7 + 3`.
"""),
        exercise('l3_inline_fix_case'),
        text(r"""
Har bir `print()` o'z natijasini **yangi qatordan** boshlaydi. Shu sababli bir necha `print` yozsangiz,
natijalar ustma-ust qatorlarda chiqadi. Keyingi darsda bu xatti-harakatni qanday o'zgartirishni o'rganamiz.
""", title="Har bir print — yangi qator"),
        exercise('l3_inline_blank'),
    ],
    'tasks': [
        code_task('l3_inline_fix_case', "Kodni tuzating: katta harf", r"""
Quyidagi kod ishlamayapti. Xatoni tuzatib, ekranga `Salom, dunyo!` chiqaring.
""", section='inline', points=2, starter_code='Print("Salom, dunyo!")\n',
            tests=[T('output_equals', "Salom, dunyo!", "Ekranga «Salom, dunyo!» chiqadi")],
            hint="Python katta-kichik harfni farqlaydi. Funksiya nomi qanday yozilishi kerak?",
            full_solution='print("Salom, dunyo!")\n',
            explanation="`print` faqat kichik harflar bilan yoziladi. `Print` — Python uchun noma'lum nom (NameError)."),
        fill('l3_inline_blank', "Bo'sh joyni to'ldiring", r"""
Dastur `Men Python o'rganyapman` matnini chiqarishi uchun bo'sh joyga **funksiya nomini** yozing.
""", snippet='___("Men Python o\'rganyapman")\n', answers=["print"],
            tests=[T('output_equals', "Men Python o'rganyapman", "To'g'ri matn chiqadi")],
            hint="Ekranga chiqaruvchi funksiya — 5 harfli, kichik harflar bilan.",
            explanation="`print` — ekranga chiqarish funksiyasi."),

        single('l3_quiz_1', "To'g'ri yozilgan qator", "Qaysi qator **xatosiz** ishlaydi?", options=[
            opt('`Print("Salom")`', False, "Katta P — xato. Python harflarni farqlaydi."),
            opt('`print("Salom")`', True),
            opt('`print("Salom)`', False, "Qo'shtirnoq yopilmagan."),
            opt('`print Salom`', False, "Qavs va qo'shtirnoq yo'q."),
        ], hint="Funksiya nomi, qavslar va qo'shtirnoqlarni tekshiring.",
            explanation="To'g'ri shakl: kichik harfli `print`, qavslar va ikkala tomonda bir xil qo'shtirnoq."),
        single('l3_quiz_2', "Apostrofli matn", "`Men o'zbekman` matnini chiqarishning **to'g'ri** usuli qaysi?", options=[
            opt("`print('Men o'zbekman')`", False, "Apostrof birlik qo'shtirnoqni «yopib» qo'yadi — xato."),
            opt('`print("Men o\'zbekman")`', True),
            opt("`print(Men o'zbekman)`", False, "Matn qo'shtirnoqsiz — Python uni nom deb o'ylaydi."),
        ], hint="Matn ichidagi `'` bilan qo'shtirnoq to'qnashmasligi kerak.",
            explanation="Matnda apostrof bo'lsa, uni qo'sh qo'shtirnoq `\"...\"` ichiga oling."),
        predict('l3_quiz_3', "Son yoki matn?", "Dastur nima chiqaradi?", code='print(5 + 5)\nprint("5 + 5")\n',
                answer="10\n5 + 5",
                hint="Qo'shtirnoqsiz ifodani Python hisoblaydi, qo'shtirnoqdagisini — yo'q.",
                explanation="Birinchi qatorda Python `5 + 5` ni hisoblab `10` chiqaradi; ikkinchisi oddiy matn."),

        single('l3_review_1', "Takrorlash: interpretator", r"""
2-darsni eslang. Python kodni qaysi tartibda bajaradi?
""", section='review', options=[
            opt("Pastdan yuqoriga", False),
            opt("Yuqoridan pastga, qatorma-qator", True),
            opt("Tasodifiy tartibda", False),
        ], hint="Interpretator — «tarjimon», u kodni o'qish tartibida bajaradi.",
            explanation="Interpretator qatorlarni yuqoridan pastga birin-ketin bajaradi."),

        code_task('l3_assignment', "O'zingiz haqingizda ikki qator", r"""
Ekranga aynan quyidagi **ikki qatorni** chiqaradigan dastur yozing:

```
Salom, dunyo!
Men Python o'rganyapman.
```

**Talablar:** har bir qator alohida `print()` bilan chiqsin; ikkinchi qatorda apostrof borligini unutmang.
""", expected_output_example="Salom, dunyo!\nMen Python o'rganyapman.",
            tests=[
                T('runs_ok', description="Dastur xatosiz ishlaydi",
                  failure="Avval xatoni tuzating: qo'shtirnoq va qavslarni tekshiring."),
                T('output_equals', "Salom, dunyo!\nMen Python o'rganyapman.", "Natija namunaga aynan mos",
                  failure="Vergul, nuqta va apostrofni tekshiring. Har bir harf muhim."),
                T('code_contains', 'print(', "Kodda print() ishlatilgan"),
            ],
            hint="Ikkinchi qatordagi o' harfi sababli matnni qo'sh qo'shtirnoq \"...\" ichiga oling.",
            partial_solution='print("Salom, dunyo!")\n# ikkinchi qatorni shu yerga yozing\n',
            full_solution='print("Salom, dunyo!")\nprint("Men Python o\'rganyapman.")\n',
            explanation="Har bir `print` yangi qator chiqaradi. Apostrofli matn qo'sh qo'shtirnoq ichida yoziladi."),

        predict('l3_practice_easy', "Qavsdagi hisob", "Natijani yozing:", code='print(2 + 3)\n', answer="5",
                section='practice', difficulty='easy', hint="Qo'shtirnoq yo'q — demak, hisoblanadi.",
                explanation="Python `2 + 3` ni hisoblab `5` chiqaradi."),
        code_task('l3_practice_medium', "Uch qatorli she'r", r"""
Ekranga quyidagini aynan chiqaring:

```
Bilim — kuch.
Kod — san'at.
Python — boshlanish.
```
""", section='practice', difficulty='medium', points=5,
            tests=[T('output_equals', "Bilim — kuch.\nKod — san'at.\nPython — boshlanish.", "Natija aynan mos")],
            hint="Uzun tire (—) ni nusxalab olishingiz mumkin. «san'at» so'zida apostrof bor.",
            full_solution='print("Bilim — kuch.")\nprint("Kod — san\'at.")\nprint("Python — boshlanish.")\n',
            explanation="Uch qator — uchta `print`. Apostrofli matn qo'sh qo'shtirnoqda."),
        code_task('l3_practice_hard', "Ramkadagi salom", r"""
Quyidagi ramkani aynan chiqaring (yuqori va pastki chiziq 17 tadan `*` belgisi):

```
*****************
* Salom, dunyo! *
*****************
```
""", section='practice', difficulty='hard', points=5,
            tests=[T('output_equals', "*****************\n* Salom, dunyo! *\n*****************", "Ramka aynan mos",
                     failure="Yulduzchalar sonini sanang: har bir chiziqda 17 ta.")],
            hint="Yuqori va pastki qator bir xil. O'rtadagi qatorda chetlarida bo'sh joy bor.",
            full_solution='print("*****************")\nprint("* Salom, dunyo! *")\nprint("*****************")\n',
            explanation="Matnli «grafika» ham oddiy `print` qatorlaridan iborat."),
    ],
}


# ==============================================================================
# 4-DARS. print() imkoniyatlari: bir nechta qiymat, sep, end, \n, \t
# ==============================================================================
LESSON_4 = {
    'order': 4,
    'title': r"print() imkoniyatlari: bir nechta qiymat, sep, end, \n, \t",
    'duration': 15,
    'objective': "print() ga bir nechta qiymat berish, ular orasidagi ajratgichni (sep) va qator oxirini (end) "
                 "boshqarish, maxsus belgilar \\n va \\t yordamida natijani chiroyli formatlash.",
    'concepts': ["Bir nechta argument", "sep parametri", "end parametri", r"\n — yangi qator", r"\t — tabulyatsiya"],
    'blocks': [
        text(r"""
`print()` ga vergul bilan ajratib **bir nechta qiymat** berish mumkin. Python ularni ketma-ket,
orasiga **bitta bo'sh joy** qo'yib chiqaradi:

```python
print("Ism:", "Ali")         # Ism: Ali
print("Yosh:", 16)           # Yosh: 16
print(1, 2, 3)               # 1 2 3
```

E'tibor bering: matn va sonni bitta `print` da birga chiqarish mumkin.
""", title="Bir nechta qiymat"),
        example(r'''
print("Ism:", "Ali")
print("Yosh:", 16)
print("Sevimli sonlar:", 7, 13, 21)
''', title="Vergul bilan bir nechta qiymat"),
        text(r"""
Qiymatlar orasidagi bo'sh joyni boshqa belgi bilan almashtirish uchun **`sep`** (inglizcha *separator* —
ajratgich) parametridan foydalanamiz:

```python
print(2026, 11, 8, sep="-")      # 2026-11-8
print("a", "b", "c", sep="")     # abc   (ajratgichsiz)
print("olma", "nok", sep=", ")   # olma, nok
```

`sep` doim qavs ichida, **oxirida** yoziladi va qiymati qo'shtirnoq ichidagi matn bo'ladi.
""", title="sep — ajratgichni o'zgartirish"),
        callout('analogy', r"""
`sep` — marjondagi **munchoqlar orasidagi tugun**. Munchoqlar (qiymatlar) o'sha-o'sha, faqat ular
orasiga nima qo'yilishini siz tanlaysiz: bo'sh joy, chiziqcha, vergul yoki hech narsa.
""", title="Hayotiy o'xshatish: marjon"),
        example(r'''
print(8, 11, 2026, sep=".")
print("08", "30", sep=":")
print("www", "roziyev", "dev", sep=".")
''', title="sep bilan sana, vaqt va manzil"),
        exercise('l4_inline_sep'),
        text(r"""
Odatda `print` oxirida avtomatik **yangi qatorga o'tadi**. Buni **`end`** parametri bilan o'zgartirish mumkin:

```python
print("Salom", end=" ")
print("dunyo")
# Natija: Salom dunyo   (bitta qatorda)
```

`end=""` — hech narsa qo'shmaydi, `end="!"` — oxiriga undov qo'yadi va yangi qatorga o'tmaydi.
""", title="end — qator oxirini boshqarish"),
        example(r'''
print("Yuklanmoqda", end="")
print(".", end="")
print(".", end="")
print(".")
print("Tayyor!")
''', title="end bilan bitta qatorda chiqarish"),
        text(r"""
Matn ichida maxsus **boshqaruv belgilari** bor. Ular teskari chiziq `\` bilan boshlanadi:

| Belgi | Ma'nosi | Misol | Natija |
|---|---|---|---|
| `\n` | yangi qator (*new line*) | `print("A\nB")` | A va B alohida qatorda |
| `\t` | tabulyatsiya (keng bo'sh joy) | `print("Ism:\tAli")` | `Ism:    Ali` |

`\n` yordamida bitta `print` bilan bir nechta qator chiqarish mumkin. `\t` esa ustunlarni tekislash
uchun qulay.
""", title=r"Maxsus belgilar: \n va \t"),
        example(r'''
print("1-qator\n2-qator\n3-qator")
print("Mahsulot\tNarx")
print("Non\t4000")
print("Sut\t12000")
''', title=r"\n va \t amalda"),
        callout('important', r"""
`sep` va `end` ni birga ham ishlatish mumkin: `print(1, 2, 3, sep=", ", end=".\n")` → `1, 2, 3.`
Ular har doim qiymatlardan **keyin**, qavs ichida yoziladi.
"""),
        exercise('l4_inline_end'),
    ],
    'tasks': [
        code_task('l4_inline_sep', "sep bilan vaqt", r"""
Bitta `print()` va `sep` yordamida ekranga `09:45` ni chiqaring. Muharrirdagi kodni o'zgartiring.
""", section='inline', points=2, starter_code='print("09", "45")\n',
            tests=[
                T('output_equals', "09:45", "Natija «09:45»"),
                T('code_contains', 'sep=', "sep parametri ishlatilgan", failure="Qavs ichiga sep=\":\" qo'shing."),
            ],
            hint='Hozir natija «09 45». Bo\'sh joy o\'rniga ikki nuqta kerak: sep=":"',
            full_solution='print("09", "45", sep=":")\n',
            explanation="`sep` qiymatlar orasidagi standart bo'sh joyni boshqa belgiga almashtiradi."),
        predict('l4_inline_end', "end ni kuzating", "Dastur nima chiqaradi?",
                code='print("A", end="-")\nprint("B", end="-")\nprint("C")\n', answer="A-B-C", section='inline',
                hint="end yangi qator o'rniga «-» qo'yadi; oxirgi print odatdagidek.",
                explanation="Birinchi ikki `print` yangi qatorga o'tmaydi, oxiriga `-` qo'yadi — hammasi bitta qatorda."),

        predict('l4_quiz_1', "Bir nechta qiymat", "Natija qanday bo'ladi?", code='print("Narx:", 5000, "so\'m")\n',
                answer="Narx: 5000 so'm",
                hint="Vergul bilan berilgan qiymatlar orasiga standart holda bitta bo'sh joy qo'yiladi.",
                explanation="Uchta qiymat orasida bittadan bo'sh joy: `Narx: 5000 so'm`."),
        single('l4_quiz_2', "sep vazifasi", "`sep` parametri nimani o'zgartiradi?", options=[
            opt("Qiymatlar orasidagi ajratgichni", True),
            opt("Qator oxiridagi belgini", False, "Bu `end` ning vazifasi."),
            opt("Matn rangini", False),
            opt("Qiymatlar tartibini", False),
        ], hint="Marjon o'xshatishini eslang.", explanation="`sep` — separator, ya'ni qiymatlar orasidagi ajratgich."),
        multiple('l4_quiz_3', "Ikki qator chiqaradigan kodlar", "Qaysi kodlar natijani **ikki alohida qatorda** chiqaradi?", options=[
            opt(r'`print("A\nB")`', True),
            opt('`print("A")` va keyin `print("B")`', True),
            opt('`print("A", "B")`', False, "Bu bitta qatorda: `A B`."),
            opt('`print("A", end="")` va keyin `print("B")`', False, "end=\"\" yangi qatorni o'chiradi: `AB`."),
        ], hint=r"`\n` va alohida `print` lar yangi qator beradi.",
            explanation=r"`\n` matn ichida yangi qator yaratadi; alohida `print` lar ham yangi qatordan boshlanadi."),

        single('l4_review_1', "Takrorlash: qo'shtirnoqlar", r"""
3-darsni eslang. `It's Python` matnini chiqarishning to'g'ri usuli qaysi?
""", section='review', options=[
            opt("`print('It's Python')`", False, "Apostrof matnni erta yopib qo'yadi."),
            opt('`print("It\'s Python")`', True),
            opt("`print(It's Python)`", False, "Qo'shtirnoq yo'q."),
        ], hint="Apostrof bor matn — qo'sh qo'shtirnoqda.", explanation="Apostrofli matn `\"...\"` ichida yoziladi."),

        code_task('l4_assignment', "Sana va chek", r"""
Ekranga aynan quyidagi natijani chiqaring:

```
Sana: 2026-11-08
Mahsulot	Narx
Non	4000
Sut	12000
```

**Talablar:**

1. Sana qismlarini (`2026`, `11`, `08`) **alohida qiymatlar** sifatida bering va ular orasidagi
   chiziqchani `sep` yordamida hosil qiling. «Sana:» so'zi va sana bitta qatorda tursin —
   buning uchun `end` parametri foydali.
2. Jadval ustunlari orasida **tabulyatsiya** `\t` bo'lsin.
""", expected_output_example="Sana: 2026-11-08\nMahsulot\tNarx\nNon\t4000\nSut\t12000",
            starter_code='# 1) Sana qatori\n\n# 2) Jadval (\\t bilan)\n',
            tests=[
                T('runs_ok', description="Dastur xatosiz ishlaydi"),
                T('output_regex', r"\ASana: 2026-11-08\n", "Birinchi qator: «Sana: 2026-11-08»"),
                T('output_contains', "Mahsulot\tNarx\nNon\t4000\nSut\t12000", r"Jadval ustunlari \t bilan ajratilgan",
                  failure=r"Ustunlar orasida bo'sh joy emas, \t bo'lishi kerak. Masalan: print('Non\t4000')"),
                T('code_contains', 'sep=', "sep parametri ishlatilgan", failure="Sana qismlarini sep=\"-\" bilan birlashtiring."),
                T('output_lines_min', '4', "Jami 4 qator"),
            ],
            hint=r'Sana uchun: print("Sana:", end=" ") va print(2026, 11, "08", sep="-"). Jadval uchun: print("Non\t4000").',
            partial_solution='print("Sana:", end=" ")\nprint(2026, 11, "08", sep="-")\n# endi jadval qatorlarini \\t bilan yozing\n',
            full_solution='print("Sana:", end=" ")\nprint(2026, 11, "08", sep="-")\nprint("Mahsulot\\tNarx")\nprint("Non\\t4000")\nprint("Sut\\t12000")\n',
            explanation=r"""`end=" "` birinchi `print` dan keyin yangi qatorga o'tkazmaydi; `sep="-"` sana qismlarini chiziqcha bilan biriktiradi; `\t` jadval ustunlarini tekislaydi."""),

        predict('l4_practice_easy', "sep=\"\"", "Natijani yozing:", code='print("Py", "thon", sep="")\n', answer="Python",
                section='practice', difficulty='easy', hint="Ajratgich bo'sh — qiymatlar yopishib qoladi.",
                explanation='`sep=""` — ajratgichsiz.'),
        predict('l4_practice_medium', r"\n va end", "Natijani yozing:", code='print("1\\n2", end=" ")\nprint(3)\n',
                answer="1\n2 3", section='practice', difficulty='medium',
                hint=r"""\n — yangi qator; end=" " — oxirida bo'sh joy, yangi qator yo'q.""",
                explanation=r"Birinchi `print` `1`, yangi qator, `2` va bo'sh joy chiqaradi; keyingi `3` shu qatorga yoziladi."),
        code_task('l4_practice_hard', "Bitta print bilan uchburchak", r"""
**Faqat bitta** `print()` va `\n` yordamida quyidagini chiqaring:

```
*
**
***
```
""", section='practice', difficulty='hard', points=5,
            tests=[
                T('output_equals', "*\n**\n***", "Uchburchak aynan mos"),
                T('code_regex', r"(?s)\A(?!.*print\(.*print\().*\Z", "Faqat bitta print() ishlatilgan",
                  failure="Bir nechta print emas — bitta print ichida \\n ishlating."),
            ],
            hint=r'print("*\n**\n***")',
            full_solution='print("*\\n**\\n***")\n',
            explanation=r"`\n` bitta matn ichida bir nechta qator yaratishga imkon beradi."),
    ],
}
