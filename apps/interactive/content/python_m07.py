"""Python — 0 dan boshlash · 7-modul: Tuple, Set va Dictionary (42–49-darslar) va 3-takrorlash (Review 3)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 7,
    'title': "Tuple, Set va Dictionary",
    'description': "Ma'lumot to'plamlarining yana uch turi: o'zgarmas tuple, takrorlanmas set va kalit–qiymat juftlari bilan ishlovchi dictionary.",
}

# ==============================================================================
# 42-DARS
# ==============================================================================
LESSON_42 = L(42, "Tuple nima?", 11,
    "Tuple (kortej) nima ekanini, listdan farqini va qachon ishlatilishini bilish; tuple yaratish va elementlarini olish.",
    ["Tuple", "Oddiy qavs ()", "O'zgarmaslik (immutable)", "Bir elementli tuple", "Tuple unpacking"],
    [
        text(r"""
Pasportdagi tug'ilgan sana, nuqtaning koordinatalari (x, y), haftaning kunlari — bular **o'zgarmasligi kerak** bo'lgan ma'lumotlar. Ularni listda saqlasak, tasodifan o'zgartirib yuborishimiz mumkin. Buning uchun **tuple** (o'qilishi: «tapl», o'zbekcha — *kortej*) bor.
""", title="O'zgarmas ma'lumot"),
        text(r"""
Tuple — list kabi tartibli to'plam, lekin **o'zgartirib bo'lmaydi** (*immutable*). U **oddiy qavs** bilan yoziladi:

```python
nuqta = (3, 7)
kunlar = ("dushanba", "seshanba", "chorshanba")
print(nuqta[0])        # 3 — indeks listdagidek
print(len(kunlar))     # 3
```

- `nuqta[0] = 5` → `TypeError` (o'zgartirib bo'lmaydi).
- **Bitta elementli tuple** — vergul shart: `(5,)`. `(5)` — oddiy son.
- **Ochish (unpacking):** `x, y = nuqta` — qiymatlar o'zgaruvchilarga taqsimlanadi.
""", title="Tuple xususiyatlari"),
        callout('analogy', r"""
Tuple — **muhrlangan konvert**: ichidagini o'qiy olasiz, lekin almashtirib bo'lmaydi. List esa — **ochiq quti**.
""", title="Hayotiy o'xshatish"),
        example(r'''
nuqta = (3, 7)
print(nuqta)
print(type(nuqta))
x, y = nuqta
print("x =", x, "y =", y)
''', title="Yaratish va ochish", body="`(3, 7)` — tuple. `x, y = nuqta` — qiymatlar bittadan o'zgaruvchilarga bo'lib berildi."),
        example(r'''
oylar = ("yanvar", "fevral", "mart")
print(oylar[-1])
bir = (5,)
print(type(bir), type((5)))
a, b = 10, 20
a, b = b, a
print(a, b)
''', title="Amaliy: bir elementli tuple va almashtirish", body="`(5,)` — tuple, `(5)` — `int`. `a, b = b, a` — ikki o'zgaruvchi qiymatini bir qatorda almashtirishning qulay usuli: `20 10`."),
        exercise('l42_inline_fix'),
        callout('warning', r"""
Tuple o'zgarmasligi uchun elementini almashtirib, `append` qilib yoki o'chirib bo'lmaydi. Kerak bo'lsa — yangi tuple yarating yoki `list(tuple)` bilan listga aylantiring.
""", title="Diqqat"),
        recap(["tuple — `( )`, o'zgarmas, tartibli", "bir elementli: `(5,)`", "`x, y = tuple` — ochish"], "tuple bilan qanday metodlar ishlaydi? Elementni qanday sanaymiz yoki qidiramiz?"),
    ],
    [
        fix_task('l42_inline_fix', "Tuple o'zgarmaydi", "Kod xato beryapti: tuple elementini almashtirib bo'lmaydi. Ikkinchi elementni 5 ga almashtiradigan qilib tuzating. Natija: `[1, 5, 3]`.", section='inline', points=2, starter_code='a = (1, 2, 3)\na[1] = 5\nprint(a)\n', tests=[T('output_equals', "[1, 5, 3]", "Natija: [1, 5, 3]")], hint="Elementni almashtirish uchun o'zgaruvchan tur kerak.", full_solution='a = [1, 2, 3]\na[1] = 5\nprint(a)\n', explanation="Tuple o'zgarmaydi — list ishlatdik."),
        predict('l42_quiz_1', "Indeks", "Dastur nima chiqaradi?", code='t = ("a", "b", "c")\nprint(t[1], t[-1])\n', answer="b c", hint="Listdagidek.", explanation="`b` va `c`."),
        single('l42_quiz_2', "Bir elementli", "Qaysi biri tuple?", options=[opt("`(7,)`", True), opt("`(7)`", False, "Bu oddiy son."), opt("`[7]`", False, "Bu list.")], hint="Vergul muhim.", explanation="`(7,)`."),
        predict('l42_quiz_3', "Ochish", "Dastur nima chiqaradi?", code='a, b, c = (1, 2, 3)\nprint(c, b, a)\n', answer="3 2 1", hint="Tartib bilan taqsimlanadi.", explanation="`a=1, b=2, c=3`."),
        code_task('l42_assignment', "Koordinatalar", r"""
Foydalanuvchi ikki son (`x` va `y`) kiritadi. Ularni `nuqta` tuple'iga joylab chiqaring, so'ng nuqtaning koordinata boshi (0, 0) dan **masofa kvadratini** (`x*x + y*y`) hisoblab, ikkinchi qatorda chiqaring. `3`, `4` → `(3, 4)` va `25`.
""", starter_code='', points=10, tests=[T('output_equals', "(3, 4)\n25", "3, 4", stdin="3\n4\n"), T('output_equals', "(0, 0)\n0", "0, 0", stdin="0\n0\n"), T('output_equals', "(-2, 5)\n29", "-2, 5", stdin="-2\n5\n", hidden=True), T('code_regex', r"\(\s*\w+\s*,\s*\w+\s*\)", "Tuple ishlatilgan")], hint="`nuqta = (x, y)`; keyin `a, b = nuqta`.", partial_solution='x = int(input())\ny = int(input())\nnuqta = (x, y)\nprint(nuqta)\n# nuqtani ochib masofa kvadratini chiqaring\n', full_solution='x = int(input())\ny = int(input())\nnuqta = (x, y)\nprint(nuqta)\na, b = nuqta\nprint(a * a + b * b)\n', explanation="Tuple yaratildi va ochildi."),
        single('l42_practice_easy', "Easy: farq", "Tuple va list orasidagi asosiy farq?", section='practice', difficulty='easy', options=[opt("Tuple o'zgarmaydi", True), opt("Tuple tezroq chiqadi", False), opt("List indeks qabul qilmaydi", False)], hint="Muhrlangan konvert.", explanation="Tuple o'zgarmas, list o'zgaruvchan."),
        code_task('l42_practice_medium', "Medium: qiymatlarni almashtirish", r"""
Foydalanuvchi `a` va `b` kiritadi (matn). Tuple unpacking bilan ularni almashtiring va `b a` tartibida emas, almashgan holda chiqaring: kiritish `salom`, `dunyo` → `dunyo salom`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "dunyo salom", "salom/dunyo", stdin="salom\ndunyo\n"), T('output_equals', "2 1", "1/2", stdin="1\n2\n"), T('code_contains', 'a, b = b, a', "`a, b = b, a` ishlatilgan")], hint="`a, b = b, a`.", full_solution='a = input()\nb = input()\na, b = b, a\nprint(a, b)\n', explanation="Vaqtincha o'zgaruvchisiz almashtirish."),
        code_task('l42_practice_hard', "Hard: min va max tuple", r"""
Foydalanuvchi 3 ta son kiritadi. `natija` tuple'ini `(eng_kichik, eng_katta)` shaklida yarating va chiqaring. `5 2 9` → `(2, 9)`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "(2, 9)", "5 2 9", stdin="5\n2\n9\n"), T('output_equals', "(-1, 7)", "7 -1 3", stdin="7\n-1\n3\n"), T('output_equals', "(4, 4)", "4 4 4", stdin="4\n4\n4\n", hidden=True)], hint="`min(a, b, c)` va `max(a, b, c)` — bir nechta argument bilan ishlaydi.", full_solution='a = int(input())\nb = int(input())\nc = int(input())\nnatija = (min(a, b, c), max(a, b, c))\nprint(natija)\n', explanation="Tuple — ikkita natijani birga qaytarishning qulay usuli."),
    ])

# ==============================================================================
# 43-DARS
# ==============================================================================
LESSON_43 = L(43, "Tuple elementlari va metodlari", 11,
    "Tuple elementlari bo'ylab yurish, count()/index() metodlari, tuple'larni qo'shish va list↔tuple aylantirish.",
    ["for bilan yurish", "count()", "index()", "tuple + tuple", "list() va tuple()"],
    [
        text(r"""
Tuple o'zgarmas bo'lsa ham, uning ichida **qidirish**, **sanash**, **sikl bilan yurish** mumkin. Faqat o'zgartiruvchi amallar (`append`, `remove`...) yo'q.
""", title="O'qish mumkin, o'zgartirish yo'q"),
        text(r"""
| Amal | Misol | Natija |
|---|---|---|
| uzunlik | `len((1, 2, 3))` | `3` |
| bor-yo'qligi | `2 in (1, 2, 3)` | `True` |
| sanash | `(1, 2, 1).count(1)` | `2` |
| o'rni | `(5, 6, 7).index(6)` | `1` |
| birlashtirish | `(1, 2) + (3,)` | `(1, 2, 3)` |
| takrorlash | `(0,) * 3` | `(0, 0, 0)` |
| turga aylantirish | `list((1, 2))`, `tuple([1, 2])` | `[1, 2]`, `(1, 2)` |

Tuple'ni «o'zgartirish» — uni **listga aylantirib**, o'zgartirib, yana `tuple()` ga qaytarish.
""", title="Tuple bilan nima qilish mumkin"),
        callout('analogy', r"""
Tuple o'zgartirishning «aylanma yo'li»: muhrlangan konvertni ochish (`list`), ichidagini almashtirish va yana muhrlash (`tuple`).
""", title="Hayotiy o'xshatish"),
        example(r'''
ranglar = ("qizil", "yashil", "qizil", "ko'k")
print(ranglar.count("qizil"))
print(ranglar.index("yashil"))
for r in ranglar:
    print(r)
''', title="Sanash, qidirish, yurish", body="`qizil` 2 marta; `yashil` — 1-indeksda; so'ng har bir rang alohida qatorda."),
        example(r'''
t = (1, 2, 3)
l = list(t)
l.append(4)
t = tuple(l)
print(t)
print((1, 2) + (3, 4))
''', title="Amaliy: tuple'ni «o'zgartirish»", body="`(1, 2, 3, 4)` va `(1, 2, 3, 4)`. Aslida yangi tuple hosil bo'ldi — eskisi o'zgarmadi."),
        exercise('l43_inline_pred'),
        recap(["`count`, `index`, `in`, `len`", "`+` va `*` yangi tuple beradi", "`list()` / `tuple()` — aylantirish"], "listdan takrorlanmaydigan elementlarni qanday ajratib olamiz? Buning uchun yangi to'plam turi bor."),
    ],
    [
        predict('l43_inline_pred', "count va index", "Dastur nima chiqaradi?", section='inline', code='t = (4, 5, 4, 6)\nprint(t.count(4), t.index(6))\n', answer="2 3", points=2, hint="Ikki marta; 3-indeksda.", explanation="`count(4)` = 2; `index(6)` = 3."),
        predict('l43_quiz_1', "Birlashtirish", "Dastur nima chiqaradi?", code='print((1,) + (2, 3) * 2)\n', answer="(1, 2, 3, 2, 3)", hint="Avval `*`, keyin `+`.", explanation="`(2, 3) * 2` = `(2, 3, 2, 3)`."),
        single('l43_quiz_2', "append", "`t = (1, 2); t.append(3)` nima beradi?", options=[opt("`AttributeError` — tuple'da `append` yo'q", True), opt("`(1, 2, 3)`", False), opt("Hech narsa", False)], hint="Tuple o'zgarmas.", explanation="Tuple'da o'zgartiruvchi metodlar yo'q."),
        predict('l43_quiz_3', "Aylantirish", "Dastur nima chiqaradi?", code='x = tuple([3, 1, 2])\nprint(x, len(x))\n', answer="(3, 1, 2) 3", hint="List → tuple.", explanation="Tartib saqlanadi."),
        code_task('l43_assignment', "Hafta kunlari", r"""
`kunlar = ("dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba", "yakshanba")` berilgan. Foydalanuvchi kun raqamini (1–7) kiritadi. Dastur kunning nomini chiqarsin. `1` → `dushanba`, `7` → `yakshanba`.
""", starter_code='kunlar = ("dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba", "yakshanba")\n', points=10, tests=[T('output_equals', "dushanba", "1", stdin="1\n"), T('output_equals', "yakshanba", "7", stdin="7\n"), T('output_equals', "payshanba", "4", stdin="4\n", hidden=True)], hint="Indeks 0 dan boshlanadi: `kunlar[raqam - 1]`.", partial_solution='kunlar = ("dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba", "yakshanba")'+'\nraqam = int(input())'+'\n# kun nomini chiqaring'+'\n', full_solution='kunlar = ("dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba", "yakshanba")\nraqam = int(input())\nprint(kunlar[raqam - 1])\n', explanation="Kun raqami 1 dan, indeks 0 dan."),
        single('l43_practice_easy', "Easy: tuple + tuple", "`(1,) + (2,)` natijasi?", section='practice', difficulty='easy', options=[opt("`(1, 2)`", True), opt("`(3,)`", False), opt("Xato", False)], hint="Birlashtirish.", explanation="Yangi tuple `(1, 2)`."),
        code_task('l43_practice_medium', "Medium: tuple'ga element qo'shish", r"""
`t = (10, 20, 30)` ga **40** ni qo'shing (listga aylantirib `append`, keyin qaytarib) va chiqaring: `(10, 20, 30, 40)`.
""", section='practice', difficulty='medium', points=5, starter_code='t = (10, 20, 30)\n', tests=[T('output_equals', "(10, 20, 30, 40)", "Natija"), T('code_contains', 'list(', "`list()` ishlatilgan"), T('code_contains', 'tuple(', "`tuple()` ishlatilgan")], hint="`t = tuple(list(t) + [40])` ham mumkin, lekin `append` ishlating.", full_solution='t = (10, 20, 30)\nl = list(t)\nl.append(40)\nt = tuple(l)\nprint(t)\n', explanation="Aylanma yo'l."),
        code_task('l43_practice_hard', "Hard: eng ko'p uchraydigan", r"""
`d = (3, 1, 3, 2, 1, 3)` tuple berilgan. Eng ko'p uchragan elementni va necha marta uchraganini chiqaring: `3 3`.
""", section='practice', difficulty='hard', points=5, starter_code='d = (3, 1, 3, 2, 1, 3)\n', tests=[T('output_equals', "3 3", "Natija")], hint="Har bir element uchun `count`.", full_solution='d = (3, 1, 3, 2, 1, 3)\neng = d[0]\nfor x in d:\n    if d.count(x) > d.count(eng):\n        eng = x\nprint(eng, d.count(eng))\n', explanation="`count` bilan eng ko'pini topdik."),
    ])

# ==============================================================================
# 44-DARS
# ==============================================================================
LESSON_44 = L(44, "Set nima va uning xususiyatlari", 12,
    "Set (to'plam) nima ekanini, takrorlanmasligini, tartibsizligini bilish; add(), remove(), discard() va listdan takrorlarni olib tashlash.",
    ["Set", "{ }", "Takrorlanmaydi", "Tartibsiz", "add / remove / discard", "set(list)"],
    [
        text(r"""
Sinfda kimlar kelganini bilmoqchisiz. Bir o'quvchi ikki marta ro'yxatga yozilgan bo'lsa-chi? Ro'yxatda **takrorlar bo'lmasligi** kerak. Buning uchun **set** (*to'plam*) bor — u har bir qiymatni **faqat bir marta** saqlaydi.
""", title="Takrorlarsiz to'plam"),
        text(r"""
```python
a = {1, 2, 3, 2, 1}
print(a)               # {1, 2, 3}  — takrorlar yo'qoldi
print(len(a))          # 3
print(2 in a)          # True  (qidirish juda tez)
```

Set xususiyatlari:
1. **Takrorlanmaydi** — bir xil qiymat bir marta.
2. **Tartibsiz** — indeks yo'q (`a[0]` — xato), chiqish tartibiga ishonmang.
3. Elementlari **o'zgarmas tur** bo'lishi kerak (son, matn, tuple — ha; list — yo'q).
4. **Bo'sh set:** `set()` — `{}` emas! (`{}` — bo'sh dictionary.)

Metodlar: `a.add(x)` — qo'shadi; `a.remove(x)` — o'chiradi (yo'q bo'lsa `KeyError`); `a.discard(x)` — o'chiradi (yo'q bo'lsa xato bermaydi).
""", title="Set xususiyatlari"),
        callout('analogy', r"""
Set — **mehmonlar ro'yxati**: kim bor-yo'qligi muhim, necha marta kelgani va tartibi emas.
""", title="Hayotiy o'xshatish"),
        example(r'''
sonlar = [3, 1, 3, 2, 1, 4]
noyob = set(sonlar)
print(len(sonlar), len(noyob))
print(sorted(noyob))
''', title="Listdan takrorlarni olib tashlash", body="List uzunligi 6, set — 4. Set tartibsiz bo'lgani uchun uni `sorted()` bilan tartiblab chiqardik: `[1, 2, 3, 4]`."),
        example(r'''
kelganlar = set()
kelganlar.add("Ali")
kelganlar.add("Vali")
kelganlar.add("Ali")
kelganlar.discard("Gulnora")
print(len(kelganlar), "Ali" in kelganlar)
''', title="Amaliy: davomat", body="`Ali` ikki marta qo'shilsa ham bir marta saqlandi: `2 True`. `discard` mavjud bo'lmagan elementda xato bermadi."),
        exercise('l44_inline_pred'),
        callout('warning', r"""
`{}` — bo'sh **dictionary**, bo'sh set emas! Bo'sh set uchun `set()` yozing.
""", title="Diqqat"),
        recap(["set — `{1, 2, 3}`, takrorlanmaydi, tartibsiz", "bo'sh set: `set()`", "`add`, `remove`, `discard`", "`set(list)` — takrorlarni olib tashlaydi"], "ikki to'plamni solishtirish — umumiy elementlar, farqlar — mumkinmi?"),
    ],
    [
        predict('l44_inline_pred', "Takrorlar", "Dastur nima chiqaradi?", section='inline', code='print(len({5, 5, 6, 6, 6}))\n', answer="2", points=2, hint="Noyob qiymatlar nechta?", explanation="`{5, 6}` — 2 ta."),
        single('l44_quiz_1', "Bo'sh set", "Bo'sh set qanday yaratiladi?", options=[opt("`set()`", True), opt("`{}`", False, "Bu bo'sh dictionary."), opt("`[]`", False, "Bu bo'sh list.")], hint="`{}` boshqa tur.", explanation="`set()`."),
        predict('l44_quiz_2', "Noyob sonlar", "Dastur nima chiqaradi?", code='print(sorted(set([4, 2, 4, 9, 2])))\n', answer="[2, 4, 9]", hint="Avval takrorlar olib tashlanadi, keyin tartiblanadi.", explanation="`{2, 4, 9}` → `[2, 4, 9]`."),
        single('l44_quiz_3', "Indeks", "`s = {1, 2, 3}`; `s[0]` nima beradi?", options=[opt("`TypeError` — set indeksni qabul qilmaydi", True), opt("`1`", False), opt("`None`", False)], hint="Tartibsiz.", explanation="Setda indeks yo'q."),
        code_task('l44_assignment', "Noyob so'zlar soni", r"""
Foydalanuvchi 5 ta so'z kiritadi. Dastur **nechta turli (noyob)** so'z kiritilganini chiqarsin. `a b a c b` → `3`.
""", starter_code='', points=10, tests=[T('output_equals', "3", "a b a c b", stdin="a\nb\na\nc\nb\n"), T('output_equals', "1", "hammasi bir xil", stdin="x\nx\nx\nx\nx\n"), T('output_equals', "5", "hammasi turli", stdin="a\nb\nc\nd\ne\n", hidden=True), T('code_contains', 'set', "`set` ishlatilgan")], hint="`soz = set()` va `add`, yoki listdan `set(...)`.", partial_solution='s = set()'+'\nfor i in range(5):'+'\n    s.add(input())'+'\n# noyob so\'zlar sonini chiqaring'+'\n', full_solution='s = set()\nfor i in range(5):\n    s.add(input())\nprint(len(s))\n', explanation="Set takrorlarni o'zi yo'qotadi."),
        single('l44_practice_easy', "Easy: tartib", "Set elementlari tartibi haqida to'g'ri gap?", section='practice', difficulty='easy', options=[opt("Kafolatlanmagan", True), opt("Doim o'sish tartibida", False), opt("Kiritilgan tartibda", False)], hint="Tartibsiz.", explanation="Set tartibsiz."),
        code_task('l44_practice_medium', "Medium: takrorlanuvchi harflar", r"""
Foydalanuvchi so'z kiritadi. Nechta **turli** harf borligini chiqaring. `banan` → `3` (b, a, n).
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "3", "banan", stdin="banan\n"), T('output_equals', "5", "kitob → k,i,t,o,b", stdin="kitob\n"), T('output_equals', "1", "aaaa", stdin="aaaa\n", hidden=True)], hint="`set(soz)` matn harflaridan set yasaydi.", full_solution='s = input()\nprint(len(set(s)))\n', explanation="`set(matn)` — noyob harflar."),
        code_task('l44_practice_hard', "Hard: birinchi takrorlangan", r"""
Foydalanuvchi 6 ta son kiritadi. Birinchi marta **ikkinchi marta uchragan** sonni chiqaring (hech qaysi takrorlanmasa — `Yo'q`). `3 1 4 1 5 3` → `1`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "1", "3 1 4 1 5 3", stdin="3\n1\n4\n1\n5\n3\n"), T('output_equals', "Yo'q", "takrorsiz", stdin="1\n2\n3\n4\n5\n6\n"), T('output_equals', "7", "7 oxirida", stdin="1\n2\n7\n3\n4\n7\n", hidden=True)], hint="Ko'rilganlar setini yuriting; son avval bor bo'lsa — topdingiz.", partial_solution='korilgan = set()\ntopildi = False\nfor i in range(6):\n    x = int(input())\n    # agar x ko\'rilganlarda bo\'lsa chiqaring\n    korilgan.add(x)\n', full_solution='korilgan = set()\ntopildi = False\nfor i in range(6):\n    x = int(input())\n    if x in korilgan and not topildi:\n        print(x)\n        topildi = True\n    korilgan.add(x)\nif not topildi:\n    print("Yo\'q")\n', explanation="`in` set uchun juda tez ishlaydi."),
    ])

# ==============================================================================
# 45-DARS
# ==============================================================================
LESSON_45 = L(45, "Set bilan birlashma, kesishma va ayirma", 12,
    "Setlar ustida birlashma (|), kesishma (&), ayirma (-) va simmetrik ayirma (^) amallarini bajarish.",
    ["Birlashma |", "Kesishma &", "Ayirma -", "Simmetrik ayirma ^", "issubset()"],
    [
        text(r"""
Ikki guruh: **Python** to'garagiga yozilganlar va **Ingliz tili** kursiga yozilganlar. Sizga kerak: kimlar **ikkalasiga** yozilgan? **Kamida bittasiga?** **Faqat Python'ga?** Bu — setlar ustidagi amallar.
""", title="Guruhlarni solishtirish"),
        text(r"""
| Amal | Belgi | Ma'nosi | `a={1,2,3}`, `b={2,3,4}` |
|---|---|---|---|
| Birlashma | `a \| b` | ikkalasidagi hamma element | `{1,2,3,4}` |
| Kesishma | `a & b` | umumiy elementlar | `{2,3}` |
| Ayirma | `a - b` | faqat `a` da bor | `{1}` |
| Simmetrik ayirma | `a ^ b` | faqat bittasida bor | `{1,4}` |

Qo'shimcha: `a.issubset(b)` — `a` butunlay `b` ichidami? Natijani `sorted()` bilan chiqarish qulay (tartibsiz bo'lgani uchun).
""", title="To'rt amal"),
        callout('analogy', r"""
Ikki aylana (Venn diagrammasi): **birlashma** — ikkala aylana, **kesishma** — ular ustma-ust tushgan joy, **ayirma** — birinchi aylananing «oy» shaklidagi qismi.
""", title="Hayotiy o'xshatish"),
        example(r'''
python = {"Ali", "Vali", "Gulnora"}
ingliz = {"Vali", "Gulnora", "Dilshod"}
print(sorted(python | ingliz))
print(sorted(python & ingliz))
print(sorted(python - ingliz))
print(sorted(python ^ ingliz))
''', title="To'rt amal", body="Birlashma: 4 kishi; kesishma: `['Gulnora', 'Vali']`; faqat Python: `['Ali']`; faqat bittasida: `['Ali', 'Dilshod']`."),
        example(r'''
kerak = {"non", "sut", "tuxum"}
bor = {"sut", "olma"}
sotib_olish = kerak - bor
print(sorted(sotib_olish))
print({"sut"}.issubset(bor))
''', title="Amaliy: nima sotib olish kerak", body="Kerakli mahsulotlardan uyda borlarini ayirdik: `['non', 'tuxum']`. `{\"sut\"}` — `bor` ning qism to'plami: `True`."),
        exercise('l45_inline_pred'),
        recap(["`|` birlashma, `&` kesishma, `-` ayirma, `^` simmetrik ayirma", "natijani `sorted()` bilan chiqaring", "`issubset()` — qism to'plam"], "ma'lumotni nom bilan saqlash — masalan, «ism: Ali, yosh: 17» — uchun qaysi tur qulay?"),
    ],
    [
        predict('l45_inline_pred', "Kesishma", "Dastur nima chiqaradi?", section='inline', code='print(sorted({1, 2, 3} & {2, 3, 4}))\n', answer="[2, 3]", points=2, hint="Umumiy elementlar.", explanation="2 va 3 ikkalasida ham bor."),
        predict('l45_quiz_1', "Ayirma", "Dastur nima chiqaradi?", code='print(sorted({1, 2, 3, 4} - {2, 4}))\n', answer="[1, 3]", hint="Birinchida bor, ikkinchida yo'q.", explanation="1 va 3."),
        predict('l45_quiz_2', "Birlashma", "Dastur nima chiqaradi?", code='print(len({1, 2} | {2, 3} | {3, 4}))\n', answer="4", hint="Noyob elementlar.", explanation="`{1, 2, 3, 4}`."),
        single('l45_quiz_3', "Simmetrik ayirma", "`a ^ b` qaysi elementlarni beradi?", options=[opt("Faqat bittasida bor elementlarni", True), opt("Umumiy elementlarni", False), opt("Hamma elementni", False)], hint="Kesishmaning teskarisi.", explanation="Faqat bittasida bor elementlar."),
        code_task('l45_assignment', "Umumiy do'stlar", r"""
Foydalanuvchi ikki do'stlar ro'yxatini kiritadi. Har birida: avval son `n`, keyin `n` ta ism. Dastur **umumiy do'stlar** sonini va ismlarini alifbo tartibida chiqarsin (soni, so'ng ismlar bir qatorda probel bilan). `2`: `Ali Vali`; `3`: `Vali Dilshod Ali` → `2` va `Ali Vali`.
""", starter_code='', points=10, tests=[T('output_equals', "2\nAli Vali", "umumiy 2", stdin="2\nAli\nVali\n3\nVali\nDilshod\nAli\n"), T('output_equals', "0\n", "umumiy yo'q", stdin="1\nA\n1\nB\n"), T('output_equals', "1\nB", "bitta", stdin="2\nA\nB\n1\nB\n", hidden=True)], hint="Ikki set yig'ing, `&` bilan kesishtiring, `sorted()` bilan tartiblang. Ismlarni probel bilan chiqarish uchun `print(*list)` ishlating (yulduzcha — elementlarni ochib beradi).", partial_solution='a = set()\nfor i in range(int(input())):\n    a.add(input())\nb = set()\nfor i in range(int(input())):\n    b.add(input())\numumiy = sorted(a & b)\nprint(len(umumiy))\n# ismlarni chiqaring\n', full_solution='a = set()\nfor i in range(int(input())):\n    a.add(input())\nb = set()\nfor i in range(int(input())):\n    b.add(input())\numumiy = sorted(a & b)\nprint(len(umumiy))\nprint(*umumiy)\n', explanation="`print(*royxat)` elementlarni probel bilan chiqaradi; bo'sh ro'yxatda bo'sh qator chiqadi."),
        single('l45_practice_easy', "Easy: & belgisi", "`&` qaysi amalni bildiradi?", section='practice', difficulty='easy', options=[opt("Kesishma", True), opt("Birlashma", False), opt("Ayirma", False)], hint="Va — umumiy.", explanation="`&` — kesishma."),
        code_task('l45_practice_medium', "Medium: faqat birinchisida", r"""
`a = {1, 2, 3, 4, 5}`, `b = {4, 5, 6}`. `a` da bor, `b` da yo'q elementlarni tartiblangan list sifatida chiqaring: `[1, 2, 3]`.
""", section='practice', difficulty='medium', points=5, starter_code='a = {1, 2, 3, 4, 5}\nb = {4, 5, 6}\n', tests=[T('output_equals', "[1, 2, 3]", "Natija"), T('code_contains', ' - ', "Ayirma ishlatilgan")], hint="`sorted(a - b)`.", full_solution='a = {1, 2, 3, 4, 5}\nb = {4, 5, 6}\nprint(sorted(a - b))\n', explanation="Ayirma + sorted."),
        code_task('l45_practice_hard', "Hard: kamida bitta yo'qlama", r"""
Ikki sinf o'quvchilari: `a = {"Ali", "Vali", "Gulnora"}`, `b = {"Vali", "Dilshod"}`. Quyidagilarni ketma-ket chiqaring (har biri `sorted()` list): birlashma, kesishma, faqat bittasida bor:

```
['Ali', 'Dilshod', 'Gulnora', 'Vali']
['Vali']
['Ali', 'Dilshod', 'Gulnora']
```
""", section='practice', difficulty='hard', points=5, starter_code='a = {"Ali", "Vali", "Gulnora"}\nb = {"Vali", "Dilshod"}\n', tests=[T('output_equals', "['Ali', 'Dilshod', 'Gulnora', 'Vali']\n['Vali']\n['Ali', 'Dilshod', 'Gulnora']", "Natija"), T('code_contains', '^', "`^` ishlatilgan")], hint="`|`, `&`, `^`.", full_solution='a = {"Ali", "Vali", "Gulnora"}\nb = {"Vali", "Dilshod"}\nprint(sorted(a | b))\nprint(sorted(a & b))\nprint(sorted(a ^ b))\n', explanation="Uchala amal birga."),
    ])

# ==============================================================================
# 46-DARS
# ==============================================================================
LESSON_46 = L(46, "Dictionary nima va uni yaratish", 12,
    "Dictionary (lug'at) — kalit–qiymat juftliklari ekanini tushunish, yaratish va kalit qoidalarini bilish.",
    ["Dictionary", "Kalit va qiymat", "{kalit: qiymat}", "Kalit noyob", "Bo'sh dict"],
    [
        text(r"""
Telefon kontaktlari: **«Ali»** → `+998901234567`. Siz raqamni **tartib raqami bo'yicha** emas, **ism bo'yicha** qidirasiz. Bunday «nom → qiymat» juftliklarini saqlash uchun **dictionary** (*lug'at*) bor.
""", title="Nom bo'yicha qidirish"),
        text(r"""
```python
talaba = {"ism": "Aziza", "yosh": 17, "shahar": "Toshkent"}
print(talaba)
print(len(talaba))      # 3 ta juftlik
print(type(talaba))     # <class 'dict'>
```

- **Figurali qavs** `{ }` ichida **`kalit: qiymat`** juftliklari, vergul bilan.
- **Kalit** — qiymatni topish uchun «yorliq»: **noyob** va **o'zgarmas** tur (odatda matn yoki son).
- **Qiymat** — istalgan tur (son, matn, list, hatto yana dict).
- Bo'sh dictionary: `{}` yoki `dict()`.
- Bir xil kalit ikki marta yozilsa, oxirgisi qoladi.
""", title="Dictionary tuzilishi"),
        callout('analogy', r"""
Dictionary — **lug'at kitobi**: so'z (kalit) bo'yicha izohini (qiymat) topasiz. Yoki **shkaf qutilari**: har bir qutining yorlig'i bor.
""", title="Hayotiy o'xshatish"),
        example(r'''
telefon = {"Ali": "901234567", "Vali": "931112233"}
print(telefon)
print(len(telefon))
''', title="Birinchi dictionary", body="Ikkita juftlik. Kalitlar — ismlar, qiymatlar — raqamlar. Natija `{'Ali': '901234567', 'Vali': '931112233'}` va `2`."),
        example(r'''
mahsulot = {
    "nom": "Non",
    "narx": 4500,
    "mavjud": True,
    "teglar": ["yangi", "issiq"],
}
print(mahsulot)
bosh = {}
print(bosh, len(bosh))
''', title="Amaliy: mahsulot kartochkasi", body="Qiymatlar turli xil: matn, son, bool va list. Ko'p qatorli yozuv o'qishni osonlashtiradi. `{}` — bo'sh dictionary."),
        exercise('l46_inline_pred'),
        callout('tip', r"""
Bir narsaning bir nechta xususiyatini saqlash kerak bo'lsa (talaba, mahsulot) — **dictionary**. Bir xil turdagi ko'p qiymat kerak bo'lsa — **list**.
""", title="Qachon nima?"),
        recap(["`{kalit: qiymat}`", "kalit noyob va o'zgarmas tur", "qiymat — istalgan tur", "bo'sh: `{}`"], "dictionary'dan kerakli qiymatni kalit bo'yicha qanday olamiz?"),
    ],
    [
        predict('l46_inline_pred', "Takroriy kalit", "Dastur nima chiqaradi?", section='inline', code='d = {"a": 1, "a": 2}\nprint(d)\n', answer="{'a': 2}", points=2, hint="Kalit noyob.", explanation="Oxirgi qiymat qoladi."),
        single('l46_quiz_1', "Dictionary belgisi", "Dictionary qaysi qavs bilan yaratiladi?", options=[opt("`{ }`", True), opt("`[ ]`", False), opt("`( )`", False)], hint="Figurali.", explanation="Figurali qavs va `kalit: qiymat`."),
        single('l46_quiz_2', "Kalit", "Qaysi biri dictionary kaliti **bo'la olmaydi**?", options=[opt("List `[1, 2]`", True), opt("Matn `\"a\"`", False), opt("Son `5`", False)], hint="Kalit o'zgarmas bo'lishi kerak.", explanation="List o'zgaruvchan — kalit bo'la olmaydi."),
        predict('l46_quiz_3', "len()", "Dastur nima chiqaradi?", code='d = {"x": 1, "y": 2, "z": 3}\nprint(len(d))\n', answer="3", hint="Juftliklar soni.", explanation="3 ta juftlik."),
        code_task('l46_assignment', "Mening kartochkam", r"""
`men` nomli dictionary yarating — kalitlari `ism`, `yosh`, `shahar` (qiymatlar ixtiyoriy). Dictionary'ni chiqaring va juftliklar sonini ikkinchi qatorda yozing: `3`.
""", starter_code='', points=10, tests=[T('output_regex', r"^\{.+\}\n3$", "Birinchi qator dict, ikkinchi — 3"), T('code_regex', r"(?m)^men\s*=\s*\{", "`men` dictionary yaratilgan"), T('code_regex', r"[\"']ism[\"']\s*:", "`ism` kaliti"), T('code_regex', r"[\"']yosh[\"']\s*:", "`yosh` kaliti"), T('code_regex', r"[\"']shahar[\"']\s*:", "`shahar` kaliti")], hint="`men = {\"ism\": \"...\", \"yosh\": 17, \"shahar\": \"...\"}`.", partial_solution='men = {"ism": "Aziza", "yosh": 17}\n# shahar kalitini qo\'shing; dict va len ni chiqaring\n', full_solution='men = {"ism": "Aziza", "yosh": 17, "shahar": "Toshkent"}\nprint(men)\nprint(len(men))\n', explanation="Uch juftlik."),
        single('l46_practice_easy', "Easy: kalit va qiymat", "`{\"a\": 1}` da `\"a\"` nima?", section='practice', difficulty='easy', options=[opt("Kalit", True), opt("Qiymat", False), opt("Indeks", False)], hint="Yorliq.", explanation="Kalit."),
        code_task('l46_practice_medium', "Medium: kitob kartochkasi", r"""
Foydalanuvchi kitob **nomi** va **narxi**ni (butun) kiritadi. `kitob` dictionary'ga `nom` va `narx` kalitlari bilan joylab chiqaring. `Alkimyogar`, `45000` → `{'nom': 'Alkimyogar', 'narx': 45000}`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "{'nom': 'Alkimyogar', 'narx': 45000}", "Alkimyogar/45000", stdin="Alkimyogar\n45000\n"), T('output_equals', "{'nom': 'X', 'narx': 1}", "X/1", stdin="X\n1\n")], hint="Narx — `int(input())`.", full_solution='nom = input()\nnarx = int(input())\nkitob = {"nom": nom, "narx": narx}\nprint(kitob)\n', explanation="Dictionary qiymatlari o'zgaruvchilardan olinadi."),
        code_task('l46_practice_hard', "Hard: ichma-ich dictionary", r"""
`maktab` dictionary yarating: `{"nom": "Maktab 5", "sinf": {"raqam": 9, "harf": "A"}}`. Ichki dictionary'ni emas, faqat **butun** `maktab` ni chiqaring: `{'nom': 'Maktab 5', 'sinf': {'raqam': 9, 'harf': 'A'}}`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "{'nom': 'Maktab 5', 'sinf': {'raqam': 9, 'harf': 'A'}}", "Natija"), T('code_regex', r"\{[^{}]*\{", "Ichma-ich dict")], hint="Qiymat sifatida yana `{ }` yozing.", full_solution='maktab = {"nom": "Maktab 5", "sinf": {"raqam": 9, "harf": "A"}}\nprint(maktab)\n', explanation="Qiymat dictionary ham bo'lishi mumkin."),
    ])

# ==============================================================================
# 47-DARS
# ==============================================================================
LESSON_47 = L(47, "Dictionary elementlarini olish va o'zgartirish", 12,
    "Kalit orqali qiymatni olish, get() bilan xavfsiz olish, yangi juftlik qo'shish, qiymatni o'zgartirish va o'chirish.",
    ["d[kalit]", "get()", "Qo'shish / o'zgartirish", "del / pop()", "KeyError", "in"],
    [
        text(r"""
Telefon daftarida «Ali» ni topasiz — **kalit** orqali. Yangi kontakt qo'shasiz, raqamini yangilaysiz, keraksizini o'chirasiz. Dictionary bilan ham xuddi shunday ishlaymiz.
""", title="Kalit orqali ishlash"),
        text(r"""
```python
d = {"ism": "Ali", "yosh": 17}
print(d["ism"])              # Ali  — olish
d["yosh"] = 18               # o'zgartirish
d["shahar"] = "Toshkent"     # yangi kalit — qo'shish
print(d.get("telefon"))      # None — yo'q bo'lsa xato bermaydi
print(d.get("telefon", "yo'q"))  # yo'q — standart qiymat bilan
del d["shahar"]              # o'chirish
print("ism" in d)            # True — kalit bormi?
```

- `d[kalit]` — mavjud bo'lmasa **`KeyError`**.
- `d.get(kalit)` — mavjud bo'lmasa `None` (yoki berilgan standart qiymat).
- Qiymat berilganda: kalit **bor** bo'lsa — o'zgaradi, **yo'q** bo'lsa — qo'shiladi.
""", title="Olish, qo'shish, o'chirish"),
        callout('analogy', r"""
`d[kalit]` — «Ali raqamini bering» (yo'q bo'lsa — g'azablanadi: `KeyError`). `d.get(kalit)` — «Ali bormi? Yo'q bo'lsa ham mayli» (xotirjam).
""", title="Hayotiy o'xshatish"),
        example(r'''
d = {"ism": "Ali", "yosh": 17}
print(d["ism"])
d["yosh"] = 18
d["shahar"] = "Toshkent"
print(d)
print(d.get("telefon", "yo'q"))
''', title="Olish va o'zgartirish", body="`Ali`; keyin `{'ism': 'Ali', 'yosh': 18, 'shahar': 'Toshkent'}`; `yo'q`."),
        example(r'''
narxlar = {"non": 4500, "sut": 12000}
nom = input("Mahsulot: ")
if nom in narxlar:
    print(nom, "narxi:", narxlar[nom])
else:
    print("Bunday mahsulot yo'q")
narxlar["non"] = narxlar["non"] + 500
print(narxlar["non"])
''', title="Amaliy: narxlar lug'ati", body="`in` bilan kalit borligini tekshirib, `KeyError` dan saqlandik. `non` kiritilsa: `non narxi: 4500` va `5000`."),
        exercise('l47_inline_fix'),
        callout('warning', r"""
`d[\"yo'q kalit\"]` — `KeyError`. Ishonchingiz komil bo'lmasa `get()` yoki `in` ishlating.
""", title="Diqqat"),
        recap(["`d[k]` olish, `d[k] = v` qo'shish/o'zgartirish", "`get(k, standart)` xavfsiz", "`del d[k]`, `k in d`"], "dictionary uchun boshqa foydali metodlar bormi? Hamma kalitlarni, hamma qiymatlarni olish mumkinmi?"),
    ],
    [
        fix_task('l47_inline_fix', "KeyError ni tuzating", "Kod xato beryapti. `yosh` kaliti yo'q bo'lsa `0` chiqishi kerak. Natija: `0`", section='inline', points=2, starter_code='d = {"ism": "Ali"}\nprint(d["yosh"])\n', tests=[T('output_equals', "0", "Natija: 0")], hint="Xato bermaydigan olish usuli.", full_solution='d = {"ism": "Ali"}\nprint(d.get("yosh", 0))\n', explanation="`get(kalit, standart)`."),
        predict('l47_quiz_1', "Qo'shish", "Dastur nima chiqaradi?", code='d = {"a": 1}\nd["b"] = 2\nd["a"] = 10\nprint(d)\n', answer="{'a': 10, 'b': 2}", hint="`a` o'zgaradi, `b` qo'shiladi.", explanation="Kalit bor — o'zgaradi; yo'q — qo'shiladi."),
        predict('l47_quiz_2', "get", "Dastur nima chiqaradi?", code='d = {"x": 5}\nprint(d.get("x"), d.get("y"), d.get("y", -1))\n', answer="5 None -1", hint="Yo'q kalit uchun `None` yoki standart.", explanation="Uch xil natija."),
        single('l47_quiz_3', "in nimani tekshiradi?", "`\"a\" in {\"a\": 1}` nimani tekshiradi?", options=[opt("Kalit borligini", True), opt("Qiymat borligini", False), opt("Indeksni", False)], hint="Dictionary'da `in` — kalit bo'yicha.", explanation="`in` kalitlarni tekshiradi."),
        code_task('l47_assignment', "Narx so'rash", r"""
`narxlar = {"non": 4500, "sut": 12000, "tuxum": 15000}` berilgan. Foydalanuvchi mahsulot nomini kiritadi. Bor bo'lsa — narxini, yo'q bo'lsa — `Topilmadi` chiqaring. `sut` → `12000`.
""", starter_code='narxlar = {"non": 4500, "sut": 12000, "tuxum": 15000}\n', points=10, tests=[T('output_equals', "12000", "sut", stdin="sut\n"), T('output_equals', "Topilmadi", "olma", stdin="olma\n"), T('output_equals', "4500", "non", stdin="non\n", hidden=True)], hint="`if nom in narxlar:`.", partial_solution='narxlar = {"non": 4500, "sut": 12000, "tuxum": 15000}\nnom = input()\nif nom in narxlar:\n    # narxini chiqaring\n    pass\nelse:\n    print("Topilmadi")\n', full_solution='narxlar = {"non": 4500, "sut": 12000, "tuxum": 15000}\nnom = input()\nif nom in narxlar:\n    print(narxlar[nom])\nelse:\n    print("Topilmadi")\n', explanation="Kalit mavjudligi tekshirildi."),
        single('l47_practice_easy', "Easy: o'chirish", "Dictionary'dan kalitni o'chirish uchun?", section='practice', difficulty='easy', options=[opt("`del d[kalit]`", True), opt("`d.remove(kalit)`", False), opt("`d.append(kalit)`", False)], hint="`del`.", explanation="`del d[kalit]` yoki `d.pop(kalit)`."),
        code_task('l47_practice_medium', "Medium: balansni yangilash", r"""
`hisob = {"ism": "Ali", "balans": 50000}`. Foydalanuvchi kiritgan summani balansga **qo'shing** va `hisob` ni chiqaring. `10000` → `{'ism': 'Ali', 'balans': 60000}`.
""", section='practice', difficulty='medium', points=5, starter_code='hisob = {"ism": "Ali", "balans": 50000}\n', tests=[T('output_equals', "{'ism': 'Ali', 'balans': 60000}", "10000", stdin="10000\n"), T('output_equals', "{'ism': 'Ali', 'balans': 50000}", "0", stdin="0\n")], hint="`hisob[\"balans\"] = hisob[\"balans\"] + summa`.", full_solution='hisob = {"ism": "Ali", "balans": 50000}\nsumma = int(input())\nhisob["balans"] = hisob["balans"] + summa\nprint(hisob)\n', explanation="Qiymatni eski qiymati asosida yangiladik."),
        code_task('l47_practice_hard', "Hard: harflar chastotasi", r"""
Foydalanuvchi so'z kiritadi. Har bir harf necha marta uchrashini dictionary'da sanang va chiqaring. `banan` → `{'b': 1, 'a': 2, 'n': 2}`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "{'b': 1, 'a': 2, 'n': 2}", "banan", stdin="banan\n"), T('output_equals', "{'a': 3}", "aaa", stdin="aaa\n"), T('output_equals', "{'k': 1, 'i': 1, 't': 1, 'o': 1, 'b': 1}", "kitob", stdin="kitob\n", hidden=True)], hint="`sanoq[h] = sanoq.get(h, 0) + 1`.", partial_solution='soz = input()\nsanoq = {}\nfor h in soz:\n    # sanoqni oshiring\n    pass\nprint(sanoq)\n', full_solution='soz = input()\nsanoq = {}\nfor h in soz:\n    sanoq[h] = sanoq.get(h, 0) + 1\nprint(sanoq)\n', explanation="`get(h, 0) + 1` — dictionary bilan sanash andozasi."),
    ])

# ==============================================================================
# 48-DARS
# ==============================================================================
LESSON_48 = L(48, "Dictionary metodlari", 12,
    "keys(), values(), items(), pop(), update() va clear() metodlarini ishlatish hamda dictionary bo'ylab sikl bilan yurish.",
    ["keys()", "values()", "items()", "update()", "pop()", "Sikl bilan yurish"],
    [
        text(r"""
Lug'atdagi **hamma so'zlarni** ko'rib chiqish yoki **hamma izohlarni** yig'ish kerak bo'lsa-chi? Buning uchun dictionary metodlari bor.
""", title="Hamma narsani ko'rib chiqish"),
        text(r"""
| Metod | Nima beradi |
|---|---|
| `d.keys()` | barcha kalitlar |
| `d.values()` | barcha qiymatlar |
| `d.items()` | (kalit, qiymat) juftliklari |
| `d.pop(k)` | kalitni o'chirib, qiymatini qaytaradi |
| `d.update(boshqa)` | boshqa dictionary'ni qo'shadi/yangilaydi |
| `d.clear()` | hammasini o'chiradi |

```python
d = {"a": 1, "b": 2}
for k in d:                 # kalitlar bo'ylab
    print(k)
for k, v in d.items():      # juftliklar bo'ylab
    print(k, v)
print(sum(d.values()))      # 3
print(list(d.keys()))       # ['a', 'b']
```
""", title="Asosiy metodlar"),
        callout('analogy', r"""
`keys()` — kitobning **mundarijasi**, `values()` — barcha **izohlar**, `items()` — **so'z + izoh** juftliklari.
""", title="Hayotiy o'xshatish"),
        example(r'''
baholar = {"matematika": 5, "fizika": 4, "tarix": 5}
for fan, ball in baholar.items():
    print(f"{fan}: {ball}")
print("Yig'indi:", sum(baholar.values()))
''', title="items() bilan yurish", body="Har fan va bahosi chiqadi; qiymatlar yig'indisi `14`."),
        example(r'''
d = {"ism": "Ali"}
d.update({"yosh": 17, "ism": "Vali"})
print(d)
yosh = d.pop("yosh")
print(yosh, d)
print(list(d.keys()), list(d.values()))
''', title="Amaliy: update va pop", body="`update` yangi kalit qo'shdi va `ism` ni almashtirdi: `{'ism': 'Vali', 'yosh': 17}`. `pop` `yosh` ni o'chirib, `17` ni qaytardi."),
        exercise('l48_inline_pred'),
        callout('tip', r"""
`keys()` va `values()` natijasini ko'pincha `list()` ga o'rab ishlatamiz: `list(d.keys())`.
"""),
        recap(["`keys()`, `values()`, `items()`", "`for k, v in d.items():`", "`update()`, `pop()`, `clear()`"], "dictionary va list birga ishlatilsa-chi? Masalan, ko'p talabaning ma'lumotlari uchun?"),
    ],
    [
        predict('l48_inline_pred', "values()", "Dastur nima chiqaradi?", section='inline', code='d = {"a": 3, "b": 4}\nprint(sum(d.values()))\n', answer="7", points=2, hint="Qiymatlar yig'indisi.", explanation="3 + 4."),
        predict('l48_quiz_1', "keys()", "Dastur nima chiqaradi?", code='d = {"x": 1, "y": 2}\nprint(list(d.keys()))\n', answer="['x', 'y']", hint="Kalitlar ro'yxati.", explanation="Kalitlar kiritilgan tartibda."),
        predict('l48_quiz_2', "items()", "Dastur nima chiqaradi?", code='d = {"a": 1}\nfor k, v in d.items():\n    print(k, "->", v)\n', answer="a -> 1", hint="Kalit va qiymat.", explanation="Juftlik ochildi."),
        predict('l48_quiz_3', "update()", "Dastur nima chiqaradi?", code='d = {"a": 1}\nd.update({"a": 5, "b": 2})\nprint(d)\n', answer="{'a': 5, 'b': 2}", hint="Mavjud kalit yangilanadi.", explanation="`a` almashdi, `b` qo'shildi."),
        code_task('l48_assignment', "O'rtacha baho", r"""
`baholar = {"matematika": 5, "fizika": 4, "tarix": 3, "ona tili": 5}` berilgan. O'rtacha bahoni 2 xonali kasr bilan chiqaring: `4.25`.
""", starter_code='baholar = {"matematika": 5, "fizika": 4, "tarix": 3, "ona tili": 5}\n', points=10, tests=[T('output_equals', "4.25", "Natija"), T('code_contains', 'values', "`values()` ishlatilgan")], hint="`sum(baholar.values()) / len(baholar)`.", partial_solution='baholar = {"matematika": 5, "fizika": 4, "tarix": 3, "ona tili": 5}'+'\nyigindi = sum(baholar.values())'+'\n# o\'rtachani hisoblab, round bilan chiqaring'+'\n', full_solution='baholar = {"matematika": 5, "fizika": 4, "tarix": 3, "ona tili": 5}\nprint(round(sum(baholar.values()) / len(baholar), 2))\n', explanation="Yig'indi / soni."),
        single('l48_practice_easy', "Easy: items()", "`items()` nima beradi?", section='practice', difficulty='easy', options=[opt("(kalit, qiymat) juftliklarini", True), opt("Faqat kalitlarni", False), opt("Faqat qiymatlarni", False)], hint="Ikkalasi.", explanation="Juftliklar."),
        code_task('l48_practice_medium', "Medium: eng yuqori baho", r"""
`baholar = {"matematika": 5, "fizika": 4, "kimyo": 5}` da eng yuqori bahoni chiqaring: `5`.
""", section='practice', difficulty='medium', points=5, starter_code='baholar = {"matematika": 5, "fizika": 4, "kimyo": 5}\n', tests=[T('output_equals', "5", "Natija")], hint="`max(baholar.values())`.", full_solution='baholar = {"matematika": 5, "fizika": 4, "kimyo": 5}\nprint(max(baholar.values()))\n', explanation="`max` + `values()`."),
        code_task('l48_practice_hard', "Hard: kalit va qiymatni almashtirish", r"""
`d = {"a": 1, "b": 2, "c": 3}` ning kalit va qiymatlarini almashtirib yangi dictionary yarating va chiqaring: `{1: 'a', 2: 'b', 3: 'c'}`.
""", section='practice', difficulty='hard', points=5, starter_code='d = {"a": 1, "b": 2, "c": 3}\n', tests=[T('output_equals', "{1: 'a', 2: 'b', 3: 'c'}", "Natija")], hint="`yangi = {}`; `for k, v in d.items(): yangi[v] = k`.", full_solution='d = {"a": 1, "b": 2, "c": 3}\nyangi = {}\nfor k, v in d.items():\n    yangi[v] = k\nprint(yangi)\n', explanation="Siklda yangi juftlik qo'shdik."),
    ])

# ==============================================================================
# 49-DARS
# ==============================================================================
LESSON_49 = L(49, "List va Dictionary bilan birgalikda ishlash", 14,
    "Dictionary'lardan iborat list (jadval) yaratish, uni sikl bilan qayta ishlash va dictionary ichida list saqlash.",
    ["List of dict", "Dict ichida list", "Sikl bilan qayta ishlash", "Qidirish va filtrlash"],
    [
        text(r"""
Bitta talaba — bitta **dictionary** (ism, yosh, ball). Sinfdagi hamma talabalar — shunday dictionary'lardan iborat **list**. Bu — haqiqiy ma'lumotlar bazalari va veb-ilovalarning asosiy ko'rinishi.
""", title="Jadval kabi ma'lumot"),
        text(r"""
```python
talabalar = [
    {"ism": "Ali", "ball": 85},
    {"ism": "Vali", "ball": 72},
]
talabalar.append({"ism": "Gulnora", "ball": 95})

for t in talabalar:
    print(t["ism"], t["ball"])
print(talabalar[0]["ism"])     # Ali
```

Teskarisi ham mumkin — dictionary ichida list:

```python
guruh = {"nom": "Python", "azolar": ["Ali", "Vali"]}
guruh["azolar"].append("Gulnora")
```

Andoza: **sikl + shart + hisoblash** — masalan, ballari 80 dan yuqori talabalarni topish.
""", title="List ichida dictionary"),
        callout('analogy', r"""
`talabalar` — **jurnal**: har bir qatori — bitta talabaning kartochkasi (dictionary); jurnalning o'zi — qatorlar ro'yxati (list).
""", title="Hayotiy o'xshatish"),
        example(r'''
talabalar = [
    {"ism": "Ali", "ball": 85},
    {"ism": "Vali", "ball": 72},
    {"ism": "Gulnora", "ball": 95},
]
jami = 0
for t in talabalar:
    jami = jami + t["ball"]
print("O'rtacha:", round(jami / len(talabalar), 1))
''', title="O'rtacha ball", body="`t` har safar bitta dictionary: `t[\"ball\"]` bilan ball olinadi. `(85 + 72 + 95) / 3 = 84.0`."),
        example(r'''
talabalar = [{"ism": "Ali", "ball": 85}, {"ism": "Vali", "ball": 72}, {"ism": "Gulnora", "ball": 95}]
a_lochilar = []
for t in talabalar:
    if t["ball"] >= 80:
        a_lochilar.append(t["ism"])
print(a_lochilar)
guruh = {"nom": "Python", "azolar": ["Ali"]}
guruh["azolar"].append("Vali")
print(guruh)
''', title="Amaliy: filtrlash va dict ichida list", body="80+ olganlar ismlari yangi listga yig'ildi: `['Ali', 'Gulnora']`. Dictionary ichidagi list ham `append` qilinadi."),
        exercise('l49_inline_pred'),
        callout('tip', r"""
Murakkab ma'lumotni chiqarishdan oldin bitta elementni `print` qilib, tuzilishini tekshiring: `print(talabalar[0])`.
"""),
        recap(["list ichida dictionary — jadval", "dictionary ichida list ham mumkin", "sikl + shart bilan qayta ishlanadi"], "modul loyihasida talabalar baholari jurnalini yaratamiz. Qanday buyruqlar kerak bo'ladi, deb o'ylaysiz?"),
    ],
    [
        predict('l49_inline_pred', "Ichma-ich indeks", "Dastur nima chiqaradi?", section='inline', code='a = [{"x": 1}, {"x": 2}]\nprint(a[1]["x"])\n', answer="2", points=2, hint="Avval list indeksi, keyin kalit.", explanation="`a[1]` = `{\"x\": 2}`."),
        predict('l49_quiz_1', "Yig'indi", "Dastur nima chiqaradi?", code='a = [{"n": 3}, {"n": 4}]\nj = 0\nfor d in a:\n    j = j + d["n"]\nprint(j)\n', answer="7", hint="Har dictionary'dan `n`.", explanation="3 + 4."),
        predict('l49_quiz_2', "Dict ichida list", "Dastur nima chiqaradi?", code='g = {"a": [1, 2]}\ng["a"].append(3)\nprint(g, len(g["a"]))\n', answer="{'a': [1, 2, 3]} 3", hint="Qiymat — list.", explanation="List `append` qilindi."),
        single('l49_quiz_3', "To'g'ri murojaat", "`t = [{\"ism\": \"Ali\"}]` dan `Ali` ni olish?", options=[opt("`t[0][\"ism\"]`", True), opt("`t[\"ism\"][0]`", False), opt("`t[\"ism\"]`", False)], hint="Avval list, keyin dictionary.", explanation="`t[0]` — dictionary, `[\"ism\"]` — kalit."),
        code_task('l49_assignment', "Eng yaxshi talaba", r"""
`talabalar = [{"ism": "Ali", "ball": 85}, {"ism": "Vali", "ball": 72}, {"ism": "Gulnora", "ball": 95}]` berilgan. Eng yuqori ball olgan talabaning ismini va ballini chiqaring: `Gulnora 95`.
""", starter_code='talabalar = [{"ism": "Ali", "ball": 85}, {"ism": "Vali", "ball": 72}, {"ism": "Gulnora", "ball": 95}]\n', points=10, tests=[T('output_equals', "Gulnora 95", "Natija"), T('code_contains', 'for ', "`for` ishlatilgan")], hint="`eng = talabalar[0]` dan boshlang; siklda `t[\"ball\"] > eng[\"ball\"]`.", partial_solution='talabalar = [{"ism": "Ali", "ball": 85}, {"ism": "Vali", "ball": 72}, {"ism": "Gulnora", "ball": 95}]\neng = talabalar[0]\nfor t in talabalar:\n    # eng yuqorisini almashtiring\n    pass\nprint(eng["ism"], eng["ball"])\n', full_solution='talabalar = [{"ism": "Ali", "ball": 85}, {"ism": "Vali", "ball": 72}, {"ism": "Gulnora", "ball": 95}]\neng = talabalar[0]\nfor t in talabalar:\n    if t["ball"] > eng["ball"]:\n        eng = t\nprint(eng["ism"], eng["ball"])\n', explanation="Eng kattani topish andozasi."),
        single('l49_practice_easy', "Easy: tuzilma", "`[{\"a\": 1}, {\"a\": 2}]` — bu nima?", section='practice', difficulty='easy', options=[opt("Dictionary'lardan iborat list", True), opt("List'lardan iborat dictionary", False), opt("Tuple", False)], hint="Tashqi qavs — `[ ]`.", explanation="List ichida dictionary."),
        code_task('l49_practice_medium', "Medium: talaba qo'shish", r"""
Bo'sh `jurnal = []` ga foydalanuvchi kiritgan **ism** va **ball** (butun) bilan bitta talaba dictionary'sini qo'shing va `jurnal` ni chiqaring. `Ali`, `90` → `[{'ism': 'Ali', 'ball': 90}]`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "[{'ism': 'Ali', 'ball': 90}]", "Ali/90", stdin="Ali\n90\n"), T('output_equals', "[{'ism': 'Vali', 'ball': 5}]", "Vali/5", stdin="Vali\n5\n")], hint="`jurnal.append({\"ism\": ..., \"ball\": ...})`.", full_solution='jurnal = []\nism = input()\nball = int(input())\njurnal.append({"ism": ism, "ball": ball})\nprint(jurnal)\n', explanation="List ichiga dictionary qo'shdik."),
        code_task('l49_practice_hard', "Hard: guruhlarga ajratish", r"""
Foydalanuvchi 4 ta talaba ballini kiritadi (alohida qatorlarda). Dastur `natija = {"o'tdi": [], "o'tmadi": []}` dictionary'ga **60 va undan yuqori** ballarni `o'tdi` ga, qolganlarini `o'tmadi` ga joylab, `natija` ni chiqarsin. `70 40 60 55` → `{"o'tdi": [70, 60], "o'tmadi": [40, 55]}`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "{\"o'tdi\": [70, 60], \"o'tmadi\": [40, 55]}", "70 40 60 55", stdin="70\n40\n60\n55\n"), T('output_equals', "{\"o'tdi\": [], \"o'tmadi\": [1, 2, 3, 4]}", "hammasi o'tmadi", stdin="1\n2\n3\n4\n", hidden=True)], hint="`natija[\"o'tdi\"].append(ball)`.", full_solution='natija = {"o\'tdi": [], "o\'tmadi": []}\nfor i in range(4):\n    b = int(input())\n    if b >= 60:\n        natija["o\'tdi"].append(b)\n    else:\n        natija["o\'tmadi"].append(b)\nprint(natija)\n', explanation="Dictionary qiymatlari list — ularga `append` qilindi."),
    ])

LESSONS = [LESSON_42, LESSON_43, LESSON_44, LESSON_45, LESSON_46, LESSON_47, LESSON_48, LESSON_49]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("7-modul yakuniy nazorati: Tuple, Set va Dictionary", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **talabalar baholari jurnali**.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m7_a_t1', "Tuple", "Tuple haqida to'g'ri gap?", section='assessment', points=2, options=[opt("O'zgartirib bo'lmaydi", True), opt("Faqat sonlarni saqlaydi", False), opt("Figurali qavs bilan yoziladi", False)], explanation="Tuple o'zgarmas, oddiy qavs `( )`."),
    single('m7_a_t2', "Set", "`{1, 2, 2, 3}` da nechta element bor?", section='assessment', points=2, options=[opt("3", True), opt("4", False), opt("2", False)], explanation="Takrorlar olib tashlanadi."),
    single('m7_a_t3', "Bo'sh set", "Bo'sh set qanday yoziladi?", section='assessment', points=2, options=[opt("`set()`", True), opt("`{}`", False), opt("`()`", False)], explanation="`{}` — bo'sh dictionary."),
    single('m7_a_t4', "get()", "`d.get(\"x\")` kalit yo'q bo'lsa nima qaytaradi?", section='assessment', points=2, options=[opt("`None`", True), opt("`KeyError`", False), opt("`0`", False)], explanation="Xato bermaydi — `None`."),
    multiple('m7_a_t5', "Dictionary kaliti", "Qaysi qiymatlar dictionary kaliti bo'la oladi?", section='assessment', points=2, options=[opt("`\"ism\"`", True), opt("`5`", True), opt("`(1, 2)`", True), opt("`[1, 2]`", False)], explanation="Kalit o'zgarmas tur bo'lishi kerak."),
    predict('m7_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = {1, 2, 3}\nb = {3, 4}\nprint(sorted(a | b), sorted(a & b))\n', answer="[1, 2, 3, 4] [3]", explanation="Birlashma va kesishma."),
    predict('m7_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='d = {"a": 1}\nd["b"] = d["a"] + 1\nd["a"] = 0\nprint(d)\n', answer="{'a': 0, 'b': 2}", explanation="`b` qo'shildi (2), keyin `a` nolga tushdi."),
    predict('m7_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='t = [{"n": 2}, {"n": 5}]\nprint(t[0]["n"] * t[1]["n"])\n', answer="10", explanation="`2 * 5`."),
    fix_task('m7_a_f1', "Xatoni tuzating (1)", "Dastur `Ali` ni chiqarishi kerak, lekin `KeyError` beryapti.", section='assessment', points=4, starter_code='talaba = {"ism": "Ali", "yosh": 17}\nprint(talaba["Ism"])\n', tests=[T('output_equals', "Ali", "Natija: Ali")], hint="Kalit harf registrini tekshiring.", full_solution='talaba = {"ism": "Ali", "yosh": 17}\nprint(talaba["ism"])\n', explanation="Kalitlar registrni farqlaydi."),
    fix_task('m7_a_f2', "Xatoni tuzating (2)", "Dastur uchta noyob sonni (`3`) chiqarishi kerak, lekin `0` chiqaryapti — bo'sh to'plam noto'g'ri yaratilgan.", section='assessment', points=4, starter_code='s = {}\nfor x in [1, 2, 2, 3, 1]:\n    s.add(x)\nprint(len(s))\n', tests=[T('output_equals', "3", "Natija: 3")], hint="`{}` — dictionary.", full_solution='s = set()\nfor x in [1, 2, 2, 3, 1]:\n    s.add(x)\nprint(len(s))\n', explanation="Bo'sh set uchun `set()`."),
    code_task('m7_a_project', "Mini-loyiha: Talabalar baholari jurnali", r"""
`jurnal = {}` — bo'sh dictionary (kalit — talaba ismi, qiymat — baholar listi). Dastur **menyu** orqali boshqariladi, `0` kiritilguncha:

| Buyruq | Amal | Chiqadigan xabar |
|---|---|---|
| `1` | keyingi qatorlarda **ism** va **baho** (butun) o'qiydi; talaba yangi bo'lsa — yaratadi; bahoni qo'shadi | `Baho qo'shildi: <ism> — <baho>` |
| `2` | keyingi qatorda **ism** o'qiydi; talabaning **o'rtachasini** (2 xonali) chiqaradi | `<ism>: o'rtacha <x.xx>` yoki `Topilmadi: <ism>` |
| `3` | barcha talabalarni **alifbo tartibida** `ism: baholar` shaklida chiqaradi (baholar probel bilan) | masalan `Ali: 5 4` |
| `4` | **eng yuqori o'rtachali** talabani chiqaradi (teng bo'lsa — alifboda birinchisi) | `Eng yaxshi: <ism> (<o'rtacha 2 xonali>)` yoki `Jurnal bo'sh` |
| `0` | tugatadi | `Talabalar soni: <N>` |

Misol: `1`,`Ali`,`5`, `1`,`Ali`,`4`, `1`,`Vali`,`3`, `2`,`Ali`, `3`, `4`, `0` →
```
Baho qo'shildi: Ali — 5
Baho qo'shildi: Ali — 4
Baho qo'shildi: Vali — 3
Ali: o'rtacha 4.50
Ali: 5 4
Vali: 3
Eng yaxshi: Ali (4.50)
Talabalar soni: 2
```
""", section='project', points=20, difficulty='hard', unlock=3, starter_code='# Talabalar baholari jurnali\njurnal = {}\n',
        expected_output_example="Baho qo'shildi: Ali — 5\nBaho qo'shildi: Ali — 4\nBaho qo'shildi: Vali — 3\nAli: o'rtacha 4.50\nAli: 5 4\nVali: 3\nEng yaxshi: Ali (4.50)\nTalabalar soni: 2",
        tests=[T('output_equals', "Baho qo'shildi: Ali — 5\nBaho qo'shildi: Ali — 4\nBaho qo'shildi: Vali — 3\nAli: o'rtacha 4.50\nAli: 5 4\nVali: 3\nEng yaxshi: Ali (4.50)\nTalabalar soni: 2", "Misol ssenariy", stdin="1\nAli\n5\n1\nAli\n4\n1\nVali\n3\n2\nAli\n3\n4\n0\n"),
               T('output_equals', "Topilmadi: Gulnora\nJurnal bo'sh\nTalabalar soni: 0", "Bo'sh jurnal", stdin="2\nGulnora\n4\n0\n"),
               T('output_equals', "Baho qo'shildi: Vali — 5\nBaho qo'shildi: Ali — 5\nAli: 5\nVali: 5\nEng yaxshi: Ali (5.00)\nTalabalar soni: 2", "Alifbo tartibi va teng o'rtacha", stdin="1\nVali\n5\n1\nAli\n5\n3\n4\n0\n", hidden=True),
               T('code_contains', 'sorted', "`sorted` ishlatilgan"), T('code_contains', 'while', "`while` ishlatilgan")],
        hint="1) `jurnal[ism] = jurnal.get(ism, []) + [baho]` yoki `if ism not in jurnal: jurnal[ism] = []`. 2) O'rtacha: `sum(baholar) / len(baholar)`. 3) Alifbo tartibi: `for ism in sorted(jurnal):`. 4) Eng yaxshi: eng yuqori o'rtachani eslab qoling (qat'iy `>` — teng bo'lsa birinchi qoladi).",
        partial_solution='jurnal = {}\nwhile True:\n    buyruq = input()\n    if buyruq == "0":\n        break\n    elif buyruq == "1":\n        ism = input()\n        baho = int(input())\n        if ism not in jurnal:\n            jurnal[ism] = []\n        jurnal[ism].append(baho)\n        print(f"Baho qo\'shildi: {ism} — {baho}")\n    # 2, 3, 4 buyruqlarini yozing\nprint("Talabalar soni:", len(jurnal))\n',
        full_solution='jurnal = {}\nwhile True:\n    buyruq = input()\n    if buyruq == "0":\n        break\n    elif buyruq == "1":\n        ism = input()\n        baho = int(input())\n        if ism not in jurnal:\n            jurnal[ism] = []\n        jurnal[ism].append(baho)\n        print(f"Baho qo\'shildi: {ism} — {baho}")\n    elif buyruq == "2":\n        ism = input()\n        if ism in jurnal:\n            print(f"{ism}: o\'rtacha {sum(jurnal[ism]) / len(jurnal[ism]):.2f}")\n        else:\n            print("Topilmadi:", ism)\n    elif buyruq == "3":\n        for ism in sorted(jurnal):\n            print(ism + ":", *jurnal[ism])\n    elif buyruq == "4":\n        if len(jurnal) == 0:\n            print("Jurnal bo\'sh")\n        else:\n            eng_ism = ""\n            eng_ortacha = -1\n            for ism in sorted(jurnal):\n                ortacha = sum(jurnal[ism]) / len(jurnal[ism])\n                if ortacha > eng_ortacha:\n                    eng_ortacha = ortacha\n                    eng_ism = ism\n            print(f"Eng yaxshi: {eng_ism} ({eng_ortacha:.2f})")\nprint("Talabalar soni:", len(jurnal))\n',
        explanation="Loyiha dictionary (ism → baholar listi), list metodlari, sorted, o'rtacha hisoblash va menyu sikli — hammasini birlashtiradi."),
])

# ==============================================================================
# 3-TAKRORLASH (REVIEW 3): 6- va 7-modullar + oldingilar
# ==============================================================================
REVIEW_3 = module_assessment("3-takrorlash (Review 3): 6- va 7-modullar (+ oldingilar)", r"""
List, tuple, set va dictionary mavzulari **sikllar, shartlar va matnlar** bilan aralash holda takrorlanadi.
O'tish — **70%**; qayta urinish cheksiz.
""", [
    single('r3_t1', "Tur tanlash", "Takrorlanmaydigan elementlar to'plami uchun qaysi tur mos?", section='assessment', points=2, options=[opt("set", True), opt("list", False), opt("tuple", False)], explanation="Set takrorlarni olib tashlaydi."),
    single('r3_t2', "Tur tanlash (2)", "«Ism → telefon» juftliklarini saqlash uchun qaysi tur qulay?", section='assessment', points=2, options=[opt("dictionary", True), opt("set", False), opt("str", False)], explanation="Kalit bo'yicha qidirish."),
    single('r3_t3', "Sikl + list", "Listdagi har bir elementni birin-ketin olish uchun?", section='assessment', points=2, options=[opt("`for x in royxat:`", True), opt("`while x in royxat:`", False), opt("`range(royxat)`", False)], explanation="`for x in list`."),
    single('r3_t4', "Matn va list", "`\"a-b-c\".replace(\"-\", \"\")` natijasi qaysi tur?", section='assessment', points=2, options=[opt("str", True), opt("list", False), opt("tuple", False)], explanation="Matn metodi matn qaytaradi."),
    multiple('r3_t5', "O'zgaruvchan turlar", "Qaysi turlar o'zgaruvchan (mutable)?", section='assessment', points=2, options=[opt("list", True), opt("dict", True), opt("set", True), opt("tuple", False)], explanation="Tuple va str o'zgarmas."),
    predict('r3_p1', "Aralash natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='s = ["salom", "dunyo", "salom"]\nsozlar = {}\nfor h in s:\n    sozlar[h] = sozlar.get(h, 0) + 1\nprint(sozlar)\n', answer="{'salom': 2, 'dunyo': 1}", explanation="Har bir so'z sanaldi."),
    predict('r3_p2', "Aralash natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = [5, 3, 5, 1, 3]\nb = sorted(set(a), reverse=True)\nprint(b, len(a) - len(b))\n', answer="[5, 3, 1] 2", explanation="Noyob: 5, 3, 1; takrorlar: 2 ta."),
    predict('r3_p3', "Aralash natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='d = {"a": [1, 2], "b": [3]}\nj = 0\nfor k in d:\n    j = j + len(d[k])\nprint(j)\n', answer="3", explanation="2 + 1."),
    fix_task('r3_f1', "Tuzating: indeks", "Dastur listning oxirgi elementini chiqarishi kerak.", section='assessment', points=4, starter_code='a = [4, 5, 6]\nprint(a[len(a)])\n', tests=[T('output_equals', "6", "Natija: 6")], hint="Oxirgi indeks `len(a) - 1`.", full_solution='a = [4, 5, 6]\nprint(a[len(a) - 1])\n', explanation="Yoki `a[-1]`."),
    fix_task('r3_f2', "Tuzating: dictionary", "Dastur `Ali 17` chiqarishi kerak.", section='assessment', points=4, starter_code='d = {"ism": "Ali", "yosh": 17}\nprint(d.ism, d.yosh)\n', tests=[T('output_equals', "Ali 17", "Natija: Ali 17")], hint="Dictionary'dan kalit bilan olinadi.", full_solution='d = {"ism": "Ali", "yosh": 17}\nprint(d["ism"], d["yosh"])\n', explanation="`d[\"kalit\"]`."),
    code_task('r3_c1', "Amaliy: kam uchraganlar", "Foydalanuvchi 6 ta so'z kiritadi. Faqat **bir marta** uchragan so'zlarni kiritilish tartibida list sifatida chiqaring. `a b a c d b` → `['c', 'd']`.", section='assessment', points=8, difficulty='medium',
              tests=[T('output_equals', "['c', 'd']", "a b a c d b", stdin="a\nb\na\nc\nd\nb\n"), T('output_equals', "[]", "hammasi takror", stdin="a\na\nb\nb\nc\nc\n"), T('output_equals', "['x', 'y', 'z', 'w', 'v', 'u']", "hammasi noyob", stdin="x\ny\nz\nw\nv\nu\n", hidden=True)],
              hint="Avval hammasini listga yig'ing, keyin `count(x) == 1` bo'lganlarini tanlang.", full_solution='s = []\nfor i in range(6):\n    s.append(input())\nnatija = []\nfor x in s:\n    if s.count(x) == 1:\n        natija.append(x)\nprint(natija)\n', explanation="List + count + filtrlash."),
    code_task('r3_c2', "Amaliy: baholar lug'ati", "Foydalanuvchi 3 ta fan nomini va har biri uchun bahoni kiritadi (nom, baho, nom, baho, ... — alohida qatorlarda). Dictionary yaratib, **o'rtacha bahoni** (1 xonali kasr) va **eng yuqori baho olingan fan** nomini chiqaring (teng bo'lsa — birinchisi). Kiritish `mat`, `5`, `fiz`, `4`, `tar`, `3` → `4.0` va `mat`.", section='assessment', points=10, difficulty='hard',
              tests=[T('output_equals', "4.0\nmat", "mat 5 fiz 4 tar 3", stdin="mat\n5\nfiz\n4\ntar\n3\n"), T('output_equals', "3.3\nb", "a 2 b 5 c 3", stdin="a\n2\nb\n5\nc\n3\n"), T('output_equals', "4.0\nx", "x 4 y 4 z 4 — birinchisi", stdin="x\n4\ny\n4\nz\n4\n", hidden=True)],
              hint="Dictionary'ga yig'ing; o'rtacha — `sum(d.values()) / len(d)`, eng yuqori — siklda qat'iy `>`.", partial_solution='d = {}\nfor i in range(3):\n    nom = input()\n    d[nom] = int(input())\nprint(round(sum(d.values()) / len(d), 1))\n# eng yuqori baho olgan fanni toping\n', full_solution='d = {}\nfor i in range(3):\n    nom = input()\n    d[nom] = int(input())\nprint(round(sum(d.values()) / len(d), 1))\neng = ""\nmax_baho = -1\nfor nom in d:\n    if d[nom] > max_baho:\n        max_baho = d[nom]\n        eng = nom\nprint(eng)\n', explanation="Dictionary + sikl + eng kattani topish."),
    code_task('r3_c3', "Amaliy: ikki guruh", "Foydalanuvchi ikki guruhning ismlarini kiritadi: har birida avval `n`, keyin `n` ta ism. Dastur **faqat birinchi guruhda** bo'lganlarni alifbo tartibida chiqarsin (probel bilan, bo'lmasa bo'sh qator). `2`: `Ali Vali`; `2`: `Vali Gul` → `Ali`.", section='assessment', points=8, difficulty='medium',
              tests=[T('output_equals', "Ali", "Ali Vali / Vali Gul", stdin="2\nAli\nVali\n2\nVali\nGul\n"), T('output_equals', "A B", "hammasi farqli", stdin="2\nB\nA\n1\nC\n"), T('output_equals', "", "hammasi umumiy", stdin="1\nA\n1\nA\n", hidden=True)],
              hint="Ikki set, `-` va `sorted`; chiqarishda `print(*sorted(...))`.", full_solution='a = set()\nfor i in range(int(input())):\n    a.add(input())\nb = set()\nfor i in range(int(input())):\n    b.add(input())\nprint(*sorted(a - b))\n', explanation="Set ayirmasi."),
], pass_percent=70)

REVIEWS = [REVIEW_3]
