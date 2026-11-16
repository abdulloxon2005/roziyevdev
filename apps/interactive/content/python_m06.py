"""Python — 0 dan boshlash · 6-modul: Ro'yxatlar (List) (34–41-darslar)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 6,
    'title': "Ro'yxatlar (List)",
    'description': "Ko'p qiymatni bitta o'zgaruvchida saqlash: list yaratish, indeks, o'zgartirish, qo'shish, o'chirish, saralash va sikllar bilan ishlash.",
}

# ==============================================================================
# 34-DARS
# ==============================================================================
LESSON_34 = L(34, "List nima va uni yaratish", 12,
    "List (ro'yxat) nima ekanini, nima uchun kerakligini bilish va turli ma'lumotli listlar yaratish.",
    ["List", "Kvadrat qavs []", "Elementlar", "Bo'sh list", "Aralash turdagi list"],
    [
        text(r"""
Xaridga ketyapsiz: non, sut, tuxum, olma. Bularni `narsa1`, `narsa2`, `narsa3`, `narsa4` nomli to'rtta o'zgaruvchida saqlaymizmi? 100 ta narsa bo'lsa-chi? Buning uchun **ro'yxat (list)** bor — ko'p qiymatni **bitta nom** ostida saqlaydi.
""", title="Ko'p qiymat — bitta nom"),
        text(r"""
List **kvadrat qavs** ichida, elementlar **vergul** bilan ajratilib yoziladi:

```python
xaridlar = ["non", "sut", "tuxum"]
sonlar = [10, 20, 30]
aralash = ["Ali", 17, True, 3.5]
bosh = []
```

- Elementlar tartibda joylashadi (har birining indeksi bor — 0 dan).
- List **har xil turdagi** qiymatlarni saqlashi mumkin.
- `[]` — bo'sh list.
- `print(xaridlar)` butun ro'yxatni chiqaradi: `['non', 'sut', 'tuxum']`.
""", title="List yaratish"),
        callout('analogy', r"""
List — **xarid savati**: ichida ko'p narsa bor, tartibda yotadi, istalgan payt qo'shish yoki olib tashlash mumkin.
""", title="Hayotiy o'xshatish"),
        example(r'''
meva = ["olma", "nok", "uzum"]
print(meva)
print(type(meva))
print(len(meva))
''', title="Birinchi list", body="Natija: `['olma', 'nok', 'uzum']`, `<class 'list'>`, `3`. `len()` elementlar sonini beradi."),
        example(r'''
talaba = ["Aziza", 17, "Toshkent", 4.8]
print(talaba)
bosh = []
print(bosh, len(bosh))
''', title="Amaliy: talaba ma'lumotlari", body="Bitta listda ism (matn), yosh (son), shahar va o'rtacha ball (kasr) saqlandi. `[]` — bo'sh list, uzunligi 0."),
        exercise('l34_inline_blank'),
        callout('tip', r"""
List nomini ko'plikda qo'ying: `xaridlar`, `ismlar`, `baholar` — shunda ichida ko'p qiymat borligi darhol ko'rinadi.
""", title="Nomlash"),
        recap(["list — `[a, b, c]`", "elementlar vergul bilan, tartibli", "har xil tur bo'lishi mumkin", "`len()` — elementlar soni"], "ro'yxatdagi bitta elementni — masalan, ikkinchisini — qanday olamiz?"),
    ],
    [
        fill('l34_inline_blank', "Bo'sh joy", "Uchta rang saqlovchi list yarating va chiqaring: `['qizil', 'yashil', 'ko\\'k']` emas — oddiy `['qizil', 'sariq']`.", 'ranglar = ___"qizil", "sariq"___\nprint(ranglar)\n', ['[', ']'], section='inline', points=2, tests=[T('output_equals', "['qizil', 'sariq']", "Natija to'g'ri")], hint="List qavsi qanday?", explanation="Kvadrat qavs `[ ]`."),
        predict('l34_quiz_1', "List chiqarish", "Dastur nima chiqaradi?", code='a = [1, 2, 3]\nprint(a)\n', answer="[1, 2, 3]", hint="List kvadrat qavs bilan chiqadi.", explanation="`[1, 2, 3]`."),
        single('l34_quiz_2', "Qavs turi", "List qaysi qavs bilan yaratiladi?", options=[opt("`[ ]`", True), opt("`( )`", False), opt("`{ }`", False)], hint="Kvadrat.", explanation="Kvadrat qavs."),
        predict('l34_quiz_3', "len()", "Dastur nima chiqaradi?", code='x = ["a", "b"]\nprint(len(x), len([]))\n', answer="2 0", hint="Bo'sh listda nechta element?", explanation="2 va 0."),
        code_task('l34_assignment', "Sevimli taomlarim", r"""
`taomlar` nomli list yarating — ichida **kamida 3 ta** sevimli taomingiz (matn). Keyin listni va undagi elementlar sonini ikki qatorda chiqaring:

```
['osh', 'manti', 'somsa']
3
```
""", starter_code='', points=10, tests=[T('output_regex', r"^\[.+\]\n\d+$", "Birinchi qator — list, ikkinchisi — son"), T('code_regex', r"(?m)^taomlar\s*=\s*\[", "`taomlar` list yaratilgan"), T('code_contains', 'len(', "`len()` ishlatilgan"), T('output_regex', r"(?m)^[3-9]|^\d{2,}$", "Kamida 3 ta element", hidden=True)],
            hint="`taomlar = [\"osh\", \"manti\", \"somsa\"]`, keyin `print(taomlar)` va `print(len(taomlar))`.", partial_solution='taomlar = ["osh", "manti", "somsa"]\nprint(taomlar)\n# elementlar sonini chiqaring\n', full_solution='taomlar = ["osh", "manti", "somsa"]\nprint(taomlar)\nprint(len(taomlar))\n', explanation="List yaratildi, chiqarildi, uzunligi `len()` bilan topildi."),
        single('l34_practice_easy', "Easy: har xil tur", "`[1, \"a\", True]` listi to'g'rimi?", section='practice', difficulty='easy', options=[opt("Ha, list har xil turni saqlay oladi", True), opt("Yo'q, faqat bir xil tur", False), opt("Faqat sonlar", False)], hint="List aralash bo'lishi mumkin.", explanation="Python listlari har xil turdagi elementlarni saqlaydi."),
        code_task('l34_practice_medium', "Medium: bo'sh va to'la", r"""
Bo'sh `a` listini va `b = [5, 6, 7, 8]` listini yarating. Ikkalasining uzunligini bir qatorda chiqaring: `0 4`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "0 4", "0 4"), T('code_contains', '[]', "Bo'sh list yaratilgan")], hint="`print(len(a), len(b))`.", full_solution='a = []\nb = [5, 6, 7, 8]\nprint(len(a), len(b))\n', explanation="`[]` — bo'sh list."),
        code_task('l34_practice_hard', "Hard: input dan list", r"""
Foydalanuvchi uch so'zni (har biri alohida qatorda) kiritadi. Ularni `soz` listiga solib, listni chiqaring. `a`, `b`, `c` → `['a', 'b', 'c']`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "['a', 'b', 'c']", "a, b, c", stdin="a\nb\nc\n"), T('output_equals', "['olma', 'nok', 'uzum']", "olma, nok, uzum", stdin="olma\nnok\nuzum\n"), T('code_regex', r"\[\s*\w+\s*,", "List ishlatilgan")], hint="Uchta `input()` ni to'g'ridan-to'g'ri `[ ]` ichiga yozish mumkin.", full_solution='a = input()\nb = input()\nc = input()\nsoz = [a, b, c]\nprint(soz)\n', explanation="List elementlari o'zgaruvchilar bo'lishi mumkin."),
    ])

# ==============================================================================
# 35-DARS
# ==============================================================================
LESSON_35 = L(35, "List elementlariga murojaat qilish", 12,
    "Indeks (musbat/manfiy) va kesim yordamida list elementlarini olish; IndexError ni tushunish.",
    ["Indeks", "Manfiy indeks", "Kesim [a:b]", "IndexError", "Ichma-ich list"],
    [
        text(r"""
Matnlardan indeksni bilasiz. List elementlari ham **xuddi shunday** olinadi — chunki list ham tartibli to'plam.
""", title="Matndagi kabi"),
        text(r"""
```python
meva = ["olma", "nok", "uzum", "anor"]
print(meva[0])     # olma
print(meva[2])     # uzum
print(meva[-1])    # anor  (oxirgisi)
print(meva[1:3])   # ['nok', 'uzum']   (kesim — yangi list)
print(meva[:2])    # ['olma', 'nok']
```

- Indeks **0 dan** boshlanadi; oxirgi element — `-1`.
- Kesim `[a:b]` — `b` kirmaydi va **list** qaytaradi (bitta indeks esa elementning o'zini).
- Mavjud bo'lmagan indeks → `IndexError: list index out of range`.
""", title="Indeks va kesim"),
        callout('analogy', r"""
List — **uy raqamlari ko'chasi**: uylar 0-raqamdan boshlanadi; `-1` — ko'chaning eng oxirgi uyi.
""", title="Hayotiy o'xshatish"),
        example(r'''
ismlar = ["Ali", "Vali", "Gulnora", "Dilshod"]
print(ismlar[0])
print(ismlar[-1])
print(ismlar[1:3])
print(ismlar[len(ismlar) - 1])
''', title="Elementlarni olish", body="Natija: `Ali`, `Dilshod`, `['Vali', 'Gulnora']`, `Dilshod`."),
        example(r'''
baholar = [5, 4, 3, 5, 4]
print("Birinchi:", baholar[0])
print("Oxirgi:", baholar[-1])
print("O'rtadagi uchtasi:", baholar[1:4])
jadval = [["Ali", 5], ["Vali", 4]]
print(jadval[1][0])
''', title="Amaliy: baholar va ichma-ich list", body="`jadval[1][0]` — avval 1-element (`[\"Vali\", 4]`), undan 0-element: `Vali`."),
        exercise('l35_inline_pred'),
        callout('warning', r"""
Bo'sh listdan element olish ham `IndexError` beradi: `[][0]`. Avval `len()` bilan tekshirish foydali.
""", title="Diqqat"),
        recap(["`list[i]` — element, `list[a:b]` — kesim", "`-1` — oxirgi element", "ichma-ich listda `list[i][j]`"], "listdagi elementni o'zgartirish mumkinmi? Matnda mumkin emas edi."),
    ],
    [
        predict('l35_inline_pred', "Indeks", "Dastur nima chiqaradi?", section='inline', code='a = [10, 20, 30, 40]\nprint(a[1], a[-2])\n', answer="20 30", points=2, hint="`-2` — oxiridan ikkinchi.", explanation="`a[1]` = 20; `a[-2]` = 30."),
        predict('l35_quiz_1', "Kesim", "Dastur nima chiqaradi?", code='a = ["a", "b", "c", "d"]\nprint(a[1:3])\n', answer="['b', 'c']", hint="3-indeks kirmaydi.", explanation="1 va 2-indekslar."),
        single('l35_quiz_2', "IndexError", "`[1, 2, 3][3]` nima beradi?", options=[opt("`IndexError`", True), opt("`3`", False), opt("`None`", False)], hint="3 ta element: indekslar 0, 1, 2.", explanation="3-indeks mavjud emas."),
        predict('l35_quiz_3', "Ichma-ich", "Dastur nima chiqaradi?", code='m = [[1, 2], [3, 4]]\nprint(m[1][0])\n', answer="3", hint="Avval `m[1]`.", explanation="`m[1]` = `[3, 4]`, uning 0-elementi — 3."),
        code_task('l35_assignment', "Birinchi va oxirgi", r"""
Foydalanuvchi to'rt so'zni (alohida qatorlarda) kiritadi va ular `soz` listiga joylanadi. Dastur birinchi va oxirgi elementni **bir qatorda** chiqarsin. `a`, `b`, `c`, `d` → `a d`.
""", starter_code='soz = [input(), input(), input(), input()]\n', points=10, tests=[T('output_equals', "a d", "a b c d", stdin="a\nb\nc\nd\n"), T('output_equals', "olma uzum", "olma nok anor uzum", stdin="olma\nnok\nanor\nuzum\n"), T('code_contains', '[-1]', "`[-1]` ishlatilgan")],
            hint="`print(soz[0], soz[-1])`.", partial_solution='soz = [input(), input(), input(), input()]\nprint(soz[0])\n# oxirgi elementni ham chiqaring\n', full_solution='soz = [input(), input(), input(), input()]\nprint(soz[0], soz[-1])\n', explanation="Birinchi — `[0]`, oxirgi — `[-1]`."),
        single('l35_practice_easy', "Easy: -1", "`a[-1]` nima?", section='practice', difficulty='easy', options=[opt("Oxirgi element", True), opt("Birinchi element", False), opt("Xato", False)], hint="Oxiridan sanash.", explanation="Oxirgi element."),
        code_task('l35_practice_medium', "Medium: o'rtadagi elementlar", r"""
`a = [1, 2, 3, 4, 5, 6]` berilgan. Kesim yordamida `[2, 3, 4]` ni chiqaring, so'ng oxirgi uch elementni (`[4, 5, 6]`) chiqaring (ikki qatorda).
""", section='practice', difficulty='medium', points=5, starter_code='a = [1, 2, 3, 4, 5, 6]\n', tests=[T('output_equals', "[2, 3, 4]\n[4, 5, 6]", "Ikki kesim"), T('code_contains', ':', "Kesim ishlatilgan")], hint="`a[1:4]` va `a[-3:]`.", full_solution='a = [1, 2, 3, 4, 5, 6]\nprint(a[1:4])\nprint(a[-3:])\n', explanation="Kesim yangi list qaytaradi."),
        code_task('l35_practice_hard', "Hard: o'rta element", r"""
Foydalanuvchi **toq** sonli (masalan, 5 ta) elementdan iborat list bo'lgan holda `n` kiritadi (`n` — elementlar soni, toq), so'ng `n` ta son kiritadi. Dastur **o'rtadagi** sonni chiqarsin. `5` ta: `1 2 3 4 5` → `3`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "3", "5: 1..5", stdin="5\n1\n2\n3\n4\n5\n"), T('output_equals', "9", "3: 7 9 1", stdin="3\n7\n9\n1\n"), T('output_equals', "42", "1: 42", stdin="1\n42\n", hidden=True)], hint="List yarating, sikl bilan `append` hali o'tilmagan — `n` ta qiymatni `[]` ga qo'shish o'rniga, o'rta indeksni hisoblab, `n` ta `input()` ni o'zgaruvchilarga saqlang. Oson yo'l: `soz = []` + `soz = soz + [x]`.", partial_solution='n = int(input())\nsonlar = []\nfor i in range(n):\n    x = int(input())\n    sonlar = sonlar + [x]\n# o\'rta indeksni toping\n', full_solution='n = int(input())\nsonlar = []\nfor i in range(n):\n    x = int(input())\n    sonlar = sonlar + [x]\nprint(sonlar[n // 2])\n', explanation="`list + list` — listlarni birlashtiradi (`[1] + [2]` → `[1, 2]`). Keyingi darslarda `append()` bilan osonroq bo'ladi."),
    ])

# ==============================================================================
# 36-DARS
# ==============================================================================
LESSON_36 = L(36, "List elementlarini o'zgartirish", 11,
    "Indeks orqali list elementini almashtirish va listlar o'zgaruvchan (mutable) ekanini tushunish.",
    ["Element almashtirish", "O'zgaruvchan tur (mutable)", "Matn bilan farqi", "Nusxa olish: copy()"],
    [
        text(r"""
Xarid ro'yxatini yozdingiz: «non, sut, tuxum». Keyin o'ylab, «sut»ni «qatiq»ka almashtirdingiz — butun ro'yxatni qayta yozmadingiz. List elementlari ham shunday **o'zgartiriladi**.
""", title="Ro'yxatni tahrirlash"),
        text(r"""
```python
xaridlar = ["non", "sut", "tuxum"]
xaridlar[1] = "qatiq"
print(xaridlar)      # ['non', 'qatiq', 'tuxum']
```

`list[indeks] = yangi_qiymat` — shu o'rindagi eski qiymat o'chib, yangisi joylashadi.

**Muhim farq:** matn (`str`) o'zgarmaydi — `"salom"[0] = "S"` xato beradi. List esa **o'zgaruvchan (mutable)**.

**Ehtiyot bo'ling:** `b = a` yangi list yaratmaydi — **bitta listga ikkita nom** beradi. Nusxa uchun `b = a.copy()`.
""", title="Element almashtirish"),
        callout('analogy', r"""
`b = a` — **bitta daftarga ikki kishi ismini yozishi**: biri o'zgartirsa, ikkinchisi ham ko'radi. `a.copy()` — **daftarni nusxalash**.
""", title="Hayotiy o'xshatish"),
        example(r'''
baholar = [3, 4, 5]
baholar[0] = 5
baholar[-1] = baholar[-1] - 1
print(baholar)
''', title="Qiymatlarni almashtirish", body="Birinchi element 5 bo'ldi, oxirgisi 1 ga kamaydi: `[5, 4, 4]`. Element qiymatidan hisob-kitobda ham foydalanish mumkin."),
        example(r'''
a = [1, 2, 3]
b = a
b[0] = 99
print(a)
c = a.copy()
c[0] = 0
print(a, c)
''', title="Amaliy: nusxa va havola", body="`b = a` — bitta list, shuning uchun `a` ham o'zgardi: `[99, 2, 3]`. `copy()` mustaqil nusxa beradi: `a` o'zgarmadi, `c` o'zgardi: `[99, 2, 3] [0, 2, 3]`."),
        exercise('l36_inline_fix'),
        recap(["`list[i] = qiymat` — almashtiradi", "list o'zgaruvchan, matn emas", "`b = a` — nusxa emas; `a.copy()` — nusxa"], "listga yangi element qo'shish mumkinmi? Yangi xarid qo'shsak-chi?"),
    ],
    [
        fix_task('l36_inline_fix', "Xatoni tuzating", "Ikkinchi elementni `\"B\"` ga almashtirish kerak. Natija: `['a', 'B', 'c']`", section='inline', points=2, starter_code='x = ["a", "b", "c"]\nx[1] == "B"\nprint(x)\n', tests=[T('output_equals', "['a', 'B', 'c']", "Natija to'g'ri")], hint="Almashtirishda `==` emas, boshqa belgi.", full_solution='x = ["a", "b", "c"]\nx[1] = "B"\nprint(x)\n', explanation="`==` tekshiradi, `=` almashtiradi."),
        predict('l36_quiz_1', "Almashtirish", "Dastur nima chiqaradi?", code='a = [1, 2, 3]\na[2] = a[0] + a[1]\nprint(a)\n', answer="[1, 2, 3]", hint="`a[0] + a[1]` = 1 + 2 = 3 — oxirgi element ham 3 edi.", explanation="3 o'rniga 3 qo'yildi — list o'zgarmadi."),
        single('l36_quiz_2', "Matn o'zgaradimi?", "`s = \"abc\"`; `s[0] = \"X\"` nima beradi?", options=[opt("`TypeError` — matn o'zgarmaydi", True), opt("`Xbc`", False), opt("Hech narsa", False)], hint="Matn — o'zgarmas tur.", explanation="Matn elementlarini almashtirib bo'lmaydi."),
        predict('l36_quiz_3', "Havola", "Dastur nima chiqaradi?", code='a = [1, 2]\nb = a\nb[0] = 9\nprint(a)\n', answer="[9, 2]", hint="`b` va `a` — bitta list.", explanation="`b = a` nusxa olmaydi."),
        code_task('l36_assignment', "Narxni yangilash", r"""
`narxlar = [12000, 8000, 15000]` berilgan. Ikkinchi mahsulot narxini **10 foizga oshiring** (`8000` → `8800`, butun son: `* 11 // 10`), listni chiqaring: `[12000, 8800, 15000]`.
""", starter_code='narxlar = [12000, 8000, 15000]\n', points=10, tests=[T('output_equals', "[12000, 8800, 15000]", "Natija"), T('code_regex', r"narxlar\[1\]\s*=", "`narxlar[1]` ga qiymat berilgan")], hint="`narxlar[1] = narxlar[1] * 11 // 10`.", partial_solution="narxlar = [12000, 8000, 15000]\nnarxlar[1] = narxlar[1] * 11\n# 10 ga butun bo'ling va chiqaring\n", full_solution='narxlar = [12000, 8000, 15000]\nnarxlar[1] = narxlar[1] * 11 // 10\nprint(narxlar)\n', explanation="Element eski qiymati asosida yangilandi."),
        single('l36_practice_easy', "Easy: mutable", "Quyidagilardan qaysi biri o'zgaruvchan (mutable) tur?", section='practice', difficulty='easy', options=[opt("list", True), opt("str", False), opt("int", False)], hint="Elementini almashtira oladigan.", explanation="List o'zgaruvchan."),
        code_task('l36_practice_medium', "Medium: ikkitasini almashtirish", r"""
`a = [1, 2, 3, 4]` da birinchi va oxirgi elementlarning o'rnini almashtiring va chiqaring: `[4, 2, 3, 1]`. (Vaqtincha o'zgaruvchi `t` ishlating.)
""", section='practice', difficulty='medium', points=5, starter_code='a = [1, 2, 3, 4]\n', tests=[T('output_equals', "[4, 2, 3, 1]", "Natija")], hint="`t = a[0]` — eskisini eslab qoling.", full_solution='a = [1, 2, 3, 4]\nt = a[0]\na[0] = a[-1]\na[-1] = t\nprint(a)\n', explanation="Vaqtincha o'zgaruvchi qiymatni yo'qotmaydi."),
        code_task('l36_practice_hard', "Hard: hamma elementni ikkilantirish", r"""
`a = [1, 2, 3]` ning **har bir** elementini 2 ga ko'paytiring (siklda indeks orqali) va chiqaring: `[2, 4, 6]`. `range(len(a))` ishlating.
""", section='practice', difficulty='hard', points=5, starter_code='a = [1, 2, 3]\n', tests=[T('output_equals', "[2, 4, 6]", "Natija"), T('code_contains', 'range(len(', "`range(len(a))` ishlatilgan")], hint="`for i in range(len(a)):` ichida `a[i] = a[i] * 2`.", full_solution='a = [1, 2, 3]\nfor i in range(len(a)):\n    a[i] = a[i] * 2\nprint(a)\n', explanation="Indeks orqali har bir elementni almashtirdik."),
    ])

# ==============================================================================
# 37-DARS
# ==============================================================================
LESSON_37 = L(37, "append() va insert() metodlari", 12,
    "append() bilan oxiriga, insert() bilan istalgan joyga element qo'shish.",
    ["append()", "insert()", "Listni o'stirish", "Bo'sh listdan boshlash"],
    [
        text(r"""
Do'konda yana bir narsa esingizga tushdi — ro'yxatga **qo'shasiz**. Listning o'lchami qat'iy emas: u **o'sib boradi**.
""", title="Ro'yxatga qo'shish"),
        text(r"""
| Metod | Vazifasi | Misol |
|---|---|---|
| `list.append(x)` | **oxiriga** qo'shadi | `a.append(5)` |
| `list.insert(i, x)` | **i-o'ringa** qo'shadi, qolganlar suriladi | `a.insert(0, 5)` |

```python
a = [1, 2, 3]
a.append(4)        # [1, 2, 3, 4]
a.insert(0, 99)    # [99, 1, 2, 3, 4]
```

Ikkala metod ham **listning o'zini o'zgartiradi** va hech narsa qaytarmaydi (`a = a.append(5)` — xato: `a` `None` bo'lib qoladi).
""", title="Ikki metod"),
        callout('analogy', r"""
`append` — **navbatning oxiriga turish**. `insert(0, x)` — **navbatning boshiga o'tib olish** (qolganlar orqaga suriladi).
""", title="Hayotiy o'xshatish"),
        example(r'''
meva = ["olma", "nok"]
meva.append("uzum")
meva.insert(1, "anor")
print(meva)
''', title="append va insert", body="Natija: `['olma', 'anor', 'nok', 'uzum']`. `anor` 1-indeksga qo'yildi, `nok` esa orqaga surildi."),
        example(r'''
xaridlar = []
for i in range(3):
    nom = input("Mahsulot: ")
    xaridlar.append(nom)
print("Xaridlar:", xaridlar)
''', title="Amaliy: list o'sib boradi", body="Bo'sh listdan boshlab, kiritilgan har bir mahsulot `append` bilan qo'shiladi. Kiritish: `non`, `sut`, `tuxum` → `Xaridlar: ['non', 'sut', 'tuxum']`."),
        exercise('l37_inline_pred'),
        callout('warning', r"""
`a = a.append(5)` yozmang! `append` `None` qaytaradi — `a` yo'qoladi. To'g'risi: shunchaki `a.append(5)`.
""", title="Eng ko'p uchraydigan xato"),
        recap(["`append(x)` — oxiriga", "`insert(i, x)` — i-o'ringa", "ikkalasi ham listning o'zini o'zgartiradi"], "elementni qanday o'chiramiz?"),
    ],
    [
        predict('l37_inline_pred', "append", "Dastur nima chiqaradi?", section='inline', code='a = [1]\na.append(2)\na.append(3)\nprint(a)\n', answer="[1, 2, 3]", points=2, hint="Har safar oxiriga.", explanation="Ketma-ket oxiriga qo'shildi."),
        predict('l37_quiz_1', "insert", "Dastur nima chiqaradi?", code='a = ["b", "c"]\na.insert(0, "a")\nprint(a)\n', answer="['a', 'b', 'c']", hint="0-o'ringa qo'shiladi.", explanation="Qolganlari o'ngga suriladi."),
        single('l37_quiz_2', "Xato", "`a = a.append(5)` dan keyin `a` nima bo'ladi?", options=[opt("`None`", True), opt("`a` + 5 elementi bilan list", False), opt("Xato beradi", False)], hint="`append` hech narsa qaytarmaydi.", explanation="`append` `None` qaytaradi."),
        predict('l37_quiz_3', "Oxirgi indeks", "Dastur nima chiqaradi?", code='a = [10, 20]\na.insert(1, 15)\nprint(a, len(a))\n', answer="[10, 15, 20] 3", hint="`insert` yangi element qo'shadi.", explanation="Uzunlik 3 bo'ldi."),
        code_task('l37_assignment', "Juft sonlar ro'yxati", r"""
1 dan 10 gacha sonlardan **faqat juftlarini** `juftlar` listiga `append` bilan qo'shing va listni chiqaring: `[2, 4, 6, 8, 10]`.
""", starter_code='juftlar = []\n', points=10, tests=[T('output_equals', "[2, 4, 6, 8, 10]", "Natija"), T('code_contains', 'append', "`append` ishlatilgan")], hint="`for i in range(1, 11): if i % 2 == 0: juftlar.append(i)`.", partial_solution="juftlar = []\nfor i in range(1, 11):\n    # juft bo'lsa append qiling\n    pass\nprint(juftlar)\n", full_solution='juftlar = []\nfor i in range(1, 11):\n    if i % 2 == 0:\n        juftlar.append(i)\nprint(juftlar)\n', explanation="Sikl + shart + append."),
        single('l37_practice_easy', "Easy: qaysi metod?", "Elementni listning **oxiriga** qo'shadigan metod?", section='practice', difficulty='easy', options=[opt("`append()`", True), opt("`insert()`", False), opt("`add()`", False)], hint="Inglizcha — qo'shmoq.", explanation="`append()`."),
        code_task('l37_practice_medium', "Medium: son kiritish", r"""
Foydalanuvchi `n` kiritadi, so'ng `n` ta son. Dastur ularni `sonlar` listiga yig'ib, listni chiqarsin. `3`, `5`, `1`, `4` → `[5, 1, 4]`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "[5, 1, 4]", "3: 5 1 4", stdin="3\n5\n1\n4\n"), T('output_equals', "[]", "0", stdin="0\n"), T('output_equals', "[7]", "1: 7", stdin="1\n7\n", hidden=True)], hint="Bo'sh listdan boshlang; siklda `int(input())` ni `append` qiling.", full_solution='n = int(input())\nsonlar = []\nfor i in range(n):\n    sonlar.append(int(input()))\nprint(sonlar)\n', explanation="List kiritilgan ma'lumot bilan to'ldirildi."),
        code_task('l37_practice_hard', "Hard: o'sish tartibida qo'shish", r"""
`a = [1, 3, 5, 9]` o'sish tartibida. `7` sonini **tartib buzilmasdan** qo'shing (`insert` bilan, o'rinni siklda toping): natija `[1, 3, 5, 7, 9]`. O'rin — birinchi `7` dan katta elementning indeksi.
""", section='practice', difficulty='hard', points=5, starter_code='a = [1, 3, 5, 9]\nyangi = 7\n', tests=[T('output_equals', "[1, 3, 5, 7, 9]", "Natija"), T('code_contains', 'insert', "`insert` ishlatilgan")], hint="`for i in range(len(a)):` — `a[i] > yangi` bo'lsa shu `i` ga qo'shing va `break`.", partial_solution='a = [1, 3, 5, 9]\nyangi = 7\nfor i in range(len(a)):\n    if a[i] > yangi:\n        # shu o\'ringa qo\'shing va to\'xtating\n        pass\nprint(a)\n', full_solution='a = [1, 3, 5, 9]\nyangi = 7\nfor i in range(len(a)):\n    if a[i] > yangi:\n        a.insert(i, yangi)\n        break\nprint(a)\n', explanation="`insert` + `break` — kerakli o'rinni topib qo'shish."),
    ])

# ==============================================================================
# 38-DARS
# ==============================================================================
LESSON_38 = L(38, "remove(), pop() va del", 13,
    "remove(), pop() va del yordamida list elementlarini o'chirish va ular orasidagi farqni bilish.",
    ["remove(qiymat)", "pop(indeks)", "del list[indeks]", "ValueError", "clear()"],
    [
        text(r"""
Xaridni olib bo'ldingiz — ro'yxatdan **o'chirasiz**. Python'da buning uch xil usuli bor — farqlari qaysi ma'lumotni bilishingizga bog'liq: **qiymatni** bilasizmi yoki **o'rnini (indeksini)**?
""", title="Ro'yxatdan o'chirish"),
        text(r"""
| Usul | Nimani bilamiz | Nima qiladi |
|---|---|---|
| `a.remove(x)` | **qiymat** | birinchi `x` ni o'chiradi (yo'q bo'lsa — `ValueError`) |
| `a.pop(i)` | **indeks** | i-elementni o'chiradi va **qaytaradi** (`i` berilmasa — oxirgisi) |
| `del a[i]` | **indeks** | i-elementni o'chiradi (qaytarmaydi) |
| `a.clear()` | — | hammasini o'chiradi |

```python
a = [10, 20, 30, 20]
a.remove(20)      # [10, 30, 20]  (faqat birinchisi)
x = a.pop()       # x = 20, a = [10, 30]
del a[0]          # [30]
```
""", title="Uch usul"),
        callout('analogy', r"""
`remove("sut")` — «ro'yxatdan **sutni** o'chiring». `del a[1]` — «**2-qatorni** o'chiring». `pop()` — «oxirgisini **oling** (va menga bering)».
""", title="Hayotiy o'xshatish"),
        example(r'''
meva = ["olma", "nok", "uzum", "nok"]
meva.remove("nok")
print(meva)
oxirgi = meva.pop()
print(oxirgi, meva)
del meva[0]
print(meva)
''', title="Uch usul", body="Natija: `['olma', 'uzum', 'nok']`, `nok ['olma', 'uzum']`, `['uzum']`. `remove` faqat birinchi `nok` ni olib tashladi."),
        example(r'''
vazifalar = ["dars", "sport", "kitob"]
bajarildi = vazifalar.pop(0)
print("Bajarildi:", bajarildi)
print("Qoldi:", vazifalar)
''', title="Amaliy: vazifalar navbati", body="`pop(0)` — navbatdagi birinchi vazifani olib, ro'yxatdan chiqaradi: `Bajarildi: dars`, `Qoldi: ['sport', 'kitob']`."),
        exercise('l38_inline_pred'),
        callout('warning', r"""
Mavjud bo'lmagan elementni `remove()` qilish `ValueError` beradi. Avval `if x in a:` bilan tekshiring. Bo'sh listda `pop()` — `IndexError`.
""", title="Diqqat"),
        recap(["`remove(qiymat)`, `pop(indeks)`, `del a[indeks]`", "`pop` o'chirib, qiymatni qaytaradi", "mavjud bo'lmasa — xato"], "listni tartiblash (kattadan kichikka, alifbo bo'yicha) uchun qanday vosita bor?"),
    ],
    [
        predict('l38_inline_pred', "remove", "Dastur nima chiqaradi?", section='inline', code='a = [1, 2, 3, 2]\na.remove(2)\nprint(a)\n', answer="[1, 3, 2]", points=2, hint="Faqat birinchi 2.", explanation="Birinchi uchragan 2 o'chdi."),
        predict('l38_quiz_1', "pop", "Dastur nima chiqaradi?", code='a = ["x", "y", "z"]\nb = a.pop(1)\nprint(b, a)\n', answer="y ['x', 'z']", hint="`pop` qiymatni qaytaradi.", explanation="`y` olindi."),
        predict('l38_quiz_2', "del", "Dastur nima chiqaradi?", code='a = [5, 6, 7]\ndel a[-1]\nprint(a)\n', answer="[5, 6]", hint="`-1` — oxirgi.", explanation="Oxirgi element o'chdi."),
        single('l38_quiz_3', "Xato turi", "`[1, 2].remove(5)` qanday xato beradi?", options=[opt("`ValueError`", True), opt("`IndexError`", False), opt("`NameError`", False)], hint="Qiymat topilmadi.", explanation="`ValueError`."),
        code_task('l38_assignment', "Xaridni olib tashlash", r"""
`xaridlar = ["non", "sut", "tuxum", "olma"]` berilgan. Foydalanuvchi o'chirilishi kerak bo'lgan mahsulot nomini kiritadi. **Agar ro'yxatda bo'lsa** — o'chirib, `Qoldi: [...]` chiqaring; bo'lmasa — `Topilmadi`. `sut` → `Qoldi: ['non', 'tuxum', 'olma']`.
""", starter_code='xaridlar = ["non", "sut", "tuxum", "olma"]\n', points=10, tests=[T('output_equals', "Qoldi: ['non', 'tuxum', 'olma']", "sut", stdin="sut\n"), T('output_equals', "Topilmadi", "nok", stdin="nok\n"), T('output_equals', "Qoldi: ['sut', 'tuxum', 'olma']", "non", stdin="non\n", hidden=True), T('code_contains', 'remove', "`remove` ishlatilgan")],
            hint="`if nom in xaridlar:` — `in` bilan tekshirish.", partial_solution='xaridlar = ["non", "sut", "tuxum", "olma"]\nnom = input()\nif nom in xaridlar:\n    # o\'chiring va chiqaring\n    pass\nelse:\n    print("Topilmadi")\n', full_solution='xaridlar = ["non", "sut", "tuxum", "olma"]\nnom = input()\nif nom in xaridlar:\n    xaridlar.remove(nom)\n    print("Qoldi:", xaridlar)\nelse:\n    print("Topilmadi")\n', explanation="`in` xatodan saqlaydi."),
        single('l38_practice_easy', "Easy: pop", "`pop()` indekssiz qaysi elementni o'chiradi?", section='practice', difficulty='easy', options=[opt("Oxirgisini", True), opt("Birinchisini", False), opt("Hammasini", False)], hint="Stack kabi.", explanation="Oxirgi elementni."),
        code_task('l38_practice_medium', "Medium: oxirgi ikkita", r"""
`a = [1, 2, 3, 4, 5]` dan **oxirgi ikkita** elementni `pop()` bilan olib tashlang va ularni olingan tartibda chiqaring, so'ng qolgan listni chiqaring:

```
5
4
[1, 2, 3]
```
""", section='practice', difficulty='medium', points=5, starter_code='a = [1, 2, 3, 4, 5]\n', tests=[T('output_equals', "5\n4\n[1, 2, 3]", "Natija"), T('code_contains', 'pop', "`pop` ishlatilgan")], hint="`print(a.pop())` ikki marta.", full_solution='a = [1, 2, 3, 4, 5]\nprint(a.pop())\nprint(a.pop())\nprint(a)\n', explanation="`pop` o'chiradi va qaytaradi."),
        code_task('l38_practice_hard', "Hard: hamma takrorlarni o'chirish", r"""
`a = [1, 2, 2, 3, 2, 4]` dan **barcha** `2` larni o'chiring (`while 2 in a:` va `remove`) va listni chiqaring: `[1, 3, 4]`.
""", section='practice', difficulty='hard', points=5, starter_code='a = [1, 2, 2, 3, 2, 4]\n', tests=[T('output_equals', "[1, 3, 4]", "Natija"), T('code_contains', 'while', "`while` ishlatilgan")], hint="`remove` faqat birinchisini oladi — takrorlang.", full_solution='a = [1, 2, 2, 3, 2, 4]\nwhile 2 in a:\n    a.remove(2)\nprint(a)\n', explanation="`remove` ni takrorlab hammasini o'chirdik."),
    ])

# ==============================================================================
# 39-DARS
# ==============================================================================
LESSON_39 = L(39, "List elementlarini saralash — sort() va sorted()", 12,
    "sort() va sorted() farqini bilish, o'sish/kamayish tartibida saralash (reverse=True) va matnlarni saralash.",
    ["sort()", "sorted()", "reverse=True", "Matnlarni saralash", "min() va max()"],
    [
        text(r"""
Test natijalari: 72, 95, 60, 88. Eng yaxshi uchtasini ko'rsatish uchun ularni **tartiblash** kerak. Python'da tartiblashning ikki usuli bor.
""", title="Tartiblash"),
        text(r"""
| | `a.sort()` | `sorted(a)` |
|---|---|---|
| Asl listga ta'siri | **o'zgartiradi** | o'zgartirmaydi |
| Qaytaradi | `None` | **yangi** tartiblangan list |

```python
a = [3, 1, 2]
b = sorted(a)       # b = [1, 2, 3], a = [3, 1, 2]
a.sort()            # a = [1, 2, 3]
a.sort(reverse=True)  # a = [3, 2, 1]  (kamayish)
```

Matnlar **alifbo tartibida** saralanadi (katta harflar kichiklardan oldin keladi!). Qo'shimcha: `min(a)`, `max(a)`, `sum(a)` — eng kichik, eng katta va yig'indi.
""", title="sort() va sorted()"),
        callout('analogy', r"""
`sort()` — **javondagi kitoblarni joyida tartiblash**. `sorted()` — **tartiblangan nusxasini yangi javonga qo'yish** (eskisi o'zgarishsiz qoladi).
""", title="Hayotiy o'xshatish"),
        example(r'''
ballar = [72, 95, 60, 88]
print(sorted(ballar))
print(ballar)
ballar.sort(reverse=True)
print(ballar)
''', title="sorted va sort", body="`sorted` asl listni o'zgartirmadi (`[72, 95, 60, 88]`), `sort(reverse=True)` esa joyida kamayish tartibida tartiblab qo'ydi: `[95, 88, 72, 60]`."),
        example(r'''
ismlar = ["Vali", "Ali", "Dilnoza", "Bobur"]
ismlar.sort()
print(ismlar)
sonlar = [4, 9, 1]
print(min(sonlar), max(sonlar), sum(sonlar))
''', title="Amaliy: ismlar va statistika", body="Ismlar alifbo tartibida: `['Ali', 'Bobur', 'Dilnoza', 'Vali']`. Sonlar uchun: `1 9 14`."),
        exercise('l39_inline_pred'),
        callout('warning', r"""
`a = a.sort()` yozmang — `sort()` `None` qaytaradi. Faqat `a.sort()` yoki `b = sorted(a)`.
""", title="Diqqat"),
        recap(["`sort()` — joyida, `sorted()` — yangi list", "`reverse=True` — kamayish tartibi", "`min`, `max`, `sum`"], "listdagi hamma elementni birin-ketin qanday ko'rib chiqamiz?"),
    ],
    [
        predict('l39_inline_pred', "sorted", "Dastur nima chiqaradi?", section='inline', code='a = [5, 2, 8]\nprint(sorted(a), a)\n', answer="[2, 5, 8] [5, 2, 8]", points=2, hint="`sorted` asl listni o'zgartirmaydi.", explanation="Yangi tartiblangan list va asl list."),
        predict('l39_quiz_1', "sort(reverse)", "Dastur nima chiqaradi?", code='a = [1, 3, 2]\na.sort(reverse=True)\nprint(a)\n', answer="[3, 2, 1]", hint="Kamayish tartibi.", explanation="Katta → kichik."),
        single('l39_quiz_2', "None", "`x = [3, 1].sort()` dan keyin `x` nima?", options=[opt("`None`", True), opt("`[1, 3]`", False), opt("`[3, 1]`", False)], hint="`sort()` hech narsa qaytarmaydi.", explanation="`None`."),
        predict('l39_quiz_3', "Statistika", "Dastur nima chiqaradi?", code='a = [4, 10, 6]\nprint(max(a) - min(a), sum(a))\n', answer="6 20", hint="10 - 4 va 4+10+6.", explanation="6 va 20."),
        code_task('l39_assignment', "Eng yaxshi uch ball", r"""
Foydalanuvchi 5 ta ball kiritadi (alohida qatorlarda). Dastur eng **yuqori uchta** ballni kamayish tartibida listda chiqarsin. `70 90 60 85 95` → `[95, 90, 85]`.
""", starter_code='', points=10, tests=[T('output_equals', "[95, 90, 85]", "70 90 60 85 95", stdin="70\n90\n60\n85\n95\n"), T('output_equals', "[5, 4, 3]", "1 2 3 4 5", stdin="1\n2\n3\n4\n5\n"), T('output_equals', "[7, 7, 7]", "teng ballar", stdin="7\n7\n7\n7\n7\n", hidden=True)], hint="Sikl bilan `append`, `sort(reverse=True)`, kesim `[:3]`.", partial_solution='ballar = []\nfor i in range(5):\n    ballar.append(int(input()))\nballar.sort(reverse=True)\n# birinchi uchtasini chiqaring\n', full_solution='ballar = []\nfor i in range(5):\n    ballar.append(int(input()))\nballar.sort(reverse=True)\nprint(ballar[:3])\n', explanation="Kamayish tartibida birinchi uchta — eng yuqorilari."),
        single('l39_practice_easy', "Easy: sorted", "`sorted()` asl listni o'zgartiradimi?", section='practice', difficulty='easy', options=[opt("Yo'q, yangi list qaytaradi", True), opt("Ha", False), opt("Faqat sonlar uchun", False)], hint="`sort()` bilan farqi.", explanation="`sorted()` yangi list qaytaradi."),
        code_task('l39_practice_medium', "Medium: eng kichik va eng katta", r"""
Foydalanuvchi 4 ta son kiritadi. `Eng kichik: X, eng katta: Y` shaklida chiqaring (`min`/`max`). `5 2 9 1` → `Eng kichik: 1, eng katta: 9`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Eng kichik: 1, eng katta: 9", "5 2 9 1", stdin="5\n2\n9\n1\n"), T('output_equals', "Eng kichik: -3, eng katta: 4", "manfiy", stdin="4\n-3\n0\n2\n")], hint="Sonlarni listga yig'ing, `min(a)` va `max(a)`.", full_solution='a = []\nfor i in range(4):\n    a.append(int(input()))\nprint(f"Eng kichik: {min(a)}, eng katta: {max(a)}")\n', explanation="`min`/`max` tartiblashsiz topadi."),
        code_task('l39_practice_hard', "Hard: o'rtacha va medianaga yaqin", r"""
Foydalanuvchi 5 ta son kiritadi. Tartiblangan listni va uning **o'rtadagi** elementini (mediana) chiqaring: `[1, 3, 5, 7, 9]` va `5`. Kiritish `9 1 5 3 7`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "[1, 3, 5, 7, 9]\n5", "9 1 5 3 7", stdin="9\n1\n5\n3\n7\n"), T('output_equals', "[2, 2, 4, 6, 8]\n4", "2 8 2 4 6", stdin="2\n8\n2\n4\n6\n", hidden=True)], hint="`a.sort()`, o'rta indeks — `len(a) // 2`.", full_solution='a = []\nfor i in range(5):\n    a.append(int(input()))\na.sort()\nprint(a)\nprint(a[len(a) // 2])\n', explanation="Tartiblangan listning o'rtasi — mediana."),
    ])

# ==============================================================================
# 40-DARS
# ==============================================================================
LESSON_40 = L(40, "List bilan sikllarda ishlash", 13,
    "for sikli bilan list elementlari bo'ylab yurish, indeks bilan (range(len())) va enumerate() bilan ishlash, yig'indi va qidirish.",
    ["for element in list", "range(len())", "enumerate()", "Filtrlash", "Yangi list yig'ish"],
    [
        text(r"""
Eng ko'p ishlatiladigan juftlik — **list + sikl**: ro'yxatdagi har bir elementni ko'rib chiqish, hisoblash, filtrlash.
""", title="List va sikl — do'st"),
        text(r"""
```python
meva = ["olma", "nok", "uzum"]

for m in meva:                       # elementlar bo'ylab
    print(m)

for i in range(len(meva)):           # indeks bo'ylab
    print(i, meva[i])

for i, m in enumerate(meva, start=1):   # indeks + element
    print(i, m)
```

`enumerate(list, start=1)` — har bir elementga **tartib raqami** beradi. Yangi list yig'ish andozasi: `yangi = []`, siklda `if shart: yangi.append(x)`.
""", title="Uch usul"),
        callout('analogy', r"""
`for m in meva` — **savatdan meva olib ko'rish**. `enumerate` — **meva olayotib, nechanchi ekanini ham sanash**.
""", title="Hayotiy o'xshatish"),
        example(r'''
ballar = [70, 55, 90, 40, 85]
jami = 0
for b in ballar:
    jami = jami + b
print("O'rtacha:", jami / len(ballar))
''', title="Yig'indi va o'rtacha", body="`jami` = 340, uzunlik 5: `O'rtacha: 68.0`."),
        example(r'''
ballar = [70, 55, 90, 40, 85]
otganlar = []
for b in ballar:
    if b >= 60:
        otganlar.append(b)
print(otganlar)
for n, b in enumerate(otganlar, start=1):
    print(f"{n}) {b} ball")
''', title="Amaliy: filtrlash va raqamlash", body="60 va undan yuqori ballar yangi listga yig'ildi: `[70, 90, 85]`; keyin raqamlab chiqarildi: `1) 70 ball` va h.k."),
        exercise('l40_inline_blank'),
        callout('tip', r"""
Listni sikl ichida o'zgartirib (element qo'shib/o'chirib) yurmang — kutilmagan natija beradi. Yangi list yig'ish xavfsizroq.
"""),
        recap(["`for x in list:` — elementlar bo'ylab", "`enumerate(list, start=1)` — raqamlash", "yangi list yig'ish: `append` + `if`"], "listdagi elementlar soni va biror element bor-yo'qligini qanday tekshiramiz?"),
    ],
    [
        fill('l40_inline_blank', "Bo'sh joy", "Listdagi har bir sonni ikkilantirib chiqaring. `[1, 2, 3]` → `2`, `4`, `6` (alohida qatorlarda).", 'a = [1, 2, 3]\nfor x ___ a:\n    print(x * 2)\n', ['in'], section='inline', points=2, tests=[T('output_equals', "2\n4\n6", "2, 4, 6")], hint="`for ... ... ...:` kalit so'zlari.", explanation="`for x in a:`."),
        predict('l40_quiz_1', "Yig'indi", "Dastur nima chiqaradi?", code='j = 0\nfor x in [3, 4, 5]:\n    j = j + x\nprint(j)\n', answer="12", hint="3+4+5.", explanation="12."),
        predict('l40_quiz_2', "enumerate", "Dastur nima chiqaradi?", code='for i, h in enumerate(["a", "b"], start=1):\n    print(i, h)\n', answer="1 a\n2 b", hint="Raqam 1 dan boshlanadi.", explanation="`start=1`."),
        predict('l40_quiz_3', "Filtrlash", "Dastur nima chiqaradi?", code='y = []\nfor x in [1, 2, 3, 4]:\n    if x % 2 == 0:\n        y.append(x * x)\nprint(y)\n', answer="[4, 16]", hint="Faqat juftlarning kvadrati.", explanation="2² va 4²."),
        code_task('l40_assignment', "Ro'yxatdagi eng uzun so'z", r"""
Foydalanuvchi 4 ta so'z kiritadi. Dastur **eng uzun** so'zni chiqarsin (teng bo'lsa — birinchisini). `kitob`, `daftar`, `qalam`, `chizg'ich` → `chizg'ich`.
""", starter_code='', points=10, tests=[T('output_equals', "chizg'ich", "chizg'ich", stdin="kitob\ndaftar\nqalam\nchizg'ich\n"), T('output_equals', "daftar", "daftar", stdin="kitob\ndaftar\nqalam\nruchka\n"), T('output_equals', "aaa", "teng bo'lsa birinchisi", stdin="aaa\nbbb\nccc\nddd\n", hidden=True)], hint="`eng = \"\"`; siklda `len(s) > len(eng)`.", partial_solution='soz = []\nfor i in range(4):\n    soz.append(input())\neng = ""\nfor s in soz:\n    # agar s eng dan uzun bo\'lsa almashtiring\n    pass\nprint(eng)\n', full_solution='soz = []\nfor i in range(4):\n    soz.append(input())\neng = ""\nfor s in soz:\n    if len(s) > len(eng):\n        eng = s\nprint(eng)\n', explanation="Qat'iy `>` — tenglarda birinchisi qoladi."),
        single('l40_practice_easy', "Easy: enumerate", "`enumerate()` nima beradi?", section='practice', difficulty='easy', options=[opt("Indeks va elementni birga", True), opt("Faqat elementlar sonini", False), opt("Tartiblangan list", False)], hint="Raqamlash.", explanation="Har bir element uchun (tartib raqami, element)."),
        code_task('l40_practice_medium', "Medium: musbatlar soni", r"""
Foydalanuvchi `n` va keyin `n` ta son kiritadi. Nechtasi **musbat** ekanini chiqaring. `4`: `3 -1 0 5` → `2`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "2", "3 -1 0 5", stdin="4\n3\n-1\n0\n5\n"), T('output_equals', "0", "hammasi manfiy", stdin="2\n-1\n-2\n"), T('output_equals', "3", "uchta", stdin="3\n1\n2\n3\n", hidden=True)], hint="Sanagich + `if x > 0`.", full_solution='n = int(input())\nsoni = 0\nfor i in range(n):\n    x = int(input())\n    if x > 0:\n        soni = soni + 1\nprint(soni)\n', explanation="Sanagich sxemasi."),
        code_task('l40_practice_hard', "Hard: takrorlanmaydigan elementlar", r"""
Foydalanuvchi 5 ta so'z kiritadi. Dastur **takrorlanmaydigan** (birinchi uchragan) so'zlarni tartib bilan chiqarsin: `olma`, `nok`, `olma`, `uzum`, `nok` → `['olma', 'nok', 'uzum']`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "['olma', 'nok', 'uzum']", "olma nok olma uzum nok", stdin="olma\nnok\nolma\nuzum\nnok\n"), T('output_equals', "['a']", "hammasi bir xil", stdin="a\na\na\na\na\n", hidden=True)], hint="`if s not in natija:` (`not in` — «yo'q bo'lsa»).", full_solution='natija = []\nfor i in range(5):\n    s = input()\n    if s not in natija:\n        natija.append(s)\nprint(natija)\n', explanation="`not in` bilan takrorlar filtrlandi."),
    ])

# ==============================================================================
# 41-DARS
# ==============================================================================
LESSON_41 = L(41, "List uzunligi va elementlarni tekshirish", 12,
    "len(), in / not in, count() va index() yordamida list haqida ma'lumot olish va bo'sh listni tekshirish.",
    ["len()", "in / not in", "count()", "index()", "Bo'sh listni tekshirish"],
    [
        text(r"""
Ro'yxat haqida savollar: **Nechta element bor? Shu element bormi? Necha marta uchraydi? Qaysi o'rinda?** Python buning hammasiga javob beradi.
""", title="Ro'yxatga savollar"),
        text(r"""
| Savol | Vosita | Natija |
|---|---|---|
| nechta element? | `len(a)` | son |
| element bormi? | `x in a` / `x not in a` | `True`/`False` |
| necha marta? | `a.count(x)` | son |
| qaysi o'rinda? | `a.index(x)` | birinchi indeks (yo'q bo'lsa — `ValueError`) |
| bo'shmi? | `len(a) == 0` yoki `not a` | `True`/`False` |

```python
a = ["olma", "nok", "olma"]
print(len(a), "nok" in a, a.count("olma"), a.index("nok"))   # 3 True 2 1
```
""", title="Tekshirish vositalari"),
        callout('analogy', r"""
Kutubxonachidan so'raysiz: «Nechta kitob bor? **Python kitobi bormi?** Nechtasi bor? Qaysi javonda?» — `len`, `in`, `count`, `index`.
""", title="Hayotiy o'xshatish"),
        example(r'''
ballar = [5, 4, 5, 3, 5]
print(len(ballar))
print(5 in ballar)
print(2 in ballar)
print(ballar.count(5))
print(ballar.index(3))
''', title="Beshta savol", body="Natija: `5`, `True`, `False`, `3`, `3`."),
        example(r'''
savat = []
if len(savat) == 0:
    print("Savat bo'sh")
savat.append("non")
if savat:
    print("Savatda", len(savat), "ta mahsulot")
''', title="Amaliy: bo'sh savat", body="Bo'sh list `if` shartida `False` deb hisoblanadi, to'la list — `True`. Shuning uchun `if savat:` — «savat bo'sh emasmi?» ma'nosida."),
        exercise('l41_inline_pred'),
        callout('warning', r"""
`a.index(x)` element topilmasa `ValueError` beradi. Avval `if x in a:` bilan tekshiring.
""", title="Diqqat"),
        recap(["`len`, `in`, `not in`, `count`, `index`", "bo'sh list shartda `False`", "`index` — topilmasa `ValueError`"], "modul oxirida interaktiv xaridlar ro'yxati dasturini yozamiz — qaysi bilimlar kerak bo'ladi?"),
    ],
    [
        predict('l41_inline_pred', "count va index", "Dastur nima chiqaradi?", section='inline', code='a = [1, 2, 1, 3]\nprint(a.count(1), a.index(3))\n', answer="2 3", points=2, hint="`1` ikki marta; `3` — 3-indeksda.", explanation="`count(1)` = 2; `index(3)` = 3."),
        predict('l41_quiz_1', "in", "Dastur nima chiqaradi?", code='print("a" in ["b", "c"], "b" in ["b", "c"])\n', answer="False True", hint="Alohida baholang.", explanation="`a` yo'q, `b` bor."),
        single('l41_quiz_2', "Bo'sh list", "`if []:` shartida nima bo'ladi?", options=[opt("Shart yolg'on (`False`)", True), opt("Shart rost", False), opt("Xato", False)], hint="Bo'sh — «yo'q».", explanation="Bo'sh list yolg'on hisoblanadi."),
        predict('l41_quiz_3', "len va in birga", "Dastur nima chiqaradi?", code='a = ["x", "y"]\na.append("z")\nprint(len(a), "z" in a)\n', answer="3 True", hint="Oldin qo'shildi.", explanation="3 ta element, `z` bor."),
        code_task('l41_assignment', "Takrorlanishlar", r"""
Foydalanuvchi 5 ta bahoni (1–5) kiritadi. Dastur uch qatorda chiqarsin: **nechta `5` olingani**, **eng yuqori bahoning** `5` bor-yo'qligi (`True`/`False`) va **bahoning ro'yxatdagi birinchi `5` ining tartib raqami** (indeks) yoki `-1` (agar yo'q bo'lsa). `3 5 4 5 2` → `2`, `True`, `1`.
""", starter_code='', points=10, tests=[T('output_equals', "2\nTrue\n1", "3 5 4 5 2", stdin="3\n5\n4\n5\n2\n"), T('output_equals', "0\nFalse\n-1", "5 yo'q", stdin="1\n2\n3\n4\n3\n"), T('output_equals', "1\nTrue\n4", "oxirida", stdin="1\n2\n3\n4\n5\n", hidden=True)], hint="`count`, `in`, va `index` (faqat `5` bor bo'lsa) — yo'q bo'lsa `-1`.", partial_solution='b = []\nfor i in range(5):\n    b.append(int(input()))\nprint(b.count(5))\nprint(5 in b)\n# indeksni chiqaring\n', full_solution='b = []\nfor i in range(5):\n    b.append(int(input()))\nprint(b.count(5))\nprint(5 in b)\nif 5 in b:\n    print(b.index(5))\nelse:\n    print(-1)\n', explanation="`index` dan oldin `in` bilan tekshirdik."),
        single('l41_practice_easy', "Easy: not in", "`\"x\" not in [\"a\"]` natijasi?", section='practice', difficulty='easy', options=[opt("`True`", True), opt("`False`", False), opt("Xato", False)], hint="`x` listda yo'q.", explanation="`x` yo'q — `not in` rost."),
        code_task('l41_practice_medium', "Medium: bor-yo'qligi", r"""
Foydalanuvchi mevalar ro'yxatiga **3 ta** meva kiritadi, so'ng yana bitta meva nomini so'rab, `Bor` yoki `Yo'q` deb javob beradi. `olma`, `nok`, `uzum`, so'rov: `nok` → `Bor`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Bor", "nok bor", stdin="olma\nnok\nuzum\nnok\n"), T('output_equals', "Yo'q", "anor yo'q", stdin="olma\nnok\nuzum\nanor\n")], hint="`in` operatori.", full_solution='m = [input(), input(), input()]\nso_rov = input()\nif so_rov in m:\n    print("Bor")\nelse:\n    print("Yo\'q")\n', explanation="`in` — bor-yo'qligini tekshiradi."),
        code_task('l41_practice_hard', "Hard: eng ko'p uchragan", r"""
Foydalanuvchi 6 ta so'z kiritadi. **Eng ko'p takrorlangan** so'zni va necha marta takrorlanganini chiqaring (teng bo'lsa — birinchi uchragani): `a b a c a b` → `a 3`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "a 3", "a b a c a b", stdin="a\nb\na\nc\na\nb\n"), T('output_equals', "x 2", "teng bo'lsa birinchisi", stdin="x\ny\nx\ny\nz\nw\n"), T('output_equals', "q 6", "hammasi bir xil", stdin="q\nq\nq\nq\nq\nq\n", hidden=True)], hint="Har bir so'z uchun `count`, eng kattasini eslab qoling.", partial_solution='s = []\nfor i in range(6):\n    s.append(input())\neng = s[0]\nfor x in s:\n    # count(x) engdan katta bo\'lsa almashtiring\n    pass\nprint(eng, s.count(eng))\n', full_solution='s = []\nfor i in range(6):\n    s.append(input())\neng = s[0]\nfor x in s:\n    if s.count(x) > s.count(eng):\n        eng = x\nprint(eng, s.count(eng))\n', explanation="`count` + eng kattani eslab qolish."),
    ])

LESSONS = [LESSON_34, LESSON_35, LESSON_36, LESSON_37, LESSON_38, LESSON_39, LESSON_40, LESSON_41]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("6-modul yakuniy nazorati: Ro'yxatlar", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **interaktiv xaridlar ro'yxati**.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m6_a_t1', "List belgisi", "List qanday yoziladi?", section='assessment', points=2, options=[opt("`[1, 2, 3]`", True), opt("`(1, 2, 3)`", False), opt("`{1, 2, 3}`", False)], explanation="Kvadrat qavs."),
    single('m6_a_t2', "Indeks", "`a = [7, 8, 9]` da `a[-1]` nima?", section='assessment', points=2, options=[opt("9", True), opt("7", False), opt("Xato", False)], explanation="Oxirgi element."),
    single('m6_a_t3', "append", "`append()` nima qiladi?", section='assessment', points=2, options=[opt("Elementni oxiriga qo'shadi", True), opt("Boshiga qo'shadi", False), opt("Listni tartiblaydi", False)], explanation="Oxiriga."),
    single('m6_a_t4', "sort", "`a.sort()` natijasi nima qaytaradi?", section='assessment', points=2, options=[opt("`None`", True), opt("Yangi list", False), opt("Asl list", False)], explanation="`sort()` listni joyida tartiblaydi va `None` qaytaradi."),
    multiple('m6_a_t5', "O'chirish usullari", "Qaysi usullar listdan element o'chiradi?", section='assessment', points=2, options=[opt("`remove()`", True), opt("`pop()`", True), opt("`del`", True), opt("`append()`", False)], explanation="Uchalasi ham o'chiradi."),
    predict('m6_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = [1, 2, 3, 4, 5]\nprint(a[1:4], a[-2:])\n', answer="[2, 3, 4] [4, 5]", explanation="`a[1:4]` — 1, 2, 3-indekslar; `a[-2:]` — oxirgi ikkita."),
    predict('m6_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = [3, 1, 2]\nb = sorted(a)\na.append(0)\nprint(a, b)\n', answer="[3, 1, 2, 0] [1, 2, 3]", explanation="`sorted` nusxa beradi."),
    predict('m6_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = ["x", "y", "z"]\nx = a.pop(0)\na.insert(1, x)\nprint(a)\n', answer="['y', 'x', 'z']", explanation="`x` olindi va 1-o'ringa qo'yildi."),
    fix_task('m6_a_f1', "Xatoni tuzating (1)", "Dastur listning oxirgi elementini (`30`) chiqarishi kerak, lekin xato beryapti.", section='assessment', points=4, starter_code='a = [10, 20, 30]\nprint(a[3])\n', tests=[T('output_equals', "30", "Natija: 30")], hint="Indekslar 0 dan boshlanadi.", full_solution='a = [10, 20, 30]\nprint(a[-1])\n', explanation="`a[3]` mavjud emas; oxirgisi `a[2]` yoki `a[-1]`."),
    fix_task('m6_a_f2', "Xatoni tuzating (2)", "Dastur listni o'sish tartibida chiqarishi kerak (`[1, 2, 3]`), lekin `None` chiqaryapti.", section='assessment', points=4, starter_code='a = [3, 1, 2]\na = a.sort()\nprint(a)\n', tests=[T('output_equals', "[1, 2, 3]", "Natija: [1, 2, 3]")], hint="`sort()` `None` qaytaradi.", full_solution='a = [3, 1, 2]\na.sort()\nprint(a)\n', explanation="`a = a.sort()` yozmang."),
    code_task('m6_a_project', "Mini-loyiha: Interaktiv xaridlar ro'yxati", r"""
Dastur **menyu** orqali boshqariladi. `xaridlar = []` bo'sh listdan boshlanadi. Foydalanuvchi **raqamli buyruq** kiritadi (har biri alohida qatorda), `0` kiritilguncha takrorlanadi:

| Buyruq | Amal | Chiqadigan xabar |
|---|---|---|
| `1` | keyingi qatorda **mahsulot nomini** o'qib, ro'yxatga qo'shadi | `Qo'shildi: <nom>` |
| `2` | ro'yxatni ko'rsatadi | har bir mahsulot `1. non` shaklida alohida qatorda; bo'sh bo'lsa `Ro'yxat bo'sh` |
| `3` | keyingi qatorda nom o'qib, ro'yxatdan o'chiradi | `O'chirildi: <nom>` yoki `Topilmadi: <nom>` |
| `4` | ro'yxatni alifbo tartibida saralaydi | `Saralandi` |
| `0` | dasturni tugatadi | `Jami: <N> ta mahsulot` |

Bir xil nomni ikki marta qo'shish mumkin emas — `Allaqachon bor: <nom>` deb chiqaring.

Misol kiritish: `1`, `non`, `1`, `sut`, `2`, `3`, `non`, `2`, `0` → natija:
```
Qo'shildi: non
Qo'shildi: sut
1. non
2. sut
O'chirildi: non
1. sut
Jami: 1 ta mahsulot
```
""", section='project', points=20, difficulty='hard', unlock=3, starter_code='# Interaktiv xaridlar ro\'yxati\nxaridlar = []\n',
        expected_output_example="Qo'shildi: non\nQo'shildi: sut\n1. non\n2. sut\nO'chirildi: non\n1. sut\nJami: 1 ta mahsulot",
        tests=[T('output_equals', "Qo'shildi: non\nQo'shildi: sut\n1. non\n2. sut\nO'chirildi: non\n1. sut\nJami: 1 ta mahsulot", "Misol ssenariy", stdin="1\nnon\n1\nsut\n2\n3\nnon\n2\n0\n"),
               T('output_equals', "Ro'yxat bo'sh\nJami: 0 ta mahsulot", "Bo'sh ro'yxat", stdin="2\n0\n"), T('output_equals', "Qo'shildi: olma\nAllaqachon bor: olma\nTopilmadi: nok\nJami: 1 ta mahsulot", "Dublikat va topilmagan", stdin="1\nolma\n1\nolma\n3\nnok\n0\n"),
               T('output_equals', "Qo'shildi: sut\nQo'shildi: non\nQo'shildi: anor\nSaralandi\n1. anor\n2. non\n3. sut\nJami: 3 ta mahsulot", "Saralash", stdin="1\nsut\n1\nnon\n1\nanor\n4\n2\n0\n", hidden=True),
               T('code_contains', 'append', "`append` ishlatilgan"), T('code_contains', 'while', "`while` ishlatilgan")],
        hint="1) `while True:` ichida `buyruq = input()`. 2) `if buyruq == \"0\": break`. 3) `\"1\"` da nomni o'qing, `if nom in xaridlar` — bor-yo'qligini tekshiring. 4) Ko'rsatishda `enumerate(xaridlar, start=1)`.",
        partial_solution='xaridlar = []\nwhile True:\n    buyruq = input()\n    if buyruq == "0":\n        break\n    elif buyruq == "1":\n        nom = input()\n        if nom in xaridlar:\n            print("Allaqachon bor:", nom)\n        else:\n            xaridlar.append(nom)\n            print("Qo\'shildi:", nom)\n    # 2, 3, 4 buyruqlarini yozing\nprint(f"Jami: {len(xaridlar)} ta mahsulot")\n',
        full_solution='xaridlar = []\nwhile True:\n    buyruq = input()\n    if buyruq == "0":\n        break\n    elif buyruq == "1":\n        nom = input()\n        if nom in xaridlar:\n            print("Allaqachon bor:", nom)\n        else:\n            xaridlar.append(nom)\n            print("Qo\'shildi:", nom)\n    elif buyruq == "2":\n        if len(xaridlar) == 0:\n            print("Ro\'yxat bo\'sh")\n        else:\n            for n, m in enumerate(xaridlar, start=1):\n                print(f"{n}. {m}")\n    elif buyruq == "3":\n        nom = input()\n        if nom in xaridlar:\n            xaridlar.remove(nom)\n            print("O\'chirildi:", nom)\n        else:\n            print("Topilmadi:", nom)\n    elif buyruq == "4":\n        xaridlar.sort()\n        print("Saralandi")\nprint(f"Jami: {len(xaridlar)} ta mahsulot")\n',
        explanation="Loyiha list metodlari (append, remove, sort), in, enumerate, while True + break va elif zanjirini birlashtiradi."),
])
