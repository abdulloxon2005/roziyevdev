"""Python — 0 dan boshlash · 9-modul: Xatolar bilan ishlash va debugging (61–65-darslar)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 9,
    'title': "Xatolar bilan ishlash va debugging",
    'description': "Python xatolarini tanish va o'qish, try/except bilan ularni boshqarish, else/finally va raise orqali o'z xatolarini chiqarish.",
}

# ==============================================================================
# 61-DARS
# ==============================================================================
LESSON_61 = L(61, "Python xatolari: SyntaxError, NameError, TypeError va ValueError", 13,
    "To'rt asosiy xato turini farqlash, xato xabarini (traceback) o'qish va xatolarni topib tuzatish (debugging).",
    ["SyntaxError", "NameError", "TypeError", "ValueError", "Traceback", "Debugging"],
    [
        text(r"""
Dasturchilar vaqtining katta qismini xatolarni **topish va tuzatish** (inglizcha *debugging*) bilan o'tkazadi. Xato — falokat emas, **ma'lumot**: Python nima noto'g'ri ketganini aytib turibdi. Faqat uni o'qishni bilish kerak.
""", title="Xato — bu maslahat"),
        text(r"""
| Xato | Qachon chiqadi | Misol | Sababi |
|---|---|---|---|
| `SyntaxError` | Kod ishga tushishdan **oldin**: yozilish qoidasi buzilgan | `print("a"` | qavs yopilmagan |
| `NameError` | Nom topilmadi | `print(x)` (x yo'q) | o'zgaruvchi yaratilmagan / xato yozilgan |
| `TypeError` | Amal bu turga mos emas | `"5" + 3` | matn + son |
| `ValueError` | Tur to'g'ri, **qiymat** mos emas | `int("abc")` | matn songa aylanmaydi |
| `ZeroDivisionError` | nolga bo'lish | `5 / 0` | |
| `IndexError` | mavjud bo'lmagan indeks | `[1, 2][5]` | |
| `KeyError` | mavjud bo'lmagan kalit | `{"a": 1}["b"]` | |

**Xato xabarini o'qish:** pastdan yuqoriga. Oxirgi qatorda — xato **turi** va **izohi**; undan yuqorida — **qaysi qatorda** (`line N`).

**Debugging usullari:** 1) xabarni o'qing; 2) shubhali joydan oldin `print()` bilan qiymatlarni tekshiring; 3) kodni kichik bo'laklarga bo'lib sinab ko'ring.
""", title="Xatolar jadvali"),
        callout('analogy', r"""
Xato xabari — **shifokor tashxisi**: «qayeringiz og'riyapti» (qator) va «nima kasalligi» (xato turi). Uni o'qimay davolab bo'lmaydi.
""", title="Hayotiy o'xshatish"),
        example(r'''
print(int("12") + 3)
print("Yosh: " + str(17))
print(len("salom"))
''', title="To'g'ri kod: xatolarsiz", body="Xatolarning oldini olish uchun turlarni mos qiling: `int()`, `str()`. Natija: `15`, `Yosh: 17`, `5`."),
        example(r'''
a = 10
b = "5"
print(a + int(b))
print(type(b))
nom = "Ali"
print(nom)
''', title="Amaliy: tuzatilgan xatolar", body="Asl kod `a + b` bo'lsa, `TypeError` bo'lardi (son + matn). `int(b)` bilan tuzatdik: `15` va `<class 'str'>`, `Ali`. `print(type(...))` — debugging uchun foydali."),
        exercise('l61_inline_pick'),
        callout('tip', r"""
Bu kursda har bir xato turini allaqachon ko'rgansiz. Endi ularni **nomi bilan** tanishga va **tuzatish usulini** bilishga harakat qiling.
""", title="Eslatma"),
        recap(["`SyntaxError` — yozilish; `NameError` — nom; `TypeError` — tur; `ValueError` — qiymat", "xabarni pastdan o'qing: tur + qator", "debugging: `print()` va kichik bo'laklar"], "xato yuz berganda dasturning to'xtab qolmasligi uchun nima qilish mumkin?"),
    ],
    [
        single('l61_inline_pick', "Xato turini toping", "`int(\"salom\")` qaysi xatoni beradi?", section='inline', points=2, options=[opt("`ValueError`", True), opt("`TypeError`", False), opt("`NameError`", False)], hint="Tur — `str`, int() qabul qiladi, lekin qiymat mos emas.", explanation="Matn to'g'ri tur, lekin qiymati songa aylanmaydi."),
        single('l61_quiz_1', "TypeError", "Qaysi ifoda `TypeError` beradi?", options=[opt("`\"5\" + 3`", True), opt("`int(\"5\") + 3`", False), opt("`5 + 3`", False)], hint="Matn va son.", explanation="Matn bilan sonni qo'shib bo'lmaydi."),
        single('l61_quiz_2', "NameError", "`print(natija)` (natija hech qachon yaratilmagan) qaysi xato?", options=[opt("`NameError`", True), opt("`SyntaxError`", False), opt("`ValueError`", False)], hint="Nom topilmadi.", explanation="O'zgaruvchi yaratilmagan."),
        single('l61_quiz_3', "SyntaxError", "`SyntaxError` qachon yuz beradi?", options=[opt("Dastur ishga tushishidan oldin, yozilish noto'g'ri bo'lsa", True), opt("Foydalanuvchi noto'g'ri son kiritsa", False), opt("Nolga bo'lganda", False)], hint="Kodning yozilishi.", explanation="Python kodni o'qiy olmaydi."),
        fix_task('l61_assignment', "Uchta xatoni tuzating", r"""
Dasturda **uchta** xato bor (har xil turda). Ularni birin-ketin topib tuzating. To'g'ri natija:

```
Ali, 17 yosh
Yig'indi: 25
```
""", section='assignment', points=10, starter_code='ism = "Ali"\nyosh = "17"\nprint(ism + ", " + yosh " yosh")\nson1 = 10\nson2 = "15"\nprint("Yig\'indi:", son1 + son2)\n',
            tests=[T('runs_ok', description="Dastur xatosiz ishlaydi"), T('output_equals', "Ali, 17 yosh\nYig'indi: 25", "Natija to'g'ri")],
            hint="1) Birinchi `print` da vergul yetishmayapti. 2) `son2` matn. Xabarni o'qing — Python o'zi aytadi.", partial_solution='ism = "Ali"\nyosh = "17"\nprint(ism + ", " + yosh + " yosh")\nson1 = 10\nson2 = "15"\n# oxirgi qatordagi tur xatosini tuzating\n', full_solution='ism = "Ali"\nyosh = "17"\nprint(ism + ", " + yosh + " yosh")\nson1 = 10\nson2 = "15"\nprint("Yig\'indi:", son1 + int(son2))\n', explanation="`SyntaxError` (yetishmayotgan `+`), `TypeError` (son + matn) tuzatildi."),
        single('l61_practice_easy', "Easy: IndexError", "`[1, 2, 3][3]` qaysi xatoni beradi?", section='practice', difficulty='easy', options=[opt("`IndexError`", True), opt("`KeyError`", False), opt("`ValueError`", False)], hint="List indeksi.", explanation="`IndexError`: 3 ta element — indekslar 0, 1, 2."),
        fix_task('l61_practice_medium', "Medium: KeyError", "`d[\"narx\"]` xato beryapti. Kalit nomini tuzating — natija `5000`.", section='practice', difficulty='medium', points=5, starter_code='d = {"nom": "Non", "Narx": 5000}\nprint(d["narx"])\n', tests=[T('output_equals', "5000", "Natija: 5000")], hint="Kalitlar harf registrini farqlaydi.", full_solution='d = {"nom": "Non", "narx": 5000}\nprint(d["narx"])\n', explanation="`\"Narx\"` va `\"narx\"` — turli kalitlar."),
        code_task('l61_practice_code', "Medium: TypeError ning oldini olish", r"""
Foydalanuvchi **ism** va **yosh**ni kiritadi (ikkita `input()`). Dastur `Ali 17 yoshda` shaklida (ism, yosh, `yoshda`) chiqarsin va **keyingi qatorda** kelasi yilgi yoshni (`yosh + 1`) chiqarsin: `18`. Xato chiqmasligi uchun turlarni mos qiling. `Ali`, `17` → `Ali 17 yoshda` va `18`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Ali 17 yoshda\n18", "Ali/17", stdin="Ali\n17\n"), T('output_equals', "Vali 30 yoshda\n31", "Vali/30", stdin="Vali\n30\n")], hint="`input()` matn qaytaradi: hisoblash uchun `int()`.", full_solution='ism = input()\nyosh = int(input())\nprint(ism, yosh, "yoshda")\nprint(yosh + 1)\n', explanation="`int()` bilan turni mos qildik — `TypeError` bo'lmaydi."),
        fix_task('l61_practice_hard', "Hard: mantiqiy xato", "Dastur xatosiz ishlaydi, lekin natija noto'g'ri: ikkita sonning **o'rtachasi** `5.0` bo'lishi kerak (`4` va `6`), lekin `7.0` chiqaryapti. Tuzating.", section='practice', difficulty='hard', points=5, starter_code='a = 4\nb = 6\nprint(a + b / 2)\n', tests=[T('output_equals', "5.0", "Natija: 5.0")], hint="Amallar tartibi: avval bo'lish bajariladi.", full_solution='a = 4\nb = 6\nprint((a + b) / 2)\n', explanation="Qavs amallar tartibini o'zgartirdi. Python mantiqiy xatolarni topmaydi — buni siz topasiz."),
    ])

# ==============================================================================
# 62-DARS
# ==============================================================================
LESSON_62 = L(62, "try va except", 13,
    "try/except bilan xatoni ushlab, dastur to'xtab qolmasligini ta'minlash.",
    ["try", "except", "Xatoni ushlash", "Dastur davom etadi", "Foydalanuvchiga tushunarli xabar"],
    [
        text(r"""
Dastur foydalanuvchidan son so'radi, u esa `salom` deb yozdi — `ValueError` va dastur **qulab tushdi**. Haqiqiy dasturlar bunday paytda to'xtab qolmaydi, «Iltimos, son kiriting» deydi. Buni **`try/except`** qiladi.
""", title="Dastur qulamasin"),
        text(r"""
```python
try:
    son = int(input("Son kiriting: "))
    print("Kvadrati:", son * son)
except:
    print("Bu son emas!")
print("Dastur davom etadi")
```

- **`try:`** — «shuni **sinab ko'r**» (xavfli kod shu yerda).
- **`except:`** — «xato bo'lsa, shuni **qil**».
- `try` ichida xato bo'lmasa — `except` o'tkazib yuboriladi.
- Xato bo'lsa — `try` ning qolgan qismi **tashlab yuboriladi**, `except` ishlaydi va dastur **davom etadi**.
- `try` dan oldin va `except` dan keyingi kod odatdagidek ishlaydi.
""", title="try / except"),
        callout('analogy', r"""
`try/except` — **xavfsizlik to'ri** sirk artistining tagida: yiqilsa ham jarohat yo'q, shou davom etadi.
""", title="Hayotiy o'xshatish"),
        example(r'''
try:
    print("Boshlandi")
    x = int("abc")
    print("Bu qator bajarilmaydi")
except:
    print("Xato yuz berdi!")
print("Davom etamiz")
''', title="Xato ushlandi", body="`int(\"abc\")` xato berishi bilan `try` to'xtadi: `Boshlandi`, `Xato yuz berdi!`, `Davom etamiz`."),
        example(r'''
matn = input("Yosh: ")
try:
    yosh = int(matn)
    print("Kelasi yil:", yosh + 1)
except:
    print("Iltimos, son kiriting")
''', title="Amaliy: xavfsiz kiritish", body="`17` → `Kelasi yil: 18`; `abc` → `Iltimos, son kiriting`. Dastur ikkala holatda ham tugallanadi — qulamaydi."),
        exercise('l62_inline_pred'),
        callout('warning', r"""
Yalang'och `except:` **hamma** xatoni ushlaydi — shu jumladan siz kutmaganlarni ham. Keyingi darsda aniq xato turini ko'rsatishni o'rganamiz — bu to'g'rirog'i.
""", title="Diqqat"),
        recap(["`try:` — xavfli kod", "`except:` — xato bo'lsa", "dastur qulamaydi, davom etadi"], "turli xatolarga (masalan, nolga bo'lish va noto'g'ri kiritish) turlicha javob berish mumkinmi?"),
    ],
    [
        predict('l62_inline_pred', "try/except", "Dastur nima chiqaradi?", section='inline', code='try:\n    print(10 / 0)\nexcept:\n    print("xato")\nprint("tugadi")\n', answer="xato\ntugadi", points=2, hint="Nolga bo'lish xato beradi.", explanation="`except` ishladi, dastur davom etdi."),
        predict('l62_quiz_1', "Xatosiz try", "Dastur nima chiqaradi?", code='try:\n    print("A")\nexcept:\n    print("B")\nprint("C")\n', answer="A\nC", hint="Xato yo'q.", explanation="`except` ishlamaydi."),
        predict('l62_quiz_2', "Qolgan qism tashlanadi", "Dastur nima chiqaradi?", code='try:\n    print("1")\n    int("x")\n    print("2")\nexcept:\n    print("3")\n', answer="1\n3", hint="Xatodan keyingi qator bajarilmaydi.", explanation="`1` chiqdi, xatodan keyin `except`."),
        single('l62_quiz_3', "try nima?", "`try:` bloki nimani bildiradi?", options=[opt("Xavfli kodni sinab ko'rish", True), opt("Xatoni yaratish", False), opt("Funksiyani yaratish", False)], hint="Sinab ko'r.", explanation="Xato bo'lishi mumkin bo'lgan kod shu yerda."),
        code_task('l62_assignment', "Xavfsiz son o'qish", r"""
Foydalanuvchi son kiritadi. Agar son to'g'ri bo'lsa — uning **ikki baravarini** chiqaring, aks holda `Son kiriting!` deb chiqaring. `5` → `10`; `abc` → `Son kiriting!`.
""", starter_code='', points=10, tests=[T('output_equals', "10", "5", stdin="5\n"), T('output_equals', "Son kiriting!", "abc", stdin="abc\n"), T('output_equals', "-6", "-3", stdin="-3\n"), T('output_equals', "Son kiriting!", "3.5 (kasr)", stdin="3.5\n", hidden=True), T('code_contains', 'try', "`try` ishlatilgan"), T('code_contains', 'except', "`except` ishlatilgan")],
            hint="`int(input())` ni `try` ichiga qo'ying.", partial_solution='try:\n    son = int(input())\n    print(son * 2)\nexcept:\n    # xabarni chiqaring\n    pass\n', full_solution='try:\n    son = int(input())\n    print(son * 2)\nexcept:\n    print("Son kiriting!")\n', explanation="Xato bo'lishi mumkin bo'lgan qator `try` ichida."),
        single('l62_practice_easy', "Easy: except", "`except` bloki qachon ishlaydi?", section='practice', difficulty='easy', options=[opt("`try` ichida xato bo'lganda", True), opt("Har doim", False), opt("Hech qachon", False)], hint="Xatoni ushlaydi.", explanation="Xato bo'lsa."),
        code_task('l62_practice_medium', "Medium: nolga bo'lish", r"""
Foydalanuvchi ikki son kiritadi (butun). Bo'linmani chiqaring; xato bo'lsa (nolga bo'lish yoki noto'g'ri kiritish) — `Hisoblab bo'lmadi`. `10`, `4` → `2.5`; `5`, `0` → `Hisoblab bo'lmadi`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "2.5", "10/4", stdin="10\n4\n"), T('output_equals', "Hisoblab bo'lmadi", "5/0", stdin="5\n0\n"), T('output_equals', "Hisoblab bo'lmadi", "a/2", stdin="a\n2\n", hidden=True)], hint="Ikkala `input` va bo'lish `try` ichida.", full_solution='try:\n    a = int(input())\n    b = int(input())\n    print(a / b)\nexcept:\n    print("Hisoblab bo\'lmadi")\n', explanation="Bitta `try` ikkala xatoni ushlaydi."),
        code_task('l62_practice_hard', "Hard: to'g'ri son kiritilguncha", r"""
Foydalanuvchi **to'g'ri butun son** kiritguncha so'rayveradi: noto'g'ri bo'lsa `Qayta kiriting` chiqaring; to'g'ri bo'lsa — `Qabul qilindi: <son>` va tugaydi. Kiritish `a`, `x1`, `7` → `Qayta kiriting`, `Qayta kiriting`, `Qabul qilindi: 7`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Qayta kiriting\nQayta kiriting\nQabul qilindi: 7", "a, x1, 7", stdin="a\nx1\n7\n"), T('output_equals', "Qabul qilindi: 5", "birinchi urinishda", stdin="5\n"), T('code_contains', 'while', "`while` ishlatilgan")], hint="`while True:` ichida `try`; muvaffaqiyatda `break`.", partial_solution='while True:\n    try:\n        son = int(input())\n        # qabul qilib to\'xtating\n    except:\n        print("Qayta kiriting")\n', full_solution='while True:\n    try:\n        son = int(input())\n        print("Qabul qilindi:", son)\n        break\n    except:\n        print("Qayta kiriting")\n', explanation="`while True` + `try/except` + `break` — kiritishni tekshirishning klassik usuli."),
    ])

# ==============================================================================
# 63-DARS
# ==============================================================================
LESSON_63 = L(63, "Bir nechta xatolarni boshqarish", 13,
    "Aniq xato turini (except ValueError) ushlash, bir nechta except yozish, `as e` bilan xato matnini olish va bir bloklarda bir nechta turni ushlash.",
    ["except ValueError", "Bir nechta except", "as e", "Tuple bilan ushlash", "Umumiy Exception"],
    [
        text(r"""
Shifokor turli kasalliklarga **turli davo** beradi. Dasturda ham: `ValueError` (noto'g'ri kiritish) va `ZeroDivisionError` (nolga bo'lish) uchun **turli xabarlar** kerak. Buning uchun `except` dan keyin **xato turini** yozamiz.
""", title="Har kasalga o'z davosi"),
        text(r"""
```python
try:
    a = int(input())
    b = int(input())
    print(a / b)
except ValueError:
    print("Son kiriting!")
except ZeroDivisionError:
    print("Nolga bo'lib bo'lmaydi!")
```

- `except TuruXato:` — faqat shu turdagi xatoni ushlaydi; boshqa xato tegilmaydi (dastur qulaydi — bu to'g'ri, yashirin xato yomonroq).
- Istalgancha `except` yozish mumkin; Python **yuqoridan pastga** tekshiradi va birinchi mosini ishlatadi.
- Ikki turga bir javob: `except (ValueError, TypeError):`.
- Xato matnini olish: `except ValueError as e:` — `print(e)`.
- Hamma xatoni ushlovchi oxirgi tarmoq: `except Exception:`.
""", title="Aniq xato turlari"),
        callout('analogy', r"""
Qo'ng'iroq markazi: «To'lov bo'yicha — 1, texnik muammo — 2». Har bir muammo **o'z bo'limiga** yo'naltiriladi.
""", title="Hayotiy o'xshatish"),
        example(r'''
def bol(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Nolga bo'lib bo'lmaydi"

print(bol(10, 2))
print(bol(1, 0))
''', title="ZeroDivisionError", body="`5.0` va `Nolga bo'lib bo'lmaydi`. Aniq tur ushlandi."),
        example(r'''
for matn in ["12", "abc", "0"]:
    try:
        son = int(matn)
        print(100 // son)
    except ValueError as e:
        print("Qiymat xato:", matn)
    except ZeroDivisionError:
        print("Nol mumkin emas")
''', title="Amaliy: bir nechta except", body="`8`, `Qiymat xato: abc`, `Nol mumkin emas`. Bitta siklda uch xil holat uch xil javob oldi."),
        exercise('l63_inline_pred'),
        callout('warning', r"""
`except` ning tartibi muhim: avval **aniq** turlar, oxirida umumiy `Exception`. Aks holda umumiy tarmoq hamma narsani «yutib» yuboradi.
""", title="Diqqat"),
        recap(["`except TuruXato:` — aniq tur", "bir nechta `except` — har biriga o'z javobi", "`as e` — xato matni; `(A, B)` — ikki tur"], "xato bo'lmagan holda yoki har qanday holatda bajariladigan kod uchun nima bor?"),
    ],
    [
        predict('l63_inline_pred', "Aniq tur", "Dastur nima chiqaradi?", section='inline', code='try:\n    print(int("x"))\nexcept ZeroDivisionError:\n    print("A")\nexcept ValueError:\n    print("B")\n', answer="B", points=2, hint="`int(\"x\")` — qaysi xato?", explanation="`ValueError`."),
        predict('l63_quiz_1', "Tartib", "Dastur nima chiqaradi?", code='try:\n    print(5 / 0)\nexcept Exception:\n    print("umumiy")\nexcept ZeroDivisionError:\n    print("aniq")\n', answer="umumiy", hint="Birinchi mos tarmoq ishlaydi.", explanation="`Exception` hamma xatoni ushlaydi — shu sabab u oxirida bo'lishi kerak."),
        predict('l63_quiz_2', "as e", "Dastur nima chiqaradi?", code='try:\n    [1, 2][5]\nexcept IndexError as e:\n    print("xato:", e)\n', answer="xato: list index out of range", hint="`e` — xato matni.", explanation="Pythonning xato matni."),
        single('l63_quiz_3', "Ikki tur", "Ikkita xato turiga bir xil javob uchun qaysi yozuv to'g'ri?", options=[opt("`except (ValueError, TypeError):`", True), opt("`except ValueError, TypeError:`", False), opt("`except ValueError and TypeError:`", False)], hint="Tuple.", explanation="Turlar tuple ichida."),
        code_task('l63_assignment', "Himoyalangan kalkulyator", r"""
Foydalanuvchi ikki son (`a`, `b`, kasr bo'lishi mumkin — `float`) kiritadi. `a / b` ni **2 xonali kasr** bilan chiqaring. Xatolar: son emas → `Faqat son kiriting`; nolga bo'lish → `Nolga bo'lib bo'lmaydi`. `7`, `2` → `3.50`.
""", starter_code='', points=10, tests=[T('output_equals', "3.50", "7/2", stdin="7\n2\n"), T('output_equals', "Faqat son kiriting", "abc", stdin="abc\n2\n"), T('output_equals', "Nolga bo'lib bo'lmaydi", "5/0", stdin="5\n0\n"), T('output_equals', "-0.50", "manfiy", stdin="-1\n2\n", hidden=True), T('code_contains', 'ValueError', "`ValueError` ushlangan"), T('code_contains', 'ZeroDivisionError', "`ZeroDivisionError` ushlangan")],
            hint="`float(input())`; ikkita alohida `except`.", partial_solution='try:\n    a = float(input())\n    b = float(input())\n    print(f"{a / b:.2f}")\nexcept ValueError:\n    print("Faqat son kiriting")\n# ZeroDivisionError uchun except qo\'shing\n', full_solution='try:\n    a = float(input())\n    b = float(input())\n    print(f"{a / b:.2f}")\nexcept ValueError:\n    print("Faqat son kiriting")\nexcept ZeroDivisionError:\n    print("Nolga bo\'lib bo\'lmaydi")\n', explanation="Har bir xato turiga o'z javobi."),
        single('l63_practice_easy', "Easy: xato turi", "Nolga bo'lish qaysi xatoni beradi?", section='practice', difficulty='easy', options=[opt("`ZeroDivisionError`", True), opt("`ValueError`", False), opt("`TypeError`", False)], hint="Nomida «nol».", explanation="`ZeroDivisionError`."),
        code_task('l63_practice_medium', "Medium: indeks yoki kalit", r"""
`royxat = [10, 20, 30]` berilgan. Foydalanuvchi indeks kiritadi — element chiqsin; indeks noto'g'ri bo'lsa (`IndexError`) → `Bunday indeks yo'q`, son emas bo'lsa (`ValueError`) → `Indeks son bo'lishi kerak`. `1` → `20`, `9` → `Bunday indeks yo'q`, `a` → `Indeks son bo'lishi kerak`.
""", section='practice', difficulty='medium', points=5, starter_code='royxat = [10, 20, 30]\n', tests=[T('output_equals', "20", "1", stdin="1\n"), T('output_equals', "Bunday indeks yo'q", "9", stdin="9\n"), T('output_equals', "Indeks son bo'lishi kerak", "a", stdin="a\n"), T('output_equals', "30", "-1", stdin="-1\n", hidden=True)], hint="Ikkita `except`.", full_solution='royxat = [10, 20, 30]\ntry:\n    i = int(input())\n    print(royxat[i])\nexcept IndexError:\n    print("Bunday indeks yo\'q")\nexcept ValueError:\n    print("Indeks son bo\'lishi kerak")\n', explanation="Turli xatolar — turli xabarlar."),
        code_task('l63_practice_hard', "Hard: xavfsiz bo'lish funksiyasi", r"""
`xavfsiz_bol(a, b)` — `a / b` ni qaytarsin; nolga bo'lishda `"nol"`, son bo'lmagan qiymatda (`TypeError`) `"tur"` qaytarsin. `xavfsiz_bol(6, 3)` → `2.0`; `xavfsiz_bol(1, 0)` → `nol`; `xavfsiz_bol("a", 2)` → `tur`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "2.0\nnol\ntur\ntur", "Natija", harness='print(xavfsiz_bol(6, 3))\nprint(xavfsiz_bol(1, 0))\nprint(xavfsiz_bol("a", 2))\nprint(xavfsiz_bol(None, 1))')], hint="`return` ni `try` ichida ham ishlatish mumkin.", full_solution='def xavfsiz_bol(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return "nol"\n    except TypeError:\n        return "tur"\n', explanation="Funksiya ichida xatolar ushlandi."),
    ])

# ==============================================================================
# 64-DARS
# ==============================================================================
LESSON_64 = L(64, "else va finally", 12,
    "try/except bilan else (xato bo'lmaganda) va finally (har doim) bloklarini ishlatish.",
    ["else", "finally", "Bajarilish tartibi", "Tozalash vazifalari"],
    [
        text(r"""
Bankomatdan pul yechishda: xato bo'lsa ham, bo'lmasa ham **karta albatta qaytariladi**. Dasturda ham ba'zi ishlar **har qanday holatda** bajarilishi kerak. Buning uchun `try` ga ikkita qo'shimcha blok bor: `else` va `finally`.
""", title="Har holda bajariladigan ish"),
        text(r"""
```python
try:
    son = int(input())
except ValueError:
    print("Xato kiritish")
else:
    print("Muvaffaqiyatli:", son)
finally:
    print("Tugadi")
```

| Blok | Qachon ishlaydi |
|---|---|
| `try` | doim boshida |
| `except` | `try` da xato bo'lsa |
| `else` | `try` da xato **bo'lmasa** |
| `finally` | **har doim** — xato bo'lsa ham, bo'lmasa ham |

- `else` — «hammasi yaxshi ketsa» bajariladigan kod (xato **ushlanmasligi kerak** bo'lgan ishlar).
- `finally` — tozalash: faylni yopish, «tugadi» deb yozish, hisoblagichni oshirish.
- Tartib: `try` → `except` → `else` → `finally`.
""", title="try / except / else / finally"),
        callout('analogy', r"""
Ofisdan chiqish: ish yaxshi o'tdimi, muammo bo'ldimi — **chiroqni o'chirib, eshikni qulflaysiz** (`finally`).
""", title="Hayotiy o'xshatish"),
        example(r'''
for matn in ["5", "x"]:
    try:
        n = int(matn)
    except ValueError:
        print(matn, "— xato")
    else:
        print(matn, "— son:", n)
    finally:
        print("tekshirildi")
''', title="Bajarilish tartibi", body="`5 — son: 5`, `tekshirildi`, `x — xato`, `tekshirildi`. `finally` ikkala holatda ham ishladi."),
        example(r'''
urinishlar = 0
for q in ["10", "abc", "7"]:
    try:
        qiymat = int(q)
    except ValueError:
        print("Noto'g'ri:", q)
    else:
        print("Qabul:", qiymat)
    finally:
        urinishlar = urinishlar + 1
print("Urinishlar:", urinishlar)
''', title="Amaliy: urinishlarni sanash", body="`finally` urinishlarni har holda oshirdi: `Qabul: 10`, `Noto'g'ri: abc`, `Qabul: 7`, `Urinishlar: 3`."),
        exercise('l64_inline_pred'),
        callout('tip', r"""
`finally` da `return` ishlatmang — u xatoni «yutib» yuborishi mumkin. U faqat tozalash uchun.
""", title="Maslahat"),
        recap(["`else` — xato bo'lmasa", "`finally` — har doim", "tartib: try → except → else → finally"], "o'zimiz xato chiqara olamizmi? Masalan, noto'g'ri qiymat kelganda dasturni to'xtatish uchun?"),
    ],
    [
        predict('l64_inline_pred', "Tartib", "Dastur nima chiqaradi?", section='inline', code='try:\n    print("1")\nexcept:\n    print("2")\nelse:\n    print("3")\nfinally:\n    print("4")\n', answer="1\n3\n4", points=2, hint="Xato yo'q.", explanation="try, else, finally."),
        predict('l64_quiz_1', "Xato bilan", "Dastur nima chiqaradi?", code='try:\n    int("a")\nexcept ValueError:\n    print("E")\nelse:\n    print("L")\nfinally:\n    print("F")\n', answer="E\nF", hint="`else` ishlamaydi.", explanation="except va finally."),
        single('l64_quiz_2', "finally", "`finally` bloki qachon ishlaydi?", options=[opt("Har doim", True), opt("Faqat xato bo'lganda", False), opt("Faqat xato bo'lmaganda", False)], hint="Chiroqni o'chirish.", explanation="Xato bo'lsa ham, bo'lmasa ham."),
        single('l64_quiz_3', "else", "`try` ga qo'shilgan `else` qachon ishlaydi?", options=[opt("`try` da xato bo'lmaganda", True), opt("Har doim", False), opt("Xato bo'lganda", False)], hint="Hammasi yaxshi bo'lsa.", explanation="Xato bo'lmasa."),
        code_task('l64_assignment', "Natijani tekshirish", r"""
Foydalanuvchi butun son kiritadi. Son to'g'ri bo'lsa (`else`) — `Kvadrat: <son*son>`; noto'g'ri bo'lsa (`except ValueError`) — `Xato`. Har ikki holatda ham oxirida `Hisoblash tugadi` chiqsin (`finally`). `4` → `Kvadrat: 16` va `Hisoblash tugadi`.
""", starter_code='', points=10, tests=[T('output_equals', "Kvadrat: 16\nHisoblash tugadi", "4", stdin="4\n"), T('output_equals', "Xato\nHisoblash tugadi", "abc", stdin="abc\n"), T('output_equals', "Kvadrat: 0\nHisoblash tugadi", "0", stdin="0\n", hidden=True), T('code_contains', 'else', "`else` ishlatilgan"), T('code_contains', 'finally', "`finally` ishlatilgan")],
            hint="`try` ga faqat `int(input())`; hisoblash `else` da.", partial_solution='try:\n    son = int(input())\nexcept ValueError:\n    print("Xato")\nelse:\n    print("Kvadrat:", son * son)\n# finally qo\'shing\n', full_solution='try:\n    son = int(input())\nexcept ValueError:\n    print("Xato")\nelse:\n    print("Kvadrat:", son * son)\nfinally:\n    print("Hisoblash tugadi")\n', explanation="`else` — muvaffaqiyat; `finally` — har doim."),
        single('l64_practice_easy', "Easy: tartib", "To'g'ri tartib qaysi?", section='practice', difficulty='easy', options=[opt("`try`, `except`, `else`, `finally`", True), opt("`try`, `finally`, `except`, `else`", False), opt("`try`, `else`, `except`, `finally`", False)], hint="Ketma-ketlikni eslang.", explanation="try → except → else → finally."),
        code_task('l64_practice_medium', "Medium: sanagich", r"""
Foydalanuvchi 3 ta qiymat kiritadi (alohida qatorlarda). Har birini `int` ga aylantirishga urinib: to'g'ri bo'lsa — `OK`, bo'lmasa — `XATO` chiqaring. Oxirida jami urinishlar sonini (`finally` bilan sanab) `Jami: 3` deb chiqaring. `5`, `a`, `7` → `OK`, `XATO`, `OK`, `Jami: 3`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "OK\nXATO\nOK\nJami: 3", "5, a, 7", stdin="5\na\n7\n"), T('output_equals', "XATO\nXATO\nXATO\nJami: 3", "hammasi xato", stdin="a\nb\nc\n", hidden=True)], hint="`sanagich` ni `finally` ichida oshiring.", full_solution='sanagich = 0\nfor i in range(3):\n    try:\n        int(input())\n    except ValueError:\n        print("XATO")\n    else:\n        print("OK")\n    finally:\n        sanagich = sanagich + 1\nprint("Jami:", sanagich)\n', explanation="`finally` har urinishda ishladi."),
        code_task('l64_practice_hard', "Hard: faqat musbat sonlar yig'indisi", r"""
Foydalanuvchi 4 ta qiymat kiritadi. Son bo'lmaganlarni `ValueError` bilan o'tkazib yuboring (`Xato: <qiymat>` chiqaring), son bo'lib **musbat** bo'lsa yig'indiga qo'shing (`else` ichida). Oxirida `Yig'indi: <N>`. `5`, `x`, `-2`, `3` → `Xato: x`, `Yig'indi: 8`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Xato: x\nYig'indi: 8", "5 x -2 3", stdin="5\nx\n-2\n3\n"), T('output_equals', "Yig'indi: 0", "hammasi manfiy", stdin="-1\n-2\n-3\n0\n"), T('output_equals', "Xato: a\nXato: b\nXato: c\nXato: d\nYig'indi: 0", "hammasi xato", stdin="a\nb\nc\nd\n", hidden=True)], hint="`try: n = int(q)`, `except ValueError: print(...)`, `else: if n > 0: ...`.", full_solution='jami = 0\nfor i in range(4):\n    q = input()\n    try:\n        n = int(q)\n    except ValueError:\n        print("Xato:", q)\n    else:\n        if n > 0:\n            jami = jami + n\nprint("Yig\'indi:", jami)\n', explanation="`else` ichida oddiy `if` ishlatildi."),
    ])

# ==============================================================================
# 65-DARS
# ==============================================================================
LESSON_65 = L(65, "raise orqali xato chiqarish va xatolarni tahlil qilish", 14,
    "raise bilan o'z xatosini chiqarish, to'g'ri xabar yozish, xatolarni uzatish va xato xabarini tahlil qilish.",
    ["raise", "Xabar bilan xato", "Tekshiruvlar (validatsiya)", "Xatoni tahlil qilish", "Debugging usullari"],
    [
        text(r"""
Siz funksiya yozdingiz: `yosh_tekshir(yosh)`. Kimdir unga `-5` bersa-chi? Funksiya jim turib noto'g'ri natija bermasligi kerak — **xato chiqarib**, «yosh manfiy bo'la olmaydi» deyishi kerak. Xatoni o'zimiz **ko'taramiz** — `raise` bilan.
""", title="Xatoni o'zimiz chiqaramiz"),
        text(r"""
```python
def yosh_tekshir(yosh):
    if yosh < 0:
        raise ValueError("Yosh manfiy bo'la olmaydi")
    return yosh

try:
    yosh_tekshir(-5)
except ValueError as e:
    print("Xato:", e)       # Xato: Yosh manfiy bo'la olmaydi
```

- `raise XatoTuri("xabar")` — xatoni ko'taradi; dastur (agar ushlanmasa) to'xtaydi.
- Xabar **aniq va foydali** bo'lishi kerak: nima noto'g'ri va nima kutilgan edi.
- Mos tur tanlang: noto'g'ri **qiymat** → `ValueError`, noto'g'ri **tur** → `TypeError`.
- Ushlangan xatoni boshqalarga **uzatish**: `except ...: raise` (bo'sh `raise`).

**Xatoni tahlil qilish tartibi:** 1) tur va izohni o'qing; 2) qator raqamini toping; 3) shu qatordagi qiymatlarni `print` bilan tekshiring; 4) bitta o'zgarish qiling va qayta sinang.
""", title="raise"),
        callout('analogy', r"""
`raise` — **qizil bayroq ko'tarish**: «bu yerda nimadir noto'g'ri!». Boshqa funksiya yoki `try/except` bayroqni ko'rib, chora ko'radi.
""", title="Hayotiy o'xshatish"),
        example(r'''
def kvadrat_ildiz_butun(n):
    if n < 0:
        raise ValueError("Manfiy sondan ildiz olinmaydi")
    return int(n ** 0.5)

print(kvadrat_ildiz_butun(16))
try:
    kvadrat_ildiz_butun(-4)
except ValueError as e:
    print("Xato:", e)
''', title="Xato chiqaruvchi funksiya", body="`4` va `Xato: Manfiy sondan ildiz olinmaydi`."),
        example(r'''
def baho_tekshir(ball):
    if type(ball) != int:
        raise TypeError("Ball butun son bo'lishi kerak")
    if ball < 0 or ball > 100:
        raise ValueError(f"Ball 0–100 oralig'ida bo'lishi kerak, berilgan: {ball}")
    return ball

for q in [85, 150, "a"]:
    try:
        print("OK:", baho_tekshir(q))
    except (ValueError, TypeError) as e:
        print("Xato:", e)
''', title="Amaliy: validatsiya", body="`OK: 85`, `Xato: Ball 0–100 oralig'ida bo'lishi kerak, berilgan: 150`, `Xato: Ball butun son bo'lishi kerak`. Turli xato turlari — turli sabablar."),
        exercise('l65_inline_pred'),
        callout('tip', r"""
Xato xabari yozganda o'zingizdan so'rang: «6 oydan keyin bu xabarni o'qigan odam muammoni darhol tushunadimi?»
""", title="Yaxshi xabar"),
        recap(["`raise XatoTuri(\"xabar\")` — xato chiqaradi", "mos tur va aniq xabar tanlang", "xatoni tahlil qilish: tur → qator → qiymatlar → bitta o'zgarish"], "modul loyihasida xatolarga chidamli kalkulyator yaratamiz. Qaysi xatolarni ushlash kerak bo'ladi?"),
    ],
    [
        predict('l65_inline_pred', "raise", "Dastur nima chiqaradi?", section='inline', code='try:\n    raise ValueError("Salom")\nexcept ValueError as e:\n    print("Ushlandi:", e)\n', answer="Ushlandi: Salom", points=2, hint="Xabar `e` da.", explanation="Xato ko'tarildi va ushlandi."),
        predict('l65_quiz_1', "Funksiya raise", "Dastur nima chiqaradi?", code='def f(x):\n    if x < 0:\n        raise ValueError("manfiy")\n    return x\n\ntry:\n    print(f(3))\n    print(f(-1))\nexcept ValueError as e:\n    print("xato:", e)\n', answer="3\nxato: manfiy", hint="Birinchi chaqiruv muvaffaqiyatli.", explanation="`3` chiqdi, keyin xato."),
        single('l65_quiz_2', "Tur tanlash", "Funksiya noto'g'ri **qiymat** (masalan, manfiy yosh) olsa, qaysi xatoni chiqarish mos?", options=[opt("`ValueError`", True), opt("`NameError`", False), opt("`SyntaxError`", False)], hint="Tur to'g'ri, qiymat noto'g'ri.", explanation="`ValueError`."),
        single('l65_quiz_3', "Tahlil", "Xatoni tahlil qilishning birinchi qadami?", options=[opt("Xato turi va izohini o'qish", True), opt("Kodni butunlay o'chirish", False), opt("Tasodifiy o'zgartirishlar kiritish", False)], hint="Tashxis.", explanation="Avval xabarni o'qing."),
        code_task('l65_assignment', "Yoshni tekshirish funksiyasi", r"""
`yosh_tekshir(yosh)` funksiyasini yarating: agar `yosh` **0 dan kichik** bo'lsa — `ValueError("Yosh manfiy bo'la olmaydi")`; **150 dan katta** bo'lsa — `ValueError("Yosh juda katta")`; aks holda yoshni qaytarsin.
""", starter_code='', points=10, tests=[T('output_equals', "17\n0\nYosh manfiy bo'la olmaydi\nYosh juda katta\n150", "Natija", harness='print(yosh_tekshir(17))\nprint(yosh_tekshir(0))\nfor q in (-5, 200):\n    try:\n        yosh_tekshir(q)\n    except ValueError as e:\n        print(e)\nprint(yosh_tekshir(150))'), T('code_contains', 'raise', "`raise` ishlatilgan")],
            hint="`if yosh < 0: raise ValueError(\"...\")`.", partial_solution='def yosh_tekshir(yosh):\n    if yosh < 0:\n        raise ValueError("Yosh manfiy bo\'la olmaydi")\n    # 150 dan kattasini ham tekshiring\n    return yosh\n', full_solution='def yosh_tekshir(yosh):\n    if yosh < 0:\n        raise ValueError("Yosh manfiy bo\'la olmaydi")\n    if yosh > 150:\n        raise ValueError("Yosh juda katta")\n    return yosh\n', explanation="Funksiya noto'g'ri qiymatni xato bilan rad etadi."),
        single('l65_practice_easy', "Easy: raise", "`raise` nima qiladi?", section='practice', difficulty='easy', options=[opt("Xato chiqaradi", True), opt("Xatoni ushlaydi", False), opt("Funksiya yaratadi", False)], hint="Qizil bayroq.", explanation="Xatoni ko'taradi."),
        code_task('l65_practice_medium', "Medium: musbat son", r"""
`musbat_son()` funksiyasi `input()` dan son o'qisin; son 0 yoki manfiy bo'lsa `ValueError("Musbat bo'lishi kerak")` chiqarsin, aks holda sonni qaytarsin. Dasturda `try` bilan chaqirib, xato bo'lsa `Xato: <xabar>` chiqaring, bo'lmasa `Son: <n>`. `5` → `Son: 5`; `-2` → `Xato: Musbat bo'lishi kerak`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Son: 5", "5", stdin="5\n"), T('output_equals', "Xato: Musbat bo'lishi kerak", "-2", stdin="-2\n"), T('output_equals', "Xato: Musbat bo'lishi kerak", "0", stdin="0\n", hidden=True)], hint="Funksiyada `raise`, tashqarida `try/except ValueError as e`.", full_solution='def musbat_son():\n    n = int(input())\n    if n <= 0:\n        raise ValueError("Musbat bo\'lishi kerak")\n    return n\n\ntry:\n    n = musbat_son()\n    print("Son:", n)\nexcept ValueError as e:\n    print("Xato:", e)\n', explanation="`raise` va `except` birgalikda."),
        code_task('l65_practice_hard', "Hard: parol validatori", r"""
`parol_tekshir(p)` — qoidalar: uzunligi **8 dan kam** bo'lsa `ValueError("Parol juda qisqa")`; tarkibida **raqam yo'q** bo'lsa `ValueError("Parolda raqam bo'lishi kerak")`; aks holda `True` qaytarsin. (Raqam bor-yo'qligini sikl bilan tekshiring: `h in "0123456789"`.)
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "True\nParol juda qisqa\nParolda raqam bo'lishi kerak\nTrue", "Natija", harness='print(parol_tekshir("python123"))\nfor q in ("abc1", "abcdefghij"):\n    try:\n        parol_tekshir(q)\n    except ValueError as e:\n        print(e)\nprint(parol_tekshir("12345678"))')], hint="Avval uzunlik, keyin raqam sikli.", partial_solution='def parol_tekshir(p):\n    if len(p) < 8:\n        raise ValueError("Parol juda qisqa")\n    # raqam borligini tekshiring\n    return True\n', full_solution='def parol_tekshir(p):\n    if len(p) < 8:\n        raise ValueError("Parol juda qisqa")\n    bor = False\n    for h in p:\n        if h in "0123456789":\n            bor = True\n    if not bor:\n        raise ValueError("Parolda raqam bo\'lishi kerak")\n    return True\n', explanation="Bir nechta tekshiruv — har biri o'z xatosi bilan."),
    ])

LESSONS = [LESSON_61, LESSON_62, LESSON_63, LESSON_64, LESSON_65]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("9-modul yakuniy nazorati: Xatolar bilan ishlash", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **xatolarga chidamli kalkulyator**.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m9_a_t1', "try/except", "`try/except` nima uchun kerak?", section='assessment', points=2, options=[opt("Xato yuz berganda dastur qulamasligi uchun", True), opt("Dasturni tezlashtirish uchun", False), opt("O'zgaruvchi yaratish uchun", False)], explanation="Xatoni ushlash uchun."),
    single('m9_a_t2', "ValueError", "`int(\"abc\")` qaysi xatoni beradi?", section='assessment', points=2, options=[opt("`ValueError`", True), opt("`TypeError`", False), opt("`SyntaxError`", False)], explanation="Qiymat songa aylanmaydi."),
    single('m9_a_t3', "finally", "`finally` blokida nima bo'ladi?", section='assessment', points=2, options=[opt("Har doim bajariladi", True), opt("Faqat xato bo'lganda", False), opt("Hech qachon", False)], explanation="Har doim."),
    single('m9_a_t4', "raise", "`raise ValueError(\"x\")` nima qiladi?", section='assessment', points=2, options=[opt("Xato chiqaradi", True), opt("Xatoni ushlaydi", False), opt("Xatoni o'chiradi", False)], explanation="Xatoni ko'taradi."),
    multiple('m9_a_t5', "else/finally", "Qaysi gaplar to'g'ri?", section='assessment', points=2, options=[opt("`else` faqat xato bo'lmaganda ishlaydi", True), opt("`finally` xato bo'lsa ham ishlaydi", True), opt("`else` `try` dan oldin yoziladi", False), opt("`except` `finally` dan keyin keladi", False)], explanation="Tartib: try, except, else, finally."),
    predict('m9_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='try:\n    x = int("5")\n    y = 10 / (x - 5)\nexcept ZeroDivisionError:\n    y = "nol"\nprint(y)\n', answer="nol", explanation="`5 - 5 = 0` — nolga bo'lish."),
    predict('m9_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='def f(n):\n    try:\n        return 10 // n\n    except ZeroDivisionError:\n        return -1\n    finally:\n        print("f")\n\nprint(f(2), f(0))\n', answer="f\nf\n5 -1", explanation="`finally` har chaqiruvda `f` chiqaradi (print argumentlari hisoblanayotganda); keyin `5 -1`."),
    predict('m9_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='try:\n    raise KeyError("a")\nexcept (ValueError, KeyError):\n    print("ushlandi")\nelse:\n    print("else")\n', answer="ushlandi", explanation="`KeyError` ushlandi; `else` ishlamaydi."),
    fix_task('m9_a_f1', "Xatoni tuzating (1)", "Dastur noto'g'ri kiritishda qulamasligi kerak: `abc` → `Xato`, `5` → `10`.", section='assessment', points=4, starter_code='son = int(input())\nprint(son * 2)\n', tests=[T('output_equals', "10", "5", stdin="5\n"), T('output_equals', "Xato", "abc", stdin="abc\n")], hint="`try/except` qo'shing.", full_solution='try:\n    son = int(input())\n    print(son * 2)\nexcept ValueError:\n    print("Xato")\n', explanation="Xavfli kod `try` ichiga."),
    fix_task('m9_a_f2', "Xatoni tuzating (2)", "Funksiya manfiy sonda `ValueError(\"manfiy\")` chiqarishi kerak, lekin xato **ushlanmayapti**.", section='assessment', points=4, starter_code='def f(n):\n    if n < 0:\n        return ValueError("manfiy")\n    return n\n', tests=[T('output_equals', "5\nmanfiy", "Natija", harness='print(f(5))\ntry:\n    f(-1)\nexcept ValueError as e:\n    print(e)')], hint="Xatoni qaytarish emas, ko'tarish kerak.", full_solution='def f(n):\n    if n < 0:\n        raise ValueError("manfiy")\n    return n\n', explanation="`return` o'rniga `raise`."),
    code_task('m9_a_project', "Mini-loyiha: Xatolarga chidamli kalkulyator", r"""
Foydalanuvchi **amal**, **birinchi son** va **ikkinchi son** kiritadi (har biri alohida qatorda). Dastur `q` (amal sifatida) kiritilguncha takrorlanadi.

Qoidalar:
- amallar: `+`, `-`, `*`, `/`;
- sonlar `float` ga aylantiriladi; son emas bo'lsa → `Xato: son kiriting`;
- nolga bo'lish → `Xato: nolga bo'lib bo'lmaydi`;
- noma'lum amal → `raise ValueError("noma'lum amal")` bilan xato chiqarib, `except` da `Xato: noma'lum amal` deb chiqarish;
- muvaffaqiyatli bo'lsa (`else`) → `Natija: <x.xx>` (2 xonali kasr);
- har bir urinishdan keyin (`finally`) sanagich oshadi; `q` kiritilganda `Urinishlar: <N>` chiqarib tugaydi (`q` urinish hisoblanmaydi).

Misol: `+`,`2`,`3` / `/`,`1`,`0` / `x`,`1`,`1` / `q` →
```
Natija: 5.00
Xato: nolga bo'lib bo'lmaydi
Xato: noma'lum amal
Urinishlar: 3
```
(Amal `q` bo'lmasa, ikkita son o'qiladi: noma'lum amal bo'lsa ham sonlar baribir o'qiladi.)
""", section='project', points=20, difficulty='hard', unlock=3, starter_code='# Xatolarga chidamli kalkulyator\n',
        expected_output_example="Natija: 5.00\nXato: nolga bo'lib bo'lmaydi\nXato: noma'lum amal\nUrinishlar: 3",
        tests=[T('output_equals', "Natija: 5.00\nXato: nolga bo'lib bo'lmaydi\nXato: noma'lum amal\nUrinishlar: 3", "Misol ssenariy", stdin="+\n2\n3\n/\n1\n0\nx\n1\n1\nq\n"),
               T('output_equals', "Xato: son kiriting\nNatija: 1.50\nUrinishlar: 2", "Son emas + bo'lish", stdin="*\nabc\n2\n/\n3\n2\nq\n"), T('output_equals', "Urinishlar: 0", "Darhol chiqish", stdin="q\n"),
               T('output_equals', "Natija: -1.00\nNatija: 8.50\nUrinishlar: 2", "Ayirish va ko'paytirish", stdin="-\n2\n3\n*\n2.5\n3.4\nq\n", hidden=True), T('code_contains', 'finally', "`finally` ishlatilgan"), T('code_contains', 'raise', "`raise` ishlatilgan"), T('code_contains', 'else', "`else` ishlatilgan")],
        hint="1) `while True:` ichida `amal = input()`; `if amal == \"q\": break`. 2) `a = input()`, `b = input()` ni `try` ichida `float` ga aylantiring. 3) `if amal == \"+\": ...` zanjiri, oxirida `else: raise ValueError(\"noma'lum amal\")`. 4) `except ValueError as e:` ikki xil holat — ularni xabar matni bilan ajrating.",
        partial_solution='urinishlar = 0\nwhile True:\n    amal = input()\n    if amal == "q":\n        break\n    a = input()\n    b = input()\n    try:\n        a = float(a)\n        b = float(b)\n        # amalni bajaring; noma\'lum amalda raise ValueError("noma\'lum amal")\n    except ValueError as e:\n        pass\n    finally:\n        urinishlar = urinishlar + 1\nprint("Urinishlar:", urinishlar)\n',
        full_solution='urinishlar = 0\nwhile True:\n    amal = input()\n    if amal == "q":\n        break\n    a = input()\n    b = input()\n    try:\n        a = float(a)\n        b = float(b)\n        if amal == "+":\n            natija = a + b\n        elif amal == "-":\n            natija = a - b\n        elif amal == "*":\n            natija = a * b\n        elif amal == "/":\n            natija = a / b\n        else:\n            raise ValueError("noma\'lum amal")\n    except ZeroDivisionError:\n        print("Xato: nolga bo\'lib bo\'lmaydi")\n    except ValueError as e:\n        if str(e) == "noma\'lum amal":\n            print("Xato: noma\'lum amal")\n        else:\n            print("Xato: son kiriting")\n    else:\n        print(f"Natija: {natija:.2f}")\n    finally:\n        urinishlar = urinishlar + 1\nprint("Urinishlar:", urinishlar)\n',
        explanation="Loyiha try/except (bir nechta tur), else, finally va raise ni birlashtiradi."),
])
