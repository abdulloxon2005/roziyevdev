"""Python — 0 dan boshlash · 5-modul: Sikllar (Loops) (27–33-darslar) va 2-takrorlash (Review 2)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 5,
    'title': "Sikllar (Loops)",
    'description': "Amallarni takrorlash: for va while sikllari, range(), break, continue va ichma-ich sikllar.",
}

# ==============================================================================
# 27-DARS
# ==============================================================================
LESSON_27 = L(27, "Sikllar nima va nima uchun kerak?", 11,
    "Takrorlanuvchi ishlarni siklsiz yozishning noqulayligini ko'rish va sikl g'oyasini (takrorlash, sanagich, tugash sharti) tushunish.",
    ["Takrorlash", "Sikl (loop)", "Iteratsiya", "Tugash sharti", "Cheksiz sikl"],
    [
        text(r"""
O'qituvchi sizni jazolab: «Daftarga 100 marta *Men darsga kechikmayman* deb yozing», dedi. Siz 100 ta `print()` yozasizmi? Kompyuter takrorlashga **charchamaydi** — faqat unga «shuni N marta qil» deyish kerak. Buning uchun **sikllar** bor.
""", title="100 marta yozish kerakmi?"),
        text(r"""
**Sikl (loop)** — bir xil kod blokini bir necha marta bajarish. Sikl tanasining har bir bajarilishi — **iteratsiya** deyiladi.

Siklsiz:
```python
print("Salom")
print("Salom")
print("Salom")
```
Siklli (keyingi darsda aniq o'rganamiz):
```python
for i in range(3):
    print("Salom")
```

Siklning uch savoli: **nimadan boshlaymiz?** **qachon to'xtaymiz?** **har qadamda nima o'zgaradi?**
""", title="Sikl g'oyasi"),
        callout('analogy', r"""
Sikl — **kir yuvish mashinasi**: «aylanish» harakati o'zi bir xil, lekin dastur belgilaydi — 10 daqiqa yoki 30 daqiqa. To'xtash sharti bo'lmasa — mashina to'xtamaydi (**cheksiz sikl**).
""", title="Hayotiy o'xshatish"),
        example(r'''
for i in range(5):
    print("Python o'rganyapman!")
''', title="Birinchi sikl", body="5 marta bir xil matn chiqadi. `range(5)` — «5 marta takrorla». Kodning chekinishli qismi — sikl tanasi."),
        example(r'''
for kun in range(1, 4):
    print("Mashq kuni:", kun)
print("Tayyor!")
''', title="Amaliy: kunlar sanagichi", body="`kun` o'zgaruvchisi har safar yangi qiymat oladi: 1, 2, 3. Chekinishsiz `print` sikldan keyin **bir marta** chiqadi."),
        exercise('l27_inline_pred'),
        callout('warning', r"""
Tugash shartisiz sikl **cheksiz** ishlaydi — kompyuter qotib qolishi mumkin. Platformada bunday kod vaqt chegarasidan keyin avtomatik to'xtatiladi.
""", title="Cheksiz sikl xavfi"),
        recap(["sikl — kodni takrorlash", "bitta takrorlash — iteratsiya", "sikl to'xtash shartiga ega bo'lishi kerak"], "`for` siklining aniq yozilishi qanday? `i` o'zgaruvchisi nima qiladi?"),
    ],
    [
        single('l27_inline_pred', "Necha marta?", "Quyidagi dastur nechta qator chiqaradi?\n\n```python\nfor i in range(4):\n    print(\"Salom\")\n```", section='inline', points=2, options=[opt("3 ta", False), opt("4 ta", True), opt("5 ta", False)], hint="`range(4)` — 4 marta.", explanation="4 ta iteratsiya — 4 ta qator."),
        single('l27_quiz_1', "Sikl nima?", "Sikl nima uchun kerak?", options=[opt("Kodni bir necha marta takrorlash uchun", True), opt("Xatolarni topish uchun", False), opt("O'zgaruvchi yaratish uchun", False)], hint="100 ta print o'rniga nima?", explanation="Takrorlanuvchi ishni qisqa yozish uchun."),
        predict('l27_quiz_2', "Chekinish", "Dastur nima chiqaradi?", code='for i in range(2):\n    print("A")\nprint("B")\n', answer="A\nA\nB", hint="`B` chekinishsiz.", explanation="`A` ikki marta, `B` sikldan keyin bir marta."),
        single('l27_quiz_3', "Cheksiz sikl", "Cheksiz sikl qachon hosil bo'ladi?", options=[opt("Tugash sharti hech qachon bajarilmasa", True), opt("`range()` ishlatilsa", False), opt("`print()` ishlatilsa", False)], hint="Mashina to'xtamasa?", explanation="To'xtash sharti bajarilmasa."),
        code_task('l27_assignment', "Salomlashuv", r"""
`for` va `range()` yordamida `Dasturlash qiziq!` matnini **aynan 3 marta** chiqaring (har biri alohida qatorda).
""", starter_code='', points=10, tests=[T('output_equals', "Dasturlash qiziq!\nDasturlash qiziq!\nDasturlash qiziq!", "3 marta"), T('code_contains', 'for ', "`for` ishlatilgan"), T('code_contains', 'range', "`range()` ishlatilgan")],
            hint="`for i in range(3):` va ichida `print`.", partial_solution='for i in range(3):\n    # shu yerga print yozing\n    pass\n', full_solution='for i in range(3):\n    print("Dasturlash qiziq!")\n', explanation="`range(3)` uch marta takrorlaydi."),
        single('l27_practice_easy', "Easy: iteratsiya", "Sikl tanasining bitta bajarilishi nima deyiladi?", section='practice', difficulty='easy', options=[opt("Iteratsiya", True), opt("Funksiya", False), opt("Blok", False)], hint="Takrorlash bosqichi.", explanation="Iteratsiya."),
        code_task('l27_practice_medium', "Medium: 5 ta yulduz", r"""
Sikl yordamida 5 ta qator chiqaring, har birida bitta `*`:

```
*
*
*
*
*
```
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "*\n*\n*\n*\n*", "5 ta yulduz"), T('code_contains', 'for ', "`for` ishlatilgan")], hint="`range(5)`.", full_solution='for i in range(5):\n    print("*")\n', explanation="Sikl tanasi 5 marta bajarildi."),
        code_task('l27_practice_hard', "Hard: foydalanuvchi aytgancha", r"""
Foydalanuvchi son kiritadi (`n`). Dastur `Salom` so'zini **n marta** chiqarsin. `2` → ikki qator `Salom`. `0` → hech narsa.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Salom\nSalom", "2", stdin="2\n"), T('output_equals', "Salom", "1", stdin="1\n"), T('output_equals', "", "0", stdin="0\n"), T('output_equals', "Salom\nSalom\nSalom\nSalom", "4", stdin="4\n", hidden=True)], hint="`range(n)` — n o'zgaruvchi bo'lishi mumkin.", full_solution='n = int(input())\nfor i in range(n):\n    print("Salom")\n', explanation="`range()` ichiga o'zgaruvchi berish mumkin."),
    ])

# ==============================================================================
# 28-DARS
# ==============================================================================
LESSON_28 = L(28, "for sikli", 13,
    "for sikli sintaksisini bilish, matn belgilari bo'ylab yurish va sikl o'zgaruvchisidan foydalanish.",
    ["for ... in ...", "Sikl o'zgaruvchisi", "Matn bo'ylab yurish", "Yig'indi (akkumulyator)"],
    [
        text(r"""
Sinfda o'qituvchi davomatni olayotganda **har bir** o'quvchi nomini birin-ketin o'qiydi. `for` sikli ham xuddi shunday — to'plamdagi **har bir elementni** birin-ketin oladi.
""", title="Har biri uchun"),
        text(r"""
```python
for harf in "Python":
    print(harf)
```

- `for` — «har bir ... uchun».
- `harf` — **sikl o'zgaruvchisi**: har iteratsiyada keyingi qiymatni oladi (nomini o'zingiz tanlaysiz).
- `in "Python"` — qayerdan olinadi (hozir matn; keyin `range` va ro'yxatlar).
- Oxiri `:`, tana — chekinish bilan.

**Yig'indi sxemasi:** siklgacha `jami = 0`, siklda `jami = jami + qiymat`. Bu sikl eng ko'p ishlatiladigan andoza.
""", title="for tuzilishi"),
        callout('analogy', r"""
`for` — **konveyer lentasi**: mahsulotlar birin-ketin keladi, siz har birini bir xil tarzda ishlaysiz.
""", title="Hayotiy o'xshatish"),
        example(r'''
for harf in "Salom":
    print(harf)
''', title="Harflar bo'ylab", body="Har bir harf alohida qatorda chiqadi: `S`, `a`, `l`, `o`, `m`."),
        example(r'''
gap = "Men Python o'rganyapman"
unli = 0
for h in gap:
    if h == "a" or h == "o" or h == "i" or h == "u" or h == "e":
        unli = unli + 1
print("Unli harflar:", unli)
''', title="Amaliy: unlilarni sanash", body="`unli` sanagichi har bir mos harfda 1 ga oshadi. Sikl ichida `if` ishlatildi — sikl va shartlar birga ishlaydi. Natija: `Unli harflar: 6`."),
        exercise('l28_inline_blank'),
        callout('tip', r"""
Sikl o'zgaruvchisiga mazmunli nom bering: harflar uchun `harf`, sonlar uchun `son`. Qisqa `i` odatda sanoq uchun ishlatiladi.
"""),
        recap(["`for element in manba:`", "sikl o'zgaruvchisi har safar yangi qiymat oladi", "yig'indi: `jami = jami + x`"], "`range()` bilan sonlar ketma-ketligini qanday hosil qilamiz?"),
    ],
    [
        fill('l28_inline_blank', "Bo'sh joy", "So'zdagi harflarni birin-ketin chiqaring. `abc` uchun har biri alohida qatorda.", 's = "abc"\n___ h in s:\n    print(h)\n', ['for'], section='inline', points=2, tests=[T('output_equals', "a\nb\nc", "a, b, c")], hint="Takrorlash kalit so'zi.", explanation="`for h in s:`."),
        predict('l28_quiz_1', "Sanagich", "Dastur nima chiqaradi?", code='n = 0\nfor h in "kitob":\n    n = n + 1\nprint(n)\n', answer="5", hint="Har harf uchun 1 qo'shiladi.", explanation="5 ta harf — 5 ta iteratsiya."),
        predict('l28_quiz_2', "Yig'indi sxemasi", "Dastur nima chiqaradi?", code='jami = 0\nfor h in "123":\n    jami = jami + int(h)\nprint(jami)\n', answer="6", hint="`int(h)` harf-raqamni songa aylantiradi.", explanation="1 + 2 + 3 = 6."),
        single('l28_quiz_3', "Sikl o'zgaruvchisi", "`for x in \"ab\":` da `x` nima?", options=[opt("Har iteratsiyada keyingi harf", True), opt("Doim `\"ab\"`", False), opt("Takrorlashlar soni", False)], hint="Konveyer lentasi.", explanation="`x` birin-ketin `a`, keyin `b` bo'ladi."),
        code_task('l28_assignment', "Harf sanash", r"""
Foydalanuvchi so'z kiritadi. Dastur so'zdagi **`a`** harflari sonini sanasin va chiqarsin. `banan` → `2`.
""", starter_code='', points=10, tests=[T('output_equals', "2", "banan", stdin="banan\n"), T('output_equals', "0", "kitob", stdin="kitob\n"), T('output_equals', "4", "aaaa", stdin="aaaa\n", hidden=True), T('code_contains', 'for ', "`for` ishlatilgan")],
            hint="Sanagich `n = 0`, siklda `if h == \"a\"`.", partial_solution='soz = input()\nn = 0\nfor h in soz:\n    # agar h == "a" bo\'lsa n ga 1 qo\'shing\n    pass\nprint(n)\n', full_solution='soz = input()\nn = 0\nfor h in soz:\n    if h == "a":\n        n = n + 1\nprint(n)\n', explanation="Sanagich + shart sxemasi."),
        single('l28_practice_easy', "Easy: sikl o'zgaruvchisi nomi", "Sikl o'zgaruvchisiga istalgan nom bersa bo'ladimi?", section='practice', difficulty='easy', options=[opt("Ha, nom qoidalariga rioya qilsa", True), opt("Faqat `i`", False), opt("Faqat `harf`", False)], hint="Oddiy o'zgaruvchi.", explanation="Nom tanlash qoidalari o'sha-o'sha."),
        code_task('l28_practice_medium', "Medium: raqamlar yig'indisi", r"""
Foydalanuvchi son kiritadi (matn sifatida). Uning raqamlari yig'indisini chiqaring. `1234` → `10`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "10", "1234", stdin="1234\n"), T('output_equals', "9", "9", stdin="9\n"), T('output_equals', "0", "0", stdin="0\n", hidden=True)], hint="Sikl ichida `int(h)`.", full_solution='son = input()\njami = 0\nfor h in son:\n    jami = jami + int(h)\nprint(jami)\n', explanation="Yig'indi sxemasi."),
        code_task('l28_practice_hard', "Hard: matnni teskari yozish", r"""
Foydalanuvchi so'z kiritadi. Dastur uni **teskari** tartibda chiqarsin (indeks ishlatmasdan, sikl bilan). `salom` → `molas`. Maslahat: yangi matnga har harfni **oldidan** qo'shing: `yangi = h + yangi`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "molas", "salom", stdin="salom\n"), T('output_equals', "a", "a", stdin="a\n"), T('output_equals', "nohtyP", "Python", stdin="Python\n", hidden=True)], hint="`yangi = \"\"` bilan boshlang.", partial_solution='soz = input()\nyangi = ""\nfor h in soz:\n    # harfni yangi ning oldiga qo\'shing\n    pass\nprint(yangi)\n', full_solution='soz = input()\nyangi = ""\nfor h in soz:\n    yangi = h + yangi\nprint(yangi)\n', explanation="Har yangi harf oldinga qo'yiladi — natijada tartib teskari bo'ladi."),
    ])

# ==============================================================================
# 29-DARS
# ==============================================================================
LESSON_29 = L(29, "range() funksiyasi", 13,
    "range(n), range(a, b), range(a, b, qadam) shakllarini ishlatish va sonlar ketma-ketligini hosil qilish.",
    ["range(n)", "range(a, b)", "range(a, b, qadam)", "Teskari sanash", "Oxirgi son kirmaydi"],
    [
        text(r"""
Raketa uchirishda sanaymiz: 10, 9, 8, ... 1. Yoki: 2, 4, 6, 8. Bunday **sonlar ketma-ketligini** `range()` funksiyasi tayyorlaydi.
""", title="Sonlar ketma-ketligi"),
        text(r"""
| Yozuv | Hosil qilgan sonlar |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(2, 11, 2)` | 2, 4, 6, 8, 10 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

- `range(a, b)` — `a` dan `b` gacha, **`b` kirmaydi** (kesimdagi kabi).
- Uchinchi son — **qadam**. Manfiy qadam — teskari sanash.
- Bitta son berilsa — 0 dan boshlanadi.
""", title="range() uch shakli"),
        callout('analogy', r"""
`range()` — **zinapoya**: qayerdan boshlash, qayerda to'xtash (tepaga chiqmaydi) va har qadamda nechta pog'ona sakrash.
""", title="Hayotiy o'xshatish"),
        example(r'''
for i in range(1, 6):
    print(i)
for i in range(10, 0, -3):
    print(i)
''', title="Oddiy va teskari", body="Birinchi sikl: 1 dan 5 gacha. Ikkinchisi: 10, 7, 4, 1 (qadam -3, 0 kirmaydi)."),
        example(r'''
jami = 0
for son in range(1, 101):
    jami = jami + son
print("1 dan 100 gacha yig'indi:", jami)

for k in range(5, 0, -1):
    print(k, end=" ")
print("Start!")
''', title="Amaliy: yig'indi va teskari sanash", body="Mashhur yig'indi `5050`. Ikkinchi sikl `5 4 3 2 1 Start!` chiqaradi (`end=\" \"` — bir qatorda)."),
        exercise('l29_inline_pred'),
        callout('warning', r"""
`range(1, 5)` — 1, 2, 3, 4 (5 **kirmaydi**). Ko'p xato shundan: «1 dan 5 gacha» uchun `range(1, 6)` yoziladi.
""", title="Diqqat"),
        recap(["`range(n)`, `range(a, b)`, `range(a, b, qadam)`", "oxirgi son kirmaydi", "manfiy qadam — teskari sanash"], "sikl necha marta ishlashi oldindan noma'lum bo'lsa-chi? Masalan, to'g'ri parol kiritilgunga qadar?"),
    ],
    [
        predict('l29_inline_pred', "range natijasi", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", section='inline', code='for i in range(2, 7, 2):\n    print(i, end=" ")\n', answer="2 4 6", points=2, hint="2 dan 7 gacha, qadam 2.", explanation="2, 4, 6 — 8 esa 7 dan katta."),
        predict('l29_quiz_1', "Oxirgi son", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", code='for i in range(1, 4):\n    print(i, end=" ")\n', answer="1 2 3", hint="4 kirmaydi.", explanation="1, 2, 3."),
        single('l29_quiz_2', "Teskari sanash", "5 dan 1 gacha kamayib sanash uchun qaysi biri to'g'ri?", options=[opt("`range(5, 0, -1)`", True), opt("`range(5, 1)`", False, "Bu bo'sh ketma-ketlik beradi."), opt("`range(1, 5, -1)`", False)], hint="Qadam manfiy bo'lishi kerak.", explanation="Boshlanish 5, tugash 0 (kirmaydi), qadam -1."),
        predict('l29_quiz_3', "Yig'indi", "Dastur nima chiqaradi?", code='j = 0\nfor i in range(1, 5):\n    j = j + i\nprint(j)\n', answer="10", hint="1+2+3+4.", explanation="1+2+3+4 = 10."),
        code_task('l29_assignment', "Ko'paytirish jadvali", r"""
Foydalanuvchi son `n` kiritadi. `n` ning ko'paytirish jadvalini 1 dan 10 gacha chiqaring (`f-string` bilan): `3 * 1 = 3`, ..., `3 * 10 = 30`. Masalan `n = 2` bo'lsa 10 qator, birinchisi `2 * 1 = 2`.
""", starter_code='', points=10, tests=[T('output_equals', "\n".join(f"3 * {i} = {3 * i}" for i in range(1, 11)), "n = 3", stdin="3\n"), T('output_equals', "\n".join(f"7 * {i} = {7 * i}" for i in range(1, 11)), "n = 7", stdin="7\n", hidden=True), T('code_contains', 'range', "`range()` ishlatilgan")],
            hint="`for i in range(1, 11):` va `print(f\"{n} * {i} = {n * i}\")`.", partial_solution='n = int(input())\nfor i in range(1, 11):\n    # f-string bilan chiqaring\n    pass\n', full_solution='n = int(input())\nfor i in range(1, 11):\n    print(f"{n} * {i} = {n * i}")\n', explanation="`range(1, 11)` 1 dan 10 gacha."),
        single('l29_practice_easy', "Easy: range(3)", "`range(3)` qaysi sonlarni beradi?", section='practice', difficulty='easy', options=[opt("0, 1, 2", True), opt("1, 2, 3", False), opt("0, 1, 2, 3", False)], hint="0 dan boshlanadi, 3 kirmaydi.", explanation="0, 1, 2."),
        code_task('l29_practice_medium', "Medium: juft sonlar", r"""
1 dan 20 gacha **juft sonlarni** bir qatorda, probel bilan chiqaring (`range` qadami bilan, `if` siz): `2 4 6 8 10 12 14 16 18 20`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "2 4 6 8 10 12 14 16 18 20", "Juft sonlar"), T('code_regex', r"range\(\s*2\s*,\s*21\s*,\s*2\s*\)", "`range(2, 21, 2)`")], hint="`end=\" \"` bilan bir qatorga chiqaring; oxirgi probel muammo emas.", full_solution='for i in range(2, 21, 2):\n    print(i, end=" ")\n', explanation="Qadam 2 — faqat juftlar."),
        code_task('l29_practice_hard', "Hard: faktorial", r"""
Foydalanuvchi musbat butun `n` kiritadi. `n!` (faktorial) = `1 * 2 * ... * n`. `5` → `120`, `1` → `1`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "120", "5", stdin="5\n"), T('output_equals', "1", "1", stdin="1\n"), T('output_equals', "3628800", "10", stdin="10\n"), T('output_equals', "720", "6", stdin="6\n", hidden=True)], hint="Ko'paytma sanagichi `p = 1` dan boshlanadi.", partial_solution='n = int(input())\np = 1\nfor i in range(1, n + 1):\n    # p ni i ga ko\'paytiring\n    pass\nprint(p)\n', full_solution='n = int(input())\np = 1\nfor i in range(1, n + 1):\n    p = p * i\nprint(p)\n', explanation="Yig'indidagi kabi, faqat ko'paytirish va boshlang'ich qiymat 1."),
    ])

# ==============================================================================
# 30-DARS
# ==============================================================================
LESSON_30 = L(30, "while sikli", 13,
    "while sikli bilan «shart rost bo'lguncha» takrorlash, sikl o'zgaruvchisini yangilash va cheksiz siklning oldini olish.",
    ["while", "Sikl sharti", "Sanagichni yangilash", "Cheksiz sikldan saqlanish"],
    [
        text(r"""
`for` — «5 marta takrorla». Lekin ba'zan necha marta ekanini **bilmaymiz**: «to'g'ri parol kiritilgunga qadar so'ra», «pul tugamaguncha xarid qil». Bunday vaziyatda **`while`** (inglizcha «...bo'lguncha») ishlatiladi.
""", title="Noma'lum marta takrorlash"),
        text(r"""
```python
n = 1
while n <= 3:
    print(n)
    n = n + 1
print("Tugadi")
```

`while shart:` — **shart rost bo'lguncha** blokni takrorlaydi. Har iteratsiyadan oldin shart qayta tekshiriladi.

Uch qadam: **1)** boshlang'ich qiymat (`n = 1`), **2)** shart (`n <= 3`), **3)** **yangilash** (`n = n + 1`) — yangilash unutilsa, shart hech qachon yolg'on bo'lmaydi: **cheksiz sikl**.
""", title="while tuzilishi"),
        callout('analogy', r"""
`while` — **choynak qaynashini kutish**: «suv qaynamaguncha kutaman». Qancha vaqt ketishini bilmaymiz, lekin to'xtash sharti aniq.
""", title="Hayotiy o'xshatish"),
        example(r'''
n = 5
while n > 0:
    print(n)
    n = n - 1
print("Start!")
''', title="Teskari sanash", body="`n` har safar 1 ga kamayadi: 5, 4, 3, 2, 1, so'ng `n > 0` yolg'on bo'lib, sikl tugaydi."),
        example(r'''
parol = ""
while parol != "python":
    parol = input("Parolni kiriting: ")
print("Xush kelibsiz!")
''', title="Amaliy: parol to'g'ri bo'lguncha", body="Foydalanuvchi qancha marta xato qilsa, shuncha marta so'raydi. Platformada kiritish maydoniga bir necha qatorni yozing: `123`, `abc`, `python`."),
        exercise('l30_inline_fix'),
        callout('warning', r"""
`n = n + 1` ni (yoki shartga ta'sir qiluvchi boshqa yangilashni) yozishni **unutmang** — aks holda sikl cheksiz ishlaydi. Platformada bunday kod ~5 soniyadan keyin to'xtatiladi.
""", title="Cheksiz sikl"),
        recap(["`while shart:` — shart rost bo'lguncha", "boshlang'ich qiymat + shart + yangilash", "yangilashni unutmang"], "siklni shart yolg'on bo'lmasdan oldin to'xtatish mumkinmi? Masalan, kerakli narsa topilganda?"),
    ],
    [
        fix_task('l30_inline_fix', "Cheksiz siklni tuzating", "Dastur 1, 2, 3 chiqarib to'xtashi kerak, lekin cheksiz ishlaydi. Tuzating.", section='inline', points=2, starter_code='n = 1\nwhile n <= 3:\n    print(n)\n', tests=[T('output_equals', "1\n2\n3", "1, 2, 3")], hint="Sikl ichida `n` yangilanmayapti.", full_solution='n = 1\nwhile n <= 3:\n    print(n)\n    n = n + 1\n', explanation="`n = n + 1` yetishmayotgan edi."),
        predict('l30_quiz_1', "while natijasi", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", code='n = 1\nwhile n < 20:\n    print(n, end=" ")\n    n = n * 2\n', answer="1 2 4 8 16", hint="Har safar ikki baravar.", explanation="1, 2, 4, 8, 16; keyin 32 < 20 yolg'on."),
        single('l30_quiz_2', "for yoki while?", "Foydalanuvchi to'g'ri javob bergunga qadar savol berish uchun qaysi sikl qulay?", options=[opt("`while`", True), opt("`for` + `range(5)`", False), opt("Hech qaysi", False)], hint="Necha marta ekani noma'lum.", explanation="Takrorlashlar soni noma'lum bo'lsa — `while`."),
        predict('l30_quiz_3', "Hech qachon bajarilmaydi", "Dastur nima chiqaradi?", code='n = 10\nwhile n < 5:\n    print("A")\nprint("B")\n', answer="B", hint="Shart boshidanoq yolg'on.", explanation="`10 < 5` yolg'on — sikl tanasi bir marta ham bajarilmaydi."),
        code_task('l30_assignment', "Pul yig'ish", r"""
Siz har kuni 5000 so'm tejaysiz. Maqsad — telefon sotib olish (narxi foydalanuvchi kiritadi). Dastur **necha kunda** pul yig'ilishini hisoblasin. `while` ishlating. Narx `23000` → `5` kun; `20000` → `4`; `5000` → `1`.
""", starter_code='', points=10, tests=[T('output_equals', "5", "23000", stdin="23000\n"), T('output_equals', "4", "20000", stdin="20000\n"), T('output_equals', "1", "5000", stdin="5000\n"), T('output_equals', "21", "101000", stdin="101000\n", hidden=True), T('code_contains', 'while', "`while` ishlatilgan")],
            hint="`yigilgan = 0`, `kun = 0`; siklda ikkalasini yangilang.", partial_solution='narx = int(input())\nyigilgan = 0\nkun = 0\nwhile yigilgan < narx:\n    # yigilgan va kun ni yangilang\n    pass\nprint(kun)\n', full_solution='narx = int(input())\nyigilgan = 0\nkun = 0\nwhile yigilgan < narx:\n    yigilgan = yigilgan + 5000\n    kun = kun + 1\nprint(kun)\n', explanation="Yig'ilgan pul narxga yetmaguncha sikl davom etadi."),
        single('l30_practice_easy', "Easy: shart", "`while` sikli qachon tugaydi?", section='practice', difficulty='easy', options=[opt("Shart yolg'on bo'lganda", True), opt("Shart rost bo'lganda", False), opt("5 marta takrorlangach", False)], hint="Rost bo'lguncha ishlaydi.", explanation="Shart yolg'on bo'lganda."),
        code_task('l30_practice_medium', "Medium: raqamlarni sanash", r"""
Foydalanuvchi musbat butun son kiritadi. `while` va `//` yordamida nechta raqamdan iboratligini toping. `12345` → `5`, `7` → `1`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "5", "12345", stdin="12345\n"), T('output_equals', "1", "7", stdin="7\n"), T('output_equals', "3", "100", stdin="100\n", hidden=True)], hint="Son 0 bo'lguncha `n = n // 10`, har safar sanagichni oshiring.", full_solution='n = int(input())\nsoni = 0\nwhile n > 0:\n    n = n // 10\n    soni = soni + 1\nprint(soni)\n', explanation="Har bo'lishda bitta raqam «tushib ketadi»."),
        code_task('l30_practice_hard', "Hard: Kollatz", r"""
Foydalanuvchi musbat son kiritadi. Son 1 bo'lmaguncha: juft bo'lsa 2 ga bo'ling (`//`), toq bo'lsa 3 ga ko'paytirib 1 qo'shing. Necha qadamda 1 ga yetganini chiqaring. `6` → `8` (6→3→10→5→16→8→4→2→1), `1` → `0`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "8", "6", stdin="6\n"), T('output_equals', "0", "1", stdin="1\n"), T('output_equals', "111", "27", stdin="27\n", hidden=True), T('output_equals', "1", "2", stdin="2\n")], hint="`while n != 1:` ichida `if n % 2 == 0`.", partial_solution='n = int(input())\nqadam = 0\nwhile n != 1:\n    # juft yoki toq holatini yozing\n    qadam = qadam + 1\nprint(qadam)\n', full_solution='n = int(input())\nqadam = 0\nwhile n != 1:\n    if n % 2 == 0:\n        n = n // 2\n    else:\n        n = 3 * n + 1\n    qadam = qadam + 1\nprint(qadam)\n', explanation="`while` ichida `if/else` — sikl va shart birga."),
    ])

# ==============================================================================
# 31-DARS
# ==============================================================================
LESSON_31 = L(31, "break operatori", 11,
    "break bilan siklni oldindan to'xtatish va «cheksiz sikl + break» andozasidan foydalanish.",
    ["break", "Siklni to'xtatish", "while True", "Qidirish"],
    [
        text(r"""
Kalitlar to'plamidan kerakli kalitni qidiryapsiz. Topishingiz bilan qolganlarini tekshirmaysiz-ku? Siklda ham shunday: maqsadga erishilsa, **darhol chiqish** kerak. Buning uchun **`break`** («uzish») ishlatiladi.
""", title="Topdim — to'xtayman!"),
        text(r"""
```python
for i in range(1, 100):
    if i % 7 == 0:
        print("Birinchi 7 ga karrali son:", i)
        break
```

`break` bajarilishi bilan sikl **darhol tugaydi** va dastur sikldan keyingi qatordan davom etadi.

**«Cheksiz sikl + break»** andozasi: `while True:` doim rost — chiqish faqat `break` bilan:

```python
while True:
    javob = input("Chiqish uchun 'q': ")
    if javob == "q":
        break
```
""", title="break"),
        callout('analogy', r"""
`break` — **yong'in signali**: mashq to'liq tugamagan bo'lsa ham, hamma darhol binodan chiqadi.
""", title="Hayotiy o'xshatish"),
        example(r'''
for son in range(10, 50):
    if son % 13 == 0:
        print("Topildi:", son)
        break
print("Qidiruv tugadi")
''', title="Birinchisini topish", body="10 dan boshlab 13 ga bo'linadigan birinchi son — `13`. Topilishi bilan sikl to'xtaydi, `Qidiruv tugadi` chiqadi."),
        example(r'''
jami = 0
while True:
    s = int(input("Son (0 — tugatish): "))
    if s == 0:
        break
    jami = jami + s
print("Yig'indi:", jami)
''', title="Amaliy: 0 kiritilguncha yig'ish", body="Kiritish: `5`, `3`, `0` → `Yig'indi: 8`. Nol — to'xtash belgisi (sentinel) — yig'indiga qo'shilmaydi."),
        exercise('l31_inline_pred'),
        callout('warning', r"""
`while True` da `break` yozishni unutmang — aks holda dastur hech qachon tugamaydi.
""", title="Diqqat"),
        recap(["`break` — siklni darhol to'xtatadi", "qidirishda topilgach to'xtash uchun ishlatiladi", "`while True` + `break` — keng tarqalgan andoza"], "agar siklni to'xtatmasdan, faqat **joriy iteratsiyani** o'tkazib yubormoqchi bo'lsak-chi?"),
    ],
    [
        predict('l31_inline_pred', "break natijasi", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", section='inline', code='for i in range(1, 10):\n    if i == 4:\n        break\n    print(i, end=" ")\n', answer="1 2 3", points=2, hint="`i == 4` da to'xtaydi, 4 chiqmaydi.", explanation="`break` chiqarishdan oldin ishlaydi."),
        predict('l31_quiz_1', "Sikldan keyingi qator", "Dastur nima chiqaradi?", code='for i in range(5):\n    if i == 1:\n        break\nprint("tamom", i)\n', answer="tamom 1", hint="Sikl o'zgaruvchisi qiymati saqlanib qoladi.", explanation="`i` = 1 da to'xtadi; sikldan keyin ham `i` = 1."),
        single('l31_quiz_2', "break vazifasi", "`break` nima qiladi?", options=[opt("Siklni to'liq to'xtatadi", True), opt("Faqat joriy iteratsiyani o'tkazib yuboradi", False), opt("Dasturni to'xtatadi", False)], hint="Sikldan chiqadi.", explanation="Sikl tugaydi, dastur davom etadi."),
        single('l31_quiz_3', "while True", "`while True:` siklini qanday to'xtatamiz?", options=[opt("`break` bilan", True), opt("Hech qanday usul yo'q", False), opt("`range()` bilan", False)], hint="Shart doim rost.", explanation="`if` ichida `break`."),
        code_task('l31_assignment', "Birinchi bo'luvchi", r"""
Foydalanuvchi 2 dan katta butun son `n` kiritadi. `2` dan boshlab `n` ning **birinchi bo'luvchisini** toping (`n % d == 0`) va chiqaring; topilganda siklni `break` bilan to'xtating. `15` → `3`, `13` → `13`, `49` → `7`.
""", starter_code='', points=10, tests=[T('output_equals', "3", "15", stdin="15\n"), T('output_equals', "13", "13", stdin="13\n"), T('output_equals', "7", "49", stdin="49\n"), T('output_equals', "2", "100", stdin="100\n", hidden=True), T('code_contains', 'break', "`break` ishlatilgan")],
            hint="`for d in range(2, n + 1):` ichida `if n % d == 0`.", partial_solution='n = int(input())\nfor d in range(2, n + 1):\n    if n % d == 0:\n        print(d)\n        # shu yerda to\'xtating\n', full_solution='n = int(input())\nfor d in range(2, n + 1):\n    if n % d == 0:\n        print(d)\n        break\n', explanation="Eng kichik bo'luvchi doim birinchi topiladi."),
        single('l31_practice_easy', "Easy: sentinel", "«Nol kiritilguncha» sxemasida nol qanday vazifani bajaradi?", section='practice', difficulty='easy', options=[opt("To'xtash belgisi", True), opt("Yig'indiga qo'shiladi", False), opt("Xato", False)], hint="Siklni to'xtatadi.", explanation="To'xtash belgisi (sentinel)."),
        code_task('l31_practice_medium', "Medium: «stop» deyilguncha", r"""
Foydalanuvchi so'zlar kiritadi. Har birini KATTA harflarda chiqaring. `stop` kiritilsa — to'xtasin (`stop` chiqarilmasin). Kiritish `salom`, `dunyo`, `stop` → `SALOM`, `DUNYO`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "SALOM\nDUNYO", "salom, dunyo, stop", stdin="salom\ndunyo\nstop\n"), T('output_equals', "", "darhol stop", stdin="stop\n"), T('output_equals', "A", "a, stop, b", stdin="a\nstop\nb\n", hidden=True)], hint="`while True:` va `if s == \"stop\": break`.", full_solution='while True:\n    s = input()\n    if s == "stop":\n        break\n    print(s.upper())\n', explanation="`while True` + `break`."),
        code_task('l31_practice_hard', "Hard: tub sonmi?", r"""
Foydalanuvchi 2 dan katta son kiritadi. Agar u faqat 1 ga va o'ziga bo'linsa `Tub`, aks holda `Tub emas` chiqaring. `7` → `Tub`, `9` → `Tub emas`, `2` → `Tub`. Bo'luvchi topilganda `break` ishlating.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Tub", "7", stdin="7\n"), T('output_equals', "Tub emas", "9", stdin="9\n"), T('output_equals', "Tub", "2", stdin="2\n"), T('output_equals', "Tub", "97", stdin="97\n", hidden=True), T('output_equals', "Tub emas", "100", stdin="100\n", hidden=True)], hint="`tub = True` belgisi: bo'luvchi topilsa `False` qilib `break`.", partial_solution='n = int(input())\ntub = True\nfor d in range(2, n):\n    if n % d == 0:\n        # belgini o\'zgartiring va to\'xtating\n        pass\n', full_solution='n = int(input())\ntub = True\nfor d in range(2, n):\n    if n % d == 0:\n        tub = False\n        break\nif tub:\n    print("Tub")\nelse:\n    print("Tub emas")\n', explanation="Belgi (flag) + break — qidirishning klassik usuli."),
    ])

# ==============================================================================
# 32-DARS
# ==============================================================================
LESSON_32 = L(32, "continue operatori", 11,
    "continue bilan joriy iteratsiyani o'tkazib yuborish va break bilan farqini ajratish.",
    ["continue", "Iteratsiyani o'tkazib yuborish", "break va continue farqi", "Filtrlash"],
    [
        text(r"""
Savatdagi mevalarni tekshiryapsiz: chirigan olmani **chetga qo'yasiz** va keyingisiga o'tasiz — butun ishni to'xtatmaysiz. Bu — **`continue`** («davom et», ya'ni «bu safarni o'tkaz»).
""", title="Buni o'tkazib yubor"),
        text(r"""
```python
for i in range(1, 6):
    if i == 3:
        continue
    print(i)
```
Natija: `1 2 4 5` (3 tushib qoldi, lekin sikl davom etdi).

| | `break` | `continue` |
|---|---|---|
| Nima qiladi | siklni **butunlay** to'xtatadi | joriy iteratsiyani **o'tkazib**, keyingisiga o'tadi |
| Sikldan keyin | dastur davom etadi | sikl davom etadi |
""", title="continue va break farqi"),
        callout('analogy', r"""
`break` — **«uyga ketdim»** (ish tugadi). `continue` — **«bu topshiriqni o'tkazib yuboraman»** (keyingisiga o'taman).
""", title="Hayotiy o'xshatish"),
        example(r'''
for i in range(1, 8):
    if i % 2 == 0:
        continue
    print(i, end=" ")
''', title="Faqat toq sonlar", body="Juft sonlarda `continue` bajarilib, `print` o'tkazib yuboriladi: `1 3 5 7`."),
        example(r'''
jami = 0
for narx in range(1000, 6000, 1000):
    if narx == 3000:
        continue
    jami = jami + narx
print("Jami:", jami)
''', title="Amaliy: aksiyadagi mahsulotni hisoblamaslik", body="3000 so'mlik mahsulot hisobga olinmadi: `1000 + 2000 + 4000 + 5000 = 12000`."),
        exercise('l32_inline_pred'),
        callout('warning', r"""
`while` siklida `continue` dan **oldin** sanagichni yangilashni unutmang — aks holda sikl cheksiz bo'lib qoladi.
""", title="Diqqat"),
        recap(["`continue` — joriy iteratsiyani o'tkazadi", "`break` — butun siklni to'xtatadi", "filtrlash uchun qulay"], "sikl ichida yana sikl yozish mumkinmi? Masalan, jadval chizish uchun?"),
    ],
    [
        predict('l32_inline_pred', "continue natijasi", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", section='inline', code='for i in range(5):\n    if i == 2:\n        continue\n    print(i, end=" ")\n', answer="0 1 3 4", points=2, hint="2 tushib qoladi.", explanation="`i == 2` da `print` o'tkazib yuboriladi."),
        single('l32_quiz_1', "Farqi", "Qaysi biri siklni **butunlay** to'xtatadi?", options=[opt("`break`", True), opt("`continue`", False), opt("Ikkalasi ham", False)], hint="Uyga ketish.", explanation="`break` to'xtatadi; `continue` keyingi iteratsiyaga o'tadi."),
        predict('l32_quiz_2', "Sanash", "Dastur nima chiqaradi?", code='n = 0\nfor i in range(1, 11):\n    if i % 3 == 0:\n        continue\n    n = n + 1\nprint(n)\n', answer="7", hint="3, 6, 9 sanalmaydi.", explanation="10 ta sondan 3 tasi (3, 6, 9) o'tkazib yuborildi: 7."),
        predict('l32_quiz_3', "break va continue", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", code='for i in range(6):\n    if i == 1:\n        continue\n    if i == 4:\n        break\n    print(i, end=" ")\n', answer="0 2 3", hint="1 o'tkazildi, 4 da to'xtadi.", explanation="`0 2 3`."),
        code_task('l32_assignment', "Unlisiz matn", r"""
Foydalanuvchi so'z kiritadi (kichik harflarda). Dastur uni **unli harflarsiz** (`a, o, i, u, e`) chiqarsin. `continue` ishlating. Natija **bir qatorda** bo'lsin (`end=""`). `salom` → `slm`.
""", starter_code='', points=10, tests=[T('output_equals', "slm", "salom", stdin="salom\n"), T('output_equals', "pythn", "python", stdin="python\n"), T('output_equals', "", "aeiou", stdin="aeiou\n", hidden=True), T('code_contains', 'continue', "`continue` ishlatilgan")],
            hint="Unli bo'lsa `continue`, aks holda `print(h, end=\"\")`.", partial_solution='soz = input()\nfor h in soz:\n    if h in "aoiue":\n        continue\n    # harfni chiqaring\n', full_solution='soz = input()\nfor h in soz:\n    if h in "aoiue":\n        continue\n    print(h, end="")\nprint()\n', explanation="`h in \"aoiue\"` — harf shu matnda bormi."),
        single('l32_practice_easy', "Easy: tushirib qoldirish", "`continue` dan keyingi (sikl tanasidagi) qatorlar shu iteratsiyada bajariladimi?", section='practice', difficulty='easy', options=[opt("Yo'q, keyingi iteratsiyaga o'tiladi", True), opt("Ha", False), opt("Faqat birinchisi", False)], hint="Joriy safarni o'tkazadi.", explanation="Qolgan qatorlar o'tkazib yuboriladi."),
        code_task('l32_practice_medium', "Medium: 5 ga karrali bo'lmaganlar", r"""
1 dan 15 gacha sonlardan **5 ga bo'linmaydiganlarini** bir qatorda, probel bilan chiqaring: `1 2 3 4 6 7 8 9 11 12 13 14`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "1 2 3 4 6 7 8 9 11 12 13 14", "Natija"), T('code_contains', 'continue', "`continue` ishlatilgan")], hint="`i % 5 == 0` bo'lsa `continue`.", full_solution='for i in range(1, 16):\n    if i % 5 == 0:\n        continue\n    print(i, end=" ")\n', explanation="5, 10, 15 o'tkazib yuboriladi."),
        code_task('l32_practice_hard', "Hard: musbat sonlar yig'indisi", r"""
Foydalanuvchi **5 ta** butun son kiritadi (alohida qatorda). Dastur faqat **musbat** sonlarning yig'indisini chiqarsin (manfiy va 0 o'tkazib yuboriladi). `3`, `-2`, `5`, `0`, `4` → `12`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "12", "3,-2,5,0,4", stdin="3\n-2\n5\n0\n4\n"), T('output_equals', "0", "hammasi manfiy", stdin="-1\n-2\n-3\n-4\n-5\n"), T('output_equals', "15", "1..5", stdin="1\n2\n3\n4\n5\n", hidden=True), T('code_contains', 'continue', "`continue` ishlatilgan")], hint="5 marta `input()` — `range(5)` ichida.", full_solution='jami = 0\nfor i in range(5):\n    s = int(input())\n    if s <= 0:\n        continue\n    jami = jami + s\nprint(jami)\n', explanation="`continue` manfiy va nolni filtrladi."),
    ])

# ==============================================================================
# 33-DARS
# ==============================================================================
LESSON_33 = L(33, "Ichma-ich sikllar", 14,
    "Sikl ichida sikl yozish, tashqi va ichki sikl qanday ishlashini bilish va yulduzchalardan shakl hamda jadval chizish.",
    ["Ichma-ich sikl", "Tashqi va ichki sikl", "Jadval chizish", "end parametri"],
    [
        text(r"""
Soat milini tasavvur qiling: **soat** miliga bir qadam — **daqiqa** mili 60 marta aylanadi. Tashqi harakat sekin, ichki — tez. Dasturda ham **sikl ichida sikl** bo'lishi mumkin — masalan, jadval (qator va ustunlar) chizishda.
""", title="Sikl ichida sikl"),
        text(r"""
```python
for qator in range(1, 4):
    for ustun in range(1, 4):
        print(qator * ustun, end=" ")
    print()
```

Natija:
```text
1 2 3
2 4 6
3 6 9
```

- **Tashqi sikl** — har bir qator uchun bir marta ishlaydi.
- **Ichki sikl** — tashqining **har bir** iteratsiyasida to'liq aylanib chiqadi.
- Jami bajarilish: `3 × 3 = 9` marta.
- `print()` (bo'sh) — yangi qatorga o'tadi. Ichki sikl uchun chekinish — 8 ta bo'sh joy.
""", title="Qanday ishlaydi?"),
        callout('analogy', r"""
Ichma-ich sikl — **kitob**: tashqi sikl — boblar, ichki sikl — har bobdagi sahifalar. Har bir bob uchun **hamma** sahifalar o'qiladi.
""", title="Hayotiy o'xshatish"),
        example(r'''
for qator in range(1, 5):
    for i in range(qator):
        print("*", end="")
    print()
''', title="Uchburchak", body="1-qatorda 1, 2-qatorda 2, ... yulduz. Ichki siklning uzunligi tashqi sikl qiymatiga bog'liq."),
        example(r'''
for soat in range(1, 3):
    for daqiqa in range(0, 60, 30):
        print(f"{soat}:{daqiqa:02d}")
''', title="Amaliy: jadval vaqtlari", body="`02d` — ikki xonali, boshida 0 bilan: `1:00`, `1:30`, `2:00`, `2:30`. Ichki sikl har soat uchun qayta ishlaydi."),
        exercise('l33_inline_pred'),
        callout('tip', r"""
Murakkab ichma-ich siklni tushunish uchun qog'ozga jadval chizib, har bir iteratsiyada o'zgaruvchilar qiymatini yozing («qo'lda bajarish»).
"""),
        recap(["ichki sikl har iteratsiyada to'liq aylanadi", "bajarilishlar soni = tashqi × ichki", "`print()` yangi qatorga o'tadi"], "modul oxirida son topish o'yini yaratamiz — buning uchun nimalar kerak bo'ladi?"),
    ],
    [
        single('l33_inline_pred', "Necha marta?", "Quyidagi dastur `*` belgisini necha marta chiqaradi?\n\n```python\nfor i in range(3):\n    for j in range(4):\n        print(\"*\")\n```", section='inline', points=2, options=[opt("7", False), opt("12", True), opt("4", False)], hint="3 × 4.", explanation="Ichki sikl 4 marta, tashqisi 3 marta — 12."),
        predict('l33_quiz_1', "Ikki o'zgaruvchi", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", code='for a in range(1, 3):\n    for b in range(1, 3):\n        print(a * b, end=" ")\n', answer="1 2 2 4", hint="(1,1) (1,2) (2,1) (2,2).", explanation="1·1, 1·2, 2·1, 2·2."),
        single('l33_quiz_2', "Qaysi sikl tezroq?", "Ichma-ich siklda qaysi biri tezroq o'zgaradi?", options=[opt("Ichki sikl", True), opt("Tashqi sikl", False), opt("Ikkalasi bir xil", False)], hint="Soat va daqiqa mili.", explanation="Ichki sikl har bir tashqi qadamda to'liq aylanadi."),
        predict('l33_quiz_3', "Uchburchak", "Dastur nima chiqaradi? (Har qatorni alohida satrga yozing.)", code='for i in range(1, 6):\n    for j in range(i):\n        print("#", end="")\n    print()\n', answer="#\n##\n###\n####\n#####", hint="Har qatorda `#` soni qator raqamiga teng.", explanation="Tashqi sikl 5 marta — 5 qator; i-qatorda i ta `#`."),
        code_task('l33_assignment', "Yulduzli to'rtburchak", r"""
Foydalanuvchi **qatorlar** va **ustunlar** sonini kiritadi (ikki son). Shuncha qator va ustundan iborat `*` to'rtburchak chizing. `2` va `3` →
```
***
***
```
""", starter_code='', points=10, tests=[T('output_equals', "***\n***", "2x3", stdin="2\n3\n"), T('output_equals', "*", "1x1", stdin="1\n1\n"), T('output_equals', "****\n****\n****", "3x4", stdin="3\n4\n", hidden=True), T('code_regex', r"(?m)^ {4}for ", "Ichma-ich for")],
            hint="Tashqi — qatorlar, ichki — ustunlar; har qatordan keyin `print()`.", partial_solution='q = int(input())\nu = int(input())\nfor i in range(q):\n    for j in range(u):\n        print("*", end="")\n    # qatorni tugating\n', full_solution='q = int(input())\nu = int(input())\nfor i in range(q):\n    for j in range(u):\n        print("*", end="")\n    print()\n', explanation="Ichki sikl bir qatorni, tashqisi hamma qatorlarni chizadi."),
        single('l33_practice_easy', "Easy: bajarilishlar soni", "Tashqi sikl 5 marta, ichki sikl 2 marta ishlasa, ichki tana jami necha marta bajariladi?", section='practice', difficulty='easy', options=[opt("10", True), opt("7", False), opt("5", False)], hint="Ko'paytma.", explanation="5 × 2 = 10."),
        code_task('l33_practice_medium', "Medium: sonli uchburchak", r"""
Foydalanuvchi `n` kiritadi. Quyidagi shaklni chizing (`n = 4`):

```
1
12
123
1234
```
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "1\n12\n123\n1234", "n=4", stdin="4\n"), T('output_equals', "1", "n=1", stdin="1\n"), T('output_equals', "1\n12\n123", "n=3", stdin="3\n", hidden=True)], hint="Ichki siklda `print(j, end=\"\")`.", full_solution='n = int(input())\nfor i in range(1, n + 1):\n    for j in range(1, i + 1):\n        print(j, end="")\n    print()\n', explanation="Ichki sikl chegarasi tashqi sikl qiymatiga bog'liq."),
        code_task('l33_practice_hard', "Hard: ko'paytirish jadvali (to'liq)", r"""
Foydalanuvchi `n` kiritadi. `n × n` ko'paytirish jadvalini chizing: har bir son orasida **bitta probel**, qator oxirida probel bo'lmasin (`n = 3`):

```
1 2 3
2 4 6
3 6 9
```
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "1 2 3\n2 4 6\n3 6 9", "n=3", stdin="3\n"), T('output_equals', "1", "n=1", stdin="1\n"), T('output_equals', "1 2 3 4\n2 4 6 8\n3 6 9 12\n4 8 12 16", "n=4", stdin="4\n", hidden=True)], hint="Qator oxirida probel chiqmasligi uchun: ichki siklda birinchi ustun bo'lmasa oldin probel chiqaring.", partial_solution='n = int(input())\nfor q in range(1, n + 1):\n    for u in range(1, n + 1):\n        if u > 1:\n            print(" ", end="")\n        # ko\'paytmani chiqaring\n    print()\n', full_solution='n = int(input())\nfor q in range(1, n + 1):\n    for u in range(1, n + 1):\n        if u > 1:\n            print(" ", end="")\n        print(q * u, end="")\n    print()\n', explanation="Ajratgichni elementlar orasiga qo'yish uchun birinchisidan boshqa hammasidan oldin chiqardik."),
    ])

LESSONS = [LESSON_27, LESSON_28, LESSON_29, LESSON_30, LESSON_31, LESSON_32, LESSON_33]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("5-modul yakuniy nazorati: Sikllar", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **son topish o'yini**.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m5_a_t1', "range()", "`range(2, 8)` nechta son beradi?", section='assessment', points=2, options=[opt("6 ta (2..7)", True), opt("7 ta", False), opt("8 ta", False)], explanation="8 kirmaydi: 2,3,4,5,6,7."),
    single('m5_a_t2', "for yoki while", "Takrorlashlar soni oldindan noma'lum bo'lsa, odatda qaysi sikl qulay?", section='assessment', points=2, options=[opt("`while`", True), opt("`for` + `range`", False), opt("Farqi yo'q", False)], explanation="Shart bo'yicha takrorlash — `while`."),
    single('m5_a_t3', "break", "`break` qayerda ishlatiladi?", section='assessment', points=2, options=[opt("Sikl ichida", True), opt("Faqat `if` ichida", False), opt("Funksiyadan tashqarida", False)], explanation="Siklni to'xtatish uchun."),
    single('m5_a_t4', "continue", "`continue` nima qiladi?", section='assessment', points=2, options=[opt("Joriy iteratsiyani o'tkazib yuboradi", True), opt("Siklni to'xtatadi", False), opt("Dasturni to'xtatadi", False)], explanation="Keyingi iteratsiyaga o'tadi."),
    multiple('m5_a_t5', "Cheksiz sikl", "Qaysi siklar cheksiz ishlaydi?", section='assessment', points=2, options=[opt("`while True:` (break siz)", True), opt("`n = 1` / `while n > 0: n = n + 1`", True), opt("`for i in range(10):`", False), opt("`n = 5` / `while n > 0: n = n - 1`", False)], explanation="Shart hech qachon yolg'on bo'lmasa — cheksiz."),
    predict('m5_a_p1', "Natija (1)", "Dastur nima chiqaradi? (Bir qatorda, probel bilan.)", section='assessment', points=2, code='for i in range(10, 0, -3):\n    print(i, end=" ")\n', answer="10 7 4 1", explanation="10, 7, 4, 1."),
    predict('m5_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='n = 0\nfor i in range(1, 6):\n    if i % 2 == 0:\n        continue\n    n = n + i\nprint(n)\n', answer="9", explanation="1 + 3 + 5."),
    predict('m5_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='for i in range(3):\n    for j in range(i + 1):\n        print(i, end="")\nprint()\n', answer="011222", explanation="i=0: bir marta `0`; i=1: ikki marta `1`; i=2: uch marta `2` → `011222`."),
    fix_task('m5_a_f1', "Xatoni tuzating (1)", "Dastur 1 dan 5 gacha sonlarni chiqarishi kerak (bir qatorda, probel bilan), lekin 5 chiqmayapti.", section='assessment', points=4, starter_code='for i in range(1, 5):\n    print(i, end=" ")\n', tests=[T('output_equals', "1 2 3 4 5", "1 2 3 4 5")], hint="Oxirgi son kirmaydi.", full_solution='for i in range(1, 6):\n    print(i, end=" ")\n', explanation="`range(1, 6)` kerak."),
    fix_task('m5_a_f2', "Xatoni tuzating (2)", "Dastur 3 marta `Salom` chiqarib to'xtashi kerak, lekin cheksiz ishlaydi.", section='assessment', points=4, starter_code='n = 0\nwhile n < 3:\n    print("Salom")\n', tests=[T('output_equals', "Salom\nSalom\nSalom", "3 marta")], hint="Sanagich yangilanmayapti.", full_solution='n = 0\nwhile n < 3:\n    print("Salom")\n    n = n + 1\n', explanation="`n = n + 1` yetishmagan."),
    code_task('m5_a_project', "Mini-loyiha: Son topish o'yini", r"""
**Yashirin son — 37.** Foydalanuvchi uni topishga **ko'pi bilan 5 ta urinish** qiladi. Har urinishda son kiritadi (`int(input())`):

- kiritilgan son yashirindan **kichik** bo'lsa — `Kichik`,
- **katta** bo'lsa — `Katta`,
- **teng** bo'lsa — `Topdingiz! Urinishlar: N` (N — nechinchi urinishda topilgani) va o'yin tugaydi.
- 5 ta urinishda topilmasa — `Yutqazdingiz! Son: 37`.

Misol: `50`, `20`, `37` → `Katta`, `Kichik`, `Topdingiz! Urinishlar: 3`.
""", section='project', points=15, difficulty='medium', unlock=3, starter_code='# Son topish o\'yini\nyashirin = 37\n',
        expected_output_example="Katta\nKichik\nTopdingiz! Urinishlar: 3",
        tests=[T('output_equals', "Katta\nKichik\nTopdingiz! Urinishlar: 3", "50, 20, 37", stdin="50\n20\n37\n"), T('output_equals', "Topdingiz! Urinishlar: 1", "birinchi urinishda", stdin="37\n"),
               T('output_equals', "Kichik\nKichik\nKichik\nKichik\nKichik\nYutqazdingiz! Son: 37", "5 ta xato", stdin="1\n2\n3\n4\n5\n"), T('output_equals', "Katta\nKatta\nKatta\nKatta\nTopdingiz! Urinishlar: 5", "5-urinishda", stdin="99\n98\n97\n96\n37\n", hidden=True),
               T('output_equals', "Kichik\nTopdingiz! Urinishlar: 2", "2-urinishda; keyingi kiritish ishlatilmaydi", stdin="10\n37\n99\n99\n", hidden=True), T('code_regex', r"while|for", "Sikl ishlatilgan")],
        hint="1) `urinish = 0`; `while urinish < 5:` ichida son so'rang va `urinish` ni oshiring. 2) To'g'ri topilsa — natijani chiqarib, `break`. 3) Yutqazish xabarini faqat topilmagan holatda chiqarish uchun `topildi = False` belgisidan foydalaning.",
        partial_solution='yashirin = 37\nurinish = 0\ntopildi = False\nwhile urinish < 5:\n    son = int(input())\n    urinish = urinish + 1\n    if son == yashirin:\n        print(f"Topdingiz! Urinishlar: {urinish}")\n        topildi = True\n        break\n    # Katta / Kichik ni yozing\nif not topildi:\n    print("Yutqazdingiz! Son: 37")\n',
        full_solution='yashirin = 37\nurinish = 0\ntopildi = False\nwhile urinish < 5:\n    son = int(input())\n    urinish = urinish + 1\n    if son == yashirin:\n        print(f"Topdingiz! Urinishlar: {urinish}")\n        topildi = True\n        break\n    elif son < yashirin:\n        print("Kichik")\n    else:\n        print("Katta")\nif not topildi:\n    print("Yutqazdingiz! Son: 37")\n',
        explanation="Loyiha while, break, if/elif/else, sanagich va belgi (flag) ni birlashtiradi."),
])

# ==============================================================================
# 2-TAKRORLASH (REVIEW 2): 1–5 modullar aralash
# ==============================================================================
REVIEW_2 = module_assessment("2-takrorlash (Review 2): 4- va 5-modullar (+ oldingilar)", r"""
Shartlar va sikllar mavzulari, shuningdek **o'zgaruvchilar, turlar va matnlar** aralash holda takrorlanadi.
Savollar atayin aralashtirilgan (*spaced repetition*). O'tish — **70%**; qayta urinish cheksiz.
""", [
    single('r2_t1', "Shart (4-modul)", "`if x = 5:` da qanday xato bor?", section='assessment', points=2, options=[opt("Tekshirish uchun `==` kerak", True), opt("`:` ortiqcha", False), opt("Xato yo'q", False)], explanation="`=` — saqlash, `==` — tekshirish."),
    single('r2_t2', "Matn (3-modul)", "`\"Python\"[1:4]` nima beradi?", section='assessment', points=2, options=[opt("`yth`", True), opt("`Pyt`", False), opt("`ytho`", False)], explanation="1, 2, 3-indekslar."),
    single('r2_t3', "Sikl (5-modul)", "`range(1, 10, 3)` qanday sonlarni beradi?", section='assessment', points=2, options=[opt("1, 4, 7", True), opt("1, 4, 7, 10", False), opt("3, 6, 9", False)], explanation="Qadam 3, 10 kirmaydi."),
    single('r2_t4', "Tur (2-modul)", "`input()` dan olingan qiymatni son sifatida ishlatish uchun nima kerak?", section='assessment', points=2, options=[opt("`int()` yoki `float()`", True), opt("`str()`", False), opt("Hech narsa", False)], explanation="`input()` doim matn qaytaradi."),
    multiple('r2_t5', "Mantiqiy ifodalar", "Qaysi ifodalar `True` beradi (`x = 6`)?", section='assessment', points=2, options=[opt("`x > 3 and x % 2 == 0`", True), opt("`not x == 6`", False), opt("`x < 3 or x == 6`", True), opt("`x != 6`", False)], explanation="Har bir ifodani qadamma-qadam baholang."),
    predict('r2_p1', "Aralash natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='s = "banan"\nn = 0\nfor h in s:\n    if h == "a":\n        n = n + 1\nprint(f"{s.upper()}: {n}")\n', answer="BANAN: 2", explanation="`banan` so'zida 2 ta `a` bor."),
    predict('r2_p2', "Aralash natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='j = 0\nfor i in range(1, 10):\n    if i % 3 == 0:\n        break\n    j = j + i\nprint(j)\n', answer="3", explanation="i=1, 2 qo'shiladi; i=3 da break: 3."),
    predict('r2_p3', "Aralash natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='x = 15\nif x > 10 and x % 2 == 0:\n    print("A")\nelif x > 10:\n    print("B")\nelse:\n    print("C")\nprint(len(str(x)))\n', answer="B\n2", explanation="`x` toq: `elif` ishlaydi; `str(15)` — 2 belgi."),
    fix_task('r2_f1', "Tuzating: sikl", "Dastur 5 dan 1 gacha sanashi kerak (`5 4 3 2 1`, probel bilan), lekin hech narsa chiqarmayapti.", section='assessment', points=4, starter_code='for i in range(5, 1):\n    print(i, end=" ")\n', tests=[T('output_equals', "5 4 3 2 1", "5 4 3 2 1")], hint="Qadam manfiy bo'lishi kerak.", full_solution='for i in range(5, 0, -1):\n    print(i, end=" ")\n', explanation="Teskari sanash uchun qadam `-1` va tugash `0`."),
    fix_task('r2_f2', "Tuzating: shart", "Dastur kiritilgan son juft bo'lsa `Juft`, aks holda `Toq` chiqarishi kerak, lekin ikkalasida ham `Juft` chiqaryapti.", section='assessment', points=4, starter_code='n = int(input())\nif n % 2 == 1:\n    print("Juft")\nelse:\n    print("Toq")\n', tests=[T('output_equals', "Juft", "4", stdin="4\n"), T('output_equals', "Toq", "7", stdin="7\n")], hint="Shart teskari.", full_solution='n = int(input())\nif n % 2 == 0:\n    print("Juft")\nelse:\n    print("Toq")\n', explanation="Juft son uchun qoldiq 0."),
    code_task('r2_c1', "Amaliy: FizzBuzz (qisqa)", r"""
1 dan 15 gacha sonlarni har birini alohida qatorda chiqaring, lekin: **3 ga bo'linsa `Fizz`**, **5 ga bo'linsa `Buzz`**, **ikkalasiga bo'linsa `FizzBuzz`** chiqaring.
""", section='assessment', points=10, difficulty='hard', tests=[T('output_equals', "\n".join("FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i) for i in range(1, 16)), "1..15")],
              hint="Avval 15 ga bo'linishini tekshiring.", partial_solution='for i in range(1, 16):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    # qolgan holatlarni yozing\n', full_solution='for i in range(1, 16):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    elif i % 3 == 0:\n        print("Fizz")\n    elif i % 5 == 0:\n        print("Buzz")\n    else:\n        print(i)\n', explanation="Sikl + elif zanjiri; eng maxsus shart birinchi."),
    code_task('r2_c2', "Amaliy: so'zdagi bosh harflar", "Foydalanuvchi gap kiritadi. Dastur gapdagi **bosh (katta) harflar sonini** chiqarsin (`h.upper() == h` va `h != ' '` emas, balki `h.isupper()` ishlatish mumkin). `Men Python Yaxshi Ko'raman` → `4`.", section='assessment', points=8, difficulty='medium',
              tests=[T('output_equals', "4", "4 ta bosh harf", stdin="Men Python Yaxshi Ko'raman\n"), T('output_equals', "0", "yo'q", stdin="salom dunyo\n"), T('output_equals', "5", "BOBUR", stdin="BOBUR\n", hidden=True)],
              hint="`isupper()` — harf katta bo'lsa `True` qaytaradi (`\"A\".isupper()`).", full_solution='gap = input()\nn = 0\nfor h in gap:\n    if h.isupper():\n        n = n + 1\nprint(n)\n', explanation="Matn metodi + sikl + sanagich."),
    code_task('r2_c3', "Amaliy: parol urinishlari", "Foydalanuvchi parol kiritadi (`python` — to'g'ri). Ko'pi bilan **3 ta urinish**. To'g'ri bo'lsa — `Xush kelibsiz`, 3 ta xato — `Hisob bloklandi`.", section='assessment', points=10, difficulty='hard',
              tests=[T('output_equals', "Xush kelibsiz", "1-urinish", stdin="python\n"), T('output_equals', "Xush kelibsiz", "3-urinish", stdin="a\nb\npython\n"), T('output_equals', "Hisob bloklandi", "3 ta xato", stdin="a\nb\nc\n"), T('output_equals', "Xush kelibsiz", "2-urinish", stdin="x\npython\nzzz\n", hidden=True)],
              hint="`for urinish in range(3)` + `break` + belgi yoki `for ... else`siz oddiy `topildi`.", partial_solution='topildi = False\nfor urinish in range(3):\n    p = input()\n    if p == "python":\n        topildi = True\n        break\n# natijani chiqaring\n', full_solution='topildi = False\nfor urinish in range(3):\n    p = input()\n    if p == "python":\n        topildi = True\n        break\nif topildi:\n    print("Xush kelibsiz")\nelse:\n    print("Hisob bloklandi")\n', explanation="Sikl + break + belgi."),
])

REVIEWS = [REVIEW_2]
