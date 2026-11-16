"""Python — 0 dan boshlash · 4-modul: Qaror qabul qilish (Conditions) (21–26-darslar)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 4,
    'title': "Qaror qabul qilish (Conditions)",
    'description': "Dastur sharoitga qarab turlicha ishlashi: if, else, elif, taqqoslash va mantiqiy operatorlar, ichma-ich shartlar.",
}

# ==============================================================================
# 21-DARS
# ==============================================================================
LESSON_21 = L(21, "Shart operatori — if", 12,
    "if operatori bilan shartni tekshirish, ikki nuqta va chekinish (4 ta bo'sh joy) qoidasini bilish.",
    ["if", "Shart (bool)", "Ikki nuqta :", "Chekinish (indentation)", "Blok"],
    [
        text(r"""
«Agar yomg'ir yog'sa — soyabon olaman.» Biz kuniga o'nlab marta shunday qaror qabul qilamiz. Dastur ham **shartga qarab** ba'zi buyruqlarni bajarishi yoki bajarmasligi kerak — buning uchun **`if`** (inglizcha «agar») ishlatiladi.
""", title="Agar... bo'lsa..."),
        text(r"""
```python
yosh = 20
if yosh >= 18:
    print("Siz voyaga yetgansiz")
print("Dastur tugadi")
```

Qoidalar:

1. `if` dan keyin **shart** yoziladi — natijasi `True` yoki `False` bo'ladigan ifoda (`yosh >= 18`).
2. Shartdan keyin **ikki nuqta `:`** shart.
3. Shart rost bo'lganda bajariladigan qatorlar **4 ta bo'sh joy** (chekinish) bilan suriladi — bu **blok** deyiladi.
4. Chekinishsiz qator shartga bog'liq emas — har doim bajariladi.
""", title="if tuzilishi"),
        callout('analogy', r"""
`if` — **svetofor**: «Agar yashil yonsa — yur». Shart bajarilmasa, blok shunchaki o'tkazib yuboriladi.
""", title="Hayotiy o'xshatish"),
        callout('important', r"""
Python'da blokni chekinish belgilaydi (boshqa tillardagi `{ }` o'rniga). Chekinishni unutsangiz — `IndentationError`, `:` ni unutsangiz — `SyntaxError`.
""", title="Eng muhim qoida"),
        example(r'''
harorat = 35
if harorat > 30:
    print("Havo issiq!")
    print("Ko'proq suv iching")
print("Xayr")
''', title="Shart rost", body="`35 > 30` rost, shuning uchun ikkala chekinishli qator bajariladi. Oxirgi `print` chekinishsiz — har doim chiqadi."),
        example(r'''
balans = 5000
narx = 8000
if balans >= narx:
    print("Xarid amalga oshdi")
print("Balans:", balans)
''', title="Amaliy: xarid", body="Balans yetmaydi (`5000 >= 8000` yolg'on) — shu sababli `Xarid amalga oshdi` chiqmaydi, faqat `Balans: 5000`. Shart yolg'on bo'lsa, blok o'tkazib yuboriladi."),
        exercise('l21_inline_fix'),
        recap(["`if shart:` — shart rost bo'lsa blok bajariladi", "`:` va 4 ta bo'sh joy chekinish shart", "yolg'on bo'lsa blok o'tkazib yuboriladi"], "shart yolg'on bo'lsa, dastur muqobil yo'ldan ketishi mumkinmi?"),
    ],
    [
        fix_task('l21_inline_fix', "Chekinishni tuzating", "Kod xato beryapti. Tuzating — natija: `Katta`", section='inline', points=2, starter_code='son = 10\nif son > 5:\nprint("Katta")\n', tests=[T('output_equals', 'Katta', "Natija: Katta")], hint="`if` ichidagi qator surilishi kerak.", full_solution='son = 10\nif son > 5:\n    print("Katta")\n', explanation="Blok ichidagi qator 4 ta bo'sh joy bilan suriladi."),
        predict('l21_quiz_1', "Shart rostmi?", "Dastur nima chiqaradi?", code='x = 3\nif x > 5:\n    print("A")\nprint("B")\n', answer="B", hint="`3 > 5` yolg'on.", explanation="Blok o'tkazib yuborildi, `print(\"B\")` har doim ishlaydi."),
        single('l21_quiz_2', "Ikki nuqta", "`if x > 5` dan keyin nima yetishmayapti?", options=[opt("Ikki nuqta `:`", True), opt("Nuqta `.`", False), opt("Vergul `,`", False)], hint="Blok boshlanishini bildiradi.", explanation="`if x > 5:` — ikki nuqta shart."),
        predict('l21_quiz_3', "Ikkita qator", "Dastur nima chiqaradi?", code='n = 8\nif n > 5:\n    print("1")\n    print("2")\nprint("3")\n', answer="1\n2\n3", hint="Ikkala qator ham chekinishli.", explanation="Shart rost: 1 va 2 chiqadi, 3 har doim chiqadi."),
        code_task('l21_assignment', "Musiqa ovozi", r"""
Foydalanuvchi ovoz balandligini (0–100, butun son) kiritadi. Agar u **80 dan katta** bo'lsa, `Ovoz juda baland!` deb chiqarsin. Aks holda **hech narsa chiqarmasin**.
""", starter_code='', points=10,
            tests=[T('output_equals', "Ovoz juda baland!", "90 → ogohlantirish", stdin="90\n"), T('output_equals', "", "50 → hech narsa", stdin="50\n"), T('output_equals', "", "80 → hech narsa (80 dan katta emas)", stdin="80\n", hidden=True), T('code_contains', 'if ', "`if` ishlatilgan")],
            hint="`if ovoz > 80:` va ichida print.", partial_solution='ovoz = int(input())\n# if bilan tekshiring\n', full_solution='ovoz = int(input())\nif ovoz > 80:\n    print("Ovoz juda baland!")\n', explanation="`>` qat'iy katta; 80 ning o'zida shart yolg'on."),
        single('l21_practice_easy', "Easy: blok", "Qaysi qator `if` bloki ichida bajariladi?", section='practice', difficulty='easy', options=[opt("Chekinishli qator", True), opt("Chekinishsiz qator", False), opt("Hamma qator", False)], hint="4 ta bo'sh joy.", explanation="Faqat chekinishli qatorlar blokka kiradi."),
        code_task('l21_practice_medium', "Medium: ball", r"""
Foydalanuvchi test ballini kiritadi. Agar ball **60 yoki undan ko'p** bo'lsa, `O'tdingiz` chiqarsin, aks holda hech narsa.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "O'tdingiz", "75", stdin="75\n"), T('output_equals', "O'tdingiz", "60", stdin="60\n"), T('output_equals', "", "59", stdin="59\n")], hint="`>=` — katta yoki teng.", full_solution='ball = int(input())\nif ball >= 60:\n    print("O\'tdingiz")\n', explanation="Chegaraviy qiymat (60) ham kiradi — `>=`."),
        code_task('l21_practice_hard', "Hard: ikkita mustaqil shart", r"""
Foydalanuvchi son kiritadi. **Alohida ikkita `if`** yozing: agar son 0 dan katta bo'lsa — `Musbat`; agar son juft bo'lsa (`% 2 == 0`) — `Juft`. Ikkalasi ham rost bo'lsa, ikkala qator chiqadi. Masalan, `4` → `Musbat` va `Juft`; `3` → `Musbat`; `-2` → `Juft`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Musbat\nJuft", "4", stdin="4\n"), T('output_equals', "Musbat", "3", stdin="3\n"), T('output_equals', "Juft", "-2", stdin="-2\n"), T('output_equals', "", "-3", stdin="-3\n", hidden=True)],
            hint="Ikkita alohida `if` — bir-biriga bog'liq emas.", full_solution='n = int(input())\nif n > 0:\n    print("Musbat")\nif n % 2 == 0:\n    print("Juft")\n', explanation="Mustaqil `if`lar har biri o'z shartini tekshiradi."),
    ])

# ==============================================================================
# 22-DARS
# ==============================================================================
LESSON_22 = L(22, "else operatori", 11,
    "if ... else bilan ikkita yo'ldan birini tanlash.",
    ["else", "Ikki yo'l", "if/else bloklari", "Juft/toq, o'tdi/o'tmadi"],
    [
        text(r"""
«Agar yomg'ir yog'sa — soyabon olaman, **aks holda** — shapka kiyaman.» Ikki yo'ldan **albatta bittasi** tanlanadi. Python'da «aks holda» — **`else`**.
""", title="Aks holda..."),
        text(r"""
```python
yosh = 15
if yosh >= 18:
    print("Kirishingiz mumkin")
else:
    print("Kirish mumkin emas")
```

- `else:` — `if` bilan **bir xil chekinishda**, oxirida `:`.
- `else` ga **shart yozilmaydi** — u «yuqoridagi shart bajarilmasa» degani.
- Ikki blokdan **aniq bittasi** bajariladi.
""", title="if ... else"),
        callout('analogy', r"""
`if/else` — **yo'l ayrilishi**: chapga yoki o'ngga — ikkalasiga birdan ketib bo'lmaydi.
""", title="Hayotiy o'xshatish"),
        example(r'''
son = 7
if son % 2 == 0:
    print("Juft")
else:
    print("Toq")
''', title="Juft yoki toq", body="`7 % 2` = 1, shart yolg'on — `else` bloki ishlaydi: `Toq`."),
        example(r'''
ball = 55
if ball >= 60:
    print("Imtihondan o'tdingiz")
else:
    print("Qayta topshirasiz")
    print("Yetishmayotgan ball:", 60 - ball)
''', title="Amaliy: imtihon natijasi", body="55 < 60, shuning uchun `else` bloki ishlaydi va yetishmayotgan ball ham chiqadi: `5`. `else` blokida bir nechta qator bo'lishi mumkin."),
        exercise('l22_inline_blank'),
        callout('warning', r"""
`else` ni **yolg'iz** yozib bo'lmaydi — u doim `if` dan keyin keladi. Alohida `else:` → `SyntaxError`.
"""),
        recap(["`else` — «aks holda»", "ikki blokdan bittasi bajariladi", "`else` ga shart yozilmaydi"], "ikkitadan ko'p yo'l kerak bo'lsa-chi? Masalan, baho: 5, 4, 3 yoki 2?"),
    ],
    [
        fill('l22_inline_blank', "Bo'sh joy", "`n` musbat bo'lsa `Musbat`, aks holda `Musbat emas`. `n = -1` uchun natija: `Musbat emas`.", 'n = -1\nif n > 0:\n    print("Musbat")\n___:\n    print("Musbat emas")\n', ['else'], section='inline', points=2, tests=[T('output_equals', 'Musbat emas', "Natija to'g'ri")], hint="Aks holda — inglizcha?", explanation="`else:`."),
        predict('l22_quiz_1', "Qaysi blok?", "Dastur nima chiqaradi?", code='x = 4\nif x > 10:\n    print("A")\nelse:\n    print("B")\n', answer="B", hint="`4 > 10` yolg'on.", explanation="`else` bloki ishladi."),
        single('l22_quiz_2', "else sharti", "`else` dan keyin shart yozish kerakmi?", options=[opt("Ha, har doim", False), opt("Yo'q, `else:` shartsiz yoziladi", True), opt("Faqat sonlar uchun", False)], hint="`else` — «boshqa hamma holat».", explanation="`else` ga shart yozilmaydi."),
        predict('l22_quiz_3', "Ikkita blok", "Dastur nima chiqaradi?", code='n = 10\nif n > 5:\n    print("katta")\nelse:\n    print("kichik")\nprint("tamom")\n', answer="katta\ntamom", hint="`else` ishlamaydi, oxirgi print har doim.", explanation="Shart rost: `katta`; `tamom` har doim."),
        code_task('l22_assignment', "Juft yoki toq", r"""
Foydalanuvchi butun son kiritadi. Juft bo'lsa `Juft`, toq bo'lsa `Toq` deb chiqarsin (`if/else` bilan).
""", starter_code='', points=10, tests=[T('output_equals', "Juft", "10", stdin="10\n"), T('output_equals', "Toq", "7", stdin="7\n"), T('output_equals', "Juft", "0", stdin="0\n", hidden=True), T('output_equals', "Toq", "-3", stdin="-3\n", hidden=True), T('code_contains', 'else', "`else` ishlatilgan")],
            hint="`son % 2 == 0` — juft.", partial_solution='son = int(input())\nif son % 2 == 0:\n    print("Juft")\n# else qismini yozing\n', full_solution='son = int(input())\nif son % 2 == 0:\n    print("Juft")\nelse:\n    print("Toq")\n', explanation="Qoldiq 0 bo'lsa juft, aks holda toq."),
        single('l22_practice_easy', "Easy: tanlov", "`if/else` da nechta blok bajariladi?", section='practice', difficulty='easy', options=[opt("Ikkalasi ham", False), opt("Aynan bittasi", True), opt("Hech biri", False)], hint="Yo'l ayrilishi.", explanation="Yo'llardan aynan bittasi."),
        code_task('l22_practice_medium', "Medium: katta son", r"""
Foydalanuvchi ikkita butun son kiritadi. Katta bo'lganini chiqarsin (teng bo'lsa — ikkinchisini). `3`, `9` → `9`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "9", "3, 9", stdin="3\n9\n"), T('output_equals', "8", "8, 2", stdin="8\n2\n"), T('output_equals', "5", "5, 5", stdin="5\n5\n")], hint="`if a > b: ... else: ...`.", full_solution='a = int(input())\nb = int(input())\nif a > b:\n    print(a)\nelse:\n    print(b)\n', explanation="Taqqoslab, kattasini chiqardik."),
        code_task('l22_practice_hard', "Hard: kirish chiptasi", r"""
Foydalanuvchi yoshini kiritadi. Agar 12 dan **kichik** bo'lsa, `Chipta: 5000 so'm`, aks holda `Chipta: 10000 so'm` deb chiqarsin. Keyin (har doim) ikkinchi qatorda `Yaxshi dam oling!` chiqsin.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Chipta: 5000 so'm\nYaxshi dam oling!", "8", stdin="8\n"), T('output_equals', "Chipta: 10000 so'm\nYaxshi dam oling!", "12", stdin="12\n"), T('output_equals', "Chipta: 10000 so'm\nYaxshi dam oling!", "40", stdin="40\n")], hint="Oxirgi `print` chekinishsiz.", full_solution='yosh = int(input())\nif yosh < 12:\n    print("Chipta: 5000 so\'m")\nelse:\n    print("Chipta: 10000 so\'m")\nprint("Yaxshi dam oling!")\n', explanation="Chekinishsiz qator har doim bajariladi."),
    ])

# ==============================================================================
# 23-DARS
# ==============================================================================
LESSON_23 = L(23, "elif orqali bir nechta shartni tekshirish", 13,
    "elif bilan ikkitadan ko'p yo'ldan birini tanlash va shartlar tartibining ahamiyatini tushunish.",
    ["elif", "Shartlar zanjiri", "Tartib muhim", "Birinchi rost shart"],
    [
        text(r"""
Baho qo'yishda ikki yo'l yetmaydi: 90+ → «5», 70+ → «4», 50+ → «3», aks holda «2». Ko'p yo'l uchun **`elif`** (*else if* — «aks holda, agar») ishlatiladi.
""", title="Ko'p yo'l"),
        text(r"""
```python
ball = 75
if ball >= 90:
    print("5")
elif ball >= 70:
    print("4")
elif ball >= 50:
    print("3")
else:
    print("2")
```

Python shartlarni **yuqoridan pastga** tekshiradi va **birinchi rost** shartning blokini bajarib, qolganlarini **o'tkazib yuboradi**. Hech biri rost bo'lmasa — `else`.

**Tartib muhim!** Agar `ball >= 50` ni birinchi yozsak, 95 ball ham «3» olib qoladi.
""", title="if – elif – else"),
        callout('analogy', r"""
`elif` — **imtihon eshigidagi navbat**: «90+ bo'lsangiz — 1-xonaga; bo'lmasa 70+ bo'lsangiz — 2-xonaga...» Har kim faqat **birinchi mos** xonaga kiradi.
""", title="Hayotiy o'xshatish"),
        example(r'''
harorat = 12
if harorat >= 30:
    print("Juda issiq")
elif harorat >= 20:
    print("Iliq")
elif harorat >= 10:
    print("Salqin")
else:
    print("Sovuq")
''', title="Havo harorati", body="12 uchun: birinchi ikki shart yolg'on, `>= 10` rost — `Salqin`. Qolgan shartlar tekshirilmaydi."),
        example(r'''
soat = 14
if soat < 6:
    print("Tun")
elif soat < 12:
    print("Ertalab")
elif soat < 18:
    print("Kunduz")
else:
    print("Kech")
''', title="Amaliy: kun vaqti", body="14 uchun `soat < 12` yolg'on, `soat < 18` rost: `Kunduz`. Shartlar o'sish tartibida joylashgani uchun har bir `elif` oldingisidan keyingi oraliqni tekshiradi."),
        exercise('l23_inline_pred'),
        callout('warning', r"""
Alohida `if`lar ketma-ketligi va `if/elif` — **farqli**: alohida `if`larda bir nechta blok ishlashi mumkin; `elif` zanjirida **faqat bittasi**.
""", title="Diqqat"),
        recap(["`elif` — qo'shimcha shart", "birinchi rost shartning bloki ishlaydi", "shartlar tartibiga e'tibor bering"], "`>=`, `==`, `!=` kabi belgilarni qisqacha «taqqoslash operatorlari» deymiz. Ularning hammasini bilasizmi?"),
    ],
    [
        predict('l23_inline_pred', "Qaysi blok?", "Dastur nima chiqaradi?", section='inline', code='n = 5\nif n > 10:\n    print("A")\nelif n > 3:\n    print("B")\nelse:\n    print("C")\n', answer="B", points=2, hint="Birinchi rost shart.", explanation="`n > 10` yolg'on, `n > 3` rost → B."),
        predict('l23_quiz_1', "Tartib muhim", "Dastur nima chiqaradi?", code='x = 95\nif x >= 50:\n    print("3")\nelif x >= 90:\n    print("5")\n', answer="3", hint="Birinchi rost shart ishlaydi.", explanation="`x >= 50` birinchi rost bo'ldi, `elif` tekshirilmaydi."),
        single('l23_quiz_2', "elif so'zi", "`elif` so'zi qaysi iboradan olingan?", options=[opt("else if (aks holda, agar)", True), opt("end if", False), opt("equal if", False)], hint="Inglizcha qisqartma.", explanation="*else if*."),
        predict('l23_quiz_3', "Alohida if'lar", "Dastur nima chiqaradi?", code='n = 8\nif n > 5:\n    print("1")\nif n > 7:\n    print("2")\n', answer="1\n2", hint="Bu `elif` emas, ikkita alohida `if`.", explanation="Ikkala shart ham rost — ikkala blok ishlaydi."),
        code_task('l23_assignment', "Baholash", r"""
Foydalanuvchi ballni (0–100) kiritadi. Baho chiqaring: **90+ → `5`, 70–89 → `4`, 50–69 → `3`, 50 dan kam → `2`.**
""", starter_code='', points=10,
            tests=[T('output_equals', "5", "95", stdin="95\n"), T('output_equals', "5", "90", stdin="90\n"), T('output_equals', "4", "75", stdin="75\n"), T('output_equals', "4", "70", stdin="70\n"), T('output_equals', "3", "50", stdin="50\n"), T('output_equals', "2", "49", stdin="49\n"), T('output_equals', "2", "0", stdin="0\n", hidden=True), T('code_contains', 'elif', "`elif` ishlatilgan")],
            hint="Eng yuqori chegaradan boshlang: avval `>= 90`.", partial_solution='ball = int(input())\nif ball >= 90:\n    print(5)\nelif ball >= 70:\n    print(4)\n# qolganlarini yozing\n', full_solution='ball = int(input())\nif ball >= 90:\n    print(5)\nelif ball >= 70:\n    print(4)\nelif ball >= 50:\n    print(3)\nelse:\n    print(2)\n', explanation="Yuqoridan pastga tartiblangan chegaralar."),
        single('l23_practice_easy', "Easy: nechta else", "Bitta `if/elif/else` zanjirida nechta `else` bo'lishi mumkin?", section='practice', difficulty='easy', options=[opt("Ko'pi bilan bitta", True), opt("Istalgancha", False), opt("Ikkita", False)], hint="`else` — «qolgan hamma holat».", explanation="Zanjirda bitta, eng oxirgi `else`."),
        code_task('l23_practice_medium', "Medium: kun nomi", r"""
Foydalanuvchi 1–7 oralig'ida kun raqamini kiritadi. 1 → `Dushanba`, 2 → `Seshanba`, 3 → `Chorshanba`, 4 → `Payshanba`, 5 → `Juma`, 6 → `Shanba`, 7 → `Yakshanba`, boshqa son → `Noto'g'ri raqam`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', n, f"{i}", stdin=f"{i}\n") for i, n in enumerate(["Noto'g'ri raqam", "Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]) if i] + [T('output_equals', "Noto'g'ri raqam", "9", stdin="9\n")],
            hint="`==` bilan har bir kunni tekshiring.", full_solution='k = int(input())\nif k == 1:\n    print("Dushanba")\nelif k == 2:\n    print("Seshanba")\nelif k == 3:\n    print("Chorshanba")\nelif k == 4:\n    print("Payshanba")\nelif k == 5:\n    print("Juma")\nelif k == 6:\n    print("Shanba")\nelif k == 7:\n    print("Yakshanba")\nelse:\n    print("Noto\'g\'ri raqam")\n', explanation="Bir nechta `==` tekshiruvi `elif` zanjirida."),
        code_task('l23_practice_hard', "Hard: uchburchak turi", r"""
Foydalanuvchi uchburchakning uchta tomonini kiritadi (butun sonlar). Agar uchalasi teng — `Teng tomonli`; agar ikkitasi teng — `Teng yonli`; aks holda — `Turli tomonli`. (Teng tomonli ham «ikkitasi teng» shartiga mos keladi, shuning uchun uni **birinchi** tekshiring.)
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Teng tomonli", "5,5,5", stdin="5\n5\n5\n"), T('output_equals', "Teng yonli", "5,5,3", stdin="5\n5\n3\n"), T('output_equals', "Teng yonli", "3,5,5", stdin="3\n5\n5\n"), T('output_equals', "Teng yonli", "5,3,5", stdin="5\n3\n5\n", hidden=True), T('output_equals', "Turli tomonli", "3,4,5", stdin="3\n4\n5\n")],
            hint="`a == b and b == c` — mantiqiy `and` hali o'tilmadi; `a == b == c` yozish mumkin. Ikkitasi teng: `a == b`, `b == c`, `a == c` ni alohida `elif`da tekshiring.", partial_solution='a = int(input())\nb = int(input())\nc = int(input())\nif a == b == c:\n    print("Teng tomonli")\nelif a == b:\n    print("Teng yonli")\n# qolgan juftliklar va else\n',
            full_solution='a = int(input())\nb = int(input())\nc = int(input())\nif a == b == c:\n    print("Teng tomonli")\nelif a == b:\n    print("Teng yonli")\nelif b == c:\n    print("Teng yonli")\nelif a == c:\n    print("Teng yonli")\nelse:\n    print("Turli tomonli")\n', explanation="Tartib: avval eng maxsus holat."),
    ])

# ==============================================================================
# 24-DARS
# ==============================================================================
LESSON_24 = L(24, "Taqqoslash operatorlari", 12,
    "==, !=, >, <, >=, <= operatorlarini bilish, = va == farqini ajratish, matnlarni taqqoslash.",
    ["==", "!=", "> < >= <=", "= va == farqi", "Matnlarni taqqoslash"],
    [
        text(r"""
Shart — bu **savol**, javobi «ha» (`True`) yoki «yo'q» (`False`). Savol berish uchun **taqqoslash operatorlari** kerak.
""", title="Savol berish"),
        text(r"""
| Operator | Ma'nosi | Misol | Natija |
|---|---|---|---|
| `==` | teng | `5 == 5` | `True` |
| `!=` | teng emas | `5 != 3` | `True` |
| `>` | katta | `3 > 5` | `False` |
| `<` | kichik | `3 < 5` | `True` |
| `>=` | katta yoki teng | `5 >= 5` | `True` |
| `<=` | kichik yoki teng | `6 <= 5` | `False` |

Matnlarni ham taqqoslash mumkin: `"olma" == "olma"` — `True`. Harf registri farqlanadi: `"Olma" == "olma"` — `False`.
""", title="Oltita operator"),
        callout('important', r"""
`=` — **saqlash** (`x = 5`), `==` — **tekshirish** (`x == 5`). `if x = 5:` yozilsa — `SyntaxError`. Eng ko'p uchraydigan boshlovchi xatosi!
""", title="= va == farqi"),
        example(r'''
a = 10
b = 7
print(a == b)
print(a != b)
print(a > b)
print(a <= b)
''', title="Sonlarni taqqoslash", body="Natijalar: `False`, `True`, `True`, `False`. Har bir taqqoslash `bool` qiymat qaytaradi."),
        example(r'''
parol = "python123"
kiritilgan = input("Parol: ")
if kiritilgan == parol:
    print("Xush kelibsiz!")
else:
    print("Parol xato")
''', title="Amaliy: parolni tekshirish", body="`python123` kiriting: `Xush kelibsiz!`; boshqa narsa kiritsangiz — `Parol xato`. `==` matnlar uchun ham ishlaydi."),
        exercise('l24_inline_fix'),
        callout('tip', r"""
Taqqoslashni zanjir qilib yozish mumkin: `1 < x < 10` — «x 1 bilan 10 orasida». Bu matematikaga yaqin va qulay.
"""),
        recap(["`==`, `!=`, `>`, `<`, `>=`, `<=`", "natija — `True`/`False`", "`=` saqlaydi, `==` tekshiradi"], "ikkita shartni birga tekshirish kerak bo'lsa — masalan, «yosh 18 dan katta VA pasport bor»?"),
    ],
    [
        fix_task('l24_inline_fix', "= va ==", "Dastur xato beryapti. Tuzating — `x = 5` uchun natija: `Beshga teng`", section='inline', points=2, starter_code='x = 5\nif x = 5:\n    print("Beshga teng")\n', tests=[T('output_equals', 'Beshga teng', "Natija to'g'ri")], hint="Shartda tekshirish operatori kerak.", full_solution='x = 5\nif x == 5:\n    print("Beshga teng")\n', explanation="Shartda `==` ishlatiladi."),
        predict('l24_quiz_1', "Taqqoslash natijasi", "Dastur nima chiqaradi?", code='print(7 != 7, 7 >= 7)\n', answer="False True", hint="Har bir taqqoslashni alohida baholang.", explanation="`7 != 7` yolg'on; `7 >= 7` rost."),
        single('l24_quiz_2', "Matn registri", "`\"Python\" == \"python\"` natijasi?", options=[opt("`True`", False), opt("`False`", True), opt("Xato", False)], hint="`P` va `p` har xil.", explanation="Harf registri farqlanadi."),
        predict('l24_quiz_3', "Zanjirli taqqoslash", "Dastur nima chiqaradi?", code='x = 5\nprint(1 < x < 10)\n', answer="True", hint="Ikkalasi ham rost.", explanation="`1 < 5` va `5 < 10` — rost."),
        code_task('l24_assignment', "Login tekshirgich", r"""
Foydalanuvchi **login** kiritadi. Agar u `admin` ga teng bo'lsa — `Salom, admin!`, teng bo'lmasa — `Kirish taqiqlangan`.
""", starter_code='', points=10, tests=[T('output_equals', "Salom, admin!", "admin", stdin="admin\n"), T('output_equals', "Kirish taqiqlangan", "user", stdin="user\n"), T('output_equals', "Kirish taqiqlangan", "Admin (katta A)", stdin="Admin\n", hidden=True), T('code_contains', '==', "`==` ishlatilgan")],
            hint="`if login == \"admin\":`", partial_solution='login = input()\nif login == "admin":\n    print("Salom, admin!")\n# else qismini yozing\n', full_solution='login = input()\nif login == "admin":\n    print("Salom, admin!")\nelse:\n    print("Kirish taqiqlangan")\n', explanation="Matnni `==` bilan taqqosladik."),
        single('l24_practice_easy', "Easy: teng emas", "\"Teng emas\" operatori qaysi?", section='practice', difficulty='easy', options=[opt("`!=`", True), opt("`=!`", False), opt("`<>`", False)], hint="Undov belgisi va tenglik.", explanation="`!=`."),
        code_task('l24_practice_medium', "Medium: bir xil so'zlar", r"""
Foydalanuvchi ikkita so'z kiritadi. Harf registriga **e'tibor bermasdan** teng bo'lsa `Bir xil`, aks holda `Har xil` chiqarsin. `Olma`, `olma` → `Bir xil`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Bir xil", "Olma/olma", stdin="Olma\nolma\n"), T('output_equals', "Har xil", "olma/nok", stdin="olma\nnok\n"), T('output_equals', "Bir xil", "PYTHON/python", stdin="PYTHON\npython\n", hidden=True)], hint="`lower()` ni eslang.", full_solution='a = input()\nb = input()\nif a.lower() == b.lower():\n    print("Bir xil")\nelse:\n    print("Har xil")\n', explanation="Ikkalasini kichik harfga keltirib taqqosladik."),
        code_task('l24_practice_hard', "Hard: oraliqda yotadimi?", r"""
Foydalanuvchi son kiritadi. Agar u **10 dan 20 gacha** (ikkala chegara ham kiradi) bo'lsa — `Oraliqda`, aks holda `Tashqarida`. Zanjirli taqqoslashdan foydalaning.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Oraliqda", "10", stdin="10\n"), T('output_equals', "Oraliqda", "20", stdin="20\n"), T('output_equals', "Oraliqda", "15", stdin="15\n"), T('output_equals', "Tashqarida", "9", stdin="9\n"), T('output_equals', "Tashqarida", "21", stdin="21\n", hidden=True)], hint="`10 <= n <= 20`.", full_solution='n = int(input())\nif 10 <= n <= 20:\n    print("Oraliqda")\nelse:\n    print("Tashqarida")\n', explanation="Chegaralar kirishi uchun `<=`."),
    ])

# ==============================================================================
# 25-DARS
# ==============================================================================
LESSON_25 = L(25, "Mantiqiy operatorlar — and, or, not", 13,
    "and, or, not operatorlari bilan murakkab shartlar tuzish va rostlik jadvallarini tushunish.",
    ["and", "or", "not", "Rostlik jadvali", "Qavslar"],
    [
        text(r"""
«Kinoga kirish uchun yoshingiz 16 dan katta **va** chiptangiz bo'lishi kerak.» Ikki shart **birga** tekshirildi. Buning uchun **mantiqiy operatorlar** bor.
""", title="Shartlarni birlashtirish"),
        text(r"""
| Operator | Ma'nosi | Qachon `True` |
|---|---|---|
| `A and B` | ikkalasi ham | A rost **va** B rost |
| `A or B` | kamida bittasi | A rost **yoki** B rost (yoki ikkalasi) |
| `not A` | teskarisi | A yolg'on bo'lsa |

```python
yosh = 20
chipta = True
if yosh >= 16 and chipta:
    print("Kirishingiz mumkin")
```

Tartib: avval `not`, keyin `and`, keyin `or`. Shubha bo'lsa — **qavs** ishlating.
""", title="and, or, not"),
        callout('analogy', r"""
`and` — **ikkita qulf**: ikkalasini ham ochish kerak. `or` — **ikkita eshik**: bittasi ochiq bo'lsa kirasiz. `not` — **«teskari» tugma**.
""", title="Hayotiy o'xshatish"),
        example(r'''
yosh = 17
chipta = False
print(yosh >= 16 and chipta)
print(yosh >= 16 or chipta)
print(not chipta)
''', title="Uchala operator", body="`True and False` → `False`; `True or False` → `True`; `not False` → `True`."),
        example(r'''
kun = "shanba"
if kun == "shanba" or kun == "yakshanba":
    print("Dam olish kuni")
else:
    print("Ish kuni")
''', title="Amaliy: dam olish kuni", body="`kun == \"shanba\" or kun == \"yakshanba\"`: bitta shart rost bo'lsa yetadi. E'tibor bering: har bir taqqoslash to'liq yoziladi (`kun == \"shanba\" or \"yakshanba\"` — **noto'g'ri**)."),
        exercise('l25_inline_pred'),
        callout('warning', r"""
`x == 1 or 2` — keng tarqalgan xato! Python buni `(x == 1) or 2` deb o'qiydi va doim rost deb hisoblaydi. To'g'ri: `x == 1 or x == 2`.
""", title="Diqqat"),
        recap(["`and` — ikkalasi rost", "`or` — kamida bittasi rost", "`not` — teskarisi", "murakkab shartda qavs ishlating"], "shartning ichida yana shart bo'lishi mumkinmi?"),
    ],
    [
        predict('l25_inline_pred', "and natijasi", "Dastur nima chiqaradi?", section='inline', code='print(True and False)\n', answer="False", points=2, hint="`and` uchun ikkalasi ham rost bo'lishi kerak.", explanation="Biri yolg'on — natija `False`."),
        predict('l25_quiz_1', "or natijasi", "Dastur nima chiqaradi?", code='a = 3\nprint(a > 5 or a < 4)\n', answer="True", hint="`or` — bittasi yetadi.", explanation="`a < 4` rost."),
        predict('l25_quiz_2', "not", "Dastur nima chiqaradi?", code='print(not (2 > 5))\n', answer="True", hint="`2 > 5` yolg'on, `not` teskari qiladi.", explanation="`not False` → `True`."),
        single('l25_quiz_3', "To'g'ri yozuv", "`x` 1 yoki 2 ekanini tekshirishning to'g'ri yozuvi?", options=[opt("`x == 1 or 2`", False, "Bu doim rost bo'ladi."), opt("`x == 1 or x == 2`", True), opt("`x == (1 or 2)`", False)], hint="Har bir taqqoslash to'liq.", explanation="Har bir shart o'z o'zgaruvchisi bilan yoziladi."),
        code_task('l25_assignment', "Kinoga kirish", r"""
Foydalanuvchi **yosh** (butun son) va **chipta bormi** (`ha` yoki `yo'q`) kiritadi. Yosh **16 dan katta yoki teng** **va** javob `ha` bo'lsa — `Kiring`, aks holda `Kirish mumkin emas`.
""", starter_code='', points=10, tests=[T('output_equals', "Kiring", "20/ha", stdin="20\nha\n"), T('output_equals', "Kirish mumkin emas", "20/yo'q", stdin="20\nyo'q\n"), T('output_equals', "Kirish mumkin emas", "12/ha", stdin="12\nha\n"), T('output_equals', "Kiring", "16/ha", stdin="16\nha\n", hidden=True), T('code_contains', ' and ', "`and` ishlatilgan")],
            hint="`if yosh >= 16 and javob == \"ha\":`", partial_solution='yosh = int(input())\njavob = input()\nif yosh >= 16 and javob == "ha":\n    print("Kiring")\n# else qismini yozing\n', full_solution='yosh = int(input())\njavob = input()\nif yosh >= 16 and javob == "ha":\n    print("Kiring")\nelse:\n    print("Kirish mumkin emas")\n', explanation="Ikkala shart ham rost bo'lishi kerak."),
        single('l25_practice_easy', "Easy: or", "`False or False` natijasi?", section='practice', difficulty='easy', options=[opt("`True`", False), opt("`False`", True), opt("Xato", False)], hint="Hech biri rost emas.", explanation="`or` uchun kamida bittasi rost bo'lishi kerak."),
        code_task('l25_practice_medium', "Medium: unli harfmi?", r"""
Foydalanuvchi bitta kichik harf kiritadi. Agar u `a`, `o`, `i`, `u`, `e` dan biri bo'lsa — `Unli`, aks holda `Undosh`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Unli", "a", stdin="a\n"), T('output_equals', "Unli", "u", stdin="u\n"), T('output_equals', "Undosh", "k", stdin="k\n"), T('output_equals', "Unli", "e", stdin="e\n", hidden=True)], hint="`or` bilan beshta taqqoslash.", full_solution='h = input()\nif h == "a" or h == "o" or h == "i" or h == "u" or h == "e":\n    print("Unli")\nelse:\n    print("Undosh")\n', explanation="Har bir variant to'liq taqqoslanadi."),
        code_task('l25_practice_hard', "Hard: kabisa yili", r"""
Yil **kabisa** bo'ladi, agar u **4 ga bo'linsa va 100 ga bo'linmasa**, **yoki 400 ga bo'linsa**. Foydalanuvchi yil kiritadi; `Kabisa` yoki `Oddiy` chiqaring. `2024` → `Kabisa`, `1900` → `Oddiy`, `2000` → `Kabisa`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Kabisa", "2024", stdin="2024\n"), T('output_equals', "Oddiy", "1900", stdin="1900\n"), T('output_equals', "Kabisa", "2000", stdin="2000\n"), T('output_equals', "Oddiy", "2023", stdin="2023\n"), T('output_equals', "Oddiy", "2100", stdin="2100\n", hidden=True)],
            hint="`(y % 4 == 0 and y % 100 != 0) or y % 400 == 0`", partial_solution='y = int(input())\nif (y % 4 == 0 and y % 100 != 0):\n    print("Kabisa")\n# 400 ga bo\'linish holatini ham qo\'shing\n', full_solution='y = int(input())\nif (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:\n    print("Kabisa")\nelse:\n    print("Oddiy")\n', explanation="Qavs `and` va `or` tartibini aniq ko'rsatadi."),
    ])

# ==============================================================================
# 26-DARS
# ==============================================================================
LESSON_26 = L(26, "Ichma-ich shartlar va murakkab shartlar", 13,
    "if ichida if yozish (ichma-ich shartlar) va ularni and/elif bilan soddalashtirish.",
    ["Ichma-ich if", "Ikki bosqichli tekshiruv", "Soddalashtirish", "Chekinish darajalari"],
    [
        text(r"""
Bankomatdan pul yechish: avval **karta to'g'rimi** tekshiriladi, **keyin** (faqat to'g'ri bo'lsa) PIN, **keyin** (faqat PIN to'g'ri bo'lsa) balans. Har bir tekshiruv oldingisiga **bog'liq**. Bunda shart ichida yana shart yoziladi — **ichma-ich shart**.
""", title="Bosqichma-bosqich tekshiruv"),
        text(r"""
```python
yosh = 20
bilet = True
if yosh >= 16:
    if bilet:
        print("Kiring")
    else:
        print("Bilet yo'q")
else:
    print("Yoshingiz yetmaydi")
```

Ichki `if` — **8 ta bo'sh joy** (yana bir daraja chekinish) bilan yoziladi. Tashqi shart yolg'on bo'lsa, ichki blok umuman tekshirilmaydi.

Ko'pincha ichma-ich shartni `and` bilan soddalashtirish mumkin: `if yosh >= 16 and bilet:`. Lekin **har xil javoblar** kerak bo'lsa (yosh yetmaydi / bilet yo'q), ichma-ich yaxshiroq.
""", title="if ichida if"),
        callout('analogy', r"""
Ichma-ich shartlar — **matryoshka**: katta qo'g'irchoq ochilsa — ichidagisi, u ham ochilsa — undagisi.
""", title="Hayotiy o'xshatish"),
        example(r'''
son = 12
if son > 0:
    if son % 2 == 0:
        print("Musbat juft")
    else:
        print("Musbat toq")
else:
    print("Musbat emas")
''', title="Musbat juft/toq", body="Avval musbatlik, keyin juft-toq tekshirildi. 12 uchun: `Musbat juft`."),
        example(r'''
login = input("Login: ")
parol = input("Parol: ")
if login == "admin":
    if parol == "1234":
        print("Xush kelibsiz!")
    else:
        print("Parol xato")
else:
    print("Bunday foydalanuvchi yo'q")
''', title="Amaliy: login va parol", body="Ichma-ich yordamida aniq xabar beramiz: login topilmadimi yoki parolmi — `and` bilan buni ajratib bo'lmas edi."),
        exercise('l26_inline_pred'),
        callout('tip', r"""
3 darajadan ortiq ichma-ich yozmang — kod o'qib bo'lmas holga keladi. `and` va `elif` ko'p hollarda soddaroq.
""", title="Maslahat"),
        recap(["ichma-ich `if` — shart ichida shart", "ichki blok qo'shimcha chekinadi", "ko'pincha `and` bilan soddalashtiriladi"], "dasturni takror-takror ishlatish — masalan, parolni to'g'ri kiritguncha so'rash uchun nima kerak?"),
    ],
    [
        predict('l26_inline_pred', "Ichki shart", "Dastur nima chiqaradi?", section='inline', code='x = 6\nif x > 0:\n    if x > 10:\n        print("A")\n    else:\n        print("B")\n', answer="B", points=2, hint="Tashqi shart rost, ichkisi yolg'on.", explanation="`x > 0` rost; ichkida `x > 10` yolg'on → `else`."),
        predict('l26_quiz_1', "Tashqi shart yolg'on", "Dastur nima chiqaradi?", code='x = -4\nif x > 0:\n    print("A")\n    if x > 10:\n        print("B")\nprint("C")\n', answer="C", hint="Tashqi blok o'tkazib yuboriladi.", explanation="`x > 0` yolg'on — ichidagilar bajarilmaydi."),
        single('l26_quiz_2', "Qachon ichma-ich?", "Qaysi holatda ichma-ich shart `and` dan afzal?", options=[opt("Har bir tekshiruv uchun alohida xabar kerak bo'lganda", True), opt("Kodni qisqartirish kerak bo'lganda", False), opt("Hech qachon", False)], hint="Xabarlar bir xilmi?", explanation="Har bir bosqichda alohida javob kerak bo'lsa ichma-ich qulay."),
        predict('l26_quiz_3', "Soddalashtirilgan", "Dastur nima chiqaradi?", code='a = 5\nb = 8\nif a > 0 and b > 0:\n    print("ikkalasi musbat")\nelse:\n    print("yo\'q")\n', answer="ikkalasi musbat", hint="Ikkala shart rost.", explanation="`and` ichma-ich ikkita `if` o'rnini bosdi."),
        code_task('l26_assignment', "Bankomat", r"""
Foydalanuvchi **PIN** (`4321` to'g'ri) va **so'ralgan summa**ni kiritadi. Balans — `500000` so'm. Qoidalar:
- PIN noto'g'ri → `PIN xato`.
- PIN to'g'ri, summa balansdan **ko'p** → `Mablag' yetarli emas`.
- PIN to'g'ri va summa yetarli → `Pul berildi` (ichma-ich `if` ishlating).
""", starter_code='', points=10, tests=[T('output_equals', "PIN xato", "noto'g'ri PIN", stdin="1111\n100000\n"), T('output_equals', "Mablag' yetarli emas", "ko'p summa", stdin="4321\n600000\n"), T('output_equals', "Pul berildi", "yetarli", stdin="4321\n200000\n"), T('output_equals', "Pul berildi", "to'liq balans", stdin="4321\n500000\n", hidden=True), T('code_regex', r"(?m)^ {4}if ", "Ichma-ich if ishlatilgan")],
            hint="Avval PIN, ichida summa.", partial_solution='pin = input()\nsumma = int(input())\nif pin == "4321":\n    # summani tekshiring\nelse:\n    print("PIN xato")\n', full_solution='pin = input()\nsumma = int(input())\nif pin == "4321":\n    if summa > 500000:\n        print("Mablag\' yetarli emas")\n    else:\n        print("Pul berildi")\nelse:\n    print("PIN xato")\n', explanation="PIN noto'g'ri bo'lsa, summa umuman tekshirilmaydi."),
        single('l26_practice_easy', "Easy: chekinish", "Ichma-ich `if` ichidagi blok necha bo'sh joy bilan suriladi (standart)?", section='practice', difficulty='easy', options=[opt("4", False), opt("8", True), opt("2", False)], hint="Har daraja 4 ta, ikki daraja.", explanation="Ikki daraja = 8 ta bo'sh joy."),
        code_task('l26_practice_medium', "Medium: sonning ishorasi va juftligi", r"""
Foydalanuvchi butun son kiritadi. 0 bo'lsa `Nol`. Aks holda ikkita so'z chiqaring: musbat/manfiy va juft/toq: `Musbat juft`, `Musbat toq`, `Manfiy juft`, `Manfiy toq`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Nol", "0", stdin="0\n"), T('output_equals', "Musbat juft", "4", stdin="4\n"), T('output_equals', "Musbat toq", "7", stdin="7\n"), T('output_equals', "Manfiy juft", "-2", stdin="-2\n"), T('output_equals', "Manfiy toq", "-9", stdin="-9\n", hidden=True)],
            hint="Avval 0 ni tekshiring, keyin ishorani, ichida juftlikni.", full_solution='n = int(input())\nif n == 0:\n    print("Nol")\nelif n > 0:\n    if n % 2 == 0:\n        print("Musbat juft")\n    else:\n        print("Musbat toq")\nelse:\n    if n % 2 == 0:\n        print("Manfiy juft")\n    else:\n        print("Manfiy toq")\n', explanation="Ichma-ich va `elif` aralash."),
        code_task('l26_practice_hard', "Hard: taksi narxi", r"""
Foydalanuvchi masofani (km, butun) va vaqtni (`kunduz` yoki `tun`) kiritadi. Narx: 1 km — 2000 so'm, minimal buyurtma — 8000 so'm. **Tunda** narx 20% ga qimmat. Natija: `Narx: 12000` (butun songa, `int()` bilan). Masalan: `5`, `kunduz` → `Narx: 10000`; `2`, `kunduz` → `Narx: 8000` (minimal); `5`, `tun` → `Narx: 12000`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Narx: 10000", "5/kunduz", stdin="5\nkunduz\n"), T('output_equals', "Narx: 8000", "2/kunduz", stdin="2\nkunduz\n"), T('output_equals', "Narx: 12000", "5/tun", stdin="5\ntun\n"), T('output_equals', "Narx: 9600", "2/tun", stdin="2\ntun\n", hidden=True)],
            hint="Avval `narx = km * 2000`; minimaldan kam bo'lsa 8000; keyin tun bo'lsa `* 1.2`.", partial_solution='km = int(input())\nvaqt = input()\nnarx = km * 2000\nif narx < 8000:\n    narx = 8000\n# tun uchun 20% qo\'shing va chiqaring\n', full_solution='km = int(input())\nvaqt = input()\nnarx = km * 2000\nif narx < 8000:\n    narx = 8000\nif vaqt == "tun":\n    narx = narx * 1.2\nprint(f"Narx: {int(round(narx))}")\n', explanation="Minimalni qo'llagandan keyin tungi ustama qo'shiladi."),
    ])

LESSONS = [LESSON_21, LESSON_22, LESSON_23, LESSON_24, LESSON_25, LESSON_26]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("4-modul yakuniy nazorati: Qaror qabul qilish", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **baholash tizimi va parol tekshiruvchi dastur**.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m4_a_t1', "if tuzilishi", "`if` qatori nima bilan tugaydi?", section='assessment', points=2, options=[opt("Ikki nuqta `:`", True), opt("Nuqtali vergul `;`", False), opt("Qavs `)`", False)], explanation="`if shart:`."),
    single('m4_a_t2', "elif", "`elif` qachon tekshiriladi?", section='assessment', points=2, options=[opt("Oldingi shartlar yolg'on bo'lganda", True), opt("Har doim", False), opt("Faqat `else` dan keyin", False)], explanation="Zanjirda faqat oldingilar yolg'on bo'lsa."),
    single('m4_a_t3', "= va ==", "Tenglikni tekshirish operatori qaysi?", section='assessment', points=2, options=[opt("`=`", False), opt("`==`", True), opt("`:=`", False)], explanation="`==` tekshiradi, `=` saqlaydi."),
    single('m4_a_t4', "and", "`True and False` natijasi?", section='assessment', points=2, options=[opt("`True`", False), opt("`False`", True), opt("Xato", False)], explanation="`and` uchun ikkalasi rost bo'lishi kerak."),
    multiple('m4_a_t5', "To'g'ri shartlar", "Qaysi yozuvlar `x` 1 yoki 2 ekanini to'g'ri tekshiradi?", section='assessment', points=2, options=[opt("`x == 1 or x == 2`", True), opt("`x in (1, 2)`", False, "`in` bu yerda hali o'tilmagan tuple bilan; asl maqsad — `or` ni bilish."), opt("`x == 1 or 2`", False), opt("`1 <= x <= 2 and x != 1.5`", True)], explanation="`x == 1 or 2` har doim rost bo'ladi — xato."),
    predict('m4_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='n = 15\nif n % 3 == 0:\n    print("A")\nelif n % 5 == 0:\n    print("B")\nelse:\n    print("C")\n', answer="A", explanation="Birinchi rost shart: `15 % 3 == 0`."),
    predict('m4_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = 4\nb = 9\nif a > 5 or b > 5:\n    print("1")\nif a > 5 and b > 5:\n    print("2")\nprint("3")\n', answer="1\n3", explanation="`or` rost, `and` yolg'on."),
    predict('m4_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='x = 7\nif x > 5:\n    if x < 7:\n        print("A")\n    else:\n        print("B")\nelse:\n    print("C")\n', answer="B", explanation="Tashqi rost; ichkida `7 < 7` yolg'on."),
    fix_task('m4_a_f1', "Xatoni tuzating (1)", "Dastur `Katta` chiqarishi kerak (`n = 10`), lekin xato beryapti.", section='assessment', points=4, starter_code='n = 10\nif n = 10\n    print("Katta")\n', tests=[T('output_equals', "Katta", "Natija: Katta")], hint="Ikkita xato: operator va ikki nuqta.", full_solution='n = 10\nif n == 10:\n    print("Katta")\n', explanation="`==` va `:` kerak edi."),
    fix_task('m4_a_f2', "Xatoni tuzating (2)", "Dastur 5 dan **kichik** sonlarga `Kichik`, qolganiga `Katta` chiqarishi kerak, lekin hammasiga `Kichik` deb chiqaryapti.", section='assessment', points=4, starter_code='n = int(input())\nif n > 5:\n    print("Kichik")\nelse:\n    print("Katta")\n', tests=[T('output_equals', "Kichik", "3 → Kichik", stdin="3\n"), T('output_equals', "Katta", "9 → Katta", stdin="9\n"), T('output_equals', "Katta", "5 → Katta", stdin="5\n")], hint="Mantiqiy xato: shart teskari.", full_solution='n = int(input())\nif n < 5:\n    print("Kichik")\nelse:\n    print("Katta")\n', explanation="Taqqoslash belgisi noto'g'ri edi."),
    code_task('m4_a_project', "Mini-loyiha: Baholash tizimi va parol tekshiruvchi", r"""
Dastur ikki qismdan iborat. Foydalanuvchi ketma-ket kiritadi:

1. **Ball** (0–100, butun son),
2. **Parol** (matn).

**1-qism — baho** (1-qatorga chiqariladi):
- 90–100 → `Baho: 5`, 70–89 → `Baho: 4`, 50–69 → `Baho: 3`, 0–49 → `Baho: 2`,
- ball 0 dan kichik yoki 100 dan katta → `Ball noto'g'ri` (va parol baribir tekshiriladi).

**2-qism — parol kuchi** (2-qatorga chiqariladi). Parol:
- 8 tadan kam belgi → `Parol: kuchsiz`,
- 8 va undan ko'p belgi **va** tarkibida `@` yoki `#` yoki `!` belgisidan biri bor → `Parol: kuchli`,
- aks holda → `Parol: o'rtacha`.

Masalan `85` va `qwerty12!` → `Baho: 4` / `Parol: kuchli`.
""", section='project', points=15, difficulty='medium', unlock=3, starter_code='# Baholash tizimi va parol tekshiruvchi\n',
        expected_output_example="Baho: 4\nParol: kuchli",
        tests=[T('output_equals', "Baho: 4\nParol: kuchli", "85 / qwerty12!", stdin="85\nqwerty12!\n"), T('output_equals', "Baho: 5\nParol: kuchsiz", "90 / abc", stdin="90\nabc\n"), T('output_equals', "Baho: 3\nParol: o'rtacha", "50 / parol12345", stdin="50\nparol12345\n"),
               T('output_equals', "Baho: 2\nParol: kuchli", "49 / secret#99", stdin="49\nsecret#99\n"), T('output_equals', "Ball noto'g'ri\nParol: kuchsiz", "101 / abc", stdin="101\nabc\n", hidden=True), T('output_equals', "Ball noto'g'ri\nParol: o'rtacha", "-5 / abcdefgh", stdin="-5\nabcdefgh\n", hidden=True), T('output_equals', "Baho: 5\nParol: kuchli", "100 / abcdefg@", stdin="100\nabcdefg@\n", hidden=True)],
        hint="1) Ballni `int(input())`, parolni `input()` bilan oling. 2) Baho uchun `if/elif/else`. 3) Parol: `len(parol) < 8` → kuchsiz; `elif` uzunlik yetarli **va** (`\"@\" in parol or \"#\" in parol or \"!\" in parol`) → kuchli.",
        partial_solution='ball = int(input())\nparol = input()\nif ball < 0 or ball > 100:\n    print("Ball noto\'g\'ri")\nelif ball >= 90:\n    print("Baho: 5")\n# qolgan baholarni va parol qismini yozing\n',
        full_solution='ball = int(input())\nparol = input()\nif ball < 0 or ball > 100:\n    print("Ball noto\'g\'ri")\nelif ball >= 90:\n    print("Baho: 5")\nelif ball >= 70:\n    print("Baho: 4")\nelif ball >= 50:\n    print("Baho: 3")\nelse:\n    print("Baho: 2")\nif len(parol) < 8:\n    print("Parol: kuchsiz")\nelif "@" in parol or "#" in parol or "!" in parol:\n    print("Parol: kuchli")\nelse:\n    print("Parol: o\'rtacha")\n',
        explanation="Loyiha taqqoslash, and/or, elif zanjiri, `len()` va `in` operatorlarini birlashtiradi."),
])
