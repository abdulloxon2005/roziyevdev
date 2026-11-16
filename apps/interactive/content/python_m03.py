"""Python — 0 dan boshlash · 3-modul: Matnlar (String) (16–20-darslar) va 1-takrorlash (Review 1)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 3,
    'title': "Matnlar (String)",
    'description': "Matn ichidagi harflarga indeks orqali murojaat, len(), katta-kichik harflar, qidirish va almashtirish, f-string bilan formatlash.",
}

# ==============================================================================
# 16-DARS
# ==============================================================================
LESSON_16 = L(16, "String bilan ishlash va indekslar", 13,
    "Matn harflar ketma-ketligi ekanini tushunish, indeks (musbat va manfiy) bilan harfni olish va kesim [a:b] bilan bo'lak ajratish.",
    ["Indeks", "0 dan boshlanadi", "Manfiy indeks", "Kesim (slice)", "IndexError"],
    [
        text(r"""
Kino zalida har bir o'rindiqning **raqami** bor: shu raqam bilan aniq o'rindiqni topasiz. Matn ham xuddi shunday — harflar qatori, har bir harfning o'z **tartib raqami (indeksi)** bor.
""", title="Matn — harflar qatori"),
        callout('important', r"""
Dasturlashda sanoq **0 dan** boshlanadi! `"Python"` so'zida: `P`→0, `y`→1, `t`→2, `h`→3, `o`→4, `n`→5. Oxiridan sanash uchun **manfiy** indeks: oxirgi harf `-1`, undan oldingisi `-2`.
""", title="Eng muhim qoida"),
        text(r"""
```python
so_z = "Python"
print(so_z[0])    # P
print(so_z[-1])   # n
print(so_z[1:4])  # yth   (1 dan 4 gacha, 4 kirmaydi)
print(so_z[:2])   # Py    (boshidan)
print(so_z[2:])   # thon  (oxirigacha)
```

`matn[a:b]` — `a`-indeksdan boshlab `b`-indeksgacha (**`b` kirmaydi**) bo'lak. Mavjud bo'lmagan indeks (`so_z[10]`) `IndexError` beradi.
""", title="Indeks va kesim"),
        example(r'''
ism = "Aziza"
print(ism[0])
print(ism[-1])
print(ism[0] + ism[-1])
''', title="Birinchi va oxirgi harf", body="Natija: `A`, `a`, `Aa`. Indeks bilan olingan harf ham matn, shuning uchun `+` bilan ulanadi."),
        example(r'''
telefon = "998901234567"
print(telefon[:3])
print(telefon[3:5])
print(telefon[-7:])
''', title="Amaliy: telefon raqamini bo'laklash", body="`998` — davlat kodi, `90` — operator kodi, qolgan 7 raqam — abonent raqami."),
        exercise('l16_inline_pred'),
        callout('tip', r"""
Eslab qolish usuli: indeks — harfning o'zi emas, **harfdan oldingi** «chiziq» raqami deb tasavvur qiling. Shunda `[1:4]` aniq — 1-chiziqdan 4-chiziqgacha.
"""),
        recap(["indeks 0 dan boshlanadi", "`-1` — oxirgi harf", "`matn[a:b]` — bo'lak (`b` kirmaydi)"], "matnda nechta harf bor — buni qanday sanaymiz?"),
    ],
    [
        predict('l16_inline_pred', "Indeks", "Dastur nima chiqaradi?", section='inline', code='print("kitob"[2])\n', answer="t", points=2, hint="0 dan sanang: k=0, i=1...", explanation="k(0) i(1) t(2)."),
        single('l16_quiz_1', "Birinchi harf indeksi", "Matnning birinchi harfi qaysi indeksda?", options=[opt("1", False), opt("0", True), opt("-1", False, "`-1` — oxirgi harf.")], hint="Python 0 dan sanaydi.", explanation="Birinchi harf indeksi — 0."),
        predict('l16_quiz_2', "Kesim", "Dastur nima chiqaradi?", code='s = "dasturlash"\nprint(s[0:6])\n', answer="dastur", hint="6-indeks kirmaydi.", explanation="0,1,2,3,4,5 indekslar: d a s t u r."),
        predict('l16_quiz_3', "Manfiy kesim", "Dastur nima chiqaradi?", code='s = "Toshkent"\nprint(s[-3:])\n', answer="ent", hint="Oxirgi 3 ta harf.", explanation="Oxiridan 3-harfdan oxirigacha: e n t."),
        code_task('l16_assignment', "Bosh harflar", r"""
Foydalanuvchi **ism** va **familiya** kiritadi (ikkita `input()`). Dastur ularning bosh harflarini nuqta bilan chiqarsin. `Aziza`, `Karimova` → `A.K.`
""", starter_code='', points=10,
            tests=[T('output_equals', "A.K.", "Aziza Karimova → A.K.", stdin="Aziza\nKarimova\n"), T('output_equals', "B.A.", "Bobur Aliyev → B.A.", stdin="Bobur\nAliyev\n"), T('output_equals', "S.T.", "Sardor Tursunov → S.T.", stdin="Sardor\nTursunov\n", hidden=True)],
            hint="`ism[0]` — birinchi harf.", partial_solution='ism = input()\nfamiliya = input()\nprint(ism[0] + ".")\n# familiyaning bosh harfini ham qo\'shing\n',
            full_solution='ism = input()\nfamiliya = input()\nprint(ism[0] + "." + familiya[0] + ".")\n', explanation="Har bir matnning `[0]` harfi olindi va nuqta bilan ulandi."),
        single('l16_practice_easy', "Easy: IndexError", "`\"abc\"[5]` nima beradi?", section='practice', difficulty='easy', options=[opt("`IndexError`", True), opt("Bo'sh matn", False), opt("`c`", False)], hint="Bunday indeks yo'q.", explanation="Matnda 3 ta harf bor (0,1,2), 5-indeks yo'q."),
        code_task('l16_practice_medium', "Medium: oxirgi harf", r"""
Foydalanuvchi so'z kiritadi. Dastur uning **oxirgi harfini** chiqarsin. `kitob` → `b`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "b", "kitob → b", stdin="kitob\n"), T('output_equals', "a", "olma → a", stdin="olma\n")],
            hint="`[-1]`.", full_solution='s = input()\nprint(s[-1])\n', explanation="`-1` — oxirgi harf."),
        code_task('l16_practice_hard', "Hard: yil va oy", r"""
Foydalanuvchi sana kiritadi, masalan `2026-03-15` (har doim shu formatda: YYYY-MM-DD). Dastur uch qatorda chiqarsin: yil, oy, kun. `2026-03-15` → `2026`, `03`, `15`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "2026\n03\n15", "2026-03-15", stdin="2026-03-15\n"), T('output_equals', "1999\n12\n01", "1999-12-01", stdin="1999-12-01\n")],
            hint="Yil — `[0:4]`, oy — `[5:7]`, kun — `[8:]`.", partial_solution='sana = input()\nprint(sana[0:4])\n# oy va kunni ham chiqaring\n', full_solution='sana = input()\nprint(sana[0:4])\nprint(sana[5:7])\nprint(sana[8:])\n', explanation="Kesimlar chiziqlar (`-`) orasidagi bo'laklarni ajratadi."),
    ])

# ==============================================================================
# 17-DARS
# ==============================================================================
LESSON_17 = L(17, "Matn uzunligini aniqlash — len()", 11,
    "len() funksiyasi bilan matn uzunligini aniqlash, uni indeks bilan birga ishlatish (oxirgi harf, o'rtasi).",
    ["len()", "Bo'sh joy ham belgi", "len() va indeks", "Bo'sh matn"],
    [
        text(r"""
SMS xabarida belgilar soni cheklangan, parolda kamida 8 ta belgi bo'lishi kerak, Twitter'da 280 ta... Hammasida **matn uzunligi** kerak. Python'da buni **`len()`** (inglizcha *length*) beradi.
""", title="Nechta belgi bor?"),
        text(r"""
```python
print(len("Python"))      # 6
print(len("Salom dunyo"))  # 11  (bo'sh joy ham belgi!)
print(len(""))            # 0   (bo'sh matn)
```

`len()` — **butun son** (`int`) qaytaradi. Bo'sh joy, vergul, nuqta — hammasi sanaladi.

Indeks bilan bog'liqlik: matnning oxirgi indeksi `len(matn) - 1`. Shuning uchun `matn[len(matn) - 1]` va `matn[-1]` bir xil.
""", title="len() qoidalari"),
        callout('analogy', r"""
`len()` — **poyezddagi vagonlarni sanash**: ichida yo'lovchi bormi-yo'qmi, har bir vagon sanaladi — bo'sh joy ham «vagon».
""", title="Hayotiy o'xshatish"),
        example(r'''
parol = "qwerty123"
print("Parol uzunligi:", len(parol))
print(len(parol) >= 8)
''', title="Parol uzunligi", body="9 ta belgi: `Parol uzunligi: 9`. Taqqoslash `True` beradi — parol yetarlicha uzun."),
        example(r'''
gap = "Men Python o'rganyapman"
n = len(gap)
print(n)
print(gap[n - 1])
print(gap[n // 2])
''', title="Amaliy: o'rtadagi belgi", body="`n // 2` — o'rta indeks. `gap[n - 1]` esa oxirgi harf (`n`). Bu yerda `len()` natijasi arifmetikada ishlatilmoqda."),
        exercise('l17_inline_blank'),
        callout('warning', r"""
`len(12345)` — xato (`TypeError`): `len()` sonlarga emas, **matnga** (va keyingi modullardagi ro'yxatlarga) ishlaydi. Songa aylantirishni eslang: `len(str(12345))` → `5`.
""", title="Diqqat"),
        recap(["`len(matn)` — belgilar soni (son)", "bo'sh joy ham sanaladi", "oxirgi indeks = `len(matn) - 1`"], "`\"Salom\"` ni KATTA harflarda chiqarish uchun nima qilish kerak?"),
    ],
    [
        fill('l17_inline_blank', "Bo'sh joy", "So'z uzunligini chiqaring. `salom` → `5`.", 's = "salom"\nprint(___(s))\n', ['len'], section='inline', points=2, tests=[T('output_equals', '5', "Natija: 5")], hint="Uzunlik — inglizcha length.", explanation="`len(s)`."),
        predict('l17_quiz_1', "Bo'sh joy sanaladimi?", "Dastur nima chiqaradi?", code='print(len("a b c"))\n', answer="5", hint="Bo'sh joylarni ham sanang.", explanation="a, bo'sh joy, b, bo'sh joy, c = 5."),
        single('l17_quiz_2', "len() turi", "`len(\"abc\")` qanday tur qaytaradi?", options=[opt("str", False), opt("int", True), opt("bool", False)], hint="Uzunlik — son.", explanation="`len()` butun son qaytaradi."),
        predict('l17_quiz_3', "Oxirgi indeks", "Dastur nima chiqaradi?", code='s = "dastur"\nprint(len(s) - 1)\n', answer="5", hint="6 ta harf, oxirgi indeks?", explanation="Oxirgi indeks — 5."),
        code_task('l17_assignment', "Parol uzunligini tekshirish", r"""
Foydalanuvchi parol kiritadi. Dastur **parolning uzunligini** chiqarsin, keyin parol **kamida 8 ta belgidan iborat bo'lsa `True`, aks holda `False`** chiqarsin (ikki qator).

`qwerty123` →
```
9
True
```
""", starter_code='', points=10,
            tests=[T('output_equals', "9\nTrue", "qwerty123 → 9, True", stdin="qwerty123\n"), T('output_equals', "4\nFalse", "abcd → 4, False", stdin="abcd\n"), T('output_equals', "8\nTrue", "12345678 → 8, True", stdin="12345678\n", hidden=True)],
            hint="`len(parol)`, keyin `len(parol) >= 8`.", partial_solution='parol = input()\nprint(len(parol))\n# taqqoslash natijasini ham chiqaring\n',
            full_solution='parol = input()\nprint(len(parol))\nprint(len(parol) >= 8)\n', explanation="Taqqoslash `bool` beradi."),
        single('l17_practice_easy', "Easy: bo'sh matn", "`len(\"\")` nimaga teng?", section='practice', difficulty='easy', options=[opt("0", True), opt("1", False), opt("Xato", False)], hint="Ichida hech narsa yo'q.", explanation="Bo'sh matnning uzunligi 0."),
        code_task('l17_practice_medium', "Medium: raqamlar soni", r"""
Foydalanuvchi butun son kiritadi (masalan `12345`). Dastur nechta raqamdan iboratligini chiqarsin: `5`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "5", "12345 → 5", stdin="12345\n"), T('output_equals', "1", "7 → 1", stdin="7\n")], hint="`input()` allaqachon matn.", full_solution='son = input()\nprint(len(son))\n', explanation="`input()` matn qaytargani uchun `len()` darhol ishlaydi."),
        code_task('l17_practice_hard', "Hard: o'rtadagi harf", r"""
Foydalanuvchi **toq** uzunlikdagi so'z kiritadi. O'rtadagi harfni chiqaring. `kitob` → `t`, `olma` emas (faqat toq). `salom` → `l`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "t", "kitob → t", stdin="kitob\n"), T('output_equals', "l", "salom → l", stdin="salom\n"), T('output_equals', "d", "abdde → d", stdin="abdde\n", hidden=True)],
            hint="O'rta indeks — `len(s) // 2`.", full_solution='s = input()\nprint(s[len(s) // 2])\n', explanation="5 ta harf bo'lsa, o'rta indeks 5 // 2 = 2."),
    ])

# ==============================================================================
# 18-DARS
# ==============================================================================
LESSON_18 = L(18, "Matnni katta va kichik harflarga o'zgartirish", 12,
    "upper(), lower(), title(), capitalize() va strip() metodlarini ishlatish; metod nima ekanini va matn o'zgarmasligini (immutable) tushunish.",
    ["Metod (matn.metod())", "upper() / lower()", "title() / capitalize()", "strip()", "Matn o'zgarmaydi"],
    [
        text(r"""
Foydalanuvchi ismini `aZIZA`, `AZIZA` yoki `aziza` deb yozishi mumkin. Saqlashdan oldin hammasini bir xil ko'rinishga keltirish kerak. Buning uchun matn **metodlari** bor.
""", title="Har kim har xil yozadi"),
        text(r"""
**Metod** — ma'lumotga **nuqta bilan** chaqiriladigan funksiya: `matn.metod()`.

| Metod | Vazifasi | `"aZiza"` uchun |
|---|---|---|
| `upper()` | hammasi KATTA | `AZIZA` |
| `lower()` | hammasi kichik | `aziza` |
| `title()` | har so'z bosh harfi katta | `Aziza` |
| `capitalize()` | faqat birinchi harf katta | `Aziza` |
| `strip()` | chetdagi bo'sh joylarni olib tashlaydi | `"  a "` → `a` |
""", title="Eng kerakli metodlar"),
        callout('important', r"""
Matn **o'zgarmaydi** — metod **yangi** matn qaytaradi. `ism.upper()` ni yozib qo'ysangiz, `ism` o'sha-o'sha qoladi. Natijani saqlash yoki chiqarish kerak: `ism = ism.upper()`.
""", title="Eng ko'p uchraydigan xato"),
        example(r'''
ism = "aZiZa kArImOvA"
print(ism.upper())
print(ism.lower())
print(ism.title())
print(ism)
''', title="Uch xil ko'rinish", body="Oxirgi qator `ism` ning **o'zgarmaganini** ko'rsatadi: `aZiZa kArImOvA`."),
        example(r'''
kiritilgan = "   toshkent  "
shahar = kiritilgan.strip().capitalize()
print("[" + shahar + "]")
print(len(kiritilgan), len(shahar))
''', title="Amaliy: kiritilganni tozalash", body="Bo'sh joylar olib tashlanib, birinchi harf kattalashtirildi: `[Toshkent]`. Uzunliklar: `12` va `8`. Metodlarni zanjir qilib ulash mumkin."),
        exercise('l18_inline_fix'),
        recap(["`upper()`, `lower()`, `title()`, `capitalize()`, `strip()`", "metod yangi matn qaytaradi, eskisi o'zgarmaydi", "natijani o'zgaruvchiga saqlang"], "matn ichidan so'z qidirib, uni boshqasiga almashtirish mumkinmi?"),
    ],
    [
        fix_task('l18_inline_fix', "Natija saqlanmadi", "Kod `salom` chiqaryapti, lekin `SALOM` chiqishi kerak. Tuzating.", section='inline', points=2, starter_code='s = "salom"\ns.upper()\nprint(s)\n',
                 tests=[T('output_equals', 'SALOM', "Natija: SALOM")], hint="Metod natijasini o'zgaruvchiga saqlang.", full_solution='s = "salom"\ns = s.upper()\nprint(s)\n', explanation="`s.upper()` yangi matn qaytaradi; uni `s` ga saqlash kerak."),
        predict('l18_quiz_1', "title()", "Dastur nima chiqaradi?", code='print("men python o\'rganaman".title())\n', answer="Men Python O'Rganaman", hint="`title()` har so'z (va apostrofdan keyingi harf) bosh harfini kattalashtiradi.", explanation="Diqqat: `o'rganaman` dagi `R` ham katta bo'ldi — apostrof so'zni ajratadi."),
        single('l18_quiz_2', "Matn o'zgaradimi?", "`x = \"abc\"`; `x.upper()`; `print(x)` nima chiqaradi?", options=[opt("`ABC`", False), opt("`abc`", True), opt("Xato", False)], hint="Natija saqlanmadi.", explanation="Metod yangi matn qaytaradi, `x` o'zgarmaydi."),
        predict('l18_quiz_3', "strip()", "Dastur nima chiqaradi?", code='print(len("  ab  ".strip()))\n', answer="2", hint="Avval strip, keyin len.", explanation="`strip()` chetdagi bo'sh joylarni olib tashlaydi: `ab` — 2 ta harf."),
        code_task('l18_assignment', "Ismni tartibga keltirish", r"""
Foydalanuvchi ismini tartibsiz yozdi (masalan, `  aZIZA  `). Dastur uni tozalab, **birinchi harfi katta, qolganlari kichik** ko'rinishda chiqarsin. `  aZIZA  ` → `Aziza`.
""", starter_code='', points=10,
            tests=[T('output_equals', "Aziza", "  aZIZA   → Aziza", stdin="  aZIZA  \n"), T('output_equals', "Bobur", "BOBUR → Bobur", stdin="BOBUR\n"), T('output_equals', "Sardor", "sARDOR → Sardor", stdin="sARDOR\n", hidden=True)],
            hint="`strip()` va `capitalize()` ni ulang.", partial_solution='ism = input()\nism = ism.strip()\n# capitalize() bilan davom eting\n', full_solution='ism = input()\nprint(ism.strip().capitalize())\n', explanation="`capitalize()` birinchisini katta, qolganini kichik qiladi."),
        single('l18_practice_easy', "Easy: qaysi metod?", "Hamma harfni kichik qiladigan metod?", section='practice', difficulty='easy', options=[opt("`lower()`", True), opt("`small()`", False), opt("`strip()`", False)], hint="Inglizcha — pastki.", explanation="`lower()`."),
        code_task('l18_practice_medium', "Medium: baqiriq", r"""
Foydalanuvchi gap kiritadi. Dastur uni KATTA harflarda, oxiriga `!` qo'shib chiqarsin. `salom` → `SALOM!`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "SALOM!", "salom → SALOM!", stdin="salom\n"), T('output_equals', "MEN KELDIM!", "men keldim → MEN KELDIM!", stdin="men keldim\n")], hint="`upper()` va `+`.", full_solution='gap = input()\nprint(gap.upper() + "!")\n', explanation="`upper()` natijasiga `+` bilan `!` qo'shildi."),
        code_task('l18_practice_hard', "Hard: katta-kichikka e'tibor bermay taqqoslash", r"""
Foydalanuvchi parolni kiritadi. Agar u (katta-kichik harfga e'tibor bermasdan) `python` ga teng bo'lsa `True`, aks holda `False` chiqarsin. `PyThon` → `True`, `java` → `False`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "True", "PyThon → True", stdin="PyThon\n"), T('output_equals', "False", "java → False", stdin="java\n"), T('output_equals', "True", "PYTHON → True", stdin="PYTHON\n", hidden=True)],
            hint="Avval `lower()` qiling, keyin `==` bilan solishtiring.", full_solution='p = input()\nprint(p.lower() == "python")\n', explanation="Ikkala tomonni bir xil ko'rinishga keltirib taqqosladik."),
    ])

# ==============================================================================
# 19-DARS
# ==============================================================================
LESSON_19 = L(19, "Matnni qidirish va almashtirish", 13,
    "`in` operatori, find(), count(), startswith()/endswith() bilan qidirish va replace() bilan almashtirish.",
    ["in operatori", "find()", "count()", "startswith() / endswith()", "replace()"],
    [
        text(r"""
Telefondagi «qidiruv» — matn ichidan kerakli so'zni topadi. Word'dagi «Almashtirish» — so'zni boshqasiga o'zgartiradi. Python'da ham ikkala vazifa uchun tayyor vositalar bor.
""", title="Qidiruv va almashtirish"),
        text(r"""
| Vosita | Nima qiladi | Misol (`s = "olma va olcha"`) |
|---|---|---|
| `"ol" in s` | bor-yo'qligini tekshiradi (`True`/`False`) | `True` |
| `s.find("va")` | birinchi topilgan **indeks** (topilmasa `-1`) | `5` |
| `s.count("ol")` | necha marta uchrashini sanaydi | `2` |
| `s.startswith("olma")` | shu bilan boshlanadimi | `True` |
| `s.endswith("cha")` | shu bilan tugaydimi | `True` |
| `s.replace("ol", "OL")` | **hammasini** almashtirib, yangi matn qaytaradi | `OLma va OLcha` |
""", title="Qidirish va almashtirish vositalari"),
        callout('analogy', r"""
`find()` — kitobda **sahifa raqamini** topish: «bu so'z 5-o'rindan boshlanadi». Topilmasa — «umuman yo'q» ma'nosida `-1`.
""", title="Hayotiy o'xshatish"),
        example(r'''
s = "olma va olcha"
print("olma" in s)
print(s.find("va"))
print(s.count("ol"))
print(s.replace("ol", "OL"))
''', title="Hammasi birgalikda", body="Natija: `True`, `5`, `2`, `OLma va OLcha`. `replace` asl `s` ni o'zgartirmaydi — yangi matn beradi."),
        example(r'''
email = "aziza@gmail.com"
print("@" in email)
print(email.endswith(".com"))
print(email.find("@"))
domen = email.replace("aziza@", "")
print(domen)
''', title="Amaliy: email tekshirish", body="`@` bor, `.com` bilan tugaydi, `@` 5-indeksda. `replace` bilan foydalanuvchi nomi olib tashlanib, domen qoldi: `gmail.com`."),
        exercise('l19_inline_pred'),
        callout('warning', r"""
Qidiruv **katta-kichik harfni farqlaydi**: `"Ol" in "olma"` — `False`. Farqsiz qidirish uchun avval `lower()` qiling.
""", title="Diqqat"),
        recap(["`in` — bor-yo'qligi", "`find()` — indeks yoki `-1`", "`count()` — sanaydi", "`replace(eski, yangi)` — almashtiradi"], "matn ichiga o'zgaruvchi qiymatini chiroyli qo'yishning qulay usuli bormi?"),
    ],
    [
        predict('l19_inline_pred', "find() natijasi", "Dastur nima chiqaradi?", section='inline', code='print("salom".find("x"))\n', answer="-1", points=2, hint="Topilmasa nima qaytadi?", explanation="Topilmasa `find()` `-1` qaytaradi."),
        predict('l19_quiz_1', "count()", "Dastur nima chiqaradi?", code='print("banan".count("an"))\n', answer="2", hint="`an` ikki marta takrorlanadi.", explanation="ba-**an**-**an**: `an` 2 marta."),
        single('l19_quiz_2', "Katta-kichik harf", "`\"Py\" in \"python\"` natijasi?", options=[opt("`True`", False), opt("`False`", True), opt("`-1`", False)], hint="`P` katta, `p` kichik — turli belgi.", explanation="Qidiruv harf registrini farqlaydi."),
        predict('l19_quiz_3', "replace()", "Dastur nima chiqaradi?", code='s = "a-b-c"\nprint(s.replace("-", ""))\n', answer="abc", hint="`-` ni bo'sh matnga almashtiramiz.", explanation="Hamma `-` olib tashlandi."),
        code_task('l19_assignment', "So'zni tekshirish", r"""
Foydalanuvchi bir gap kiritadi. Dastur ikki qator chiqarsin: 1) gapda **`python`** so'zi (harf registrini hisobga olmasdan) bor-yo'qligi (`True`/`False`), 2) gapdagi **`a`** harflari soni.

`Men PYTHON o'rganaman` →
```
True
3
```
""", starter_code='', points=10,
            tests=[T('output_equals', "True\n3", "Men PYTHON o'rganaman → True, 3", stdin="Men PYTHON o'rganaman\n"), T('output_equals', "False\n0", "hello → False, 0", stdin="hello\n"), T('output_equals', "True\n0", "python → True, 0", stdin="python\n", hidden=True)],
            hint="Avval `lower()`; `in` va `count()`.", partial_solution='gap = input().lower()\nprint("python" in gap)\n# a harflari sonini ham chiqaring\n', full_solution='gap = input().lower()\nprint("python" in gap)\nprint(gap.count("a"))\n', explanation="`lower()` registrdan qutqardi; `count(\"a\")` harflarni sanadi."),
        single('l19_practice_easy', "Easy: tugash", "Fayl nomi `rasm.png` ni `.png` bilan tugashini tekshirish uchun qaysi metod?", section='practice', difficulty='easy', options=[opt("`startswith()`", False), opt("`endswith()`", True), opt("`count()`", False)], hint="Oxiri — end.", explanation="`endswith(\".png\")`."),
        code_task('l19_practice_medium', "Medium: telefon raqamini tozalash", r"""
Foydalanuvchi telefon raqamini `+998 90 123 45 67` ko'rinishida kiritadi. Dastur bo'sh joylarni olib tashlab chiqarsin: `+998901234567`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "+998901234567", "Bo'shliqlarsiz", stdin="+998 90 123 45 67\n"), T('output_equals', "998331112233", "Boshqa raqam", stdin="998 33 111 22 33\n")], hint="`replace(\" \", \"\")`.", full_solution='t = input()\nprint(t.replace(" ", ""))\n', explanation="Bo'sh joy bo'sh matnga almashtirildi."),
        code_task('l19_practice_hard', "Hard: so'zni yashirish (tsenzura)", r"""
Foydalanuvchi gap kiritadi. Dastur `yomon` so'zini (harf registridan qat'i nazar emas, aynan shu yozuvda) `*****` ga almashtirib chiqarsin, so'ngra ikkinchi qatorda necha marta almashtirilganini yozsin. `yomon kun, yomon ish` → `***** kun, ***** ish` va `2`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "***** kun, ***** ish\n2", "2 marta", stdin="yomon kun, yomon ish\n"), T('output_equals', "yaxshi kun\n0", "0 marta", stdin="yaxshi kun\n")],
            hint="Avval `count()` ni o'zgaruvchiga oling, keyin `replace()`.", partial_solution='gap = input()\nsoni = gap.count("yomon")\n# replace bilan almashtirib chiqaring, keyin soni\n', full_solution='gap = input()\nsoni = gap.count("yomon")\nprint(gap.replace("yomon", "*****"))\nprint(soni)\n', explanation="Almashtirishdan oldin sanash kerak — keyin so'z yo'qolib ketadi."),
    ])

# ==============================================================================
# 20-DARS
# ==============================================================================
LESSON_20 = L(20, "String formatlash — f-string", 13,
    "f-string yordamida o'zgaruvchilarni matn ichiga qo'yish, ifodalarni {} ichida hisoblash va :.2f bilan kasrni formatlash.",
    ["f-string", "{o'zgaruvchi}", "{ifoda}", ":.2f formati", "Ko'p qatorli chiqarish"],
    [
        text(r"""
Hozirgacha matn ichiga qiymat qo'yish uchun `+` va `str()` ishlatdik: `"Ism: " + ism + ", yosh: " + str(yosh)` — noqulay va xatolarga boy. **f-string** buni juda osonlashtiradi.
""", title="Chiroyli matn qurish"),
        text(r"""
Matn oldiga **`f`** harfi qo'yiladi, qiymatlar esa **`{ }`** ichiga yoziladi:

```python
ism = "Aziza"
yosh = 16
print(f"Ism: {ism}, yosh: {yosh}")
```

- `str()` kerak emas — son avtomatik matnga aylanadi.
- `{ }` ichida **ifoda** yozish mumkin: `{yosh + 1}`, `{ism.upper()}`, `{len(ism)}`.
- Kasr sonni chiroyli chiqarish: `{narx:.2f}` — **2 ta kasr xona** (`12.5` → `12.50`).
""", title="f-string"),
        callout('analogy', r"""
f-string — **ariza shabloni**: «Men, `{ism}`, `{shahar}` da yashayman». Bo'sh joylarga ma'lumot qo'yilib, tayyor matn chiqadi.
""", title="Hayotiy o'xshatish"),
        example(r'''
ism = "Aziza"
yosh = 16
print(f"Ism: {ism}, yosh: {yosh}")
print(f"Kelasi yil {yosh + 1} yoshda bo'ladi")
print(f"{ism.upper()} ismi {len(ism)} ta harfdan iborat")
''', title="f-string asoslari", body="Natija: `Ism: Aziza, yosh: 16`, `Kelasi yil 17 yoshda bo'ladi`, `AZIZA ismi 5 ta harfdan iborat`."),
        example(r'''
mahsulot = "Non"
narx = 4500
soni = 3
jami = narx * soni
kasr = 12.5
print(f"{mahsulot}: {narx} so'm x {soni} = {jami} so'm")
print(f"Kasr: {kasr:.2f}")
''', title="Amaliy: chek", body="`Non: 4500 so'm x 3 = 13500 so'm` va `Kasr: 12.50`. `:.2f` — doimo 2 ta kasr xona."),
        exercise('l20_inline_fill'),
        callout('tip', r"""
Qo'shtirnoq ichida `{` `}` ni o'zini chiqarish uchun ikkilang: `f"{{salom}}"` → `{salom}`. Odatda kerak bo'lmaydi.
"""),
        recap(["`f\"...{qiymat}...\"` — formatlash", "`{}` ichida ifoda yozish mumkin", "`:.2f` — 2 xonali kasr"], "keyingi modulda dastur turli sharoitda turlicha qaror qabul qilishni o'rganamiz. Bunga nima kerak, deb o'ylaysiz?"),
    ],
    [
        fill('l20_inline_fill', "f-string yarating", "Natija: `Salom, Ali!`", 'ism = "Ali"\nprint(___"Salom, {ism}!")\n', ['f'], section='inline', points=2, tests=[T('output_equals', 'Salom, Ali!', "Natija: Salom, Ali!")], hint="Matn oldiga bitta harf qo'yiladi.", explanation="`f\"...\"`."),
        predict('l20_quiz_1', "f-string natijasi", "Dastur nima chiqaradi?", code='a = 4\nb = 5\nprint(f"{a} * {b} = {a * b}")\n', answer="4 * 5 = 20", hint="`{}` ichidagi ifoda hisoblanadi.", explanation="`{a * b}` → 20."),
        single('l20_quiz_2', "f harfi", "`print(\"Yosh: {yosh}\")` (f siz) nima chiqaradi?", options=[opt("`Yosh: {yosh}` (aynan shunday)", True), opt("`Yosh: 16`", False), opt("Xato", False)], hint="`f` yo'q bo'lsa — oddiy matn.", explanation="`f` bo'lmasa, `{}` oddiy belgi sifatida chiqadi."),
        predict('l20_quiz_3', "Kasr formati", "Dastur nima chiqaradi?", code='x = 3.14159\nprint(f"{x:.2f}")\n', answer="3.14", hint="2 ta kasr xona.", explanation="`:.2f` — ikki xonaga yaxlitlash."),
        code_task('l20_assignment', "Foydalanuvchi kartochkasi", r"""
Foydalanuvchi **ism**, **yosh** va **shahar**ni kiritadi (uchta `input()`). **f-string** yordamida bir qatorda chiqaring:

`Aziza, 16 yosh, Toshkent shahri`
""", starter_code='', points=10,
            tests=[T('output_equals', "Aziza, 16 yosh, Toshkent shahri", "Aziza/16/Toshkent", stdin="Aziza\n16\nToshkent\n"), T('output_equals', "Bobur, 20 yosh, Samarqand shahri", "Bobur/20/Samarqand", stdin="Bobur\n20\nSamarqand\n"), T('code_regex', r'f["\']', "f-string ishlatilgan")],
            hint="`print(f\"{ism}, {yosh} yosh, {shahar} shahri\")`.", partial_solution='ism = input()\nyosh = input()\nshahar = input()\n# f-string bilan chiqaring\n', full_solution='ism = input()\nyosh = input()\nshahar = input()\nprint(f"{ism}, {yosh} yosh, {shahar} shahri")\n', explanation="f-string ichida `int()` shart emas — yoshni matn sifatida qo'yaverdik."),
        single('l20_practice_easy', "Easy: formatlash", "Qaysi yozuv f-string?", section='practice', difficulty='easy', options=[opt("`f\"Salom {ism}\"`", True), opt("`\"Salom {ism}\"`", False), opt("`\"Salom \" + {ism}`", False)], hint="Qo'shtirnoq oldida `f`.", explanation="f-string — qo'shtirnoq oldida `f` bor."),
        code_task('l20_practice_medium', "Medium: chegirma", r"""
Foydalanuvchi mahsulot narxini (butun son) kiritadi. Dastur 10% chegirmali narxni **2 xonali kasr** bilan chiqarsin: `Chegirma bilan: 9000.00`. Kiritish `10000`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Chegirma bilan: 9000.00", "10000 → 9000.00", stdin="10000\n"), T('output_equals', "Chegirma bilan: 45.00", "50 → 45.00", stdin="50\n"), T('code_contains', ':.2f', "`:.2f` ishlatilgan")],
            hint="`narx * 0.9`, chiqarishda `{x:.2f}`.", full_solution='narx = int(input())\nprint(f"Chegirma bilan: {narx * 0.9:.2f}")\n', explanation="`{ifoda:.2f}` ifodani hisoblab, formatlaydi."),
        code_task('l20_practice_hard', "Hard: jadval qatori", r"""
Foydalanuvchi mahsulot nomi, narxi (butun) va sonini (butun) kiritadi. Quyidagi shaklda chiqaring (jami 2 xonali kasr bilan):

`Non | 4500 x 3 = 13500.00`
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Non | 4500 x 3 = 13500.00", "Non/4500/3", stdin="Non\n4500\n3\n"), T('output_equals', "Sut | 12000 x 2 = 24000.00", "Sut/12000/2", stdin="Sut\n12000\n2\n"), T('code_regex', r'f["\']', "f-string ishlatilgan")],
            hint="Narx va sonni `int()` bilan aylantiring.", partial_solution='nom = input()\nnarx = int(input())\nsoni = int(input())\n# f-string bilan chiqaring\n', full_solution='nom = input()\nnarx = int(input())\nsoni = int(input())\nprint(f"{nom} | {narx} x {soni} = {narx * soni:.2f}")\n', explanation="Ifoda `{narx * soni:.2f}` ichida hisoblandi va formatlandi."),
    ])

LESSONS = [LESSON_16, LESSON_17, LESSON_18, LESSON_19, LESSON_20]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("3-modul yakuniy nazorati: Matnlar (String)", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — ism va foydalanuvchi ma'lumotlarini formatlovchi dastur.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m3_a_t1', "Indeks", "`\"Python\"[0]` nima beradi?", section='assessment', points=2, options=[opt("`P`", True), opt("`y`", False), opt("`n`", False)], explanation="Indeks 0 dan boshlanadi."),
    single('m3_a_t2', "len()", "`len(\"a b\")` nimaga teng?", section='assessment', points=2, options=[opt("2", False), opt("3", True), opt("1", False)], explanation="Bo'sh joy ham belgi."),
    single('m3_a_t3', "Metod natijasi", "`s.lower()` nima qiladi?", section='assessment', points=2, options=[opt("`s` ni o'zgartiradi", False), opt("Kichik harfli YANGI matn qaytaradi", True), opt("`s` ni o'chiradi", False)], explanation="Matn o'zgarmaydi, yangi matn qaytadi."),
    single('m3_a_t4', "find() topilmasa", "`find()` matn topolmasa nima qaytaradi?", section='assessment', points=2, options=[opt("0", False), opt("-1", True), opt("Xato", False)], explanation="Topilmasa `-1`."),
    multiple('m3_a_t5', "To'g'ri f-stringlar", "Qaysi qatorlar `Salom, Ali!` chiqaradi (`ism = \"Ali\"`)?", section='assessment', points=2, options=[opt("`print(f\"Salom, {ism}!\")`", True), opt("`print(\"Salom, \" + ism + \"!\")`", True), opt("`print(\"Salom, {ism}!\")`", False), opt("`print(f\"Salom, ism!\")`", False)], explanation="Ikki usul ham to'g'ri; `f` siz yoki `{}` siz — noto'g'ri."),
    predict('m3_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='s = "dasturlash"\nprint(s[:3] + s[-3:])\n', answer="dasash", explanation="`das` + `ash`."),
    predict('m3_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='s = " Salom "\nprint(len(s.strip()), s.strip().upper())\n', answer="5 SALOM", explanation="`strip()` bo'sh joylarni oladi: 5 ta harf."),
    predict('m3_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='x = 7.5\nprint(f"{x:.2f} / {int(x)} / {x * 2}")\n', answer="7.50 / 7 / 15.0", explanation="`:.2f` → 7.50; `int(7.5)` → 7; `7.5*2` → 15.0."),
    fix_task('m3_a_f1', "Xatoni tuzating (1)", "Dastur `SALOM` chiqarishi kerak.", section='assessment', points=4, starter_code='s = "salom"\ns.upper()\nprint(s)\n', tests=[T('output_equals', "SALOM", "Natija: SALOM")], hint="Natijani saqlang.", full_solution='s = "salom"\ns = s.upper()\nprint(s)\n', explanation="Metod yangi matn qaytaradi."),
    fix_task('m3_a_f2', "Xatoni tuzating (2)", "Dastur `Yosh: 18` chiqarishi kerak, lekin xato beryapti.", section='assessment', points=4, starter_code='yosh = 18\nprint(f"Yosh: " + yosh)\n', tests=[T('output_equals', "Yosh: 18", "Natija: Yosh: 18")], hint="f-string ishlating.", full_solution='yosh = 18\nprint(f"Yosh: {yosh}")\n', explanation="Matn+son — TypeError; f-string buni hal qiladi."),
    code_task('m3_a_project', "Mini-loyiha: Foydalanuvchi ma'lumotlarini formatlash", r"""
Dastur foydalanuvchidan ketma-ket kiritishni so'raydi: **to'liq ism** (bo'sh joy orqali ism va familiya, tartibsiz harflar bilan, chetlarda ortiqcha bo'sh joy bo'lishi mumkin), **yosh** (butun son) va **email**.

Chiqarish (aynan 5 qator, `f-string` bilan):

```
Ism: Aziza
Familiya: Karimova
Yosh: 16 (kelasi yil 17)
Login: aziza_karimova (14 belgi)
Domen: gmail.com
```

- Ism va familiya — birinchi harfi katta, qolgani kichik.
- `Login` — kichik harfli `ism_familiya`; qavs ichida shu loginning uzunligi.
- `Domen` — emailning `@` dan keyingi qismi (5-qator): `Domen: gmail.com`.

Kiritish: `  aZIZA kARIMOVA `, `16`, `aziza@gmail.com`. 
""", section='project', points=15, difficulty='medium', unlock=3, starter_code='# Foydalanuvchi ma\'lumotlari\n',
        expected_output_example="Ism: Aziza\nFamiliya: Karimova\nYosh: 16 (kelasi yil 17)\nLogin: aziza_karimova (14 belgi)\nDomen: gmail.com",
        tests=[T('output_equals', "Ism: Aziza\nFamiliya: Karimova\nYosh: 16 (kelasi yil 17)\nLogin: aziza_karimova (14 belgi)\nDomen: gmail.com", "Aziza Karimova uchun to'liq natija", stdin="  aZIZA kARIMOVA \n16\naziza@gmail.com\n"),
               T('output_equals', "Ism: Bobur\nFamiliya: Aliyev\nYosh: 20 (kelasi yil 21)\nLogin: bobur_aliyev (12 belgi)\nDomen: mail.ru", "Boshqa kiritish bilan ham to'g'ri", stdin="BOBUR aliyev\n20\nbobur@mail.ru\n"),
               T('output_equals', "Ism: Sardor\nFamiliya: Tursunov\nYosh: 9 (kelasi yil 10)\nLogin: sardor_tursunov (15 belgi)\nDomen: uz.org", "Yashirin test", stdin="sardor Tursunov\n9\nx@uz.org\n", hidden=True),
               T('code_regex', r'f["\']', "f-string ishlatilgan"), T('code_contains', 'strip', "`strip()` ishlatilgan"), T('code_contains', 'len(', "`len()` ishlatilgan")],
        hint="1) `to_liq = input().strip()`; 2) `ism, familiya = to_liq.split()` — bu yangi buyruq: matnni bo'sh joy bo'yicha ikkiga ajratadi (misol: `\"a b\".split()` → ikkita qiymat). 3) `ism.capitalize()`; 4) login: `ism.lower() + \"_\" + familiya.lower()`; 5) domen: `email[email.find(\"@\") + 1:]`.",
        partial_solution='to_liq = input().strip()\nism, familiya = to_liq.split()\nyosh = int(input())\nemail = input()\nism = ism.capitalize()\nfamiliya = familiya.capitalize()\n# login, domen hisoblab f-string bilan chiqaring\n',
        full_solution='to_liq = input().strip()\nism, familiya = to_liq.split()\nyosh = int(input())\nemail = input()\nism = ism.capitalize()\nfamiliya = familiya.capitalize()\nlogin = ism.lower() + "_" + familiya.lower()\ndomen = email[email.find("@") + 1:]\nprint(f"Ism: {ism}")\nprint(f"Familiya: {familiya}")\nprint(f"Yosh: {yosh} (kelasi yil {yosh + 1})")\nprint(f"Login: {login} ({len(login)} belgi)")\nprint(f"Domen: {domen}")\n',
        explanation="Loyiha strip, capitalize, lower, len, indeks/kesim, find va f-string ni birlashtiradi."),
])

# ==============================================================================
# 1-TAKRORLASH (REVIEW 1): 2- va 3-modullar
# ==============================================================================
REVIEW_1 = module_assessment("1-takrorlash (Review 1): 2- va 3-modullar", r"""
2-modul (**o'zgaruvchilar, turlar, input()**) va 3-modul (**matnlar**) mavzulari **aralash** holda takrorlanadi.
Savollar tartibi ataylab aralashtirilgan — bu xotirani mustahkamlaydi (*spaced repetition*). Ball olish uchun **70%** kerak; istagancha qayta urinishingiz mumkin.
""", [
    single('r1_t1', "int yoki str?", "`input()` dan olingan `\"25\"` ni songa aylantiruvchi funksiya?", section='assessment', points=2, options=[opt("`str()`", False), opt("`int()`", True), opt("`type()`", False)], explanation="`int(\"25\")` → 25."),
    single('r1_t2', "Indeks (3-modul)", "`\"salom\"[-1]` nima beradi?", section='assessment', points=2, options=[opt("`s`", False), opt("`m`", True), opt("`o`", False)], explanation="`-1` — oxirgi harf: `m`."),
    single('r1_t3', "bool (2-modul)", "`10 % 3 == 1` natijasi?", section='assessment', points=2, options=[opt("`True`", True), opt("`False`", False), opt("`1`", False)], explanation="10 % 3 = 1, taqqoslash `True`."),
    single('r1_t4', "replace (3-modul)", "`\"a,b\".replace(\",\", \"-\")` nima beradi?", section='assessment', points=2, options=[opt("`a-b`", True), opt("`a,b`", False), opt("`ab`", False)], explanation="Vergul chiziqqa almashdi."),
    multiple('r1_t5', "Yaroqli nomlar (2-modul)", "Qaysi o'zgaruvchi nomlari to'g'ri?", section='assessment', points=2, options=[opt("`jami_narx`", True), opt("`_x`", True), opt("`2-son`", False), opt("`jami narx`", False)], explanation="Raqam bilan boshlanmaydi; `-` va bo'sh joy mumkin emas."),
    predict('r1_p1', "Aralash natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = "7"\nb = 3\nprint(a * b, int(a) * b)\n', answer="777 21", explanation="Matn takrorlanadi, son ko'paytiriladi."),
    predict('r1_p2', "Aralash natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='ism = "Dilnoza"\nprint(f"{ism[0]}.{len(ism)}")\n', answer="D.7", explanation="Birinchi harf va uzunlik."),
    predict('r1_p3', "Aralash natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='x = 17\nprint(x // 5, x % 5, round(x / 5, 1))\n', answer="3 2 3.4", explanation="17 // 5 = 3; 17 % 5 = 2; 17 / 5 = 3.4."),
    fix_task('r1_f1', "Tuzating: tur xatosi", "Dastur ikki sonning yig'indisini chiqarishi kerak (`4` va `5` → `9`).", section='assessment', points=4, starter_code='a = input()\nb = input()\nprint(f"{a + b}")\n', tests=[T('output_equals', "9", "4, 5 → 9", stdin="4\n5\n"), T('output_equals', "30", "10, 20 → 30", stdin="10\n20\n")], hint="`input()` matn qaytaradi.", full_solution='a = int(input())\nb = int(input())\nprint(f"{a + b}")\n', explanation="`int()` yetishmayotgan edi."),
    fix_task('r1_f2', "Tuzating: indeks", "Dastur so'zning **oxirgi harfini** chiqarishi kerak (`kitob` → `b`), lekin xato beryapti.", section='assessment', points=4, starter_code='s = input()\nprint(s[len(s)])\n', tests=[T('output_equals', "b", "kitob → b", stdin="kitob\n"), T('output_equals', "a", "olma → a", stdin="olma\n")], hint="Oxirgi indeks `len(s) - 1`.", full_solution='s = input()\nprint(s[len(s) - 1])\n', explanation="`len(s)` — mavjud bo'lmagan indeks; `-1` kerak."),
    code_task('r1_c1', "Amaliy: ism va yosh", "Foydalanuvchi ism va tug'ilgan yilini kiritadi (joriy yil 2026). Dastur `Aziza, 21 yosh` shaklida (ism bosh harfi katta) chiqarsin. `aZIZA`, `2005` → `Aziza, 21 yosh`.", section='assessment', points=8, difficulty='medium',
              tests=[T('output_equals', "Aziza, 21 yosh", "aZIZA / 2005", stdin="aZIZA\n2005\n"), T('output_equals', "Bobur, 30 yosh", "BOBUR / 1996", stdin="BOBUR\n1996\n"), T('code_regex', r'f["\']', "f-string ishlatilgan")],
              hint="`capitalize()`, `2026 - yil`, f-string.", partial_solution='ism = input().capitalize()\nyil = int(input())\n# yoshni hisoblab f-string bilan chiqaring\n', full_solution='ism = input().capitalize()\nyil = int(input())\nprint(f"{ism}, {2026 - yil} yosh")\n', explanation="Tur o'zgartirish, arifmetika, matn metodi va f-string birga ishlatildi."),
    code_task('r1_c2', "Amaliy: narx va chegirma", "Foydalanuvchi mahsulot nomini va narxini (butun son) kiritadi. Dastur `NON: 4500 so'm (4 ta belgi)` ko'rinishida chiqarsin: nom KATTA harflarda, narx, nomning uzunligi. `non`, `4500` → `NON: 4500 so'm (3 ta belgi)`.", section='assessment', points=8, difficulty='medium',
              tests=[T('output_equals', "NON: 4500 so'm (3 ta belgi)", "non / 4500", stdin="non\n4500\n"), T('output_equals', "SUT: 12000 so'm (3 ta belgi)", "sut / 12000", stdin="sut\n12000\n"), T('output_equals', "KEFIR: 15000 so'm (5 ta belgi)", "kefir / 15000", stdin="kefir\n15000\n", hidden=True)],
              hint="`nom.upper()` va `len(nom)`.", full_solution='nom = input()\nnarx = int(input())\nprint(f"{nom.upper()}: {narx} so\'m ({len(nom)} ta belgi)")\n', explanation="Matn metodlari, len() va f-string aralash."),
    code_task('r1_c3', "Amaliy: login yaratish", "Foydalanuvchi email kiritadi (`aziza@gmail.com`). Dastur `@` dan oldingi qismni (login) KATTA harflarda, uzunligi bilan chiqarsin: `AZIZA (5)`.", section='assessment', points=10, difficulty='hard',
              tests=[T('output_equals', "AZIZA (5)", "aziza@gmail.com", stdin="aziza@gmail.com\n"), T('output_equals', "BOBUR123 (8)", "bobur123@mail.ru", stdin="bobur123@mail.ru\n"), T('output_equals', "X (1)", "x@uz.org", stdin="x@uz.org\n", hidden=True)],
              hint="`find(\"@\")` — `@` indeksi; kesim `[:indeks]`.", partial_solution='email = input()\nindeks = email.find("@")\nlogin = email[:indeks]\n# upper va len bilan chiqaring\n', full_solution='email = input()\nlogin = email[:email.find("@")]\nprint(f"{login.upper()} ({len(login)})")\n', explanation="`find()`, kesim, `upper()`, `len()` va f-string birga."),
], pass_percent=70)

REVIEWS = [REVIEW_1]
