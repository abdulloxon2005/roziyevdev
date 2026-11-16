"""Python — 0 dan boshlash · 2-modul: O'zgaruvchilar va ma'lumot turlari (7–15-darslar)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 2,
    'title': "O'zgaruvchilar va ma'lumot turlari",
    'description': "Ma'lumotni xotirada saqlash: o'zgaruvchi, nomlash qoidalari, int, float, str, bool, type(), "
                   "turlarni almashtirish va input() orqali foydalanuvchidan ma'lumot olish.",
}

# ==============================================================================
# 7-DARS
# ==============================================================================
LESSON_7 = L(7, "O'zgaruvchi (Variable) nima?", 12,
    "O'zgaruvchi nima ekanini tushunish, `=` belgisi bilan qiymat saqlash va o'zgaruvchini print() bilan ishlatish.",
    ["O'zgaruvchi", "Tayinlash (=)", "Qiymatni o'zgartirish", "O'zgaruvchini chiqarish"],
    [
        text(r"""
Do'kondan chiqayotib kassirga aytasiz: «Menga 3 ta non kerak edi». Keyin yana «shu nonlarning narxi qancha?» deb so'raysiz.
«Shu non» deganda siz **eslab qolingan ma'lumotga** murojaat qilyapsiz. Dasturlarga ham ma'lumotni **eslab qolish** kerak —
buning uchun **o'zgaruvchi** ishlatiladi.
""", title="Nima uchun kerak?"),
        callout('analogy', r"""
O'zgaruvchi — **ustiga yorliq yopishtirilgan quti**. Yorliq — o'zgaruvchining *nomi*, quti ichidagi narsa — *qiymati*.
Qutini ochmasdan ham yorliqqa qarab nima kerakligini topasiz. Qutidagi narsani istagan payt almashtirish mumkin.
""", title="Hayotiy o'xshatish: quti va yorliq"),
        text(r"""
Python'da o'zgaruvchi `=` belgisi bilan yaratiladi:

```python
yosh = 16
```

Bu «`yosh` nomli qutiga 16 sonini sol» degani. Bu yerda `=` matematikadagi «teng» emas, **«saqla»** (tayinlash) degani.
O'zgaruvchi nomini `print()` ichiga qo'shtirnoqsiz yozsangiz, uning qiymati chiqadi.
""", title="O'zgaruvchi yaratish"),
        example(r'''
ism = "Aziza"
yosh = 16
print(ism)
print(yosh)
''', title="Ikkita o'zgaruvchi", body="`ism`da matn, `yosh`da son saqlandi. `print(ism)` qo'shtirnoqsiz — nomning o'zini emas, **ichidagi qiymatni** chiqaradi. Natija: `Aziza` va `16`."),
        example(r'''
narx = 12000
print("Non narxi:", narx)
narx = 13000
print("Yangi narx:", narx)
''', title="Qiymatni o'zgartirish (hayotiy misol)", body="Xuddi do'kondagi narx kabi: avval 12000, keyin 13000. O'zgaruvchiga yangi qiymat bersangiz, **eskisi o'chib ketadi**. Dastur qatorma-qator ishlagani uchun avval eski, keyin yangi narx chiqadi."),
        exercise('l7_inline_blank'),
        callout('important', r"""
1. `=` — o'ngdagi qiymatni chapdagi nomga **saqlaydi**.
2. Matn qo'shtirnoqda (`"Aziza"`), son qo'shtirnoqsiz (`16`).
3. `print(ism)` — qiymatni, `print("ism")` — «ism» so'zining o'zini chiqaradi.
4. Avval o'zgaruvchini **yarating**, keyin ishlating, aks holda `NameError`.
""", title="Eslab qoling"),
        recap(["o'zgaruvchi — nomlangan xotira «qutisi»", "`=` qiymatni saqlaydi", "qiymatni istalgan payt almashtirish mumkin"],
              "o'zgaruvchiga istalgan nomni berish mumkinmi? `2kitob` yoki `mening ismim` to'g'ri nomlarmi?"),
    ],
    [
        fill('l7_inline_blank', "Bo'sh joyni to'ldiring", "Shahar nomini saqlovchi o'zgaruvchi yarating va chiqaring. Natija: `Toshkent`",
             'shahar ___ "Toshkent"\nprint(___)\n', ['=', 'shahar'], tests=[T('output_equals', 'Toshkent', "Natija: Toshkent")],
             hint="Qiymat berish uchun `=` kerak, chiqarish uchun o'zgaruvchi nomi.", explanation="`shahar = \"Toshkent\"` saqlaydi, `print(shahar)` chiqaradi.",
             points=2),
        single('l7_quiz_1', "= belgisi", "`x = 5` qatorida `=` nima qiladi?", options=[
            opt("5 soni x ga teng ekanini tekshiradi", False, "Tekshirish boshqa belgi bilan qilinadi; `=` — saqlash."),
            opt("5 qiymatini x o'zgaruvchisiga saqlaydi", True),
            opt("x va 5 ni qo'shadi", False)], hint="Quti va yorliq o'xshatishini eslang.",
            explanation="`=` — tayinlash: o'ngdagi qiymat chapdagi nomga saqlanadi."),
        predict('l7_quiz_2', "Qiymat almashdi", "Dastur nima chiqaradi?", code='a = 10\na = 25\nprint(a)\n', answer="25",
                hint="Yangi qiymat eskisini o'chiradi.", explanation="`a` avval 10, keyin 25 bo'ldi — chiqadigan qiymat oxirgisi."),
        single('l7_quiz_3', "Qo'shtirnoq farqi", '`ism = "Ali"` bo\'lsa, `print("ism")` nima chiqaradi?', options=[
            opt("Ali", False, "Qo'shtirnoq ichidagi narsa matn sifatida chiqadi, o'zgaruvchi sifatida emas."),
            opt("ism", True), opt("Xato beradi", False)], hint="Qo'shtirnoq ichidagi narsa — oddiy matn.",
            explanation="`\"ism\"` — matn, shuning uchun so'zning o'zi chiqadi. Qiymat uchun `print(ism)`."),
        code_task('l7_assignment', "Vizitka o'zgaruvchilari", r"""
Uchta o'zgaruvchi yarating: `ism` (matn), `yosh` (son), `shahar` (matn). Qiymatlarni o'zingiznikiga qo'ying va **har birini alohida qatorda `print()` bilan** chiqaring (faqat o'zgaruvchi nomlarini print qiling, matnni qo'lda yozmang).

**Chiquvchi natija namunasi:**

```
Aziza
16
Toshkent
```
""", starter_code='# o\'zgaruvchilarni yarating\n', expected_output_example="Aziza\n16\nToshkent", points=10,
            tests=[T('output_lines_min', '3', "Kamida 3 qator chiqdi"),
                   T('code_regex', r"(?m)^\s*ism\s*=", "`ism` o'zgaruvchisi yaratilgan"),
                   T('code_regex', r"(?m)^\s*yosh\s*=\s*\d+", "`yosh` — son"),
                   T('code_regex', r"(?m)^\s*shahar\s*=", "`shahar` o'zgaruvchisi yaratilgan"),
                   T('code_regex', r"print\(\s*ism\s*\)(?s:.*)print\(\s*yosh\s*\)(?s:.*)print\(\s*shahar\s*\)", "Uchala o'zgaruvchi nomi bilan chiqarilgan")],
            hint="`ism = \"...\"` ko'rinishida yarating, keyin `print(ism)`.",
            partial_solution='ism = "Aziza"\nyosh = 16\n# shahar o\'zgaruvchisini yarating va uchalasini print qiling\n',
            full_solution='ism = "Aziza"\nyosh = 16\nshahar = "Toshkent"\nprint(ism)\nprint(yosh)\nprint(shahar)\n',
            explanation="Har bir o'zgaruvchi alohida yaratilib, nomi orqali chiqarildi."),
        predict('l7_practice_easy', "Easy: natijani toping", "Dastur nima chiqaradi?", section='practice', difficulty='easy',
                code='x = 7\nprint(x)\nprint("x")\n', answer="7\nx", hint="Qo'shtirnoqli va qo'shtirnoqsiz farqi.", explanation="Birinchisi qiymat, ikkinchisi matn."),
        code_task('l7_practice_medium', "Medium: narx almashdi", r"""
`narx` o'zgaruvchisini 5000 qiling va chiqaring. Keyin uni 7500 ga almashtirib, yana chiqaring.

```
5000
7500
```
""", section='practice', difficulty='medium', points=5, starter_code='',
            tests=[T('output_equals', "5000\n7500", "Natija: 5000 va 7500"), T('code_regex', r"\bnarx\b", "`narx` o'zgaruvchisi ishlatilgan")],
            hint="Ikki marta `narx = ...` deb yozing, har safar print qiling.", full_solution='narx = 5000\nprint(narx)\nnarx = 7500\nprint(narx)\n',
            explanation="Qiymat almashganda eskisi yo'qoladi."),
        code_task('l7_practice_hard', "Hard: qiymatni nusxalash", r"""
`a = 3` va `b = 8` o'zgaruvchilarini yarating. Keyin `c` o'zgaruvchisiga `a` ning qiymatini saqlang (`c = a`) va `c` ni chiqaring. Oxirida `a` ni 100 ga o'zgartirib, yana `a` va `c` ni chiqaring.

```
3
100
3
```
""", section='practice', difficulty='hard', points=5,
            tests=[T('output_equals', "3\n100\n3", "Natija: 3, 100, 3"), T('code_regex', r"(?m)^\s*c\s*=\s*a\s*$", "`c = a` ishlatilgan")],
            hint="`c = a` qutiga nusxa oladi — `a` keyin o'zgarsa, `c` o'zgarmaydi.",
            partial_solution='a = 3\nb = 8\nc = a\nprint(c)\n# a ni 100 qiling va a, c ni chiqaring\n',
            full_solution='a = 3\nb = 8\nc = a\nprint(c)\na = 100\nprint(a)\nprint(c)\n', explanation="`c = a` qiymatni nusxalaydi; keyin `a` o'zgarsa, `c` eski qiymatda qoladi."),
    ])

# ==============================================================================
# 8-DARS
# ==============================================================================
LESSON_8 = L(8, "O'zgaruvchilarni nomlash qoidalari", 12,
    "O'zgaruvchi nomi qoidalarini bilish, to'g'ri va noto'g'ri nomlarni ajratish va tushunarli nom tanlash.",
    ["Nom qoidalari", "Katta-kichik harf farqi", "snake_case", "Zaxira so'zlar", "Tushunarli nom"],
    [
        text(r"""
Uyingizdagi javonlarga «1», «2», «3» deb yozib qo'ysangiz, qaysi birida nima borligini unutasiz. «Kitoblar», «Kiyimlar» deb yozsangiz — hammasi tushunarli.
O'zgaruvchi nomi ham shunday: Python ma'lum **qoidalarni** talab qiladi, dasturchilar esa **tushunarli** nomlar tanlaydi.
""", title="Nom — o'zgaruvchining yuzi"),
        text(r"""
**Python qoidalari (buzilsa — xato):**

1. Nom **harf** yoki `_` bilan boshlanadi (raqam bilan emas): `kitob1` ✔, `1kitob` ✘.
2. Faqat harf, raqam va `_` bo'lishi mumkin: `my_name` ✔, `my-name` ✘, `my name` ✘.
3. **Katta-kichik harf farqlanadi**: `yosh`, `Yosh`, `YOSH` — uchta alohida o'zgaruvchi.
4. Python'ning o'z so'zlarini (`if`, `for`, `class`, `True`...) nom qilib bo'lmaydi.

**Dasturchilar kelishuvi (xato emas, lekin shart):** kichik harf, so'zlar `_` bilan ajratiladi — **snake_case**: `talaba_ismi`, `jami_narx`.
""", title="Qoidalar"),
        callout('tip', r"""
Nom **nima saqlayotganini** aytsin: `x` o'rniga `yosh`, `n` o'rniga `kitoblar_soni`. Olti oydan keyin o'z kodingizni o'qiganingizda minnatdor bo'lasiz.
""", title="Yaxshi nom"),
        example(r'''
talaba_ismi = "Bobur"
talaba_yoshi = 18
Talaba_ismi = "Boshqa"
print(talaba_ismi)
print(Talaba_ismi)
print(talaba_yoshi)
''', title="Katta-kichik harf farqi", body="`talaba_ismi` va `Talaba_ismi` — **ikki xil** o'zgaruvchi. Shuning uchun ikkita turli natija chiqadi: `Bobur` va `Boshqa`."),
        example(r'''
birinchi_son = 20
ikkinchi_son = 30
print("Birinchi:", birinchi_son)
print("Ikkinchi:", ikkinchi_son)
print(birinchi_son)
''', title="Amaliy: tushunarli nomlar", body="Nomlar o'zini izohlaydi, qo'shimcha izoh shart emas. Ko'p so'zli nomlarda so'zlar `_` bilan ajratildi."),
        exercise('l8_inline_fix'),
        recap(["nom harf yoki `_` bilan boshlanadi", "bo'sh joy va `-` mumkin emas", "katta-kichik harf farqlanadi", "snake_case — odat"],
              "butun son (masalan, 25) va kasr son (2.5) bir xil turdagi qiymatmi?"),
    ],
    [
        fix_task('l8_inline_fix', "Nomni tuzating", "Kod xato beryapti. Tuzating — natija: `Salom`", starter_code='my name = "Salom"\nprint(my_name)\n', points=2,
                 section='inline', tests=[T('output_equals', 'Salom', "Natija: Salom")], hint="Nomda bo'sh joy bo'lmaydi.",
                 full_solution='my_name = "Salom"\nprint(my_name)\n', explanation="Bo'sh joy o'rniga `_` ishlatiladi."),
        single('l8_quiz_1', "To'g'ri nom", "Qaysi nom Python'da **to'g'ri**?", options=[
            opt("`2kitob`", False, "Raqam bilan boshlanmaydi."), opt("`kitob_2`", True), opt("`kitob-2`", False, "`-` belgisi mumkin emas.")],
            hint="Raqam boshida bo'lmasin, `-` bo'lmasin.", explanation="`kitob_2` — harf bilan boshlanadi va faqat harf, raqam, `_` dan iborat."),
        single('l8_quiz_2', "Katta-kichik harf", "`Yosh = 5` va `yosh = 9` yozildi. Nechta o'zgaruvchi yaratildi?", options=[
            opt("1 ta", False), opt("2 ta", True), opt("Xato beradi", False)], hint="Python katta-kichik harfni farqlaydi.",
            explanation="`Yosh` va `yosh` — turli nomlar, ikkita alohida o'zgaruvchi."),
        predict('l8_quiz_3', "Qaysi qiymat?", "Dastur nima chiqaradi?", code='son = 4\nSon = 9\nprint(son)\n', answer="4", hint="`son` va `Son` boshqa-boshqa.",
                explanation="`print(son)` kichik harfli o'zgaruvchini chiqaradi — 4."),
        code_task('l8_assignment', "Kitob ma'lumotlari", r"""
`kitob_nomi`, `kitob_narxi` va `sahifalar_soni` nomli uchta o'zgaruvchi yarating (qiymatlar ixtiyoriy: matn, son, son). Uchalasini **tartib bilan** alohida qatorda chiqaring.

**Chiquvchi natija namunasi:**

```
O'tkan kunlar
45000
350
```
""", starter_code='', points=10,
            tests=[T('output_lines_min', '3', "Kamida 3 qator"), T('code_regex', r"(?m)^kitob_nomi\s*=", "`kitob_nomi` yaratilgan"),
                   T('code_regex', r"(?m)^kitob_narxi\s*=\s*\d+", "`kitob_narxi` — son"), T('code_regex', r"(?m)^sahifalar_soni\s*=\s*\d+", "`sahifalar_soni` — son"),
                   T('code_regex', r"print\(\s*kitob_nomi\s*\)(?s:.*)print\(\s*kitob_narxi\s*\)(?s:.*)print\(\s*sahifalar_soni\s*\)", "Nomlar bilan tartib bo'yicha chiqarilgan")],
            hint="Nomlarni aynan masalada yozilgandek yozing.", partial_solution='kitob_nomi = "O\'tkan kunlar"\nkitob_narxi = 45000\n# sahifalar_soni ni qo\'shing\n',
            full_solution='kitob_nomi = "O\'tkan kunlar"\nkitob_narxi = 45000\nsahifalar_soni = 350\nprint(kitob_nomi)\nprint(kitob_narxi)\nprint(sahifalar_soni)\n',
            explanation="snake_case nomlar tushunarli bo'ldi."),
        single('l8_practice_easy', "Easy: zaxira so'z", "Nima uchun `if = 5` yozib bo'lmaydi?", section='practice', difficulty='easy', options=[
            opt("`if` Python'ning o'z so'zi", True), opt("`if` juda qisqa", False), opt("5 son emas", False)], hint="Zaxira so'zlar nomga berilmaydi.",
            explanation="`if`, `for`, `class`, `True` kabi zaxira so'zlarni nom qilib bo'lmaydi."),
        fix_task('l8_practice_medium', "Medium: ikkita xato", r"""
Dasturda ikkita noto'g'ri nom bor. Tuzating. Natija: `18` va `Ali`
""", section='practice', difficulty='medium', points=5, starter_code='1yosh = 18\ntalaba-ismi = "Ali"\nprint(yosh)\nprint(talaba_ismi)\n',
            tests=[T('output_equals', "18\nAli", "Natija: 18 va Ali")], hint="Birinchisi raqam bilan boshlanmoqda, ikkinchisida `-` bor.",
            full_solution='yosh = 18\ntalaba_ismi = "Ali"\nprint(yosh)\nprint(talaba_ismi)\n', explanation="Nomlar `yosh` va `talaba_ismi` bo'lishi kerak."),
        code_task('l8_practice_hard', "Hard: uchta turli o'zgaruvchi", r"""
`olma`, `Olma` va `OLMA` nomli uchta o'zgaruvchi yarating — qiymatlari mos ravishda 1, 2, 3. Ularni shu tartibda (`olma`, `Olma`, `OLMA`) chiqaring:

```
1
2
3
```
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "1\n2\n3", "Natija: 1, 2, 3"), T('code_contains', 'OLMA', "`OLMA` ishlatilgan")],
            hint="Katta-kichik harf farqlanishidan foydalaning.", full_solution='olma = 1\nOlma = 2\nOLMA = 3\nprint(olma)\nprint(Olma)\nprint(OLMA)\n',
            explanation="Uchta nom — uchta mustaqil «quti»."),
    ])

# ==============================================================================
# 9-DARS
# ==============================================================================
LESSON_9 = L(9, "Butun sonlar — int", 12,
    "int turini tanish, butun sonlar ustida arifmetik amallar (+, -, *, //, %, **) bajarish.",
    ["int", "Arifmetik amallar", "Butun bo'lish //", "Qoldiq %", "Daraja **", "Amallar tartibi"],
    [
        text(r"""
Savatda 7 ta olma bor, uni 3 do'stga teng bo'lmoqchisiz. Har biriga nechta tegadi, nechta ortib qoladi? Bunday savollar — **butun sonlar** bilan ishlash.
Python'da butun sonlar turi **`int`** (inglizcha *integer*) deb ataladi: `5`, `-12`, `0`, `1000`.
""", title="Olmalarni bo'lishamiz"),
        text(r"""
| Amal | Belgi | Misol | Natija |
|---|---|---|---|
| Qo'shish | `+` | `7 + 3` | `10` |
| Ayirish | `-` | `7 - 3` | `4` |
| Ko'paytirish | `*` | `7 * 3` | `21` |
| Butun bo'lish | `//` | `7 // 3` | `2` |
| Qoldiq | `%` | `7 % 3` | `1` |
| Daraja | `**` | `2 ** 3` | `8` |

Amallar tartibi matematikadagidek: avval `**`, keyin `*` `//` `%`, keyin `+` `-`. Qavs (`( )`) tartibni o'zgartiradi.
""", title="Arifmetik amallar"),
        callout('analogy', r"""
`7 // 3` — «7 olmani 3 kishiga bo'ldim, har biriga **2 tadan** tegdi» (`2`). `7 % 3` — «**1 ta olma ortib qoldi**» (`1`).
Qoldiq `%` juftlikni tekshirishda ham ishlatiladi: `n % 2` juft sonlar uchun 0 beradi.
""", title="Bo'lish va qoldiq"),
        example(r'''
olma = 7
dostlar = 3
print("Har biriga:", olma // dostlar)
print("Ortib qoldi:", olma % dostlar)
''', title="Olmalarni bo'lish", body="Natija: `Har biriga: 2` va `Ortib qoldi: 1`. Sonlarni o'zgaruvchiga saqlab, amal bajardik."),
        example(r'''
narx = 12000
soni = 3
jami = narx * soni
print("Jami:", jami)
print((2 + 3) * 4)
print(2 + 3 * 4)
''', title="Amaliy: jami narx va amallar tartibi", body="`12000 * 3 = 36000`. Oxirgi ikki qatorda qavsning ta'siri ko'rinadi: `20` va `14`."),
        exercise('l9_inline_pred'),
        callout('warning', r"""
Bo'lishda `/` belgisi ham bor, lekin u **kasr** natija beradi (`7 / 2` → `3.5`). Butun natija kerak bo'lsa `//` ishlating. Kasr sonlarni keyingi darsda o'rganamiz.
""", title="Diqqat"),
        recap(["`int` — butun sonlar turi", "`+ - * // % **` amallari", "`//` — butun bo'lish, `%` — qoldiq"],
              "5 ni 2 ga bo'lsangiz 2.5 chiqadi. Bu qanday son turi?"),
    ],
    [
        predict('l9_inline_pred', "Qoldiqni toping", "Dastur nima chiqaradi?", section='inline', code='print(17 % 5)\n', answer="2", points=2,
                hint="17 ichida 5 necha marta bor va qancha qoladi?", explanation="17 = 5·3 + 2, qoldiq — 2."),
        single('l9_quiz_1', "Butun bo'lish", "`20 // 6` nimaga teng?", options=[opt("3", True), opt("3.33", False, "`//` kasr bermaydi."), opt("2", False)],
               hint="20 ichida 6 necha marta to'liq bor?", explanation="6·3 = 18 ≤ 20, shuning uchun 3."),
        predict('l9_quiz_2', "Amallar tartibi", "Dastur nima chiqaradi?", code='print(2 + 3 * 4 ** 2)\n', answer="50", hint="Avval **, keyin *, keyin +.",
                explanation="4**2 = 16, 3*16 = 48, 2+48 = 50."),
        single('l9_quiz_3', "Juftmi?", "Qaysi ifoda son juft ekanini bildiradi (agar `n` juft bo'lsa)?", options=[
            opt("`n % 2` natijasi 0", True), opt("`n // 2` natijasi 0", False), opt("`n ** 2` natijasi 2", False)], hint="Juft son 2 ga qoldiqsiz bo'linadi.",
            explanation="Juft son 2 ga qoldiqsiz bo'linadi — qoldiq 0."),
        code_task('l9_assignment', "Olma bo'lish", r"""
`olmalar` o'zgaruvchisida 23 ta olma bor, `bolalar` o'zgaruvchisida 5 ta bola. Dastur ikki qator chiqarsin: har bir bolaga nechta olma tegishi va nechta olma ortib qolishi (faqat sonlar, avval tegadigani).

**Chiquvchi natija:**

```
4
3
```
""", starter_code='olmalar = 23\nbolalar = 5\n', points=10,
            tests=[T('output_equals', "4\n3", "Natija: 4 va 3"), T('code_contains', '//', "`//` ishlatilgan"), T('code_contains', '%', "`%` ishlatilgan")],
            hint="`//` — nechta tegadi, `%` — nechta ortadi.", partial_solution='olmalar = 23\nbolalar = 5\nprint(olmalar // bolalar)\n# qoldiqni ham chiqaring\n',
            full_solution='olmalar = 23\nbolalar = 5\nprint(olmalar // bolalar)\nprint(olmalar % bolalar)\n', explanation="23 // 5 = 4, 23 % 5 = 3."),
        single('l9_practice_easy', "Easy: daraja", "`3 ** 2` nimaga teng?", section='practice', difficulty='easy', options=[opt("6", False), opt("9", True), opt("5", False)],
               hint="`**` — darajaga ko'tarish.", explanation="3 ning kvadrati 9."),
        code_task('l9_practice_medium', "Medium: soatlarni daqiqaga", r"""
`soat = 3` o'zgaruvchisi bor. Necha daqiqa ekanini hisoblab chiqaring: `180`
""", section='practice', difficulty='medium', points=5, starter_code='soat = 3\n', tests=[T('output_equals', "180", "Natija: 180"), T('code_contains', '*', "Ko'paytirish ishlatilgan")],
            hint="1 soat = 60 daqiqa.", full_solution='soat = 3\nprint(soat * 60)\n', explanation="3 · 60 = 180."),
        code_task('l9_practice_hard', "Hard: daqiqalarni soat va daqiqaga ajrating", r"""
`jami = 135` daqiqa. Necha soat va necha daqiqa ekanini ikki qatorda chiqaring (avval soat, keyin qolgan daqiqa):

```
2
15
```
""", section='practice', difficulty='hard', points=5, starter_code='jami = 135\n',
            tests=[T('output_equals', "2\n15", "Natija: 2 va 15"), T('code_contains', '//', "`//` ishlatilgan"), T('code_contains', '%', "`%` ishlatilgan")],
            hint="Soat uchun `//`, qolgan daqiqa uchun `%`.", full_solution='jami = 135\nprint(jami // 60)\nprint(jami % 60)\n', explanation="135 // 60 = 2, 135 % 60 = 15."),
    ])

# ==============================================================================
# 10-DARS
# ==============================================================================
LESSON_10 = L(10, "Haqiqiy sonlar — float", 12,
    "float turini tanish, kasr sonlar bilan amallar bajarish, `/` bo'lish va round() funksiyasidan foydalanish.",
    ["float", "Kasr son (nuqta bilan)", "/ bo'lish", "round()", "int va float aralashmasi"],
    [
        text(r"""
Narxlar kasr bo'lishi mumkin (12.5 ming so'm), bo'y 1.75 m, harorat 36.6°. Kasr qismi bor sonlar Python'da **`float`** deb ataladi.
Muhim: kasr **nuqta** bilan yoziladi (vergul bilan emas): `3.14`, `0.5`, `-2.75`.
""", title="Kasr sonlar"),
        callout('analogy', r"""
`int` — **dona** hisoblanadigan narsalar (3 ta olma). `float` — **o'lchanadigan** narsalar (1.5 kg olma, 36.6° harorat).
""", title="Hayotiy o'xshatish"),
        text(r"""
- `float` bilan ham `+ - * **` amallari ishlaydi: `2.5 * 2` → `5.0`.
- `/` bo'lish — **har doim `float`** qaytaradi: `10 / 4` → `2.5`, `10 / 2` → `5.0`.
- `int` va `float` aralashsa, natija `float` bo'ladi: `3 + 1.5` → `4.5`.
- `round(son, k)` — sonni `k` ta kasr xonagacha yaxlitlaydi: `round(3.14159, 2)` → `3.14`.
""", title="Qoidalar"),
        example(r'''
bo_y = 1.75
vazn = 68.5
print(bo_y)
print(vazn / 2)
print(10 / 4)
print(10 / 2)
''', title="float bilan tanishuv", body="Natija: `1.75`, `34.25`, `2.5`, `5.0`. E'tibor bering: `10 / 2` ham `5.0` — kasr ko'rinishida."),
        example(r'''
narx = 2.5
kilo = 3
jami = narx * kilo
print("Jami:", jami)
print("Yaxlitlangan:", round(10 / 3, 2))
''', title="Amaliy: olma narxi", body="2.5 · 3 = `7.5`. `10 / 3` cheksiz kasr (`3.3333...`), `round(..., 2)` esa 2 xonagacha yaxlitlaydi: `3.33`."),
        exercise('l10_inline_pred'),
        callout('warning', r"""
Kompyuterda kasr sonlar ba'zan **yaqinlashtirilgan** saqlanadi: `0.1 + 0.2` natijasi `0.30000000000000004` bo'ladi. Bu xato emas, kompyuter ishlash usuli. Chiroyli ko'rsatish uchun `round()` ishlatamiz.
""", title="Kichik sir"),
        recap(["`float` — kasr sonlar (nuqta bilan)", "`/` har doim float beradi", "`round(son, k)` yaxlitlaydi"],
              "matn ham o'zgaruvchida saqlanishini bilasiz. Matn va son orasida qanday farq bor?"),
    ],
    [
        predict('l10_inline_pred', "Natijani toping", "Dastur nima chiqaradi?", section='inline', code='print(9 / 2)\n', answer="4.5", points=2,
                hint="`/` kasr natija beradi.", explanation="9 / 2 = 4.5."),
        single('l10_quiz_1', "Bo'lish turi", "`8 / 2` natijasi qanday ko'rinadi?", options=[opt("4", False, "`/` har doim float qaytaradi."), opt("4.0", True), opt("2", False)],
               hint="`/` natijasi float.", explanation="`/` har doim float beradi: `4.0`."),
        predict('l10_quiz_2', "Aralash amal", "Dastur nima chiqaradi?", code='print(2 + 0.5)\n', answer="2.5", hint="int + float = float.", explanation="Natija float: 2.5."),
        predict('l10_quiz_3', "round()", "Dastur nima chiqaradi?", code='print(round(2.71828, 2))\n', answer="2.72", hint="Ikkita kasr xonagacha yaxlitlanadi.",
                explanation="2.71828 → 2.72."),
        code_task('l10_assignment', "O'rtacha baho", r"""
Uch fan bahosi: `a = 5`, `b = 4`, `c = 4`. O'rtacha qiymatni hisoblab, **ikki kasr xonagacha yaxlitlab** chiqaring.

**Chiquvchi natija:**

```
4.33
```
""", starter_code='a = 5\nb = 4\nc = 4\n', points=10,
            tests=[T('output_equals', "4.33", "Natija: 4.33"), T('code_contains', 'round', "`round()` ishlatilgan"), T('code_contains', '/', "`/` ishlatilgan")],
            hint="O'rtacha = yig'indi / 3. Keyin `round(..., 2)`.", partial_solution='a = 5\nb = 4\nc = 4\nortacha = (a + b + c) / 3\n# yaxlitlab chiqaring\n',
            full_solution='a = 5\nb = 4\nc = 4\nortacha = (a + b + c) / 3\nprint(round(ortacha, 2))\n', explanation="13 / 3 = 4.3333…, round → 4.33."),
        single('l10_practice_easy', "Easy: nuqta yoki vergul?", "Qaysi yozuv `float`?", section='practice', difficulty='easy', options=[opt("`3,5`", False, "Vergul bilan yozilmaydi."), opt("`3.5`", True), opt("`\"3.5\"`", False, "Bu matn.")],
               hint="Kasr nuqta bilan.", explanation="`3.5` — float."),
        code_task('l10_practice_medium', "Medium: Selsiy → Farengeyt", r"""
`c = 25` (Selsiy). Farengeytni hisoblang: `F = C * 9 / 5 + 32` va chiqaring: `77.0`
""", section='practice', difficulty='medium', points=5, starter_code='c = 25\n', tests=[T('output_equals', "77.0", "Natija: 77.0")],
            hint="Formulani Python'ga ko'chiring.", full_solution='c = 25\nf = c * 9 / 5 + 32\nprint(f)\n', explanation="25·9/5 = 45.0, +32 = 77.0."),
        code_task('l10_practice_hard', "Hard: dumaloq yuzi", r"""
`r = 3` radiusli doira yuzini hisoblang: `3.14 * r ** 2`, natijani 1 xonagacha yaxlitlab chiqaring: `28.3`
""", section='practice', difficulty='hard', points=5, starter_code='r = 3\n', tests=[T('output_equals', "28.3", "Natija: 28.3"), T('code_contains', 'round', "`round()` ishlatilgan")],
            hint="Daraja `**`; avval hisoblang, keyin round.", full_solution='r = 3\nyuza = 3.14 * r ** 2\nprint(round(yuza, 1))\n', explanation="3.14 · 9 = 28.26 → 28.3."),
    ])

# ==============================================================================
# 11-DARS
# ==============================================================================
LESSON_11 = L(11, "Matn va mantiqiy qiymatlar — str va bool", 13,
    "str (matn) va bool (True/False) turlarini tanish, matnlarni `+` va `*` bilan birlashtirish, taqqoslash natijasi bool ekanini bilish.",
    ["str", "Matnni birlashtirish (+)", "Matnni takrorlash (*)", "bool: True va False", "Taqqoslash natijasi"],
    [
        text(r"""
Telefoningizda ism — matn, yosh — son, «bildirishnomalar yoqilganmi?» — **ha/yo'q** javob. Dasturlashda ham shunday: matn (`str`), son (`int`, `float`) va **ha/yo'q** (`bool`) qiymatlari bor.
""", title="Turli xil ma'lumotlar"),
        text(r"""
**`str`** — qo'shtirnoq ichidagi matn: `"Salom"`, `'Python'`, hatto `"123"` ham matn (qo'shtirnoqda bo'lgani uchun).

- `+` matnlarni **ulaydi**: `"Salom, " + "Ali"` → `Salom, Ali`.
- `*` matnni **takrorlaydi**: `"ha" * 3` → `hahaha`.

**`bool`** faqat ikki qiymat oladi: `True` (rost) va `False` (yolg'on) — birinchi harfi **katta**, qo'shtirnoqsiz.
Taqqoslash natijasi `bool` bo'ladi: `5 > 3` → `True`, `5 == 7` → `False`.
""", title="Ikkita yangi tur"),
        callout('important', r"""
`==` — **tenglikni tekshirish** (ikkita belgi). `=` esa **saqlash**. Aralashtirib yubormang: `x = 5` (saqla), `x == 5` (tekshir: rostmi?).
""", title="== va = farqi"),
        example(r'''
ism = "Aziza"
salom = "Salom, " + ism + "!"
print(salom)
print("=" * 20)
print("ha" * 3)
''', title="Matnlar bilan amallar", body="`+` bilan matnlar ulandi, `*` bilan chiziq chizdik. Natija: `Salom, Aziza!`, 20 ta `=`, `hahaha`."),
        example(r'''
yosh = 17
print(yosh >= 18)
print(yosh == 17)
tolangan = True
print(tolangan)
''', title="Amaliy: bool qiymatlar", body="`17 >= 18` yolg'on — `False`; `17 == 17` rost — `True`. `tolangan` o'zgaruvchisi to'g'ridan-to'g'ri `True` saqlaydi (to'lov amalga oshdi)."),
        exercise('l11_inline_fill'),
        callout('warning', r"""
Matn bilan sonni `+` bilan ulab bo'lmaydi: `"Yosh: " + 16` — `TypeError`. Buni 13-darsda to'g'rilaymiz. Hozircha `print("Yosh:", 16)` ishlating.
""", title="Diqqat"),
        recap(["`str` — matn, `+` ulaydi, `*` takrorlaydi", "`bool` — `True` yoki `False`", "`==` tekshiradi, `=` saqlaydi"],
              "o'zgaruvchi ichida nima turdagi qiymat borligini qanday bilish mumkin?"),
    ],
    [
        fill('l11_inline_fill', "Matnlarni ulang", "Natija: `Salom Python`", 'a = "Salom"\nb = "Python"\nprint(a + ___ + b)\n', ['" "'], section='inline', points=2,
             tests=[T('output_equals', 'Salom Python', "Natija: Salom Python")], hint="Orasida bo'sh joy matni kerak.", explanation="`\" \"` — bitta bo'sh joydan iborat matn."),
        single('l11_quiz_1', "bool qiymati", "Qaysi biri to'g'ri `bool` qiymat?", options=[opt("`true`", False, "Birinchi harf katta bo'lishi kerak."), opt("`True`", True), opt("`\"True\"`", False, "Bu matn.")],
               hint="Katta harf, qo'shtirnoqsiz.", explanation="`True` — bool; `\"True\"` — str."),
        predict('l11_quiz_2', "Matn ko'paytirish", "Dastur nima chiqaradi?", code='print("ab" * 3)\n', answer="ababab", hint="`*` matnni takrorlaydi.", explanation="`ab` 3 marta."),
        predict('l11_quiz_3', "Taqqoslash", "Dastur nima chiqaradi?", code='x = 10\nprint(x == 5 + 5)\n', answer="True", hint="Avval o'ng tomon hisoblanadi.", explanation="`5 + 5 = 10`, `10 == 10` — `True`."),
        code_task('l11_assignment', "Salomlashuv matni", r"""
`ism = "Dilnoza"` o'zgaruvchisi berilgan. `+` yordamida **`Assalomu alaykum, Dilnoza!`** matnini hosil qilib chiqaring. Ismingiz o'zgarsa, natija ham o'zgarishi kerak (ismni qo'lda yozmang).
""", starter_code='ism = "Dilnoza"\n', points=10,
            tests=[T('output_equals', "Assalomu alaykum, Dilnoza!", "Natija to'g'ri"), T('code_contains', '+', "`+` ishlatilgan")],
            hint="`\"Assalomu alaykum, \" + ism + \"!\"`", partial_solution='ism = "Dilnoza"\nsalom = "Assalomu alaykum, " + ism\n# oxiriga "!" ni qo\'shing va chiqaring\n',
            full_solution='ism = "Dilnoza"\nprint("Assalomu alaykum, " + ism + "!")\n', explanation="Matnlar `+` bilan ulandi; vergul va bo'sh joy ham matnning bir qismi."),
        single('l11_practice_easy', "Easy: bool natijasi", "`7 > 10` natijasi qanday tur?", section='practice', difficulty='easy', options=[opt("int", False), opt("str", False), opt("bool", True)],
               hint="Taqqoslash natijasi ha/yo'q.", explanation="`7 > 10` → `False`, ya'ni bool."),
        code_task('l11_practice_medium', "Medium: chiziq chizish", r"""
`*` bilan 15 ta `-` dan iborat chiziq chizing, uning ostida `MENYU` yozing:

```
---------------
MENYU
```
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "---------------\nMENYU", "Natija to'g'ri"), T('code_contains', '*', "`*` ishlatilgan")],
            hint="`\"-\" * 15`", full_solution='print("-" * 15)\nprint("MENYU")\n', explanation="Matnni takrorlash chiroyli ramkalar uchun qulay."),
        code_task('l11_practice_hard', "Hard: voyaga yetganmi?", r"""
`yosh = 21` o'zgaruvchisi bor. `yosh >= 18` natijasini `voyaga_yetgan` o'zgaruvchisiga saqlang va chiqaring: `True`
""", section='practice', difficulty='hard', points=5, starter_code='yosh = 21\n', tests=[T('output_equals', "True", "Natija: True"), T('code_regex', r"voyaga_yetgan\s*=", "`voyaga_yetgan` yaratilgan")],
            hint="Taqqoslash natijasini o'zgaruvchiga saqlash mumkin.", full_solution='yosh = 21\nvoyaga_yetgan = yosh >= 18\nprint(voyaga_yetgan)\n',
            explanation="bool qiymatni ham o'zgaruvchiga saqlash mumkin."),
    ])

# ==============================================================================
# 12-DARS
# ==============================================================================
LESSON_12 = L(12, "Ma'lumot turini aniqlash — type()", 11,
    "type() funksiyasi bilan qiymat turini aniqlash va int, float, str, bool turlarini ishonch bilan farqlash.",
    ["type()", "int / float / str / bool", "\"5\" va 5 farqi"],
    [
        text(r"""
Do'konda «5» yozilgan qutini ko'rdingiz: ichida 5 ta olma bormi yoki «5» deb yozilgan qog'ozmi? Dasturda ham `5` (son) va `"5"` (matn) **butunlay boshqa** narsalar. Qiymat turini aniqlash uchun **`type()`** funksiyasi bor.
""", title="Bu qiymat qanday turda?"),
        text(r"""
```python
print(type(5))        # <class 'int'>
print(type(5.0))      # <class 'float'>
print(type("5"))      # <class 'str'>
print(type(True))     # <class 'bool'>
```

`type()` ichiga qiymat yoki o'zgaruvchi berilsa, tur nomini qaytaradi. Chiqishdagi `<class 'int'>` — «tur: `int`».
""", title="type() qanday ishlaydi"),
        callout('analogy', r"""
`type()` — **mahsulot yorlig'idagi «tarkibi» yozuvi** kabi: ichida nima borligini aytadi.
""", title="Hayotiy o'xshatish"),
        example(r'''
a = 5
b = "5"
c = 5.0
d = 5 > 3
print(type(a))
print(type(b))
print(type(c))
print(type(d))
''', title="Beshta turli qiymat", body="`5`, `\"5\"`, `5.0` va `5 > 3` — bir xil ko'rinsa ham turlari boshqa: `int`, `str`, `float`, `bool`."),
        example(r'''
yosh = 16
ism = "Aziza"
print("yosh:", type(yosh))
print("ism:", type(ism))
print("yosh / 2:", type(yosh / 2))
''', title="Amaliy: o'zgaruvchi turini tekshirish", body="O'zgaruvchi qiymati o'zgarsa, turi ham o'zgarishi mumkin. `yosh / 2` — `/` sabab `float` bo'ldi."),
        exercise('l12_inline_pred'),
        callout('tip', r"""
Dastur kutilmagan natija bersa, avval `print(type(o'zgaruvchi))` bilan turini tekshiring — xatolarning ko'pi tur noto'g'ri bo'lgani uchun.
""", title="Dasturchi maslahati"),
        recap(["`type(qiymat)` — turni aytadi", "`5` — int, `\"5\"` — str", "`/` natijasi float"], "matnni songa aylantirib bo'ladimi? `\"5\"` ni 5 ga qanday aylantirish mumkin?"),
    ],
    [
        predict('l12_inline_pred', "Turni toping", "Dastur nima chiqaradi?", section='inline', code='print(type("12"))\n', answer="<class 'str'>", points=2,
                hint="Qo'shtirnoq ichidagi — matn.", explanation="`\"12\"` qo'shtirnoqda, demak `str`."),
        single('l12_quiz_1', "int yoki str?", "`type(100)` va `type(\"100\")` nechta turli natija beradi?", options=[opt("Bir xil", False), opt("Har xil: int va str", True), opt("Xato beradi", False)],
               hint="Qo'shtirnoq farqi.", explanation="Birinchisi `int`, ikkinchisi `str`."),
        predict('l12_quiz_2', "Bo'lish turi", "Dastur nima chiqaradi?", code='print(type(6 / 3))\n', answer="<class 'float'>", hint="`/` har doim float.", explanation="`6 / 3 = 2.0` — float."),
        single('l12_quiz_3', "bool turi", "`type(3 < 1)` qanday natija beradi?", options=[opt("`<class 'bool'>`", True), opt("`<class 'int'>`", False), opt("`False`", False, "Bu qiymat; `type()` esa turni qaytaradi.")],
               hint="Taqqoslash natijasi bool.", explanation="`3 < 1` — `False`, uning turi bool."),
        code_task('l12_assignment', "Turlar jadvali", r"""
Quyidagi to'rtta qiymatning turini har biri alohida qatorda chiqaring (`type()` bilan, shu tartibda): `42`, `3.14`, `"Python"`, `True`.

**Chiquvchi natija:**

```
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```
""", starter_code='', points=10,
            tests=[T('output_equals', "<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>", "To'rtta tur to'g'ri tartibda"), T('code_contains', 'type(', "`type()` ishlatilgan")],
            hint="`print(type(42))` ko'rinishida.", partial_solution='print(type(42))\nprint(type(3.14))\n# qolganlarini qo\'shing\n',
            full_solution='print(type(42))\nprint(type(3.14))\nprint(type("Python"))\nprint(type(True))\n', explanation="Har bir qiymatning turi `type()` bilan aniqlandi."),
        single('l12_practice_easy', "Easy: tur nomi", "`type(2.5)` qaysi turni ko'rsatadi?", section='practice', difficulty='easy', options=[opt("int", False), opt("float", True), opt("str", False)],
               hint="Kasr son.", explanation="2.5 — float."),
        code_task('l12_practice_medium', "Medium: o'zgaruvchi turi", r"""
`x = "2026"` berilgan. `x` ning turini chiqaring: `<class 'str'>`
""", section='practice', difficulty='medium', points=5, starter_code='x = "2026"\n', tests=[T('output_equals', "<class 'str'>", "Natija to'g'ri"), T('code_regex', r"type\(\s*x\s*\)", "`type(x)` ishlatilgan")],
            hint="Qiymat emas, o'zgaruvchi nomini bering.", full_solution='x = "2026"\nprint(type(x))\n', explanation="Qo'shtirnoqdagi raqam ham `str`."),
        code_task('l12_practice_hard', "Hard: amal natijasi turi", r"""
`a = 7` va `b = 2` berilgan. `a // b` va `a / b` natijalarining **turini** chiqaring (shu tartibda):

```
<class 'int'>
<class 'float'>
```
""", section='practice', difficulty='hard', points=5, starter_code='a = 7\nb = 2\n',
            tests=[T('output_equals', "<class 'int'>\n<class 'float'>", "Natija to'g'ri"), T('code_contains', '//', "`//` ishlatilgan")],
            hint="`type(a // b)` va `type(a / b)`.", full_solution='a = 7\nb = 2\nprint(type(a // b))\nprint(type(a / b))\n', explanation="`//` int, `/` float beradi."),
    ])

# ==============================================================================
# 13-DARS
# ==============================================================================
LESSON_13 = L(13, "Ma'lumot turlarini o'zgartirish — int(), float(), str()", 13,
    "int(), float(), str() funksiyalari yordamida turlarni o'zgartirish va tur mos kelmasligidan kelib chiqadigan TypeError/ValueError ni tushunish.",
    ["int()", "float()", "str()", "TypeError", "ValueError"],
    [
        text(r"""
Kassa apparati sizga «narxi: 5000» deb matn ko'rsatadi. Lekin hisoblash uchun u **son** bo'lishi kerak. Matnni songa (yoki aksincha) aylantirish — **tur o'zgartirish** (*type casting*).
""", title="Kerakli turga o'tkazish"),
        text(r"""
| Funksiya | Nima qiladi | Misol | Natija |
|---|---|---|---|
| `int()` | butun songa aylantiradi | `int("25")`, `int(3.9)` | `25`, `3` (kasr kesiladi) |
| `float()` | kasr songa aylantiradi | `float("2.5")`, `float(4)` | `2.5`, `4.0` |
| `str()` | matnga aylantiradi | `str(99)` | `"99"` |

`int(3.9)` yaxlitlamaydi — kasr qismini **kesib tashlaydi** (`3`). `int("salom")` esa `ValueError` beradi — «salom» songa aylanmaydi.
""", title="Uchta funksiya"),
        callout('important', r"""
Matn va sonni birga `+` qilib bo'lmaydi: `"Yosh: " + 16` ✘ `TypeError`. Yechim: `"Yosh: " + str(16)` ✔ (yoki `print("Yosh:", 16)`).
""", title="Eng ko'p uchraydigan xato"),
        example(r'''
a = "25"
b = "15"
print(a + b)
print(int(a) + int(b))
''', title="Matn va son qo'shilishi", body="Matnlar **ulanadi** (`2515`), sonlar **qo'shiladi** (`40`). Sababi — `int()` matnni songa aylantirdi."),
        example(r'''
ism = "Ali"
yosh = 17
print("Ismi: " + ism + ", yoshi: " + str(yosh))
print(int(7.9))
print(float(3))
print(float("1.5") + 1)
''', title="Amaliy: matn ichida son", body="`str(yosh)` sonni matnga aylantirdi, shuning uchun `+` ishladi. `int(7.9)` → `7`, `float(3)` → `3.0`, `float(\"1.5\") + 1` → `2.5`."),
        exercise('l13_inline_fix'),
        recap(["`int()`, `float()`, `str()` — turni o'zgartiradi", "`int(3.9)` kasrni kesadi", "matn + son — `TypeError`; yechim `str()`"],
              "foydalanuvchi klaviaturadan son kiritsa, Python uni qaysi turda oladi?"),
    ],
    [
        fix_task('l13_inline_fix', "TypeError ni tuzating", "Kod xato beryapti. Natija: `Yosh: 16`", section='inline', points=2, starter_code='yosh = 16\nprint("Yosh: " + yosh)\n',
                 tests=[T('output_equals', 'Yosh: 16', "Natija: Yosh: 16")], hint="Sonni matnga aylantiring.", full_solution='yosh = 16\nprint("Yosh: " + str(yosh))\n', explanation="`str(yosh)` sonni matnga aylantiradi."),
        predict('l13_quiz_1', "int() kesadi", "Dastur nima chiqaradi?", code='print(int(5.99))\n', answer="5", hint="`int()` yaxlitlamaydi.", explanation="Kasr qismi kesiladi: 5."),
        predict('l13_quiz_2', "Matn qo'shish", "Dastur nima chiqaradi?", code='print("3" + "4")\n', answer="34", hint="Matnlar ulanadi.", explanation="Ikkala qiymat ham matn."),
        single('l13_quiz_3', "ValueError", "Qaysi ifoda `ValueError` beradi?", options=[opt("`int(\"12\")`", False), opt("`int(\"abc\")`", True), opt("`str(12)`", False)],
               hint="Qaysi matnni songa aylantirib bo'lmaydi?", explanation="\"abc\" raqamlardan iborat emas."),
        code_task('l13_assignment', "Matn sonlarni qo'shish", r"""
`a = "120"` va `b = "35.5"` matn ko'rinishidagi sonlar. Ularni songa aylantirib, yig'indisini chiqaring: `155.5`
""", starter_code='a = "120"\nb = "35.5"\n', points=10,
            tests=[T('output_equals', "155.5", "Natija: 155.5"), T('code_contains', 'float(', "`float()` ishlatilgan")],
            hint="`b` kasr, shuning uchun `float()` kerak.", partial_solution='a = "120"\nb = "35.5"\nson1 = int(a)\n# b ni float() bilan aylantiring va yig\'indini chiqaring\n',
            full_solution='a = "120"\nb = "35.5"\nprint(float(a) + float(b))\n', explanation="120.0 + 35.5 = 155.5."),
        single('l13_practice_easy', "Easy: float(4)", "`float(4)` nima beradi?", section='practice', difficulty='easy', options=[opt("4", False), opt("4.0", True), opt("\"4\"", False)],
               hint="float — kasr ko'rinishi.", explanation="`4.0`."),
        code_task('l13_practice_medium', "Medium: ball matni", r"""
`ball = 87` berilgan. Dastur `Sizning balingiz: 87 ball` matnini **bitta matn sifatida `+` bilan** hosil qilib chiqarsin.
""", section='practice', difficulty='medium', points=5, starter_code='ball = 87\n',
            tests=[T('output_equals', "Sizning balingiz: 87 ball", "Natija to'g'ri"), T('code_contains', 'str(', "`str()` ishlatilgan")],
            hint="`\"Sizning balingiz: \" + str(ball) + \" ball\"`", full_solution='ball = 87\nprint("Sizning balingiz: " + str(ball) + " ball")\n', explanation="Son matnga aylantirildi."),
        code_task('l13_practice_hard', "Hard: raqamlar yig'indisi", r"""
`son = "47"` matn. Uning raqamlari yig'indisini toping: `4 + 7 = 11`. Faqat `int()`, `//` va `%` dan foydalaning (indeks hali o'tilmagan):

```
11
```
""", section='practice', difficulty='hard', points=5, starter_code='son = "47"\n', tests=[T('output_equals', "11", "Natija: 11"), T('code_contains', '%', "`%` ishlatilgan")],
            hint="Avval `n = int(son)`. Keyin `n // 10` — o'nlik, `n % 10` — birlik.", full_solution='son = "47"\nn = int(son)\nprint(n // 10 + n % 10)\n', explanation="47 // 10 = 4, 47 % 10 = 7."),
    ])

# ==============================================================================
# 14-DARS
# ==============================================================================
LESSON_14 = L(14, "Foydalanuvchidan ma'lumot olish — input()", 13,
    "input() bilan foydalanuvchidan matn olish, uni o'zgaruvchiga saqlash va input() har doim str qaytarishini bilish.",
    ["input()", "Savol matni (prompt)", "input() natijasi — str", "Interaktiv dastur"],
    [
        text(r"""
Hozirgacha dasturimiz hamma ma'lumotni **o'zi** bilar edi. Haqiqiy dasturlar esa foydalanuvchidan so'raydi: «Ismingiz nima?», «Necha yoshdasiz?». Buning uchun **`input()`** funksiyasi bor.
""", title="Dastur savol bersin"),
        text(r"""
```python
ism = input("Ismingiz nima? ")
print("Salom,", ism)
```

`input("savol")` — savolni ekranga chiqaradi, foydalanuvchi yozib **Enter** bosguncha kutadi va yozilgan matnni **qaytaradi**. Biz uni o'zgaruvchiga saqlaymiz.

**Muhim:** `input()` har doim **`str`** (matn) qaytaradi. Hatto foydalanuvchi `25` yozsa ham, bu `"25"` matn.
""", title="input() qanday ishlaydi"),
        callout('analogy', r"""
`input()` — **kassir so'rashiga o'xshaydi**: «Nima olasiz?» — siz javob berguncha kassa to'xtab turadi. Javob esa har doim «qog'ozga yozilgan matn» ko'rinishida keladi.
""", title="Hayotiy o'xshatish"),
        callout('tip', r"""
Bu platformada kod ishga tushganda `input()` qiymatlari uchun «Kiritish (stdin)» maydoniga javoblarni yozing — **har bir javob alohida qatorda**. Masalan, ikkita `input()` bo'lsa, ikki qator yozing.
""", title="Platformada input()"),
        example(r'''
ism = input("Ismingiz nima? ")
print("Salom,", ism + "!")
''', title="Birinchi interaktiv dastur", body="Kiritish maydoniga `Aziza` yozing. Dastur ismni o'qib, salom beradi: `Salom, Aziza!`."),
        example(r'''
ism = input("Ism: ")
shahar = input("Shahar: ")
yosh = input("Yosh: ")
print(ism, "-", shahar, "-", yosh)
print(type(yosh))
''', title="Amaliy: anketa", body="Uch qator kiriting (masalan: `Ali`, `Toshkent`, `17`). `yosh` son kabi ko'rinsa ham, `type(yosh)` — `<class 'str'>`: `input()` har doim matn qaytaradi."),
        exercise('l14_inline_pred'),
        callout('warning', r"""
`input()` dan olingan sonni hisoblashga ishlatishdan oldin `int()` yoki `float()` bilan aylantirish kerak — bu keyingi darsning mavzusi.
""", title="Eslatma"),
        recap(["`input(\"savol\")` foydalanuvchidan matn oladi", "natija o'zgaruvchiga saqlanadi", "`input()` doim `str` qaytaradi"],
              "foydalanuvchi yoshini kiritdi. Uni 1 yilga oshirish uchun nima qilish kerak?"),
    ],
    [
        single('l14_inline_pred', "input() turi", "Foydalanuvchi `42` yozdi: `x = input()`. `x` qanday tur?", section='inline', points=2,
               options=[opt("int", False, "`input()` hech qachon avtomatik songa aylantirmaydi."), opt("str", True), opt("float", False)], hint="input() natijasi — har doim matn.",
               explanation="`input()` har doim `str` qaytaradi."),
        single('l14_quiz_1', "Savol matni", "`input(\"Yosh: \")` dagi `\"Yosh: \"` nima uchun kerak?", options=[opt("Foydalanuvchiga ko'rsatiladigan savol", True), opt("Javobning to'g'ri qiymati", False), opt("O'zgaruvchi nomi", False)],
               hint="Ekranda nima ko'rinadi?", explanation="Prompt — foydalanuvchi ko'radigan taklif matni."),
        predict('l14_quiz_2', "Natijani toping", "`input()` dan foydalanuvchi `5` kiritgan holat (`a = \"5\"`) uchun dastur nima chiqaradi?", code='a = "5"\nprint(a * 3)\n', answer="555", hint="`a` — matn, `*` matnni takrorlaydi.",
                explanation="`\"5\" * 3` → `555`."),
        single('l14_quiz_3', "Nima uchun saqlaymiz?", "Nima uchun `input()` natijasini o'zgaruvchiga saqlaymiz?", options=[opt("Keyin ishlatish uchun — aks holda qiymat yo'qoladi", True), opt("Aks holda Python xato beradi", False), opt("input() faqat o'zgaruvchiga saqlanganda ishlaydi", False)],
               hint="Dastur keyinroq javobni ishlatadimi?", explanation="Saqlamasak, kiritilgan qiymatga keyin murojaat qila olmaymiz."),
        code_task('l14_assignment', "Tanishuv dasturi", r"""
Dastur foydalanuvchining **ismini** va **shahrini** so'rasin (ikkita `input()`), keyin shunday chiqarsin:

```
Salom, Aziza! Siz Toshkentdansiz.
```

(Kiritishda `Aziza` va `Toshkent` berilsa.)
""", starter_code='', points=10,
            tests=[T('output_regex', r"^Salom, Aziza! Siz Toshkent\w*\.$", "Aziza / Toshkent bilan to'g'ri natija", stdin="Aziza\nToshkent\n", failure="Ism va shaharni o'zgaruvchiga saqlab, shu shablonda chiqaring."),
                   T('output_regex', r"^Salom, Bobur! Siz Samarqand\w*\.$", "Boshqa kiritish bilan ham to'g'ri", stdin="Bobur\nSamarqand\n"),
                   T('code_regex', r"input\((?s:.*)input\(", "Ikkita input() ishlatilgan")],
            hint="`ism = input(...)`, `shahar = input(...)`, keyin `print(\"Salom, \" + ism + ...)`. «-dansiz» qo'shimchasini qo'shing.",
            partial_solution='ism = input()\nshahar = input()\n# print bilan shablonni chiqaring\n',
            full_solution='ism = input()\nshahar = input()\nprint("Salom, " + ism + "! Siz " + shahar + "dansiz.")\n',
            explanation="Natija kiritilgan qiymatlarga bog'liq bo'ladi, shuning uchun dastur har xil kiritishda to'g'ri ishlashi kerak."),
        single('l14_practice_easy', "Easy: qaysi funksiya?", "Foydalanuvchidan matn olish uchun qaysi funksiya ishlatiladi?", section='practice', difficulty='easy', options=[opt("`print()`", False), opt("`input()`", True), opt("`type()`", False)],
               hint="Kirish — inglizcha input.", explanation="`input()` ma'lumot oladi, `print()` chiqaradi."),
        code_task('l14_practice_medium', "Medium: takrorlash", r"""
Foydalanuvchidan bir so'z oling va uni **3 marta** (orasida bo'sh joysiz) chiqaring. Masalan, `ha` kiritilsa: `hahaha`.
""", section='practice', difficulty='medium', points=5,
            tests=[T('output_equals', "hahaha", "`ha` uchun hahaha", stdin="ha\n"), T('output_equals', "salomsalomsalom", "`salom` uchun salomsalomsalom", stdin="salom\n")],
            hint="`soz * 3`.", full_solution='soz = input()\nprint(soz * 3)\n', explanation="Matnni `*` bilan takrorlash."),
        code_task('l14_practice_hard', "Hard: ismni qaytarish", r"""
Foydalanuvchi ism va familiyasini ikkita `input()` bilan kiritadi. Dastur **«Familiya Ism»** tartibida chiqarsin. Masalan, `Aziza` va `Karimova` → `Karimova Aziza`.
""", section='practice', difficulty='hard', points=5,
            tests=[T('output_equals', "Karimova Aziza", "Aziza Karimova → Karimova Aziza", stdin="Aziza\nKarimova\n"), T('output_equals', "Aliyev Bobur", "Bobur Aliyev → Aliyev Bobur", stdin="Bobur\nAliyev\n")],
            hint="Avval ismni, keyin familiyani oling; chiqarishda tartibni almashtiring.", full_solution='ism = input()\nfamiliya = input()\nprint(familiya, ism)\n', explanation="`print(a, b)` ikkisini bo'sh joy bilan chiqaradi."),
    ])

# ==============================================================================
# 15-DARS
# ==============================================================================
LESSON_15 = L(15, "input() bilan hisoblash va ma'lumotlarni qayta ishlash", 14,
    "input() orqali olingan sonlarni int()/float() bilan aylantirib hisoblash va natijani chiroyli shaklda chiqarish.",
    ["input() + int()", "input() + float()", "Hisoblash va chiqarish", "Dastur rejasi: kiritish → hisoblash → chiqarish"],
    [
        text(r"""
Kalkulyator, to'lov hisoblagich, valyuta almashtirgich — hammasi bir sxemada ishlaydi: **kiritish → hisoblash → chiqarish**.
Siz hozir uchchala qadamni ham bilasiz: `input()`, `int()/float()` va `print()`. Ularni birlashtiramiz!
""", title="Dasturning uch qadami"),
        text(r"""
`input()` matn qaytargani uchun, hisoblashdan oldin aylantiramiz:

```python
a = int(input("Birinchi son: "))
b = int(input("Ikkinchi son: "))
print("Yig'indi:", a + b)
```

`int(input(...))` — avval `input()` ishlaydi (matn oladi), keyin `int()` uni songa aylantiradi. Kasr sonlar uchun `float(input(...))`.
""", title="Kiritilgan sonni hisoblash"),
        callout('analogy', r"""
Bu **non do'koni** kabi: mijoz aytadi (kiritish), novvoy hisoblaydi (qayta ishlash), kassa chek beradi (chiqarish).
""", title="Hayotiy o'xshatish"),
        example(r'''
a = int(input("Birinchi son: "))
b = int(input("Ikkinchi son: "))
print("Yig'indi:", a + b)
print("Ko'paytma:", a * b)
''', title="Ikki son kalkulyatori", body="Kiritishga `8` va `5` yozing: `Yig'indi: 13`, `Ko'paytma: 40`."),
        example(r'''
narx = float(input("Mahsulot narxi (so'm): "))
soni = int(input("Nechta dona: "))
jami = narx * soni
print("Jami to'lov:", jami, "so'm")
''', title="Amaliy: to'lov hisoblagich", body="`2500.5` va `4` kiritilsa: `Jami to'lov: 10002.0 so'm`. Narx — `float`, soni — `int`."),
        exercise('l15_inline_blank'),
        callout('warning', r"""
Foydalanuvchi son o'rniga `salom` yozsa, `int()` `ValueError` beradi. Bunday xatolardan 9-modulda (`try/except`) himoyalanishni o'rganamiz. Hozircha foydalanuvchi to'g'ri kiritadi deb hisoblaymiz.
""", title="Eslatma"),
        recap(["`int(input())` — butun son oladi", "`float(input())` — kasr son oladi", "kiritish → hisoblash → chiqarish"],
              "ikki yo'l bilan matn ichiga son qo'shish mumkin: vergul yoki `str()`. Qaysi biri sizga qulay?"),
    ],
    [
        fill('l15_inline_blank', "Bo'sh joyni to'ldiring", "Son kiritilsa, uni 2 ga ko'paytirib chiqaring. `5` kiritilsa — `10`.", 'n = ___(input())\nprint(n * 2)\n', ['int'], section='inline', points=2,
             tests=[T('output_equals', "10", "5 → 10", stdin="5\n")], hint="Butun songa aylantiruvchi funksiya.", explanation="`int(input())`."),
        predict('l15_quiz_1', "Qo'shish yoki ulash?", "Foydalanuvchi `3` va `4` kiritdi. Dastur nima chiqaradi?", code='a = "3"\nb = "4"\nprint(a + b)\n', answer="34", hint="`input()` — matn.", explanation="Aylantirilmagan matnlar ulanadi."),
        predict('l15_quiz_2', "Aylantirilgan holda", "Foydalanuvchi `3` va `4` kiritdi va qiymatlar `int()` bilan aylantirildi. Dastur nima chiqaradi?", code='a = int("3")\nb = int("4")\nprint(a + b)\n', answer="7", hint="`int()` songa aylantiradi.", explanation="3 + 4 = 7."),
        single('l15_quiz_3', "Kasr kiritish", "Narx `12.5` kabi kasr bo'lishi mumkin. Qaysi biri to'g'ri?", options=[opt("`int(input())`", False, "`int(\"12.5\")` xato beradi."), opt("`float(input())`", True), opt("`str(input())`", False)],
               hint="Kasr uchun qaysi funksiya?", explanation="`float()` kasr matnni songa aylantiradi."),
        code_task('l15_assignment', "To'g'ri to'rtburchak yuzi", r"""
Foydalanuvchi **eni** va **bo'yini** (butun son) kiritadi. Dastur yuzini chiqarsin. `4` va `6` → `24`.
""", starter_code='', points=10,
            tests=[T('output_equals', "24", "4 va 6 → 24", stdin="4\n6\n"), T('output_equals', "35", "5 va 7 → 35", stdin="5\n7\n"), T('output_equals', "0", "0 va 9 → 0", stdin="0\n9\n", hidden=True)],
            hint="Ikkita `int(input())`, keyin ko'paytirib chiqaring.", partial_solution='eni = int(input())\nboyi = int(input())\n# yuzini chiqaring\n',
            full_solution='eni = int(input())\nboyi = int(input())\nprint(eni * boyi)\n', explanation="Sonlarni int ga aylantirib ko'paytirdik."),
        single('l15_practice_easy', "Easy: dastur tartibi", "Dasturning to'g'ri tartibi qaysi?", section='practice', difficulty='easy', options=[opt("Chiqarish → hisoblash → kiritish", False), opt("Kiritish → hisoblash → chiqarish", True), opt("Hisoblash → kiritish → chiqarish", False)],
               hint="Avval ma'lumot kerak.", explanation="Ma'lumot olinadi, qayta ishlanadi, ko'rsatiladi."),
        code_task('l15_practice_medium', "Medium: o'rtacha", r"""
Uch son (butun) kiritiladi. Ularning o'rtachasini chiqaring (kasr bo'lishi mumkin). `3`, `4`, `5` → `4.0`.
""", section='practice', difficulty='medium', points=5,
            tests=[T('output_equals', "4.0", "3,4,5 → 4.0", stdin="3\n4\n5\n"), T('output_equals', "2.0", "1,2,3 → 2.0", stdin="1\n2\n3\n"), T('output_equals', "3.0", "1,2,6 → 3.0", stdin="1\n2\n6\n", hidden=True)],
            hint="Yig'indini 3 ga `/` bilan bo'ling.", full_solution='a = int(input())\nb = int(input())\nc = int(input())\nprint((a + b + c) / 3)\n', explanation="(a+b+c)/3."),
        code_task('l15_practice_hard', "Hard: sekundlarni soat-daqiqa-sekundga", r"""
Foydalanuvchi sekundlar sonini kiritadi. Uch qatorda chiqaring: soat, daqiqa, sekund. `3725` → `1`, `2`, `5`.
""", section='practice', difficulty='hard', points=5,
            tests=[T('output_equals', "1\n2\n5", "3725 → 1, 2, 5", stdin="3725\n"), T('output_equals', "0\n1\n1", "61 → 0, 1, 1", stdin="61\n"), T('output_equals', "2\n0\n0", "7200 → 2, 0, 0", stdin="7200\n", hidden=True)],
            hint="Soat: `// 3600`. Qolgan: `% 3600`. Keyin daqiqa va sekund.", partial_solution='s = int(input())\nsoat = s // 3600\nqolgan = s % 3600\n# daqiqa va sekundni toping\n',
            full_solution='s = int(input())\nsoat = s // 3600\nqolgan = s % 3600\nprint(soat)\nprint(qolgan // 60)\nprint(qolgan % 60)\n', explanation="`//` va `%` ni ketma-ket qo'llab vaqtni bo'laklaymiz."),
    ])

LESSONS = [LESSON_7, LESSON_8, LESSON_9, LESSON_10, LESSON_11, LESSON_12, LESSON_13, LESSON_14, LESSON_15]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("2-modul yakuniy nazorati: O'zgaruvchilar va ma'lumot turlari", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **yosh hisoblagich va valyuta konvertori**.
Mini-loyiha uchun haqiqiy kod yozasiz. O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m2_a_t1', "O'zgaruvchi", "O'zgaruvchi nima?", section='assessment', points=2, options=[opt("Nom berilgan qiymat saqlovchi xotira joyi", True), opt("Faqat sonlarni chiqaruvchi buyruq", False), opt("Dasturdagi xato turi", False)], explanation="O'zgaruvchi — qiymat saqlanadigan nomli «quti»."),
    single('m2_a_t2', "To'g'ri nom", "Qaysi o'zgaruvchi nomi to'g'ri?", section='assessment', points=2, options=[opt("`talaba yoshi`", False), opt("`3son`", False), opt("`talaba_yoshi`", True)], explanation="Bo'shliq va boshidagi raqam mumkin emas."),
    single('m2_a_t3', "// amali", "`17 // 5` nimaga teng?", section='assessment', points=2, options=[opt("3", True), opt("2", False), opt("3.4", False)], explanation="17 ichida 5 uch marta to'liq bor."),
    single('m2_a_t4', "input() turi", "`input()` qanday tur qaytaradi?", section='assessment', points=2, options=[opt("int", False), opt("str", True), opt("bool", False)], explanation="Har doim str."),
    multiple('m2_a_t5', "float qiymatlari", "Qaysi qiymatlar `float`?", section='assessment', points=2, options=[opt("`2.0`", True), opt("`10 / 5`", True), opt("`10 // 5`", False), opt("`\"2.0\"`", False)], explanation="`/` doim float; `//` butun sonlarda int; qo'shtirnoqdagi — str."),
    predict('m2_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = 7\nb = 2\nprint(a // b, a % b)\n', answer="3 1", explanation="7 // 2 = 3, 7 % 2 = 1."),
    predict('m2_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='x = "5"\ny = 3\nprint(int(x) * y)\nprint(x * y)\n', answer="15\n555", explanation="Birinchisi son ko'paytmasi, ikkinchisi matn takrori."),
    predict('m2_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='print(type(3 > 2), type(3 / 1))\n', answer="<class 'bool'> <class 'float'>", explanation="Taqqoslash — bool, `/` — float."),
    fix_task('m2_a_f1', "Xatoni tuzating (1)", "Natija: `Narx: 5000 so'm`", section='assessment', points=4, starter_code='narx = 5000\nprint("Narx: " + narx + " so\'m")\n',
             tests=[T('output_equals', "Narx: 5000 so'm", "Natija to'g'ri")], hint="Sonni matnga aylantiring.", full_solution='narx = 5000\nprint("Narx: " + str(narx) + " so\'m")\n', explanation="`TypeError` — `str()` bilan tuzatildi."),
    fix_task('m2_a_f2', "Xatoni tuzating (2)", "Dastur kiritilgan ikki sonning yig'indisini chiqarishi kerak (`2` va `3` → `5`), lekin `23` chiqaryapti.", section='assessment', points=4,
             starter_code='a = input()\nb = input()\nprint(a + b)\n', tests=[T('output_equals', "5", "2 va 3 → 5", stdin="2\n3\n"), T('output_equals', "17", "10 va 7 → 17", stdin="10\n7\n")],
             hint="`input()` matn qaytaradi.", full_solution='a = int(input())\nb = int(input())\nprint(a + b)\n', explanation="Matnlar ulanib ketgan edi — `int()` bilan aylantirildi."),
    code_task('m2_a_project', "Mini-loyiha: Yosh hisoblagich va valyuta konvertori", r"""
Dastur **ikki qism**dan iborat bo'lsin. Foydalanuvchi quyidagilarni ketma-ket kiritadi:

1. **Tug'ilgan yili** (butun son),
2. **Joriy yil** (butun son),
3. **Pul miqdori so'mda** (butun yoki kasr son),
4. **Dollar kursi** (1 dollar necha so'm — butun yoki kasr son).

**Chiqarish — aynan 2 qator:**

```
Yoshingiz: 21
Dollarda: 79.37
```

- `Yoshingiz:` — joriy yil minus tug'ilgan yil.
- `Dollarda:` — `pul / kurs` ning **ikki kasr xonagacha yaxlitlangani**.

Kiritish tartibi: tug'ilgan yil, joriy yil, pul, kurs. Masalan: `2005`, `2026`, `1000000`, `12600` → yuqoridagi natija.
""", section='project', points=15, difficulty='medium', unlock=3, starter_code='# Yosh hisoblagich va valyuta konvertori\n',
        expected_output_example="Yoshingiz: 21\nDollarda: 79.37",
        tests=[T('output_equals', "Yoshingiz: 21\nDollarda: 79.37", "2005/2026/1000000/12600 → to'g'ri natija", stdin="2005\n2026\n1000000\n12600\n"),
               T('output_equals', "Yoshingiz: 30\nDollarda: 100.0", "2000/2030/1280000/12800 → 30 va 100.0", stdin="2000\n2030\n1280000\n12800\n"),
               T('output_equals', "Yoshingiz: 0\nDollarda: 0.5", "Chegaraviy qiymatlar", stdin="2026\n2026\n6400\n12800\n", hidden=True),
               T('code_regex', r"(?s)input\(.*input\(.*input\(.*input\(", "To'rtta input() ishlatilgan"), T('code_contains', 'round', "`round()` ishlatilgan")],
        hint="1) To'rt qiymatni oling: `int(input())`, `int(input())`, `float(input())`, `float(input())`. 2) Yosh = joriy - tug'ilgan. 3) Dollar = round(pul / kurs, 2).",
        partial_solution='tugilgan = int(input())\njoriy = int(input())\npul = float(input())\nkurs = float(input())\nprint("Yoshingiz:", joriy - tugilgan)\n# dollarni hisoblab chiqaring\n',
        full_solution='tugilgan = int(input())\njoriy = int(input())\npul = float(input())\nkurs = float(input())\nprint("Yoshingiz:", joriy - tugilgan)\nprint("Dollarda:", round(pul / kurs, 2))\n',
        explanation="Loyiha modul mavzularini birlashtiradi: input(), int()/float(), arifmetika, round(), print()."),
])
