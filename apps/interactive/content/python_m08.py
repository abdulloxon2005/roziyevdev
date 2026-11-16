"""Python — 0 dan boshlash · 8-modul: Funksiyalar (Functions) (50–60-darslar)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 8,
    'title': "Funksiyalar (Functions)",
    'description': "Kodni qayta ishlatish: def, parametr va argument, return, standart qiymatlar, nomlangan argumentlar, *args, **kwargs va o'zgaruvchi ko'rinish sohasi.",
}

# ==============================================================================
# 50-DARS
# ==============================================================================
LESSON_50 = L(50, "Funksiya nima va nima uchun kerak?", 11,
    "Funksiya g'oyasini (kirish → ishlov → natija) tushunish, tayyor funksiyalarni eslash va bir xil kodni takrorlashning zararini ko'rish.",
    ["Funksiya", "Tayyor (built-in) funksiyalar", "Kodni takrorlamaslik (DRY)", "Chaqirish"],
    [
        text(r"""
Oshxonada **blender** bor: meva solasiz (kirish), tugmani bosasiz (ishlov), sharbat chiqadi (natija). Har safar mevani qanday maydalashni o'ylamaysiz — blender buni biladi. **Funksiya** — dasturdagi shunday «blender»: bir marta yoziladi, ko'p marta ishlatiladi.
""", title="Blender o'xshatishi"),
        text(r"""
Siz allaqachon ko'plab funksiyalarni ishlatgansiz:

| Funksiya | Kirish | Natija |
|---|---|---|
| `len("salom")` | matn | `5` |
| `max(3, 9, 4)` | sonlar | `9` |
| `round(3.14159, 2)` | son, xonalar | `3.14` |
| `print("Salom")` | matn | ekranga chiqaradi |

Funksiya **chaqiriladi** (nomi + qavs). Qavs ichidagi qiymatlar — funksiyaga beriladigan ma'lumot.

**Nima uchun o'zimiz ham yozishimiz kerak?** Bir xil kodni ko'p joyda takrorlash — noqulay va xavfli: o'zgartirish kerak bo'lsa, hamma joyni topib tuzatish kerak. Funksiya bilan kodni **bir joyda** yozib, **ko'p marta chaqiramiz**.
""", title="Funksiya — tayyor buyruq"),
        callout('important', r"""
Funksiya uch qismdan iborat: **kirish** (parametrlar), **ishlov** (tana) va **natija** (qaytariladigan qiymat). Hamma funksiyada ham kirish va natija bo'lishi shart emas.
""", title="Funksiya tuzilishi"),
        example(r'''
print(len("Python"))
print(max(3, 9, 4))
print(round(10 / 3, 2))
''', title="Tayyor funksiyalar", body="Natija: `6`, `9`, `3.33`. Har safar nima ishlashini bilmasak ham, funksiya ishni bajaradi."),
        example(r'''
print("=" * 20)
print("  Hisobot: Yanvar")
print("=" * 20)
print("=" * 20)
print("  Hisobot: Fevral")
print("=" * 20)
''', title="Takrorlanuvchi kod (muammo)", body="Bu yerda sarlavha chizish kodi **ikki marta** yozildi. Chiziq uzunligini o'zgartirmoqchi bo'lsak, hamma joyni tahrirlashimiz kerak. Keyingi darslarda buni funksiya bilan hal qilamiz."),
        exercise('l50_inline_pred'),
        recap(["funksiya — qayta ishlatiladigan kod bo'lagi", "`len`, `max`, `round`, `print` — tayyor funksiyalar", "takrorlanuvchi kodni funksiyaga olish kerak"], "o'zimizning funksiyamizni qanday yaratamiz? Buning kalit so'zi nima?"),
    ],
    [
        predict('l50_inline_pred', "Funksiya natijasi", "Dastur nima chiqaradi?", section='inline', code='print(max(len("ab"), len("abcd"), 3))\n', answer="4", points=2, hint="Avval ichki funksiyalar hisoblanadi.", explanation="`len` lar: 2, 4, 3; `max` → 4."),
        single('l50_quiz_1', "Funksiya nima?", "Funksiya nima uchun kerak?", options=[opt("Kodni qayta ishlatish uchun", True), opt("Faqat sonlarni chiqarish uchun", False), opt("Dasturni sekinlashtirish uchun", False)], hint="Blender.", explanation="Bir marta yozib, ko'p marta ishlatamiz."),
        single('l50_quiz_2', "Chaqirish", "Funksiyani chaqirish qanday yoziladi?", options=[opt("Nomi va qavs: `len(x)`", True), opt("Faqat nomi: `len`", False), opt("Nomi va figurali qavs: `len{x}`", False)], hint="Qavs bilan.", explanation="`nom(argumentlar)`."),
        predict('l50_quiz_3', "Ichma-ich chaqirish", "Dastur nima chiqaradi?", code='print(round(max(1.234, 2.567), 1))\n', answer="2.6", hint="Avval `max`, keyin `round`.", explanation="`max` → 2.567; `round(2.567, 1)` → 2.6."),
        code_task('l50_assignment', "Tayyor funksiyalar bilan", r"""
Foydalanuvchi uchta butun son kiritadi (alohida qatorlarda). **Tayyor funksiyalar** (`max`, `min`, `sum`) yordamida eng katta, eng kichik va yig'indini uch qatorda chiqaring. `4`, `9`, `2` → `9`, `2`, `15`.
""", starter_code='', points=10, tests=[T('output_equals', "9\n2\n15", "4, 9, 2", stdin="4\n9\n2\n"), T('output_equals', "-1\n-5\n-8", "-5, -2, -1 (manfiy)", stdin="-5\n-2\n-1\n".replace("-5\n-2\n-1\n", "-5\n-2\n-1\n"), hidden=True), T('code_contains', 'max(', "`max()` ishlatilgan"), T('code_contains', 'min(', "`min()` ishlatilgan")],
            hint="`max(a, b, c)`, `min(a, b, c)` va `sum([a, b, c])` — `sum` ro'yxat oladi.", partial_solution='a = int(input())\nb = int(input())\nc = int(input())\nprint(max(a, b, c))\n# min va sum ni chiqaring\n', full_solution='a = int(input())\nb = int(input())\nc = int(input())\nprint(max(a, b, c))\nprint(min(a, b, c))\nprint(sum([a, b, c]))\n', explanation="Uchta tayyor funksiya ishlatildi."),
        single('l50_practice_easy', "Easy: funksiya qismlari", "Funksiyaga beriladigan ma'lumot nima deyiladi?", section='practice', difficulty='easy', options=[opt("Kirish (argument/parametr)", True), opt("Natija", False), opt("Blok", False)], hint="Blenderga solinadigan meva.", explanation="Kirish ma'lumoti."),
        code_task('l50_practice_medium', "Medium: matn funksiyalari", r"""
Foydalanuvchi so'z kiritadi. Dastur so'zning uzunligini va KATTA harflardagi ko'rinishini ikki qatorda chiqarsin. `python` → `6` va `PYTHON`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "6\nPYTHON", "python", stdin="python\n"), T('output_equals', "1\nA", "a", stdin="a\n")], hint="`len` va `upper`.", full_solution='s = input()\nprint(len(s))\nprint(s.upper())\n', explanation="Tayyor funksiya va metod."),
        code_task('l50_practice_hard', "Hard: takrorni sezish", r"""
Quyidagi uchta kodni bitta **siklga** keltiring (funksiya hali o'tilmadi, lekin takrorni siklga yig'ish ham shu g'oya): `Salom, Ali!`, `Salom, Vali!`, `Salom, Gulnora!` ni chiqaring — `ismlar` listi va sikldan foydalaning.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Salom, Ali!\nSalom, Vali!\nSalom, Gulnora!", "Natija"), T('code_contains', 'for ', "`for` ishlatilgan")], hint="`for ism in ismlar:` ichida f-string.", full_solution='ismlar = ["Ali", "Vali", "Gulnora"]\nfor ism in ismlar:\n    print(f"Salom, {ism}!")\n', explanation="Takrorlanuvchi kodni bir joyga yig'dik — funksiyaning ham asosiy g'oyasi shu."),
    ])

# ==============================================================================
# 51-DARS
# ==============================================================================
LESSON_51 = L(51, "def orqali funksiya yaratish", 12,
    "def kalit so'zi bilan o'z funksiyasini yaratish va uni chaqirish; funksiya yaratish va chaqirishni farqlash.",
    ["def", "Funksiya nomi", "Tana va chekinish", "Chaqirish", "Funksiya bir necha marta chaqiriladi"],
    [
        text(r"""
Oldingi darsda sarlavha chizish kodi takrorlandi. Endi uni **bir marta yozib**, kerak bo'lganda **chaqiramiz**. Funksiya **`def`** (inglizcha *define* — «aniqla») bilan yaratiladi.
""", title="O'z funksiyamiz"),
        text(r"""
```python
def salom():
    print("Assalomu alaykum!")
    print("Xush kelibsiz!")

salom()
salom()
```

- `def` + **nom** + `()` + `:` — funksiya sarlavhasi.
- Tana — **4 ta bo'sh joy** bilan suriladi.
- `def` faqat funksiyani **yaratadi** (ishlatmaydi!). Ishlatish uchun uni **chaqirish** kerak: `salom()`.
- Funksiya nomlari ham o'zgaruvchilardek `snake_case`: `sarlavha_chiz`.
- Funksiya **chaqirishdan oldin** yaratilgan bo'lishi kerak.
""", title="def tuzilishi"),
        callout('analogy', r"""
`def` — **retsept yozish**. Retsept yozilishi bilan ovqat tayyor bo'lmaydi; ovqat tayyorlash uchun retseptni **bajarish** (chaqirish) kerak. Bitta retseptni istagancha ishlatish mumkin.
""", title="Hayotiy o'xshatish"),
        example(r'''
def sarlavha():
    print("=" * 20)
    print("  HISOBOT")
    print("=" * 20)

sarlavha()
print("Savdo: 5 mln")
sarlavha()
''', title="Sarlavha funksiyasi", body="`sarlavha()` ikki marta chaqirildi — sarlavha ikki marta chiqdi, lekin kod bir marta yozildi."),
        example(r'''
def xayrlash():
    print("Xayr!")

print("Dastur boshlandi")
xayrlash()
print("Dastur tugadi")
''', title="Amaliy: chaqirish tartibi", body="Funksiya yaratilganda hech narsa chiqmaydi. Dastur yuqoridan pastga boradi va `xayrlash()` chaqirilgan joyda ishlaydi: `Dastur boshlandi`, `Xayr!`, `Dastur tugadi`."),
        exercise('l51_inline_fix'),
        callout('warning', r"""
`def` ni yozib, chaqirishni **unutmang** — aks holda hech narsa bo'lmaydi. `salom` (qavssiz) funksiyani chaqirmaydi, faqat nomini ko'rsatadi.
""", title="Diqqat"),
        recap(["`def nom():` — yaratish", "`nom()` — chaqirish", "tana chekinish bilan yoziladi"], "funksiyaga ma'lumot (masalan, ism) berish mumkinmi? Shunda har safar boshqa odamga salom beradi!"),
    ],
    [
        fix_task('l51_inline_fix', "Chaqirishni unutdik", "Dastur hech narsa chiqarmayapti. Natija `Salom!` bo'lsin.", section='inline', points=2, starter_code='def salom():\n    print("Salom!")\n', tests=[T('output_equals', "Salom!", "Natija: Salom!")], hint="Funksiya yaratildi, lekin ishlatilmadi.", full_solution='def salom():\n    print("Salom!")\n\nsalom()\n', explanation="Funksiyani chaqirish kerak."),
        predict('l51_quiz_1', "Chaqirish soni", "Dastur nima chiqaradi?", code='def a():\n    print("X")\n\na()\na()\n', answer="X\nX", hint="Ikki marta chaqirilgan.", explanation="Ikkita chaqiruv — ikkita `X`."),
        predict('l51_quiz_2', "Tartib", "Dastur nima chiqaradi?", code='def f():\n    print("2")\n\nprint("1")\nf()\nprint("3")\n', answer="1\n2\n3", hint="Funksiya chaqirilganda ishlaydi.", explanation="Qatorma-qator bajariladi."),
        single('l51_quiz_3', "def", "`def salom():` nima qiladi?", options=[opt("Funksiyani yaratadi (hali ishlatmaydi)", True), opt("Funksiyani ishga tushiradi", False), opt("Matn chiqaradi", False)], hint="Retsept yozish.", explanation="Faqat yaratadi."),
        code_task('l51_assignment', "Vizitka funksiyasi", r"""
`vizitka` nomli funksiya yarating: u uch qator chiqarsin — `==========`, `  PYTHON  `, `==========` (ikki chetda 10 ta `=`; ichkarida ikki bo'sh joy + `PYTHON` + ikki bo'sh joy). So'ng uni **ikki marta** chaqiring.
""", starter_code='', points=10, tests=[T('output_equals', "==========\n  PYTHON  \n==========\n==========\n  PYTHON  \n==========", "Ikki marta chaqirilgan"), T('code_regex', r"def\s+vizitka\s*\(\s*\)\s*:", "`vizitka` funksiyasi yaratilgan"), T('code_regex', r"(?m)^vizitka\(\)(?s:.*)^vizitka\(\)", "Ikki marta chaqirilgan")],
            hint="`def vizitka():` ichida uchta `print`; keyin `vizitka()` ikki marta.", partial_solution='def vizitka():\n    print("==========")\n    # qolgan ikki qatorni yozing\n\nvizitka()\n', full_solution='def vizitka():\n    print("==========")\n    print("  PYTHON  ")\n    print("==========")\n\nvizitka()\nvizitka()\n', explanation="Bir marta yozildi — ikki marta ishladi."),
        single('l51_practice_easy', "Easy: kalit so'z", "Funksiya yaratish uchun qaysi kalit so'z ishlatiladi?", section='practice', difficulty='easy', options=[opt("`def`", True), opt("`func`", False), opt("`function`", False)], hint="Define.", explanation="`def`."),
        code_task('l51_practice_medium', "Medium: uch xil salom", r"""
`salom` funksiyasi `Salom!` chiqarsin; `xayr` funksiyasi `Xayr!` chiqarsin. Ketma-ket chaqiring: `salom`, `xayr`, `salom`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Salom!\nXayr!\nSalom!", "Natija"), T('code_regex', r"def\s+salom", "`salom` yaratilgan"), T('code_regex', r"def\s+xayr", "`xayr` yaratilgan")], hint="Ikkita `def`.", full_solution='def salom():\n    print("Salom!")\n\ndef xayr():\n    print("Xayr!")\n\nsalom()\nxayr()\nsalom()\n', explanation="Funksiyalarni mustaqil chaqirish."),
        code_task('l51_practice_hard', "Hard: funksiya ichida funksiya chaqirish", r"""
`chiziq()` — 15 ta `-` chiqaradi. `menyu()` — `chiziq()` ni chaqirib, keyin `1. Boshlash`, `2. Chiqish` va yana `chiziq()` chiqaradi. Faqat `menyu()` ni bir marta chaqiring:

```
---------------
1. Boshlash
2. Chiqish
---------------
```
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "---------------\n1. Boshlash\n2. Chiqish\n---------------", "Natija")], hint="Funksiya ichidan boshqa funksiyani ham chaqirish mumkin.", full_solution='def chiziq():\n    print("-" * 15)\n\ndef menyu():\n    chiziq()\n    print("1. Boshlash")\n    print("2. Chiqish")\n    chiziq()\n\nmenyu()\n', explanation="Funksiyalar bir-birini chaqira oladi."),
    ])

# ==============================================================================
# 52-DARS
# ==============================================================================
LESSON_52 = L(52, "Funksiyaga parametr berish", 12,
    "Funksiyaga ma'lumot uzatish uchun parametrlardan foydalanish va bir nechta parametrli funksiyalar yaratish.",
    ["Parametr", "Bir nechta parametr", "Funksiya ichida parametrdan foydalanish"],
    [
        text(r"""
`salom()` funksiyasi hammaga bir xil salom beradi. Lekin biz «Salom, **Aziza**!» deb **ism bo'yicha** salom bermoqchimiz. Buning uchun funksiyaga **ma'lumot uzatish** kerak — buni **parametr** qiladi.
""", title="Funksiya ma'lumot qabul qilsin"),
        text(r"""
```python
def salom(ism):
    print(f"Salom, {ism}!")

salom("Aziza")
salom("Bobur")
```

- Qavs ichidagi `ism` — **parametr**: funksiya ichida o'zgaruvchi kabi ishlatiladi.
- Chaqirishda berilgan `"Aziza"` — parametrga **qiymat** bo'lib tushadi.
- Bir nechta parametr — vergul bilan: `def qosh(a, b):`.
- Parametr faqat funksiya **ichida** mavjud.
""", title="Parametr"),
        callout('analogy', r"""
Parametr — **blenderdagi bo'sh joy**: qanday meva solinishini oldindan bilmaymiz, shuning uchun «bu yerga meva solinadi» deb joy qoldiramiz.
""", title="Hayotiy o'xshatish"),
        example(r'''
def salom(ism):
    print(f"Salom, {ism}!")

salom("Aziza")
salom("Bobur")
''', title="Bitta parametr", body="Funksiya bir xil, lekin har safar boshqa ism bilan ishlaydi: `Salom, Aziza!` va `Salom, Bobur!`."),
        example(r'''
def chek(mahsulot, narx, soni):
    print(f"{mahsulot}: {narx} x {soni} = {narx * soni}")

chek("Non", 4500, 3)
chek("Sut", 12000, 2)
''', title="Amaliy: bir nechta parametr", body="Uchta parametr. Natija: `Non: 4500 x 3 = 13500` va `Sut: 12000 x 2 = 24000`."),
        exercise('l52_inline_blank'),
        callout('warning', r"""
Parametrlar soni chaqiruvdagi qiymatlar soniga mos bo'lishi kerak: `chek("Non", 4500)` (3 ta kerak, 2 ta berildi) — `TypeError`.
""", title="Diqqat"),
        recap(["parametr — funksiya kirishi", "`def nom(a, b):`", "chaqirishda qiymatlar beriladi"], "«parametr» va «argument» — bir narsami yoki farqi bormi?"),
    ],
    [
        fill('l52_inline_blank', "Bo'sh joy", "Funksiya berilgan sonning ikkilangan qiymatini chiqarsin: `kopaytir(5)` → `10`.", 'def ikki_baravar(___):\n    print(son * 2)\n\nikki_baravar(5)\n', ['son'], section='inline', points=2, tests=[T('output_equals', "10", "Natija: 10")], hint="Funksiya ichida `son` ishlatilgan.", explanation="Parametr nomi tanada ishlatilgan nom bilan bir xil."),
        predict('l52_quiz_1', "Parametr", "Dastur nima chiqaradi?", code='def f(x):\n    print(x + 1)\n\nf(4)\nf(10)\n', answer="5\n11", hint="Har chaqiruvda `x` boshqa.", explanation="`4 + 1`, `10 + 1`."),
        single('l52_quiz_2', "Xato", "`def f(a, b): ...` ni `f(1)` deb chaqirsak?", options=[opt("`TypeError`: argument yetmaydi", True), opt("Natija chiqadi", False), opt("`NameError`", False)], hint="Ikkita kerak.", explanation="Argumentlar soni mos bo'lishi shart."),
        predict('l52_quiz_3', "Ikki parametr", "Dastur nima chiqaradi?", code='def f(a, b):\n    print(a - b)\n\nf(10, 3)\nf(3, 10)\n', answer="7\n-7", hint="Tartib muhim.", explanation="Birinchi qiymat `a` ga, ikkinchisi `b` ga."),
        code_task('l52_assignment', "Salomlashish funksiyasi", r"""
`salom(ism, shahar)` funksiyasini yarating: u `Salom, <ism>! Siz <shahar>danmisiz?` chiqarsin. Quyidagi chaqiruvlar uchun ishlashi kerak: `salom("Aziza", "Toshkent")` → `Salom, Aziza! Siz Toshkentdanmisiz?`
""", starter_code='', points=10, tests=[T('output_equals', "Salom, Aziza! Siz Toshkentdanmisiz?\nSalom, Bobur! Siz Samarqanddanmisiz?", "Ikki chaqiruv", harness='salom("Aziza", "Toshkent")\nsalom("Bobur", "Samarqand")'), T('code_regex', r"def\s+salom\s*\(\s*\w+\s*,\s*\w+\s*\)", "Ikki parametrli `salom`")],
            hint="`def salom(ism, shahar):` va ichida f-string.", partial_solution='def salom(ism, shahar):\n    # f-string bilan chiqaring\n    pass\n', full_solution='def salom(ism, shahar):\n    print(f"Salom, {ism}! Siz {shahar}danmisiz?")\n', explanation="Tekshiruv funksiyangizni turli argumentlar bilan chaqirib ko'radi."),
        single('l52_practice_easy', "Easy: parametr", "Parametr qayerda yoziladi?", section='practice', difficulty='easy', options=[opt("`def` qatoridagi qavs ichida", True), opt("Funksiya tanasida", False), opt("Chaqirishda", False)], hint="Sarlavhada.", explanation="`def nom(parametr):`."),
        code_task('l52_practice_medium', "Medium: yulduzlar", r"""
`yulduz(n)` funksiyasi `n` ta `*` ni bir qatorda chiqarsin. `yulduz(3)` → `***`, `yulduz(5)` → `*****`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "***\n*****\n*", "Uch chaqiruv", harness='yulduz(3)\nyulduz(5)\nyulduz(1)'), T('output_equals', "", "n = 0 — bo'sh qator", harness='yulduz(0)')], hint="`print(\"*\" * n)`.", full_solution='def yulduz(n):\n    print("*" * n)\n', explanation="Matnni `*` bilan takrorlash."),
        code_task('l52_practice_hard', "Hard: jadval qatori", r"""
`qator(nom, narx)` funksiyasi `nom` ni 10 belgi kenglikda chapga tekislab, `narx` ni 8 belgi kenglikda o'ngga tekislab chiqarsin: `qator("Non", 4500)` → `Non           4500` (`f"{nom:<10}{narx:>8}"`).
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Non           4500\nSut          12000", "Ikki qator", harness='qator("Non", 4500)\nqator("Sut", 12000)')], hint="f-stringda `<10` — chapga, `>8` — o'ngga tekislash: `f\"{nom:<10}{narx:>8}\"`.", full_solution='def qator(nom, narx):\n    print(f"{nom:<10}{narx:>8}")\n', explanation="f-string tekislash: `<` chap, `>` o'ng, raqam — kenglik."),
    ])

# ==============================================================================
# 53-DARS
# ==============================================================================
LESSON_53 = L(53, "Argumentlar va parametrlar farqi", 11,
    "Parametr va argument orasidagi farqni, argumentlarning tartibi (pozitsion) va sonining ahamiyatini tushunish.",
    ["Parametr", "Argument", "Pozitsion argumentlar", "Argumentlar soni", "TypeError"],
    [
        text(r"""
Oshxonada retseptda yozilgan: «**___ gramm un** qo'shing» — bu **parametr** (bo'sh joy). Siz «**200 gramm**» qo'shsangiz — bu **argument** (aniq qiymat). Ikkala so'z ko'pincha aralashadi, lekin farqi bor.
""", title="Retsept va ingredient"),
        text(r"""
| Atama | Qayerda | Misol |
|---|---|---|
| **Parametr** | funksiyani **yaratishda** (`def` qatorida) — nom | `def kvadrat(son):` — `son` |
| **Argument** | funksiyani **chaqirishda** — haqiqiy qiymat | `kvadrat(5)` — `5` |

Argumentlar parametrlarga **tartib bilan** (pozitsiyasi bo'yicha) moslanadi:

```python
def bo_l(a, b):
    print(a / b)

bo_l(10, 2)   # a=10, b=2 → 5.0
bo_l(2, 10)   # a=2, b=10 → 0.2
```

Argumentlar soni parametrlar soniga teng bo'lishi shart (hozircha): kam yoki ko'p bo'lsa — `TypeError`.
""", title="Farqi"),
        callout('analogy', r"""
Parametr — **bo'sh formadagi grafa** («Ism: ____»). Argument — **to'ldirilgan qiymat** («Ism: Aziza»).
""", title="Hayotiy o'xshatish"),
        example(r'''
def ayir(a, b):
    print(a - b)

ayir(10, 4)
ayir(4, 10)
''', title="Tartib muhim", body="Argumentlar o'rni almashsa, natija o'zgaradi: `6` va `-6`."),
        example(r'''
def tanishtir(ism, yosh, shahar):
    print(f"{ism}, {yosh} yosh, {shahar}")

tanishtir("Ali", 17, "Buxoro")
tanishtir("Gulnora", 19, "Xiva")
''', title="Amaliy: uchta argument", body="Uchta parametr — uchta argument kerak, tartib: ism, yosh, shahar. `tanishtir(17, \"Ali\", \"Buxoro\")` ma'noga ega bo'lmagan natija bergan bo'lardi."),
        exercise('l53_inline_pred'),
        recap(["parametr — `def` dagi nom", "argument — chaqirishdagi qiymat", "argumentlar tartib bilan moslanadi"], "argument bermasak ham funksiya ishlashi uchun parametrga «standart qiymat» berish mumkinmi?"),
    ],
    [
        predict('l53_inline_pred', "Tartib", "Dastur nima chiqaradi?", section='inline', code='def f(a, b):\n    print(a, b)\n\nf("x", "y")\n', answer="x y", points=2, hint="Birinchi argument — `a`.", explanation="Tartib bilan."),
        single('l53_quiz_1', "Parametr yoki argument", "`kvadrat(7)` dagi `7` nima?", options=[opt("Argument", True), opt("Parametr", False), opt("Funksiya nomi", False)], hint="Chaqirishda berilgan.", explanation="Argument."),
        single('l53_quiz_2', "Parametr yoki argument (2)", "`def kvadrat(son):` dagi `son` nima?", options=[opt("Parametr", True), opt("Argument", False), opt("Natija", False)], hint="`def` qatorida.", explanation="Parametr."),
        predict('l53_quiz_3', "Almashgan tartib", "Dastur nima chiqaradi?", code='def f(a, b):\n    print(a // b)\n\nf(7, 2)\nf(2, 7)\n', answer="3\n0", hint="Qaysi biri `a`, qaysi `b`?", explanation="`7 // 2 = 3`, `2 // 7 = 0`."),
        code_task('l53_assignment', "Bo'lish funksiyasi", r"""
`bo_l(bolinuvchi, bo_luvchi)` funksiyasini yarating: u bo'linmani **2 xonali kasr** bilan chiqarsin. `bo_l(10, 4)` → `2.50`, `bo_l(1, 3)` → `0.33`.
""", starter_code='', points=10, tests=[T('output_equals', "2.50\n0.33\n5.00", "Uch chaqiruv", harness='bo_l(10, 4)\nbo_l(1, 3)\nbo_l(10, 2)'), T('output_equals', "0.50\n2.00", "Tartib muhim", harness='bo_l(1, 2)\nbo_l(2, 1)', hidden=True)],
            hint="`print(f\"{bolinuvchi / bo_luvchi:.2f}\")`.", partial_solution='def bo_l(bolinuvchi, bo_luvchi):\n    # bo\'linmani 2 xonali chiqaring\n    pass\n', full_solution='def bo_l(bolinuvchi, bo_luvchi):\n    print(f"{bolinuvchi / bo_luvchi:.2f}")\n', explanation="Tartib: birinchi — bo'linuvchi."),
        single('l53_practice_easy', "Easy: soni", "`def f(a, b, c)` ni nechta argument bilan chaqirish kerak?", section='practice', difficulty='easy', options=[opt("3 ta", True), opt("2 ta", False), opt("Istalgancha", False)], hint="Parametrlar soniga teng.", explanation="3 ta."),
        code_task('l53_practice_medium', "Medium: to'g'ri to'rtburchak", r"""
`yuza(en, boy)` va `perimetr(en, boy)` funksiyalarini yarating — ular mos ravishda yuza va perimetrni chiqarsin. `yuza(3, 4)` → `12`, `perimetr(3, 4)` → `14`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "12\n14\n25\n20", "Natija", harness='yuza(3, 4)\nperimetr(3, 4)\nyuza(5, 5)\nperimetr(5, 5)')], hint="Perimetr: `2 * (en + boy)`.", full_solution='def yuza(en, boy):\n    print(en * boy)\n\ndef perimetr(en, boy):\n    print(2 * (en + boy))\n', explanation="Ikkita funksiya, bir xil parametrlar."),
        code_task('l53_practice_hard', "Hard: chegirma", r"""
`chegirma(narx, foiz)` — narxdan `foiz` foiz chegirma qilingan yakuniy narxni **butun son sifatida** (`int` ga aylantirmay, oddiy hisob: `narx * (100 - foiz) // 100`) chiqarsin. `chegirma(200000, 15)` → `170000`, `chegirma(1000, 0)` → `1000`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "170000\n1000\n0", "Natija", harness='chegirma(200000, 15)\nchegirma(1000, 0)\nchegirma(500, 100)')], hint="`narx * (100 - foiz) // 100`.", full_solution='def chegirma(narx, foiz):\n    print(narx * (100 - foiz) // 100)\n', explanation="Butun bo'lish bilan butun natija."),
    ])

# ==============================================================================
# 54-DARS
# ==============================================================================
LESSON_54 = L(54, "return operatori", 13,
    "return bilan funksiyadan qiymat qaytarish, print va return farqini tushunish va natijani o'zgaruvchiga saqlash.",
    ["return", "print va return farqi", "Natijani saqlash", "None", "return dan keyingi kod"],
    [
        text(r"""
Hozirgacha funksiyalarimiz natijani ekranga **chiqarib** qo'ydi. Lekin `len("salom")` natijani ekranga chiqarmaydi — **qaytaradi**, biz uni o'zgaruvchiga saqlab, keyin ishlata olamiz: `n = len("salom")`. O'z funksiyalarimiz ham shunday qilishi uchun **`return`** kerak.
""", title="Ekranga chiqarish va qaytarish"),
        text(r"""
```python
def kvadrat(son):
    return son * son

x = kvadrat(5)       # 25 saqlandi
print(x + 1)         # 26
print(kvadrat(3) + kvadrat(4))   # 25
```

| | `print()` | `return` |
|---|---|---|
| Nima qiladi | natijani **ekranga** chiqaradi | natijani **chaqirgan joyga qaytaradi** |
| Keyin ishlatish | mumkin emas | mumkin (o'zgaruvchiga, hisobga) |

- `return` bajarilishi bilan funksiya **tugaydi** — undan keyingi qatorlar bajarilmaydi.
- `return` yo'q funksiya `None` qaytaradi.
""", title="return"),
        callout('analogy', r"""
`print` — **ovoz chiqarib o'qish** (eshitgan odam eslab qolmasa, yo'qoladi). `return` — **javobni qog'ozga yozib berish** (saqlab, keyin ishlatsa bo'ladi).
""", title="Hayotiy o'xshatish"),
        example(r'''
def yig_indi(a, b):
    return a + b

natija = yig_indi(3, 4)
print(natija)
print(yig_indi(1, 2) * 10)
''', title="Qaytarilgan qiymatni ishlatish", body="`7` va `30`. `return` tufayli natijani hisobda ishlatdik — `print` bilan bu mumkin emas edi."),
        example(r'''
def narx_hisobla(narx, soni):
    jami = narx * soni
    return jami

a = narx_hisobla(4500, 3)
b = narx_hisobla(12000, 2)
print("Jami:", a + b)

def f():
    print("ichida")

x = f()
print(x)
''', title="Amaliy: bir nechta chaqiruv natijasi + None", body="`Jami: 37500`. `f()` `return` siz — shuning uchun `x` — `None`: `ichida` va `None` chiqadi."),
        exercise('l54_inline_pred'),
        callout('warning', r"""
`return` dan keyingi kod **hech qachon bajarilmaydi**. Ko'p boshlovchilar `return` o'rniga `print` yozib, keyin natijani ishlata olmay qoladi.
""", title="Diqqat"),
        recap(["`return` qiymat qaytaradi va funksiyani tugatadi", "qaytarilgan qiymatni o'zgaruvchiga saqlash mumkin", "`return` yo'q bo'lsa — `None`"], "agar funksiyaga argument bermasak ham ishlashi uchun standart qiymat bersak-chi?"),
    ],
    [
        predict('l54_inline_pred', "return", "Dastur nima chiqaradi?", section='inline', code='def f(x):\n    return x * 2\n\nprint(f(3) + f(4))\n', answer="14", points=2, hint="6 + 8.", explanation="`f(3)` = 6, `f(4)` = 8."),
        predict('l54_quiz_1', "return dan keyin", "Dastur nima chiqaradi?", code='def f():\n    return "A"\n    print("B")\n\nprint(f())\n', answer="A", hint="`return` funksiyani tugatadi.", explanation="`print(\"B\")` bajarilmaydi."),
        predict('l54_quiz_2', "None", "Dastur nima chiqaradi?", code='def f(x):\n    print(x)\n\nr = f(5)\nprint(r)\n', answer="5\nNone", hint="`f` hech narsa qaytarmaydi.", explanation="`return` yo'q — `None`."),
        single('l54_quiz_3', "Farqi", "Natijani keyinroq hisobda ishlatish uchun nima kerak?", options=[opt("`return`", True), opt("`print`", False), opt("`input`", False)], hint="Qaytarilgan qiymatni saqlab bo'ladi.", explanation="`return`."),
        code_task('l54_assignment', "Katta sonni qaytaruvchi", r"""
`katta(a, b)` funksiyasini yarating: u ikki sonning **kattasini qaytarsin** (`print` emas, `return`). `katta(3, 9)` → `9`, `katta(-1, -5)` → `-1`, `katta(4, 4)` → `4`.
""", starter_code='', points=10, tests=[T('output_equals', "9\n-1\n4\n10", "To'rt chaqiruv", harness='print(katta(3, 9))\nprint(katta(-1, -5))\nprint(katta(4, 4))\nprint(katta(10, 2))'), T('output_equals', "True", "Natijani hisobda ishlatish mumkin", harness='print(katta(2, 5) + katta(1, 3) == 8)'), T('code_contains', 'return', "`return` ishlatilgan")],
            hint="`if a > b: return a`, aks holda `return b`.", partial_solution='def katta(a, b):\n    if a > b:\n        return a\n    # aks holda b ni qaytaring\n', full_solution='def katta(a, b):\n    if a > b:\n        return a\n    return b\n', explanation="Funksiya qiymat qaytaradi; tekshiruv natijani hisobda ishlatadi."),
        single('l54_practice_easy', "Easy: return nima qiladi?", "`return x` nima qiladi?", section='practice', difficulty='easy', options=[opt("x ni qaytarib, funksiyani tugatadi", True), opt("x ni ekranga chiqaradi", False), opt("x ni o'chiradi", False)], hint="Javob berish.", explanation="Qiymat qaytaradi."),
        code_task('l54_practice_medium', "Medium: juftmi?", r"""
`juft_mi(n)` funksiyasi `n` juft bo'lsa `True`, aks holda `False` **qaytarsin**. `juft_mi(4)` → `True`, `juft_mi(7)` → `False`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "True\nFalse\nTrue\nFalse", "Natija", harness='print(juft_mi(4))\nprint(juft_mi(7))\nprint(juft_mi(0))\nprint(juft_mi(-3))')], hint="`return n % 2 == 0`.", full_solution='def juft_mi(n):\n    return n % 2 == 0\n', explanation="Taqqoslash natijasi `bool` — to'g'ridan-to'g'ri qaytarish mumkin."),
        code_task('l54_practice_hard', "Hard: ro'yxat statistikasi", r"""
`statistika(sonlar)` funksiyasi list oladi va **ikkita qiymat** qaytarsin: `(eng_kichik, eng_katta)` tuple'i. `statistika([3, 1, 8])` → `(1, 8)`. (`return a, b` tuple qaytaradi.)
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "(1, 8)\n(5, 5)\n(-2, 4)", "Natija", harness='print(statistika([3, 1, 8]))\nprint(statistika([5]))\nprint(statistika([4, -2, 0]))')], hint="`return min(sonlar), max(sonlar)`.", full_solution='def statistika(sonlar):\n    return min(sonlar), max(sonlar)\n', explanation="`return a, b` — tuple qaytaradi."),
    ])

# ==============================================================================
# 55-DARS
# ==============================================================================
LESSON_55 = L(55, "Standart parametr qiymatlari", 11,
    "Parametrga standart (default) qiymat berish, ixtiyoriy argumentlar va standart qiymatli parametrlarni oxirida yozish qoidasi.",
    ["Standart qiymat", "Ixtiyoriy argument", "Parametrlar tartibi", "Qiymatni qayta belgilash"],
    [
        text(r"""
Pochta xizmatida «yetkazib berish»: agar manzil aytmasangiz — **odatiy** (uyingizga) yetkaziladi. Funksiyada ham: argument berilmasa, **standart qiymat** ishlatiladi.
""", title="Aytilmasa — odatdagidek"),
        text(r"""
```python
def salom(ism, til="uz"):
    if til == "uz":
        print(f"Salom, {ism}!")
    else:
        print(f"Hello, {ism}!")

salom("Aziza")          # til berilmadi → "uz"
salom("Aziza", "en")    # til = "en"
```

- `parametr=qiymat` — standart qiymat (`=` atrofida bo'sh joysiz yozish odat).
- Argument berilsa — standart qiymat **bekor** bo'ladi.
- **Qoida:** standart qiymatli parametrlar **oxirida** turishi kerak: `def f(a, b=1)` ✔, `def f(a=1, b)` ✘ (`SyntaxError`).
""", title="Standart qiymat"),
        callout('analogy', r"""
Kafedagi **«odatdagi qahva»**: «bitta qahva» desangiz — shakarsiz, standart o'lchamda. «Shakar bilan, katta» desangiz — odatdagidan farqli.
""", title="Hayotiy o'xshatish"),
        example(r'''
def daraja(son, d=2):
    return son ** d

print(daraja(5))
print(daraja(2, 10))
''', title="Daraja", body="`daraja(5)` — kvadrat (`25`); `daraja(2, 10)` — `1024`."),
        example(r'''
def chegirmali_narx(narx, chegirma=10):
    return narx - narx * chegirma // 100

print(chegirmali_narx(50000))
print(chegirmali_narx(50000, 25))
print(chegirmali_narx(50000, 0))
''', title="Amaliy: standart chegirma", body="Standart chegirma 10%: `45000`; 25% bilan: `37500`; chegirmasiz: `50000`."),
        exercise('l55_inline_fix'),
        callout('warning', r"""
Standart qiymat sifatida o'zgaruvchan tur (list, dict) ishlatmang: `def f(a=[])` — kutilmagan xatolarga olib keladi. Hozircha oddiy qiymatlar (son, matn, `True`) ishlating.
""", title="Diqqat"),
        recap(["`def f(a, b=qiymat)`", "berilmasa standart qiymat ishlaydi", "standart qiymatlilar oxirida"], "argumentlarni tartib emas, NOMI bilan berish mumkinmi? Masalan, `f(b=5, a=1)`."),
    ],
    [
        fix_task('l55_inline_fix', "Tartibni tuzating", "Kod `SyntaxError` beryapti. Tuzating — natija `Salom, Ali!`", section='inline', points=2, starter_code='def salom(belgi="!", ism):\n    print("Salom, " + ism + belgi)\n\nsalom("Ali")\n', tests=[T('output_equals', "Salom, Ali!", "Natija to'g'ri")], hint="Standart qiymatli parametr oxirida bo'lishi kerak.", full_solution='def salom(ism, belgi="!"):\n    print("Salom, " + ism + belgi)\n\nsalom("Ali")\n', explanation="Standart qiymatli parametr oxirga o'tdi."),
        predict('l55_quiz_1', "Standart qiymat", "Dastur nima chiqaradi?", code='def f(a, b=10):\n    return a + b\n\nprint(f(1), f(1, 2))\n', answer="11 3", hint="Ikkinchi chaqiruvda `b` berilgan.", explanation="`1 + 10` va `1 + 2`."),
        single('l55_quiz_2', "Qoida", "Qaysi yozuv noto'g'ri?", options=[opt("`def f(a=1, b):`", True), opt("`def f(a, b=1):`", False), opt("`def f(a=1, b=2):`", False)], hint="Standart qiymatsiz parametr standartlidan keyin kelolmaydi.", explanation="Standart qiymatlilar oxirida."),
        predict('l55_quiz_3', "Qayta belgilash", "Dastur nima chiqaradi?", code='def f(x=5):\n    return x * 2\n\nprint(f(), f(1))\n', answer="10 2", hint="Argument bersa — u ishlatiladi.", explanation="`f()` → 10; `f(1)` → 2."),
        code_task('l55_assignment', "Salomlashuv", r"""
`salom(ism, belgi="!")` funksiyasi `Salom, <ism><belgi>` **qaytarsin** (`print` emas). `salom("Ali")` → `Salom, Ali!`; `salom("Ali", "?")` → `Salom, Ali?`.
""", starter_code='', points=10, tests=[T('output_equals', "Salom, Ali!\nSalom, Ali?\nSalom, Vali.", "Uch chaqiruv", harness='print(salom("Ali"))\nprint(salom("Ali", "?"))\nprint(salom("Vali", "."))'), T('code_contains', 'return', "`return` ishlatilgan"), T('code_regex', r'belgi\s*=\s*["\']!["\']', "Standart qiymat `!`")],
            hint="`def salom(ism, belgi=\"!\"):`.", partial_solution='def salom(ism, belgi="!"):\n    # natijani qaytaring\n    pass\n', full_solution='def salom(ism, belgi="!"):\n    return "Salom, " + ism + belgi\n', explanation="Standart qiymat berilmasa ishlaydi."),
        single('l55_practice_easy', "Easy: standart", "`def f(x=3)` ni `f()` deb chaqirsak, `x` nechaga teng?", section='practice', difficulty='easy', options=[opt("3", True), opt("0", False), opt("Xato", False)], hint="Standart qiymat.", explanation="3."),
        code_task('l55_practice_medium', "Medium: takrorlash", r"""
`takrorla(matn, soni=2)` funksiyasi matnni `soni` marta takrorlab **qaytarsin**. `takrorla("ha")` → `haha`; `takrorla("ha", 3)` → `hahaha`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "haha\nhahaha\n\nab", "Natija", harness='print(takrorla("ha"))\nprint(takrorla("ha", 3))\nprint(takrorla("x", 0))\nprint(takrorla("ab", 1))')], hint="`return matn * soni`.", full_solution='def takrorla(matn, soni=2):\n    return matn * soni\n', explanation="Matn * son."),
        code_task('l55_practice_hard', "Hard: soliq hisobi", r"""
`jami_narx(narx, soni=1, qqs=12)` — `narx * soni` ga `qqs` foiz soliq qo'shib, **butun son** qaytarsin (`narx * soni * (100 + qqs) // 100`). `jami_narx(1000)` → `1120`; `jami_narx(1000, 3)` → `3360`; `jami_narx(1000, 2, 0)` → `2000`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "1120\n3360\n2000\n5500", "Natija", harness='print(jami_narx(1000))\nprint(jami_narx(1000, 3))\nprint(jami_narx(1000, 2, 0))\nprint(jami_narx(5000, 1, 10))')], hint="Ikki standart parametr, ikkalasi oxirida.", full_solution='def jami_narx(narx, soni=1, qqs=12):\n    return narx * soni * (100 + qqs) // 100\n', explanation="Bir nechta standart parametr."),
    ])

# ==============================================================================
# 56-DARS
# ==============================================================================
LESSON_56 = L(56, "Nomlangan argumentlar", 11,
    "Argumentlarni tartib bilan emas, nomi bilan (keyword arguments) berish va uning afzalliklarini bilish.",
    ["Nomlangan argument", "Tartibdan mustaqillik", "Aralash berish", "O'qilishi oson"],
    [
        text(r"""
Restoranda buyurtma: «Palov — **katta**, **go'shtli**, **achchiq emas**». Har bir xususiyatni **nomi bilan** aytasiz, tartib muhim emas. Funksiyalarda ham argumentni **parametr nomi bilan** berish mumkin.
""", title="Nomi bilan aytamiz"),
        text(r"""
```python
def royxat(ism, yosh, shahar):
    return f"{ism}, {yosh}, {shahar}"

print(royxat("Ali", 17, "Toshkent"))                 # tartib bilan
print(royxat(shahar="Toshkent", ism="Ali", yosh=17)) # nomi bilan, tartib erkin
print(royxat("Ali", shahar="Toshkent", yosh=17))      # aralash
```

- `nom=qiymat` ko'rinishida yoziladi (`=` atrofida bo'sh joysiz).
- Nomlangan argumentlar **tartibga bog'liq emas**.
- Aralash berilsa — avval **tartibli**, keyin **nomlilar** (`f(ism="Ali", 17)` — xato).
- Foyda: kod **o'qilishi oson** (`f(10, True, False)` o'rniga `f(narx=10, chegirma=True, ...)`).
""", title="Nomlangan argumentlar"),
        callout('analogy', r"""
Anketa to'ldirishda **«Ism: ___, Yosh: ___»** — qaysi maydon nima ekani aniq. «Ali, 17, Toshkent» — faqat tartibni eslasangiz tushunasiz.
""", title="Hayotiy o'xshatish"),
        example(r'''
def tanishtir(ism, yosh, shahar="Toshkent"):
    print(f"{ism} ({yosh}), {shahar}")

tanishtir("Ali", 17)
tanishtir(yosh=19, ism="Vali")
tanishtir("Gulnora", shahar="Xiva", yosh=20)
''', title="Uch usul", body="`Ali (17), Toshkent` / `Vali (19), Toshkent` / `Gulnora (20), Xiva`. Standart qiymatli `shahar` ni faqat kerak bo'lganda berdik."),
        example(r'''
def narx(asosiy, soliq=12, chegirma=0):
    return asosiy + asosiy * soliq // 100 - asosiy * chegirma // 100

print(narx(1000, chegirma=10))
print(narx(1000, soliq=0))
''', title="Amaliy: faqat kerakli parametrni berish", body="Standart qiymatlilardan faqat bittasini o'zgartirdik: `1020` va `1000`. Nomlangan argumentsiz oradagi `soliq` ni ham berish kerak bo'lardi."),
        exercise('l56_inline_pred'),
        callout('warning', r"""
Bir parametrni ham tartib bilan, ham nom bilan bersangiz — `TypeError`. Masalan, `royxat("Ali", ism="Vali")`.
""", title="Diqqat"),
        recap(["`f(nom=qiymat)` — nomlangan argument", "tartibga bog'liq emas", "avval tartibli, keyin nomlilar"], "agar noma'lum miqdordagi argument berilsa-chi? Masalan, istalgancha sonning yig'indisi?"),
    ],
    [
        predict('l56_inline_pred', "Nomi bilan", "Dastur nima chiqaradi?", section='inline', code='def f(a, b):\n    return a - b\n\nprint(f(b=1, a=10))\n', answer="9", points=2, hint="`a=10`, `b=1`.", explanation="Tartib muhim emas."),
        predict('l56_quiz_1', "Aralash", "Dastur nima chiqaradi?", code='def f(a, b, c=0):\n    return a * 100 + b * 10 + c\n\nprint(f(1, c=3, b=2))\n', answer="123", hint="`a=1`, `b=2`, `c=3`.", explanation="100 + 20 + 3."),
        single('l56_quiz_2', "Xato", "Qaysi chaqiruv xato?", options=[opt("`f(a=1, 2)`", True), opt("`f(1, b=2)`", False), opt("`f(b=2, a=1)`", False)], hint="Tartibli argument nomlidan oldin.", explanation="Nomlilardan keyin tartibli argument bo'lmaydi."),
        predict('l56_quiz_3', "Standart + nom", "Dastur nima chiqaradi?", code='def f(x, y=5, z=7):\n    return x + y + z\n\nprint(f(1, z=0))\n', answer="6", hint="`y` standart (5).", explanation="1 + 5 + 0."),
        code_task('l56_assignment', "Ro'yxatga olish", r"""
`tavsif(nom, narx, mavjud=True)` funksiyasi `<nom>: <narx> so'm (mavjud)` yoki `<nom>: <narx> so'm (tugagan)` matnini **qaytarsin**. `tavsif("Non", 4500)` → `Non: 4500 so'm (mavjud)`; `tavsif("Sut", 12000, mavjud=False)` → `Sut: 12000 so'm (tugagan)`.
""", starter_code='', points=10, tests=[T('output_equals', "Non: 4500 so'm (mavjud)\nSut: 12000 so'm (tugagan)\nOlma: 8000 so'm (mavjud)", "Natija", harness='print(tavsif("Non", 4500))\nprint(tavsif("Sut", 12000, mavjud=False))\nprint(tavsif(narx=8000, nom="Olma"))')],
            hint="`if mavjud:` — holatga qarab matn.", partial_solution='def tavsif(nom, narx, mavjud=True):\n    if mavjud:\n        holat = "mavjud"\n    # aks holda "tugagan"\n    return f"{nom}: {narx} so\'m ({holat})"\n', full_solution='def tavsif(nom, narx, mavjud=True):\n    if mavjud:\n        holat = "mavjud"\n    else:\n        holat = "tugagan"\n    return f"{nom}: {narx} so\'m ({holat})"\n', explanation="Nomlangan argument bilan ham ishlaydi."),
        single('l56_practice_easy', "Easy: afzallik", "Nomlangan argumentlarning asosiy afzalligi?", section='practice', difficulty='easy', options=[opt("Tartib muhim emas va kod tushunarli", True), opt("Funksiya tezroq ishlaydi", False), opt("Xotira tejaladi", False)], hint="Anketa.", explanation="O'qilishi oson va tartibdan mustaqil."),
        code_task('l56_practice_medium', "Medium: uchburchak perimetri", r"""
`perimetr(a, b, c)` uch tomon yig'indisini qaytarsin. Tekshiruv uni nomi bilan ham chaqiradi: `perimetr(c=3, a=1, b=2)` → `6`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "6\n12\n3", "Natija", harness='print(perimetr(c=3, a=1, b=2))\nprint(perimetr(3, 4, 5))\nprint(perimetr(1, 1, c=1))')], hint="Parametr nomlari aynan `a`, `b`, `c`.", full_solution='def perimetr(a, b, c):\n    return a + b + c\n', explanation="Nomlar mos bo'lsa, tartib muhim emas."),
        code_task('l56_practice_hard', "Hard: maosh hisobi", r"""
`maosh(stavka, soat, bonus=0, soliq=12)` — `stavka * soat + bonus` dan `soliq` foiz ushlab qolib, **butun son** qaytarsin: `(stavka*soat+bonus) * (100-soliq) // 100`. `maosh(20000, 100)` → `1760000`; `maosh(20000, 100, soliq=0)` → `2000000`; `maosh(20000, 100, bonus=100000, soliq=10)` → `1890000`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "1760000\n2000000\n1890000\n88", "Natija", harness='print(maosh(20000, 100))\nprint(maosh(20000, 100, soliq=0))\nprint(maosh(20000, 100, bonus=100000, soliq=10))\nprint(maosh(1, 100, soliq=12))')], hint="Avval jami, keyin soliq ayriladi.", full_solution='def maosh(stavka, soat, bonus=0, soliq=12):\n    jami = stavka * soat + bonus\n    return jami * (100 - soliq) // 100\n', explanation="Standart + nomlangan argumentlar."),
    ])

# ==============================================================================
# 57-DARS
# ==============================================================================
LESSON_57 = L(57, "*args bilan ishlash", 12,
    "*args yordamida istalgancha pozitsion argumentni qabul qiluvchi funksiya yozish va args ni tuple sifatida ishlatish.",
    ["*args", "Noma'lum miqdordagi argument", "args — tuple", "* bilan ochish"],
    [
        text(r"""
`print("a", "b", "c")` ham, `print("a")` ham ishlaydi — `print` istalgancha argument qabul qiladi. `max(1, 5, 3, 9)` ham. O'z funksiyamizni ham shunday qilish mumkin — **`*args`** yordamida.
""", title="Istalgancha argument"),
        text(r"""
```python
def yig_indi(*args):
    jami = 0
    for x in args:
        jami = jami + x
    return jami

print(yig_indi(1, 2))            # 3
print(yig_indi(1, 2, 3, 4, 5))   # 15
print(yig_indi())                # 0
```

- Parametr oldidagi **`*`** — «hamma tartibli argumentlarni **tuple** ga yig».
- `args` — oddiy nom (odat shunday, istalgan nom mumkin: `*sonlar`).
- Funksiya ichida `args` — **tuple**: `for`, `len()`, indeks bilan ishlaydi.
- Teskarisi: chaqirishda `*list` — listni argumentlarga «ochadi»: `yig_indi(*[1, 2, 3])`.
- `*args` oddiy parametrlardan **keyin** keladi: `def f(a, b, *args)`.
""", title="*args"),
        callout('analogy', r"""
`*args` — **cheksiz sig'imli sumka**: nechta narsa solsangiz, hammasini bitta sumkaga (tuple) joylaydi.
""", title="Hayotiy o'xshatish"),
        example(r'''
def ko_rsat(*args):
    print(args)
    print(len(args))

ko_rsat(1, "a", True)
ko_rsat()
''', title="args — tuple", body="`(1, 'a', True)` va `3`; keyin `()` va `0` — bo'sh tuple."),
        example(r'''
def o_rtacha(*baholar):
    return sum(baholar) / len(baholar)

print(o_rtacha(5, 4, 3))
sonlar = [5, 5, 4, 4]
print(o_rtacha(*sonlar))
''', title="Amaliy: o'rtacha baho", body="Istalgancha baho berish mumkin: `4.0` va `4.5`. `*sonlar` — list elementlarini alohida argumentlarga ochdi."),
        exercise('l57_inline_pred'),
        callout('warning', r"""
`*args` ga argumentlar bo'lmasa (`o_rtacha()`), `len(baholar)` — 0 bo'ladi va bo'lishda `ZeroDivisionError` chiqadi. Kerak bo'lsa, tekshiring.
""", title="Diqqat"),
        recap(["`*args` — tuple ga yig'adi", "ichida sikl, `len`, `sum` ishlaydi", "`*royxat` — listni ochib beradi"], "nomlangan argumentlar-chi — ularni ham noma'lum miqdorda qabul qilsa bo'ladimi?"),
    ],
    [
        predict('l57_inline_pred', "args", "Dastur nima chiqaradi?", section='inline', code='def f(*a):\n    return len(a)\n\nprint(f(), f(1), f(1, 2, 3))\n', answer="0 1 3", points=2, hint="`a` — tuple.", explanation="Argumentlar soni."),
        predict('l57_quiz_1', "Yig'indi", "Dastur nima chiqaradi?", code='def f(*x):\n    return sum(x)\n\nprint(f(1, 2, 3, 4))\n', answer="10", hint="`sum` tuple bilan ishlaydi.", explanation="1+2+3+4."),
        single('l57_quiz_2', "args turi", "Funksiya ichida `*args` qanday tur bo'ladi?", options=[opt("tuple", True), opt("list", False), opt("dict", False)], hint="O'zgarmas to'plam.", explanation="Tuple."),
        predict('l57_quiz_3', "Ochish", "Dastur nima chiqaradi?", code='def f(a, b, c):\n    return a + b + c\n\nsonlar = [1, 2, 3]\nprint(f(*sonlar))\n', answer="6", hint="`*sonlar` elementlarni ochadi.", explanation="`f(1, 2, 3)`."),
        code_task('l57_assignment', "Eng katta son", r"""
`eng_katta(*sonlar)` funksiyasi istalgancha sondan eng kattasini qaytarsin (agar son berilmasa — `None`). `max()` ishlatmang — sikl bilan toping. `eng_katta(3, 9, 4)` → `9`; `eng_katta(-5, -2)` → `-2`; `eng_katta()` → `None`.
""", starter_code='', points=10, tests=[T('output_equals', "9\n-2\nNone\n7", "Natija", harness='print(eng_katta(3, 9, 4))\nprint(eng_katta(-5, -2))\nprint(eng_katta())\nprint(eng_katta(7))'), T('code_not_contains', 'max(', "`max()` ishlatilmagan")],
            hint="Birinchi elementdan boshlang: `eng = sonlar[0]`; bo'sh bo'lsa `return None`.", partial_solution='def eng_katta(*sonlar):\n    if len(sonlar) == 0:\n        return None\n    eng = sonlar[0]\n    # sikl bilan eng kattasini toping\n    return eng\n', full_solution='def eng_katta(*sonlar):\n    if len(sonlar) == 0:\n        return None\n    eng = sonlar[0]\n    for s in sonlar:\n        if s > eng:\n            eng = s\n    return eng\n', explanation="Bo'sh holat alohida tekshirildi."),
        single('l57_practice_easy', "Easy: belgi", "`*args` dagi `*` nimani bildiradi?", section='practice', difficulty='easy', options=[opt("Qolgan argumentlarni tuple ga yig'ish", True), opt("Ko'paytirish", False), opt("Standart qiymat", False)], hint="Sumka.", explanation="Argumentlarni yig'ish."),
        code_task('l57_practice_medium', "Medium: matnlarni birlashtirish", r"""
`birlashtir(*sozlar)` istalgancha so'zni **probel bilan** birlashtirib matn qaytarsin. `birlashtir("a", "b", "c")` → `a b c`; `birlashtir("x")` → `x`; `birlashtir()` → bo'sh matn.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "a b c\nx\n\nsalom dunyo", "Natija", harness='print(birlashtir("a", "b", "c"))\nprint(birlashtir("x"))\nprint(birlashtir())\nprint(birlashtir("salom", "dunyo"))')], hint="`\" \".join(sozlar)` — matn metodi: elementlarni shu matn bilan ulaydi.", full_solution='def birlashtir(*sozlar):\n    return " ".join(sozlar)\n', explanation="`\" \".join(...)` tuple elementlarini probel bilan ulaydi."),
        code_task('l57_practice_hard', "Hard: sodiq mijoz hisobi", r"""
`hisob(chegirma, *narxlar)` — birinchi argument — chegirma foizi, qolganlari — narxlar. **Butun son** qaytarsin: narxlar yig'indisidan `chegirma` foiz ayirilgani (`yigindi * (100 - chegirma) // 100`). `hisob(10, 1000, 2000)` → `2700`; `hisob(0, 500)` → `500`; `hisob(50)` → `0`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "2700\n500\n0\n450", "Natija", harness='print(hisob(10, 1000, 2000))\nprint(hisob(0, 500))\nprint(hisob(50))\nprint(hisob(10, 100, 200, 200))')], hint="Oddiy parametr + `*narxlar`.", full_solution='def hisob(chegirma, *narxlar):\n    yigindi = sum(narxlar)\n    return yigindi * (100 - chegirma) // 100\n', explanation="`*args` oddiy parametrdan keyin."),
    ])

# ==============================================================================
# 58-DARS
# ==============================================================================
LESSON_58 = L(58, "**kwargs bilan ishlash", 12,
    "**kwargs yordamida istalgancha nomlangan argumentni qabul qilish va kwargs ni dictionary sifatida ishlatish.",
    ["**kwargs", "Noma'lum nomlangan argumentlar", "kwargs — dict", "** bilan ochish"],
    [
        text(r"""
Ro'yxatdan o'tishda: ba'zilar telefon kiritadi, ba'zilar email, ba'zilar ikkalasini ham. Qanday maydonlar kelishini oldindan bilmaymiz. **`**kwargs`** — istalgancha **nomlangan argumentni** qabul qiladi.
""", title="Istalgancha nomli argument"),
        text(r"""
```python
def profil(ism, **kwargs):
    print("Ism:", ism)
    for kalit, qiymat in kwargs.items():
        print(f"{kalit}: {qiymat}")

profil("Ali", yosh=17, shahar="Toshkent")
```

- `**kwargs` — «hamma **nomlangan** argumentlarni **dictionary** ga yig'». (*kwargs* — *keyword arguments*.)
- Funksiya ichida `kwargs` — **dict**: `.items()`, `.get()`, `kwargs["yosh"]` ishlaydi.
- Teskarisi: chaqirishda `**dict` — dictionary'ni nomlangan argumentlarga ochadi.
- Tartib: `def f(a, *args, **kwargs)` — oddiy, `*args`, `**kwargs`.
""", title="**kwargs"),
        callout('analogy', r"""
`**kwargs` — **yorliqli qutilar** qabul qiluvchi ombor: har bir quti nomi (yorliq) bilan keladi, ombor ularni yorlig'i bo'yicha tartiblab qo'yadi (dictionary).
""", title="Hayotiy o'xshatish"),
        example(r'''
def ko_rsat(**kw):
    print(kw)
    print(len(kw))

ko_rsat(a=1, b=2)
ko_rsat()
''', title="kwargs — dict", body="`{'a': 1, 'b': 2}` va `2`; keyin `{}` va `0`."),
        example(r'''
def kartochka(ism, **malumot):
    satr = ism
    for k in malumot:
        satr = satr + f", {k}={malumot[k]}"
    return satr

print(kartochka("Ali", yosh=17, shahar="Toshkent"))
sozlama = {"yosh": 20, "til": "uz"}
print(kartochka("Vali", **sozlama))
''', title="Amaliy: kartochka", body="`Ali, yosh=17, shahar=Toshkent` va `Vali, yosh=20, til=uz`. `**sozlama` dictionary'ni nomlangan argumentlarga ochdi."),
        exercise('l58_inline_pred'),
        callout('tip', r"""
`**kwargs` konfiguratsiya, tizim sozlamalari va boshqa funksiyani «o'rab» ishlatishda juda qulay.
""", title="Qachon kerak"),
        recap(["`**kwargs` — dict ga yig'adi", "`kwargs.items()` bilan yurish mumkin", "`**dict` — dictionary'ni ochadi"], "o'zgaruvchilar funksiya ichida va tashqarisida bir xilmi? Qaysi o'zgaruvchi qayerda ko'rinadi?"),
    ],
    [
        predict('l58_inline_pred', "kwargs", "Dastur nima chiqaradi?", section='inline', code='def f(**k):\n    return sorted(k)\n\nprint(f(b=1, a=2))\n', answer="['a', 'b']", points=2, hint="Kalitlar tartiblangan.", explanation="`kwargs` — dict; `sorted` kalitlarni tartiblaydi."),
        predict('l58_quiz_1', "get", "Dastur nima chiqaradi?", code='def f(**k):\n    return k.get("x", 0)\n\nprint(f(x=5), f(y=1))\n', answer="5 0", hint="`k` — dictionary.", explanation="`get` standart qiymat bilan."),
        single('l58_quiz_2', "kwargs turi", "Funksiya ichida `**kwargs` qanday tur?", options=[opt("dict", True), opt("tuple", False), opt("list", False)], hint="Nom → qiymat.", explanation="Dictionary."),
        predict('l58_quiz_3', "Ochish", "Dastur nima chiqaradi?", code='def f(a, b):\n    return a * b\n\nd = {"a": 3, "b": 4}\nprint(f(**d))\n', answer="12", hint="`**d` — `a=3, b=4`.", explanation="`f(a=3, b=4)`."),
        code_task('l58_assignment', "Moslashuvchan kartochka", r"""
`kartochka(ism, **malumot)` funksiyasi matn qaytarsin: avval ism, keyin har bir qo'shimcha ma'lumot `, kalit: qiymat` shaklida (kiritilgan tartibda). `kartochka("Ali")` → `Ali`; `kartochka("Ali", yosh=17)` → `Ali, yosh: 17`; `kartochka("Vali", yosh=19, shahar="Xiva")` → `Vali, yosh: 19, shahar: Xiva`.
""", starter_code='', points=10, tests=[T('output_equals', "Ali\nAli, yosh: 17\nVali, yosh: 19, shahar: Xiva", "Natija", harness='print(kartochka("Ali"))\nprint(kartochka("Ali", yosh=17))\nprint(kartochka("Vali", yosh=19, shahar="Xiva"))')], hint="`satr = ism` dan boshlab, siklda qo'shing.", partial_solution='def kartochka(ism, **malumot):\n    satr = ism\n    for k, v in malumot.items():\n        # satrga qo\'shing\n        pass\n    return satr\n', full_solution='def kartochka(ism, **malumot):\n    satr = ism\n    for k, v in malumot.items():\n        satr = satr + f", {k}: {v}"\n    return satr\n', explanation="`items()` bilan kalit va qiymat olindi."),
        single('l58_practice_easy', "Easy: belgi", "`**` (ikki yulduzcha) parametr oldida nimani bildiradi?", section='practice', difficulty='easy', options=[opt("Nomlangan argumentlarni dict ga yig'ish", True), opt("Darajaga ko'tarish", False), opt("Standart qiymat", False)], hint="Dictionary.", explanation="`**kwargs`."),
        code_task('l58_practice_medium', "Medium: sonlarni sanash", r"""
`nechta(**kw)` — nechta nomlangan argument berilganini qaytarsin. `nechta(a=1, b=2)` → `2`; `nechta()` → `0`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "2\n0\n3", "Natija", harness='print(nechta(a=1, b=2))\nprint(nechta())\nprint(nechta(x=1, y=2, z=3))')], hint="`len(kw)`.", full_solution='def nechta(**kw):\n    return len(kw)\n', explanation="`kw` — dictionary, `len` juftliklar sonini beradi."),
        code_task('l58_practice_hard', "Hard: narxlar yig'indisi", r"""
`savat(**mahsulotlar)` — kalit: mahsulot nomi, qiymat: narx. **Eng qimmat mahsulot nomini** va **jami narxni** `(nom, jami)` tuple sifatida qaytarsin. `savat(non=4500, sut=12000, olma=8000)` → `('sut', 24500)`. (Bo'sh bo'lsa `(None, 0)`.)
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "('sut', 24500)\n(None, 0)\n('a', 5)", "Natija", harness='print(savat(non=4500, sut=12000, olma=8000))\nprint(savat())\nprint(savat(a=5))')], hint="`eng = None`, `eng_narx = -1` bilan boshlang.", full_solution='def savat(**mahsulotlar):\n    eng = None\n    eng_narx = -1\n    jami = 0\n    for nom, narx in mahsulotlar.items():\n        jami = jami + narx\n        if narx > eng_narx:\n            eng_narx = narx\n            eng = nom\n    return eng, jami\n', explanation="Dictionary bo'ylab yurib, ikki qiymatni hisobladik."),
    ])

# ==============================================================================
# 59-DARS
# ==============================================================================
LESSON_59 = L(59, "Lokal va global o'zgaruvchilar", 12,
    "Lokal va global o'zgaruvchilar farqini, ko'rinish sohasini (scope) tushunish va global kalit so'zining kamchiliklarini bilish.",
    ["Lokal o'zgaruvchi", "Global o'zgaruvchi", "Ko'rinish sohasi (scope)", "global kalit so'zi", "Parametrlar ham lokal"],
    [
        text(r"""
Uyingizda **xonalar** bor. Oshxonadagi narsalarni yotoqxonadan ko'rib bo'lmaydi, lekin **uyning umumiy** (koridordagi) narsalarni hamma xonadan ko'rish mumkin. O'zgaruvchilar ham shunday: ba'zilari faqat **funksiya ichida** ko'rinadi, ba'zilari **hamma joyda**.
""", title="Xonalar va koridor"),
        text(r"""
```python
dastur_nomi = "Kalkulyator"     # GLOBAL — hamma joyda ko'rinadi

def salom():
    ism = "Ali"                 # LOKAL — faqat shu funksiya ichida
    print(dastur_nomi, ism)

salom()
print(ism)                      # NameError! ism tashqarida ko'rinmaydi
```

- **Lokal** o'zgaruvchi — funksiya ichida yaratilgan; funksiya tugashi bilan yo'qoladi. **Parametrlar** ham lokal.
- **Global** o'zgaruvchi — funksiyalardan tashqarida yaratilgan; funksiya ichida **o'qish** mumkin.
- Funksiya ichida global nomli o'zgaruvchiga qiymat bersangiz — **yangi lokal** o'zgaruvchi yaratiladi, global o'zgarmaydi.
- Globalni funksiya ichida o'zgartirish uchun `global nom` deb e'lon qilinadi — lekin bu **yomon odat**: funksiya ichidagi o'zgarishni topish qiyin. Yaxshisi — qiymatni `return` bilan qaytarish.
""", title="Lokal va global"),
        callout('analogy', r"""
Lokal o'zgaruvchi — **xonadagi shaxsiy narsa**; global — **koridordagi umumiy osma tokcha**. Xonadagi narsa xonadan chiqqach yo'qoladi.
""", title="Hayotiy o'xshatish"),
        example(r'''
x = 10

def f():
    x = 99
    print("ichida:", x)

f()
print("tashqarida:", x)
''', title="Lokal global'ni o'zgartirmaydi", body="`ichida: 99`, `tashqarida: 10`. Funksiya ichidagi `x = 99` — yangi lokal `x`; tashqi `x` o'zgarmadi."),
        example(r'''
soliq = 12

def narx_bilan(narx):
    return narx + narx * soliq // 100

def hisobot(narx):
    jami = narx_bilan(narx)
    print("Jami:", jami)

hisobot(1000)
''', title="Amaliy: global sozlama (o'qish)", body="`soliq` — global sozlama; ikkala funksiya uni o'qiydi: `Jami: 1120`. `jami` esa faqat `hisobot` ichida mavjud."),
        exercise('l59_inline_pred'),
        callout('warning', r"""
Funksiya ichida o'zgaruvchini ishlatib, keyin shu nomga qiymat berish `UnboundLocalError` beradi. Lokal va global nomlarni **aralashtirmang**; funksiyaga kerakli qiymatni **parametr** orqali bering.
""", title="Diqqat"),
        recap(["lokal — faqat funksiya ichida", "global — hamma joyda o'qiladi", "funksiya ichida o'zgartirish yangi lokal yaratadi", "global'dan qochish — yaxshi odat"], "bir nechta funksiyani birga ishlatib, katta dastur qanday quriladi?"),
    ],
    [
        predict('l59_inline_pred', "Global o'zgarmadi", "Dastur nima chiqaradi?", section='inline', code='a = 5\n\ndef f():\n    a = 1\n    return a + 1\n\nprint(f(), a)\n', answer="2 5", points=2, hint="Funksiya ichidagi `a` — boshqa.", explanation="Lokal `a = 1`; global `a` 5 qoldi."),
        predict('l59_quiz_1', "Global o'qish", "Dastur nima chiqaradi?", code='k = 3\n\ndef f(x):\n    return x * k\n\nprint(f(4))\n', answer="12", hint="Funksiya global `k` ni o'qiydi.", explanation="`4 * 3`."),
        single('l59_quiz_2', "NameError", "Funksiya ichida yaratilgan `y` ni tashqarida `print(y)` qilsak?", options=[opt("`NameError`", True), opt("`y` qiymati chiqadi", False), opt("`None`", False)], hint="Lokal o'zgaruvchi funksiyadan chiqib ko'rinmaydi.", explanation="Lokal `y` funksiya tugagach yo'qoladi."),
        predict('l59_quiz_3', "Parametr — lokal", "Dastur nima chiqaradi?", code='n = 10\n\ndef f(n):\n    n = n + 1\n    return n\n\nprint(f(1), n)\n', answer="2 10", hint="Parametr `n` — lokal.", explanation="Global `n` o'zgarmadi."),
        code_task('l59_assignment', "Hisoblagich muammosi", r"""
`hisob = 0` global o'zgaruvchi bor. `qosh(son)` funksiyasi `hisob` ni **o'zgartirmasdan**, `hisob + son` ni qaytarsin. Funksiyani ishlatib `hisob` ni yangilang: `hisob = qosh(5)`, keyin yana `hisob = qosh(3)` va chiqaring: `8`. (`global` ishlatmang.)
""", starter_code='hisob = 0\n', points=10, tests=[T('output_equals', "8", "Natija"), T('code_not_contains', 'global', "`global` ishlatilmagan"), T('code_contains', 'return', "`return` ishlatilgan")],
            hint="Funksiya `hisob` ni parametr sifatida olishi shart emas: global'ni o'qish mumkin.", partial_solution='hisob = 0\n\ndef qosh(son):\n    # hisob + son ni qaytaring\n    pass\n\nhisob = qosh(5)\n', full_solution='hisob = 0\n\ndef qosh(son):\n    return hisob + son\n\nhisob = qosh(5)\nhisob = qosh(3)\nprint(hisob)\n', explanation="Funksiya global'ni o'qidi, o'zgartirishni esa tashqarida `=` bilan qildik."),
        single('l59_practice_easy', "Easy: scope", "O'zgaruvchining «ko'rinish sohasi» nimani bildiradi?", section='practice', difficulty='easy', options=[opt("Kodning qaysi qismida ishlatish mumkinligini", True), opt("Qiymat turini", False), opt("Xotira hajmini", False)], hint="Xonalar.", explanation="Qayerda ko'rinishini."),
        code_task('l59_practice_medium', "Medium: lokal nom", r"""
`f()` funksiyasi ichida `natija = 100` o'zgaruvchisini yarating va qaytaring. Tashqarida `natija = 1` yarating, `f()` ni chaqirib, ikkala qiymatni chiqaring: `100 1`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "100 1", "Natija")], hint="Ikki alohida `natija`.", full_solution='def f():\n    natija = 100\n    return natija\n\nnatija = 1\nprint(f(), natija)\n', explanation="Lokal va global bir xil nomda, lekin mustaqil."),
        code_task('l59_practice_hard', "Hard: o'rtacha funksiyasi lokal o'zgaruvchilari bilan", r"""
`statistika(sonlar)` funksiyasi lokal `jami` va `soni` o'zgaruvchilarini hisoblab, **o'rtachani** qaytarsin. Tashqarida `jami = 999` global ham bo'lsin — u o'zgarmasligi kerak. `statistika([2, 4, 6])` → `4.0`, va global `jami` hamon `999`.
""", section='practice', difficulty='hard', points=5, starter_code='jami = 999\n', tests=[T('output_equals', "4.0\n999\n2.5\n999", "Natija", harness='print(statistika([2, 4, 6]))\nprint(jami)\nprint(statistika([2, 3]))\nprint(jami)')], hint="Funksiya ichida `jami = 0` — bu lokal.", full_solution='jami = 999\n\ndef statistika(sonlar):\n    jami = 0\n    soni = 0\n    for s in sonlar:\n        jami = jami + s\n        soni = soni + 1\n    return jami / soni\n', explanation="Lokal `jami` global `jami` ga tegmadi."),
    ])

# ==============================================================================
# 60-DARS
# ==============================================================================
LESSON_60 = L(60, "Funksiyalarni birgalikda ishlatish va kodni qayta ishlatish", 14,
    "Kichik funksiyalarni birlashtirib dastur qurish, har bir funksiya bitta ishni bajarishi tamoyili va funksiyalardan modulli dastur yozish.",
    ["Funksiyalarni birlashtirish", "Bitta funksiya — bitta vazifa", "Kodni qayta ishlatish", "Menyu va main()"],
    [
        text(r"""
Katta dasturni bir «uzun fayl»ga yozish — bitta katta xonada yashash kabi: hamma narsa aralash. **Funksiyalar** dasturni **xonalarga** bo'ladi: har biri bitta vazifa uchun. Ularni birlashtirib murakkab dastur quramiz.
""", title="Katta dastur — kichik bo'laklardan"),
        text(r"""
**Yaxshi funksiya qoidalari:**

1. **Bitta funksiya — bitta vazifa** (`yuza_hisobla`, `ma_lumot_ol`, `natija_chiqar`).
2. **Tushunarli nom** (`x` emas, `yuza_hisobla`).
3. Ma'lumotni **parametr** bilan oladi, natijani **return** bilan qaytaradi (global'ga tayanmaydi).
4. Hisoblash (return) va chiqarish (print) **ajratiladi** — hisoblovchi funksiyani qayta ishlatish oson.

Dastur tuzilishi:

```python
def kvadrat(x):
    return x * x

def yig_indi(a, b):
    return a + b

def main():
    s = int(input())
    print(yig_indi(kvadrat(s), 1))

main()
```

`main()` — asosiy funksiya: dastur ishini boshqaradi, kichik funksiyalarni chaqiradi.
""", title="Funksiyalardan dastur qurish"),
        callout('analogy', r"""
Funksiyalar — **konstruktor detallari**: har biri oddiy, lekin ulardan murakkab narsa yig'iladi. Bitta detalni almashtirish uchun butun konstruksiyani buzish shart emas.
""", title="Hayotiy o'xshatish"),
        example(r'''
def yuza(en, boy):
    return en * boy

def perimetr(en, boy):
    return 2 * (en + boy)

def hisobot(en, boy):
    print(f"Yuza: {yuza(en, boy)}")
    print(f"Perimetr: {perimetr(en, boy)}")

hisobot(3, 5)
hisobot(10, 2)
''', title="Kichik funksiyalardan hisobot", body="`hisobot` ikki hisoblovchi funksiyani chaqiradi: `Yuza: 15`, `Perimetr: 16`, `Yuza: 20`, `Perimetr: 24`."),
        example(r'''
def baho(ball):
    if ball >= 90:
        return 5
    elif ball >= 70:
        return 4
    elif ball >= 50:
        return 3
    return 2

def o_rtacha_baho(*ballar):
    jami = 0
    for b in ballar:
        jami = jami + baho(b)
    return jami / len(ballar)

print(baho(95), baho(40))
print(o_rtacha_baho(95, 75, 55))
''', title="Amaliy: baho tizimi funksiyalari", body="4-moduldagi baholash kodi endi `baho()` funksiyasi — uni istalgan joyda qayta ishlatamiz. `5 2` va o'rtacha `4.0`."),
        exercise('l60_inline_pred'),
        callout('tip', r"""
Funksiya uzun bo'lib ketsa (20+ qator) yoki «va» bilan tushuntirsangiz («hisoblaydi **va** chiqaradi **va** saqlaydi») — uni bo'laklarga ajrating.
""", title="Maslahat"),
        recap(["bitta funksiya — bitta vazifa", "return bilan natijani qaytaring, print alohida", "`main()` bilan dasturni boshqaring"], "modul loyihasida ko'p funksiyali kalkulyator yaratamiz. Qanday funksiyalar kerak bo'ladi?"),
    ],
    [
        predict('l60_inline_pred', "Ichma-ich chaqirish", "Dastur nima chiqaradi?", section='inline', code='def a(x):\n    return x + 1\n\ndef b(x):\n    return a(x) * 2\n\nprint(b(3))\n', answer="8", points=2, hint="Avval `a(3)`.", explanation="`a(3)` = 4; `b` = 8."),
        predict('l60_quiz_1', "Zanjir", "Dastur nima chiqaradi?", code='def kv(x):\n    return x * x\n\ndef yig(a, b):\n    return kv(a) + kv(b)\n\nprint(yig(3, 4))\n', answer="25", hint="9 + 16.", explanation="Pifagor: 3² + 4²."),
        single('l60_quiz_2', "Yaxshi funksiya", "Yaxshi funksiyaning belgisi qaysi?", options=[opt("Bitta aniq vazifani bajaradi", True), opt("Hamma ishni bir o'zi qiladi", False), opt("Faqat global o'zgaruvchilarga tayanadi", False)], hint="Bitta funksiya — bitta vazifa.", explanation="Aniq va kichik vazifa."),
        single('l60_quiz_3', "print yoki return", "Qayta ishlatish uchun hisoblovchi funksiya nima qilishi kerak?", options=[opt("Natijani `return` qilishi", True), opt("Natijani `print` qilishi", False), opt("Global o'zgaruvchiga yozishi", False)], hint="Natijani boshqa joyda ham ishlatamiz.", explanation="`return` bilan qaytarish."),
        code_task('l60_assignment', "Doira funksiyalari", r"""
Ikkita funksiya yarating: `doira_yuzi(r)` — `3.14 * r * r` ni qaytarsin; `doira_uzunligi(r)` — `2 * 3.14 * r` ni qaytarsin. Ikkalasi ham natijani **2 xonaga yaxlitlab** (`round(..., 2)`) qaytarsin. `doira_yuzi(2)` → `12.56`; `doira_uzunligi(2)` → `12.56`; `doira_yuzi(1)` → `3.14`.
""", starter_code='', points=10, tests=[T('output_equals', "12.56\n12.56\n3.14\n6.28\n28.26", "Natija", harness='print(doira_yuzi(2))\nprint(doira_uzunligi(2))\nprint(doira_yuzi(1))\nprint(doira_uzunligi(1))\nprint(doira_yuzi(3))'), T('code_contains', 'return', "`return` ishlatilgan")],
            hint="`return round(3.14 * r * r, 2)`.", partial_solution='def doira_yuzi(r):\n    return round(3.14 * r * r, 2)\n\n# doira_uzunligi ni yozing\n', full_solution='def doira_yuzi(r):\n    return round(3.14 * r * r, 2)\n\ndef doira_uzunligi(r):\n    return round(2 * 3.14 * r, 2)\n', explanation="Ikkita kichik, mustaqil funksiya."),
        single('l60_practice_easy', "Easy: main()", "`main()` funksiyasi odatda nima qiladi?", section='practice', difficulty='easy', options=[opt("Dasturning asosiy ishini boshqaradi", True), opt("Faqat matn chiqaradi", False), opt("Xatolarni topadi", False)], hint="Dirijyor.", explanation="Kichik funksiyalarni chaqirib, ishni boshqaradi."),
        code_task('l60_practice_medium', "Medium: palindrom", r"""
`palindrom_mi(s)` — matn teskarisi bilan bir xil bo'lsa `True` qaytarsin (`s == s[::-1]` ishlatmang — teskari qilish uchun sikl yoki kesim `[::-1]` o'rniga oddiy indeks bilan solishtiring). `palindrom_mi("oyo")` → `True`; `palindrom_mi("salom")` → `False`; `palindrom_mi("a")` → `True`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "True\nFalse\nTrue\nTrue\nFalse", "Natija", harness='print(palindrom_mi("oyo"))\nprint(palindrom_mi("salom"))\nprint(palindrom_mi("a"))\nprint(palindrom_mi(""))\nprint(palindrom_mi("abca"))')], hint="`for i in range(len(s))`: `s[i]` va `s[len(s) - 1 - i]` ni solishtiring.", full_solution='def palindrom_mi(s):\n    for i in range(len(s)):\n        if s[i] != s[len(s) - 1 - i]:\n            return False\n    return True\n', explanation="Birinchi nomuvofiqlikda `return False`; sikl tugasa — `True`."),
        code_task('l60_practice_hard', "Hard: tub sonlar", r"""
`tub_mi(n)` (`n >= 2` uchun) — `n` tub bo'lsa `True` qaytarsin; `tublar(n)` — 2 dan `n` gacha (n ham kiradi) tub sonlar **listini** qaytarsin (`tub_mi` dan foydalaning). `tub_mi(7)` → `True`; `tublar(10)` → `[2, 3, 5, 7]`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "True\nFalse\n[2, 3, 5, 7]\n[2]\n[2, 3, 5, 7, 11, 13, 17, 19]", "Natija", harness='print(tub_mi(7))\nprint(tub_mi(9))\nprint(tublar(10))\nprint(tublar(2))\nprint(tublar(20))')], hint="`tub_mi` da 2 dan `n - 1` gacha bo'luvchi qidiring.", partial_solution='def tub_mi(n):\n    for d in range(2, n):\n        if n % d == 0:\n            return False\n    return True\n\n# tublar(n) ni yozing\n', full_solution='def tub_mi(n):\n    for d in range(2, n):\n        if n % d == 0:\n            return False\n    return True\n\ndef tublar(n):\n    natija = []\n    for k in range(2, n + 1):\n        if tub_mi(k):\n            natija.append(k)\n    return natija\n', explanation="Bir funksiya ikkinchisini qayta ishlatdi."),
    ])

LESSONS = [LESSON_50, LESSON_51, LESSON_52, LESSON_53, LESSON_54, LESSON_55, LESSON_56, LESSON_57, LESSON_58, LESSON_59, LESSON_60]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("8-modul yakuniy nazorati: Funksiyalar", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **ko'p funksiyali kalkulyator**.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m8_a_t1', "def", "Funksiyani qaysi kalit so'z yaratadi?", section='assessment', points=2, options=[opt("`def`", True), opt("`fun`", False), opt("`return`", False)], explanation="`def`."),
    single('m8_a_t2', "return", "`return` dan keyingi qatorlar nima bo'ladi?", section='assessment', points=2, options=[opt("Bajarilmaydi", True), opt("Bajariladi", False), opt("Xato beradi", False)], explanation="`return` funksiyani tugatadi."),
    single('m8_a_t3', "Standart parametr", "Qaysi yozuv to'g'ri?", section='assessment', points=2, options=[opt("`def f(a, b=2):`", True), opt("`def f(a=2, b):`", False), opt("`def f(a == 2):`", False)], explanation="Standart qiymatlilar oxirida."),
    single('m8_a_t4', "*args", "Funksiya ichida `*args` qanday tur?", section='assessment', points=2, options=[opt("tuple", True), opt("list", False), opt("dict", False)], explanation="Tuple."),
    multiple('m8_a_t5', "Ko'rinish sohasi", "Qaysi gaplar to'g'ri?", section='assessment', points=2, options=[opt("Lokal o'zgaruvchi funksiyadan tashqarida ko'rinmaydi", True), opt("Parametr lokal o'zgaruvchi hisoblanadi", True), opt("Funksiya ichida global nomga qiymat berilsa, global o'zgaradi", False), opt("Global o'zgaruvchini funksiya ichida o'qish mumkin", True)], explanation="Qiymat berish yangi lokal yaratadi."),
    predict('m8_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='def f(a, b=3):\n    return a * b\n\nprint(f(2), f(2, 5), f(b=1, a=9))\n', answer="6 10 9", explanation="Standart, berilgan va nomlangan argumentlar."),
    predict('m8_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='def f(*x, **y):\n    return len(x), len(y)\n\nprint(f(1, 2, a=3))\n', answer="(2, 1)", explanation="2 ta pozitsion, 1 ta nomlangan."),
    predict('m8_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='n = 1\n\ndef f():\n    n = 5\n    return n\n\nprint(f() + n)\n', answer="6", explanation="Lokal 5 + global 1."),
    fix_task('m8_a_f1', "Xatoni tuzating (1)", "`kvadrat(4)` `16` qaytarishi kerak, lekin `None` qaytaryapti.", section='assessment', points=4, starter_code='def kvadrat(x):\n    x * x\n', tests=[T('output_equals', "16\n25", "Natija", harness='print(kvadrat(4))\nprint(kvadrat(5))')], hint="Qiymat qaytarilmayapti.", full_solution='def kvadrat(x):\n    return x * x\n', explanation="`return` yetishmayotgan edi."),
    fix_task('m8_a_f2', "Xatoni tuzating (2)", "`salom(\"Ali\")` `Salom, Ali!` **qaytarishi** kerak, lekin funksiya xato beryapti.", section='assessment', points=4, starter_code='def salom(ism)\n    return "Salom, " + ism + "!"\n', tests=[T('output_equals', "Salom, Ali!\nSalom, Vali!", "Natija", harness='print(salom("Ali"))\nprint(salom("Vali"))')], hint="`def` qatori oxirida nima yo'q?", full_solution='def salom(ism):\n    return "Salom, " + ism + "!"\n', explanation="Ikki nuqta unutilgan."),
    code_task('m8_a_project', "Mini-loyiha: Ko'p funksiyali kalkulyator", r"""
**Funksiyalar** yozing (har biri natijani `return` qilsin):

- `qosh(a, b)`, `ayir(a, b)`, `kopaytir(a, b)` — oddiy amallar,
- `bol(a, b)` — bo'lish; `b == 0` bo'lsa `None` qaytaradi,
- `daraja(a, b=2)` — `a` ning `b`-darajasi (standart — kvadrat),
- `yigindi(*sonlar)` — istalgancha sonning yig'indisi,
- `hisobla(amal, a, b)` — `amal` belgisiga (`+`, `-`, `*`, `/`, `**`) qarab tegishli funksiyani chaqirib natijani qaytaradi; noma'lum belgi bo'lsa `None`.

Keyin `main()` funksiyasi: foydalanuvchi `amal` (matn), `a` va `b` (**kasr bo'lishi mumkin**, `float`) kiritadi va dastur natijani chiqaradi:
- natija `None` bo'lsa: `Xato: amalni bajarib bo'lmaydi`,
- aks holda: `a amal b = natija` — natija **ikki xonali kasr** bilan (`f"{natija:.2f}"`). Masalan `+`, `2`, `3.5` → `2.00 + 3.50 = 5.50`; `a` va `b` ham `:.2f` bilan.
- `main()` ni oxirida chaqiring.

Tekshiruv ham alohida funksiyalarni sinaydi (`qosh(2, 3)`, `bol(1, 0)`, `yigindi(1, 2, 3)` ...).
""", section='project', points=20, difficulty='hard', unlock=3, starter_code='# Ko\'p funksiyali kalkulyator\n',
        expected_output_example="2.00 + 3.50 = 5.50",
        tests=[T('output_equals', "5\n-1\n6\nNone\n0.5\n9\n8\n6\n3\nNone", "Alohida funksiyalar", harness='print(qosh(2, 3))\nprint(ayir(2, 3))\nprint(kopaytir(2, 3))\nprint(bol(1, 0))\nprint(bol(1, 2))\nprint(daraja(3))\nprint(daraja(2, 3))\nprint(yigindi(1, 2, 3))\nprint(hisobla("-", 5, 2))\nprint(hisobla("%", 1, 2))', stdin="+\n1\n1\n"),
               T('output_equals', "2.00 + 3.50 = 5.50", "main: qo'shish", stdin="+\n2\n3.5\n"), T('output_equals', "10.00 / 4.00 = 2.50", "main: bo'lish", stdin="/\n10\n4\n"), T('output_equals', "Xato: amalni bajarib bo'lmaydi", "main: nolga bo'lish", stdin="/\n5\n0\n"),
               T('output_equals', "2.00 ** 10.00 = 1024.00", "main: daraja", stdin="**\n2\n10\n", hidden=True), T('output_equals', "Xato: amalni bajarib bo'lmaydi", "main: noma'lum amal", stdin="%\n5\n2\n", hidden=True), T('code_regex', r"def\s+main\s*\(", "`main()` funksiyasi bor")],
        hint="1) Har bir amal uchun alohida `def`. 2) `hisobla` ichida `if amal == \"+\": return qosh(a, b)` ... 3) `main()` da: `amal = input()`, `a = float(input())`, `b = float(input())`. 4) `bol` da `if b == 0: return None`.",
        partial_solution='def qosh(a, b):\n    return a + b\n\ndef ayir(a, b):\n    return a - b\n\n# qolgan funksiyalarni, hisobla() va main() ni yozing\n',
        full_solution='def qosh(a, b):\n    return a + b\n\ndef ayir(a, b):\n    return a - b\n\ndef kopaytir(a, b):\n    return a * b\n\ndef bol(a, b):\n    if b == 0:\n        return None\n    return a / b\n\ndef daraja(a, b=2):\n    return a ** b\n\ndef yigindi(*sonlar):\n    return sum(sonlar)\n\ndef hisobla(amal, a, b):\n    if amal == "+":\n        return qosh(a, b)\n    elif amal == "-":\n        return ayir(a, b)\n    elif amal == "*":\n        return kopaytir(a, b)\n    elif amal == "/":\n        return bol(a, b)\n    elif amal == "**":\n        return daraja(a, b)\n    return None\n\ndef main():\n    amal = input()\n    a = float(input())\n    b = float(input())\n    natija = hisobla(amal, a, b)\n    if natija is None:\n        print("Xato: amalni bajarib bo\'lmaydi")\n    else:\n        print(f"{a:.2f} {amal} {b:.2f} = {natija:.2f}")\n\nmain()\n',
        explanation="Loyiha funksiyalar, return, standart parametr, *args, funksiyalarni birlashtirish va main() ni qamrab oladi."),
])
