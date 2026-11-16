"""Python — 0 dan boshlash · 10-modul: Fayllar va JSON (66–69-darslar)."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 10,
    'title': "Fayllar va JSON",
    'description': "Ma'lumotni dastur yopilgandan keyin ham saqlash: open(), yozish va o'qish, with bilan xavfsiz ishlash va JSON formati.",
}

NOTE_SANDBOX = r"""
> **Eslatma.** O'quv platformasida kodingiz **vaqtincha ishchi papkada** bajariladi: fayllar shu papkada yaratiladi va ishga tushish tugagach avtomatik o'chiriladi. Bu xavfsizlik uchun. Shuning uchun bir ishga tushishda yozilgan faylni **o'sha ishga tushish ichida** o'qishingiz mumkin. Kompyuteringizda (11-modul) fayllar haqiqatan ham saqlanib qoladi.
"""

# ==============================================================================
# 66-DARS
# ==============================================================================
LESSON_66 = L(66, "Fayllar bilan ishlash va open()", 13,
    "Fayl nima ekanini, nima uchun kerakligini bilish, open() va fayl rejimlarini ('r', 'w', 'a') tanish, close() bilan faylni yopish.",
    ["Fayl", "open()", "Rejimlar: r, w, a", "encoding", "close()", "FileNotFoundError"],
    [
        text(r"""
Dastur yopilsa — o'zgaruvchilardagi hamma ma'lumot **yo'qoladi**. Hisob-kitoblar, kundalik yozuvlari, o'yin natijalari saqlanib qolishi uchun ularni **faylga** yozish kerak. Fayl — diskda saqlanadigan nomli ma'lumot.
""", title="Dastur yopilsa ham ma'lumot qolsin"),
        text(NOTE_SANDBOX + r"""
Faylni **ochish** uchun `open()` funksiyasi:

```python
f = open("salom.txt", "w", encoding="utf-8")
f.write("Salom, fayl!")
f.close()
```

| Rejim | Ma'nosi | Fayl yo'q bo'lsa | Fayl bor bo'lsa |
|---|---|---|---|
| `"r"` | o'qish (standart) | `FileNotFoundError` | o'qiydi |
| `"w"` | yozish | yaratadi | **tozalab** qayta yozadi! |
| `"a"` | oxiriga qo'shish | yaratadi | oxiriga qo'shadi |

- Birinchi argument — fayl nomi; ikkinchisi — rejim.
- **`encoding="utf-8"`** — o'zbekcha harflar (`o'`, `g'`, `sh`) to'g'ri saqlanishi uchun har doim yozing.
- Ishlab bo'lgach, **`close()`** bilan yoping (keyingi darslarda buni avtomatlashtiramiz).
""", title="open() va rejimlar"),
        callout('analogy', r"""
`open()` — **daftarni ochish**: `"r"` — o'qish uchun, `"w"` — yangi varaq (eskisi yirtiladi!), `"a"` — oxiriga yozish. `close()` — daftarni yopib qo'yish.
""", title="Hayotiy o'xshatish"),
        example(r'''
f = open("salom.txt", "w", encoding="utf-8")
f.write("Salom, fayl!")
f.close()

g = open("salom.txt", "r", encoding="utf-8")
print(g.read())
g.close()
''', title="Yozish va o'qish", body="Fayl yaratildi, ichiga matn yozildi, yopildi; keyin o'qish uchun qayta ochildi: `Salom, fayl!`."),
        example(r'''
try:
    f = open("yoq_fayl.txt", "r", encoding="utf-8")
    print(f.read())
    f.close()
except FileNotFoundError:
    print("Fayl topilmadi")
''', title="Amaliy: mavjud bo'lmagan fayl", body="Bunday fayl yo'q — `FileNotFoundError`. 9-moduldagi `try/except` bilan ushladik: `Fayl topilmadi`."),
        exercise('l66_inline_fill'),
        callout('warning', r"""
`"w"` rejimi mavjud faylni **to'liq tozalaydi**! Mavjud ma'lumotni saqlab, yangisini qo'shmoqchi bo'lsangiz — `"a"`.
""", title="Diqqat"),
        recap(["`open(nom, rejim, encoding=\"utf-8\")`", "`r` — o'qish, `w` — yozish (tozalaydi), `a` — qo'shish", "ishlab bo'lgach `close()`"], "faylga yozish va undan o'qishning boshqa usullari ham bormi?"),
    ],
    [
        fill('l66_inline_fill', "Rejimni toping", "Faylga **yozish** uchun rejim belgisini yozing.", 'f = open("a.txt", "___", encoding="utf-8")\nf.write("ok")\nf.close()\nprint(open("a.txt", encoding="utf-8").read())\n', ['w'], section='inline', points=2, tests=[T('output_equals', "ok", "Natija: ok")], hint="Yozish — inglizcha write.", explanation="`\"w\"` — yozish."),
        single('l66_quiz_1', "w rejimi", "`\"w\"` rejimi mavjud faylga nima qiladi?", options=[opt("Tozalab, qayta yozadi", True), opt("Oxiriga qo'shadi", False), opt("Faqat o'qiydi", False)], hint="Eski varaq yirtiladi.", explanation="`\"w\"` eski mazmunni o'chiradi."),
        single('l66_quiz_2', "a rejimi", "Mavjud faylning **oxiriga** qo'shish uchun qaysi rejim?", options=[opt("`\"a\"`", True), opt("`\"w\"`", False), opt("`\"r\"`", False)], hint="Append.", explanation="`\"a\"`."),
        predict('l66_quiz_3', "Yozib o'qish", "Dastur nima chiqaradi?", code='f = open("t.txt", "w", encoding="utf-8")\nf.write("Python")\nf.close()\nprint(open("t.txt", encoding="utf-8").read())\n', answer="Python", hint="Yozilgan matn o'qiladi.", explanation="Fayl `Python` bilan to'ldirildi."),
        code_task('l66_assignment', "Ism faylga", r"""
Foydalanuvchi ism kiritadi. Dastur uni `ism.txt` fayliga **yozsin**, keyin faylni qayta ochib o'qisin va `Faylda: <ism>` shaklida chiqarsin. `Aziza` → `Faylda: Aziza`.
""", starter_code='', points=10, tests=[T('output_equals', "Faylda: Aziza", "Aziza", stdin="Aziza\n"), T('output_equals', "Faylda: O'ktam", "O'ktam (maxsus belgi)", stdin="O'ktam\n"), T('code_contains', 'open(', "`open()` ishlatilgan"), T('code_contains', 'close', "`close()` ishlatilgan")],
            hint="`\"w\"` bilan yozing, `close()`, keyin `\"r\"` bilan o'qing.", partial_solution='ism = input()\nf = open("ism.txt", "w", encoding="utf-8")\nf.write(ism)\nf.close()\n# faylni o\'qing va chiqaring\n', full_solution='ism = input()\nf = open("ism.txt", "w", encoding="utf-8")\nf.write(ism)\nf.close()\ng = open("ism.txt", "r", encoding="utf-8")\nprint("Faylda:", g.read())\ng.close()\n', explanation="Avval yozdik va yopdik, keyin o'qish uchun qayta ochdik."),
        single('l66_practice_easy', "Easy: encoding", "O'zbekcha harflar uchun `open()` ga qaysi parametrni qo'shish kerak?", section='practice', difficulty='easy', options=[opt("`encoding=\"utf-8\"`", True), opt("`lang=\"uz\"`", False), opt("`mode=\"u\"`", False)], hint="Kodlash.", explanation="`encoding=\"utf-8\"`."),
        code_task('l66_practice_medium', "Medium: qo'shib yozish", r"""
`log.txt` ga avval `Birinchi` yozing (`"w"`), keyin `"a"` rejimida `Ikkinchi` ni qo'shing. Faylni o'qib chiqaring: `BirinchiIkkinchi`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "BirinchiIkkinchi", "Natija"), T('code_contains', '"a"', "`\"a\"` rejimi ishlatilgan")], hint="Ikki marta `open` — ikki xil rejim.", full_solution='f = open("log.txt", "w", encoding="utf-8")\nf.write("Birinchi")\nf.close()\nf = open("log.txt", "a", encoding="utf-8")\nf.write("Ikkinchi")\nf.close()\nprint(open("log.txt", encoding="utf-8").read())\n', explanation="`\"a\"` oldingi mazmunni saqlaydi."),
        code_task('l66_practice_hard', "Hard: fayl bormi?", r"""
Foydalanuvchi fayl nomini kiritadi. Dastur uni o'qishga harakat qilsin: bor bo'lsa — mazmunini chiqarsin, yo'q bo'lsa — `Fayl topilmadi`. (Tekshiruvda faylni dastur o'zi yaratadi: kod avval `bor.txt` ga `Salom` yozadi.) Nom `bor.txt` → `Salom`; `yoq.txt` → `Fayl topilmadi`.
""", section='practice', difficulty='hard', points=5, starter_code='f = open("bor.txt", "w", encoding="utf-8")\nf.write("Salom")\nf.close()\n', tests=[T('output_equals', "Salom", "bor.txt", stdin="bor.txt\n"), T('output_equals', "Fayl topilmadi", "yoq.txt", stdin="yoq.txt\n")], hint="`try/except FileNotFoundError`.", full_solution='f = open("bor.txt", "w", encoding="utf-8")\nf.write("Salom")\nf.close()\nnom = input()\ntry:\n    g = open(nom, "r", encoding="utf-8")\n    print(g.read())\n    g.close()\nexcept FileNotFoundError:\n    print("Fayl topilmadi")\n', explanation="Mavjud bo'lmagan fayl — `FileNotFoundError`."),
    ])

# ==============================================================================
# 67-DARS
# ==============================================================================
LESSON_67 = L(67, "Faylga yozish va fayldan o'qish", 14,
    "write(), read(), readline(), readlines() usullari, fayl qatorlari bo'ylab for bilan yurish va '\\n' belgisini tushunish.",
    ["write()", "read()", "readline()", "readlines()", "for line in f", "\\n va strip()"],
    [
        text(NOTE_SANDBOX + r"""
Faylga **bir necha qator** yozish va ularni qayta o'qishning usullari bilan tanishamiz.
""", title="Qatorlar bilan ishlash"),
        text(r"""
**Yozish.** `f.write(matn)` — qator oxiriga o'zi `\n` qo'shmaydi! Yangi qator uchun `\n` ni o'zingiz yozing:

```python
f = open("royxat.txt", "w", encoding="utf-8")
f.write("non\n")
f.write("sut\n")
f.close()
```

**O'qish usullari:**

| Usul | Nima beradi |
|---|---|
| `f.read()` | butun faylni **bitta matn** sifatida |
| `f.readline()` | **bitta qator** (oxirida `\n` bilan) |
| `f.readlines()` | hamma qatorlar **ro'yxati** |
| `for qator in f:` | qatorma-qator yurish (eng qulayi) |

Qatorlar oxiridagi `\n` ni olib tashlash uchun `qator.strip()` ishlating.
""", title="write() va o'qish usullari"),
        callout('analogy', r"""
`read()` — **kitobni to'liq o'qib chiqish**, `readline()` — **bitta satr**, `for qator in f` — **barmoq bilan har satrni birin-ketin kuzatish**.
""", title="Hayotiy o'xshatish"),
        example(r'''
f = open("royxat.txt", "w", encoding="utf-8")
f.write("non\n")
f.write("sut\n")
f.write("tuxum\n")
f.close()

g = open("royxat.txt", "r", encoding="utf-8")
for qator in g:
    print(qator.strip())
g.close()
''', title="Yozish va qatorma-qator o'qish", body="Uch qator yozildi, so'ng `for` bilan birin-ketin o'qildi. `strip()` ortiqcha bo'sh qatorlarni (`\\n`) olib tashladi: `non`, `sut`, `tuxum`."),
        example(r'''
f = open("ballar.txt", "w", encoding="utf-8")
f.write("85\n72\n95\n")
f.close()

g = open("ballar.txt", "r", encoding="utf-8")
sonlar = []
for qator in g:
    sonlar.append(int(qator))
g.close()
print(sonlar, sum(sonlar) / len(sonlar))
''', title="Amaliy: fayldan sonlar o'qish", body="Faylda matn sifatida saqlangan ballarni `int()` bilan songa aylantirdik (`int(\"85\\n\")` ham ishlaydi — probel va `\\n` e'tiborsiz). Natija: `[85, 72, 95] 84.0`."),
        exercise('l67_inline_pred'),
        callout('warning', r"""
Fayldan o'qilgan hamma narsa — **matn**. Songa aylantirish uchun `int()`/`float()` kerak. Ro'yxat yoki dictionary'ni faylga yozish uchun esa keyingi darslardagi JSON qulay.
""", title="Diqqat"),
        recap(["`write()` `\\n` ni o'zi qo'shmaydi", "`read()`, `readline()`, `readlines()`, `for qator in f`", "`strip()` — chetdagi `\\n` va bo'sh joylarni olib tashlaydi"], "faylni yopishni unutib qo'ysak-chi? Buni avtomatlashtirish yo'li bormi?"),
    ],
    [
        predict('l67_inline_pred', "readlines()", "Dastur nima chiqaradi?", section='inline', code='f = open("a.txt", "w", encoding="utf-8")\nf.write("x\\ny\\n")\nf.close()\nprint(open("a.txt", encoding="utf-8").readlines())\n', answer="['x\\n', 'y\\n']", points=2, hint="Qatorlar `\\n` bilan.", explanation="`readlines()` qatorlar ro'yxatini `\\n` bilan qaytaradi."),
        predict('l67_quiz_1', "read()", "Dastur nima chiqaradi?", code='f = open("a.txt", "w", encoding="utf-8")\nf.write("ab")\nf.write("cd")\nf.close()\nprint(open("a.txt", encoding="utf-8").read())\n', answer="abcd", hint="`write` yangi qator qo'shmaydi.", explanation="`abcd`."),
        predict('l67_quiz_2', "Qatorlar soni", "Dastur nima chiqaradi?", code='f = open("a.txt", "w", encoding="utf-8")\nf.write("1\\n2\\n3\\n")\nf.close()\nn = 0\nfor q in open("a.txt", encoding="utf-8"):\n    n = n + 1\nprint(n)\n', answer="3", hint="Uch qator.", explanation="3."),
        single('l67_quiz_3', "strip()", "Fayldan o'qilgan qatordagi `\\n` ni olib tashlash uchun?", options=[opt("`qator.strip()`", True), opt("`qator.remove()`", False), opt("`qator.clean()`", False)], hint="Matn metodi.", explanation="`strip()`."),
        code_task('l67_assignment', "Xarid ro'yxatini saqlash", r"""
Foydalanuvchi **3 ta mahsulotni** kiritadi. Dastur ularni `xarid.txt` fayliga har birini **alohida qatorda** yozsin, so'ng faylni o'qib, har bir qatorni `1. non` shaklida raqamlab chiqarsin. `non`, `sut`, `tuxum` →
```
1. non
2. sut
3. tuxum
```
""", starter_code='', points=10, tests=[T('output_equals', "1. non\n2. sut\n3. tuxum", "non sut tuxum", stdin="non\nsut\ntuxum\n"), T('output_equals', "1. a\n2. b\n3. c", "a b c", stdin="a\nb\nc\n", hidden=True), T('code_contains', 'write', "`write` ishlatilgan")],
            hint="Yozishda har mahsulotdan keyin `\\n`; o'qishda `strip()` va `enumerate(..., start=1)`.", partial_solution='f = open("xarid.txt", "w", encoding="utf-8")\nfor i in range(3):\n    f.write(input() + "\\n")\nf.close()\n# faylni o\'qib, raqamlab chiqaring\n', full_solution='f = open("xarid.txt", "w", encoding="utf-8")\nfor i in range(3):\n    f.write(input() + "\\n")\nf.close()\ng = open("xarid.txt", "r", encoding="utf-8")\nfor n, qator in enumerate(g, start=1):\n    print(f"{n}. {qator.strip()}")\ng.close()\n', explanation="Yozish, yopish, o'qish, raqamlash."),
        single('l67_practice_easy', "Easy: read()", "`f.read()` nima qaytaradi?", section='practice', difficulty='easy', options=[opt("Butun faylni bitta matn", True), opt("Faqat birinchi qator", False), opt("Qatorlar ro'yxati", False)], hint="Hammasini.", explanation="Butun fayl bitta matn sifatida."),
        code_task('l67_practice_medium', "Medium: qatorlarni sanash", r"""
Dastur avval `matn.txt` ga 4 qator yozsin: `bir`, `ikki`, `uch`, `to'rt` (har biri alohida qatorda). Keyin faylni o'qib, **qatorlar sonini** va **eng uzun qator** nomini chiqarsin: `4` va `to'rt`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "4\nto'rt", "Natija"), T('code_contains', 'open(', "`open()` ishlatilgan")], hint="`readlines()` va sikl.", full_solution='f = open("matn.txt", "w", encoding="utf-8")\nf.write("bir\\nikki\\nuch\\nto\'rt\\n")\nf.close()\nqatorlar = []\nfor q in open("matn.txt", encoding="utf-8"):\n    qatorlar.append(q.strip())\neng = qatorlar[0]\nfor q in qatorlar:\n    if len(q) > len(eng):\n        eng = q\nprint(len(qatorlar))\nprint(eng)\n', explanation="`to'rt` (5 belgi) eng uzun."),
        code_task('l67_practice_hard', "Hard: qiymatlar yig'indisi", r"""
Foydalanuvchi `n` va keyin `n` ta butun son kiritadi. Dastur sonlarni `sonlar.txt` ga qatorma-qator yozsin, so'ng faylni o'qib, **yig'indi** va **eng katta** qiymatni chiqarsin. `3`: `4`, `9`, `2` → `15` va `9`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "15\n9", "4 9 2", stdin="3\n4\n9\n2\n"), T('output_equals', "-3\n-1", "manfiy", stdin="2\n-2\n-1\n"), T('output_equals', "5\n5", "bitta son", stdin="1\n5\n", hidden=True)], hint="Yozib, yopib, qayta o'qing; `int(qator)`.", full_solution='n = int(input())\nf = open("sonlar.txt", "w", encoding="utf-8")\nfor i in range(n):\n    f.write(input() + "\\n")\nf.close()\nsonlar = []\nfor q in open("sonlar.txt", encoding="utf-8"):\n    sonlar.append(int(q))\nprint(sum(sonlar))\nprint(max(sonlar))\n', explanation="Fayl orqali ma'lumot almashdik."),
    ])

# ==============================================================================
# 68-DARS
# ==============================================================================
LESSON_68 = L(68, "with orqali fayllarni xavfsiz boshqarish", 12,
    "with open(...) as f konstruksiyasi bilan faylni avtomatik yopish va nima uchun u xavfsiz ekanini tushunish.",
    ["with", "as", "Avtomatik yopish", "Xatoda ham yopiladi", "Tozaroq kod"],
    [
        text(NOTE_SANDBOX + r"""
`open()` dan keyin `close()` ni **yozishni unutish** oson. Yoki `close()` ga yetmasdan dastur xato berib to'xtasa-chi? Fayl ochiq qolib, ma'lumot yo'qolishi mumkin. Buning yechimi — **`with`**.
""", title="close() ni unutsak?"),
        text(r"""
```python
with open("royxat.txt", "w", encoding="utf-8") as f:
    f.write("non\n")
    f.write("sut\n")
# bu yerda fayl avtomatik yopilgan
```

- `with open(...) as f:` — blok boshlanishida fayl ochiladi, blok tugashi bilan (xato bo'lsa ham) **avtomatik yopiladi**.
- `close()` yozish **kerak emas**.
- Fayl bilan barcha ishlar **chekinishli blok ichida** bajariladi.
- Bu — fayl bilan ishlashning **tavsiya etilgan** yo'li.
""", title="with open(...) as f"),
        callout('analogy', r"""
`with` — **avtomatik eshik**: kirasiz, ishlaysiz, chiqishingiz bilan u o'zi yopiladi. Hatto yiqilib chiqsangiz ham yopiladi.
""", title="Hayotiy o'xshatish"),
        example(r'''
with open("kundalik.txt", "w", encoding="utf-8") as f:
    f.write("1-kun: Python boshladim\n")
    f.write("2-kun: sikllar\n")

with open("kundalik.txt", "r", encoding="utf-8") as f:
    for qator in f:
        print(qator.strip())
''', title="with bilan yozish va o'qish", body="Natija: `1-kun: Python boshladim` va `2-kun: sikllar`. `close()` kerak bo'lmadi."),
        example(r'''
with open("soz.txt", "w", encoding="utf-8") as f:
    f.write("salom dunyo salom")

with open("soz.txt", "r", encoding="utf-8") as f:
    matn = f.read()

print(matn.count("salom"))
print(len(matn))
''', title="Amaliy: matnni o'qib tahlil qilish", body="`with` blokidan chiqqach, `matn` o'zgaruvchisi baribir mavjud: `2` va `17`. Fayl esa allaqachon yopilgan."),
        exercise('l68_inline_fix'),
        callout('tip', r"""
Ikkita fayl bilan bir vaqtda ishlash: `with open("a.txt") as f1, open("b.txt", "w") as f2:` — ikkalasi ham avtomatik yopiladi.
""", title="Maslahat"),
        recap(["`with open(...) as f:` — avtomatik yopadi", "xato bo'lsa ham fayl yopiladi", "fayl bilan ishlar blok ichida"], "murakkab ma'lumotni (ro'yxat, lug'at) faylga qanday qulay yozamiz?"),
    ],
    [
        fix_task('l68_inline_fix', "with ga o'tkazing", "Kodni `with` ishlatadigan qilib qayta yozing (`close()` siz). Natija: `Salom`", section='inline', points=2, starter_code='f = open("a.txt", "w", encoding="utf-8")\nf.write("Salom")\nf.close()\nf = open("a.txt", "r", encoding="utf-8")\nprint(f.read())\nf.close()\n', tests=[T('output_equals', "Salom", "Natija: Salom"), T('code_contains', 'with open', "`with open` ishlatilgan"), T('code_not_contains', '.close()', "`close()` yozilmagan")], hint="`with open(...) as f:` va chekinish.", full_solution='with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("Salom")\nwith open("a.txt", "r", encoding="utf-8") as f:\n    print(f.read())\n', explanation="`with` faylni o'zi yopadi."),
        single('l68_quiz_1', "with afzalligi", "`with` ning asosiy afzalligi?", options=[opt("Faylni avtomatik yopadi (xato bo'lsa ham)", True), opt("Faylni tezroq o'qiydi", False), opt("Fayl nomini o'zgartiradi", False)], hint="Eshik.", explanation="Avtomatik yopish."),
        predict('l68_quiz_2', "with natijasi", "Dastur nima chiqaradi?", code='with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("12")\nwith open("a.txt", encoding="utf-8") as f:\n    n = int(f.read())\nprint(n + 1)\n', answer="13", hint="Fayldan o'qilgan matn songa aylantirildi.", explanation="`12 + 1`."),
        single('l68_quiz_3', "Chekinish", "Fayl bilan ishlar `with` ning qayerida yoziladi?", options=[opt("Chekinishli blok ichida", True), opt("Blokdan keyin", False), opt("Blokdan oldin", False)], hint="Blok.", explanation="Blok tugagach fayl yopiladi."),
        code_task('l68_assignment', "Kundalik yozuvi", r"""
Foydalanuvchi bitta **yozuv matnini** kiritadi. Dastur `with` yordamida uni `kundalik.txt` ga **yozsin**, keyin xuddi shu faylni `with` bilan o'qib, `Yozuv: <matn>` deb chiqarsin. `Bugun yaxshi kun` → `Yozuv: Bugun yaxshi kun`.
""", starter_code='', points=10, tests=[T('output_equals', "Yozuv: Bugun yaxshi kun", "Bugun yaxshi kun", stdin="Bugun yaxshi kun\n"), T('output_equals', "Yozuv: Salom!", "Salom!", stdin="Salom!\n", hidden=True), T('code_contains', 'with open', "`with open` ishlatilgan"), T('code_not_contains', '.close()', "`close()` yozilmagan")], hint="Ikkita `with` bloki.", partial_solution='matn = input()\nwith open("kundalik.txt", "w", encoding="utf-8") as f:\n    f.write(matn)\n# with bilan o\'qing va chiqaring\n', full_solution='matn = input()\nwith open("kundalik.txt", "w", encoding="utf-8") as f:\n    f.write(matn)\nwith open("kundalik.txt", "r", encoding="utf-8") as f:\n    print("Yozuv:", f.read())\n', explanation="`close()` kerak emas."),
        single('l68_practice_easy', "Easy: as", "`with open(\"a.txt\") as f:` dagi `f` nima?", section='practice', difficulty='easy', options=[opt("Fayl obyekti", True), opt("Fayl nomi", False), opt("Fayl mazmuni", False)], hint="Fayl bilan ishlash uchun tutqich.", explanation="`f` — ochilgan fayl obyekti."),
        code_task('l68_practice_medium', "Medium: qo'shib borish", r"""
Dastur `with ... "a"` bilan `hisob.txt` ga uch marta qator qo'shsin: `1`, `2`, `3` (har biri alohida qatorda; avval fayl bo'sh), so'ng uni o'qib, qatorlarni vergul bilan ajratib bir qatorda chiqarsin: `1,2,3`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "1,2,3", "Natija"), T('code_contains', '"a"', "`\"a\"` rejimi ishlatilgan")], hint="`for i in range(1, 4):` ichida `with open(..., \"a\")`; keyin `read().split()` — qatorlarni ro'yxatga ajratadi.", full_solution='for i in range(1, 4):\n    with open("hisob.txt", "a", encoding="utf-8") as f:\n        f.write(str(i) + "\\n")\nwith open("hisob.txt", "r", encoding="utf-8") as f:\n    qismlar = f.read().split()\nprint(",".join(qismlar))\n', explanation="`split()` — bo'sh joy/yangi qator bo'yicha ajratadi; `\",\".join(...)` ularni vergul bilan ulaydi."),
        code_task('l68_practice_hard', "Hard: fayldagi so'zlar", r"""
Foydalanuvchi gap kiritadi. Dastur uni `gap.txt` ga yozsin, o'qib, so'zlar sonini (`split()` bilan) va **eng uzun so'zni** chiqarsin. `men python o'rganaman` → `3` va `o'rganaman`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "3\no'rganaman", "men python o'rganaman", stdin="men python o'rganaman\n"), T('output_equals', "1\nsalom", "salom", stdin="salom\n"), T('output_equals', "4\nmening", "bu mening yangi maktab", stdin="bu mening yangi maktab\n", hidden=True)], hint="`soz = matn.split()`; eng uzunini sikl bilan toping.", full_solution='gap = input()\nwith open("gap.txt", "w", encoding="utf-8") as f:\n    f.write(gap)\nwith open("gap.txt", "r", encoding="utf-8") as f:\n    sozlar = f.read().split()\neng = sozlar[0]\nfor s in sozlar:\n    if len(s) > len(eng):\n        eng = s\nprint(len(sozlar))\nprint(eng)\n', explanation="`with` + `split()` + eng uzunini topish."),
    ])

# ==============================================================================
# 69-DARS
# ==============================================================================
LESSON_69 = L(69, "JSON bilan ishlash: json.load(), json.dump(), json.loads(), json.dumps()", 14,
    "JSON formatini va nima uchun kerakligini bilish; json.dumps/loads (matn bilan) va json.dump/load (fayl bilan) funksiyalarini ishlatish.",
    ["JSON", "json moduli", "dumps() / loads()", "dump() / load()", "ensure_ascii=False", "indent"],
    [
        text(NOTE_SANDBOX + r"""
List va dictionary'larni oddiy matn faylga yozish noqulay: qaytib o'qiganda ular yana oddiy matn bo'lib qoladi. **JSON** — dasturlar orasida ma'lumot almashishning universal formati: dictionary va listga juda o'xshash, lekin **matn** ko'rinishida. Veb-saytlar, ilovalar, o'yinlar — hammasi JSON ishlatadi.
""", title="Murakkab ma'lumotni saqlash"),
        text(r"""
JSON bilan ishlash uchun `json` **modulini** chaqiramiz (modullarni keyingi modulda batafsil o'rganamiz): `import json`.

| Funksiya | Nima qiladi |
|---|---|
| `json.dumps(obyekt)` | Python obyektini **JSON matniga** aylantiradi |
| `json.loads(matn)` | JSON matnini **Python obyektiga** aylantiradi |
| `json.dump(obyekt, fayl)` | obyektni **faylga** yozadi |
| `json.load(fayl)` | fayldan o'qib, **Python obyekti** qaytaradi |

```python
import json

talaba = {"ism": "Ali", "yosh": 17, "ballar": [5, 4]}

matn = json.dumps(talaba, ensure_ascii=False)
print(matn)                      # {"ism": "Ali", "yosh": 17, "ballar": [5, 4]}
asl = json.loads(matn)
print(asl["ism"])                # Ali

with open("t.json", "w", encoding="utf-8") as f:
    json.dump(talaba, f, ensure_ascii=False, indent=2)
with open("t.json", "r", encoding="utf-8") as f:
    yangi = json.load(f)
```

- `ensure_ascii=False` — o'zbekcha harflar `\u...` ko'rinishida emas, o'qiladigan holda yozilsin.
- `indent=2` — chiroyli (ko'p qatorli) yozuv.
- JSON'da kalitlar doim matn; `True` → `true`, `None` → `null` (Python tuple — JSON'da list bo'ladi).
- `s` harfi — *string* (matn): `dumps`/`loads` — matn bilan; `dump`/`load` — fayl bilan.
""", title="json moduli"),
        callout('analogy', r"""
JSON — **xalqaro tilda yozilgan xat**: istalgan dastur uni o'qiy oladi. `dumps` — «xatga yozish», `loads` — «xatni o'qib tushunish».
""", title="Hayotiy o'xshatish"),
        example(r'''
import json

talaba = {"ism": "Ali", "yosh": 17, "ballar": [5, 4]}
matn = json.dumps(talaba)
print(matn)
print(type(matn))
asl = json.loads(matn)
print(asl["ballar"][0], type(asl))
''', title="dumps va loads", body="`{\"ism\": \"Ali\", \"yosh\": 17, \"ballar\": [5, 4]}`, `<class 'str'>`, keyin `5 <class 'dict'>`. Obyekt matnga, matn yana obyektga aylandi."),
        example(r'''
import json

kundalik = [{"sana": "2026-01-01", "matn": "Yangi yil"}, {"sana": "2026-01-02", "matn": "Dam olish"}]
with open("kundalik.json", "w", encoding="utf-8") as f:
    json.dump(kundalik, f, ensure_ascii=False, indent=2)

with open("kundalik.json", "r", encoding="utf-8") as f:
    yuklangan = json.load(f)
print(len(yuklangan), yuklangan[1]["matn"])
yuklangan.append({"sana": "2026-01-03", "matn": "Python"})
print(len(yuklangan))
''', title="Amaliy: kundalikni JSON faylga saqlash", body="Dictionary'lar listi faylga yozildi va qayta o'qildi: `2 Dam olish`, keyin yangi yozuv qo'shilgach `3`. Aynan shu yo'l bilan loyihada kundalik saqlanadi."),
        exercise('l69_inline_pred'),
        callout('warning', r"""
`json.load(f)` — fayl **bo'sh** yoki noto'g'ri JSON bo'lsa `json.JSONDecodeError` (u ham `ValueError` ning bir turi) beradi. Fayl bo'lmasa — `FileNotFoundError`. Ikkalasini `try/except` bilan ushlang.
""", title="Diqqat"),
        recap(["`dumps/loads` — matn bilan, `dump/load` — fayl bilan", "`ensure_ascii=False`, `indent=2`", "list/dict ↔ JSON"], "bu modulda `import` ishlatdik. Boshqa tayyor modullar ham bormi? O'z modulimizni yaratsa bo'ladimi?"),
    ],
    [
        predict('l69_inline_pred', "dumps", "Dastur nima chiqaradi?", section='inline', code='import json\nprint(json.dumps([1, "a", True, None]))\n', answer='[1, "a", true, null]', points=2, hint="JSON'da `true` va `null` kichik harfda.", explanation="`True` → `true`, `None` → `null`."),
        predict('l69_quiz_1', "loads", "Dastur nima chiqaradi?", code='import json\nd = json.loads(\'{"x": 5, "y": [1, 2]}\')\nprint(d["x"] + len(d["y"]))\n', answer="7", hint="`d` — dictionary.", explanation="`5 + 2`."),
        single('l69_quiz_2', "dump yoki dumps", "Obyektni **faylga** yozish uchun qaysi funksiya?", options=[opt("`json.dump()`", True), opt("`json.dumps()`", False), opt("`json.loads()`", False)], hint="`s` siz — fayl bilan.", explanation="`json.dump(obyekt, fayl)`."),
        predict('l69_quiz_3', "Fayl orqali", "Dastur nima chiqaradi?", code='import json\nwith open("a.json", "w", encoding="utf-8") as f:\n    json.dump({"a": [1, 2, 3]}, f)\nwith open("a.json", encoding="utf-8") as f:\n    d = json.load(f)\nprint(sum(d["a"]))\n', answer="6", hint="Fayldan list o'qildi.", explanation="`1 + 2 + 3`."),
        code_task('l69_assignment', "Talaba ma'lumotlarini saqlash", r"""
Foydalanuvchi **ism** va **yosh**ni kiritadi. Dastur `{"ism": ..., "yosh": ...}` dictionary yarating, uni `talaba.json` ga **JSON** sifatida yozsin (`json.dump`, `ensure_ascii=False`), keyin fayldan `json.load` bilan o'qib, `<ism> (<yosh>)` shaklida chiqarsin. `Aziza`, `17` → `Aziza (17)`.
""", starter_code='import json\n', points=10, tests=[T('output_equals', "Aziza (17)", "Aziza/17", stdin="Aziza\n17\n"), T('output_equals', "O'ktam (20)", "O'ktam/20", stdin="O'ktam\n20\n", hidden=True), T('code_contains', 'json.dump', "`json.dump` ishlatilgan"), T('code_contains', 'json.load', "`json.load` ishlatilgan")],
            hint="`yosh` ni `int` qiling, `json.dump(d, f, ensure_ascii=False)`.", partial_solution='import json\n\nism = input()\nyosh = int(input())\nd = {"ism": ism, "yosh": yosh}\nwith open("talaba.json", "w", encoding="utf-8") as f:\n    json.dump(d, f, ensure_ascii=False)\n# faylni o\'qing va chiqaring\n', full_solution='import json\n\nism = input()\nyosh = int(input())\nd = {"ism": ism, "yosh": yosh}\nwith open("talaba.json", "w", encoding="utf-8") as f:\n    json.dump(d, f, ensure_ascii=False)\nwith open("talaba.json", "r", encoding="utf-8") as f:\n    y = json.load(f)\nprint(f"{y[\'ism\']} ({y[\'yosh\']})")\n', explanation="Dictionary faylga JSON bo'lib yozildi va qayta tiklandi."),
        single('l69_practice_easy', "Easy: JSON", "JSON nima?", section='practice', difficulty='easy', options=[opt("Ma'lumot almashish uchun universal matn formati", True), opt("Python funksiyasi", False), opt("Fayl turi emas, xato turi", False)], hint="Xalqaro til.", explanation="Matn ko'rinishidagi ma'lumot formati."),
        code_task('l69_practice_medium', "Medium: dictionary → matn", r"""
`d = {"nom": "Non", "narx": 4500}` ni `json.dumps` bilan JSON matniga aylantirib chiqaring, so'ng `json.loads` bilan qaytarib, `narx` ni 500 ga oshirib chiqaring: `{"nom": "Non", "narx": 4500}` va `5000`.
""", section='practice', difficulty='medium', points=5, starter_code='import json\n\nd = {"nom": "Non", "narx": 4500}\n', tests=[T('output_equals', '{"nom": "Non", "narx": 4500}\n5000', "Natija"), T('code_contains', 'dumps', "`dumps` ishlatilgan"), T('code_contains', 'loads', "`loads` ishlatilgan")], hint="`matn = json.dumps(d)`, `yangi = json.loads(matn)`.", full_solution='import json\n\nd = {"nom": "Non", "narx": 4500}\nmatn = json.dumps(d)\nprint(matn)\nyangi = json.loads(matn)\nprint(yangi["narx"] + 500)\n', explanation="Aylantirish ikki tomonlama."),
        code_task('l69_practice_hard', "Hard: xavfsiz yuklash", r"""
`yukla()` funksiyasi `baza.json` ni o'qib, ro'yxatni qaytarsin; fayl yo'q bo'lsa (`FileNotFoundError`) — bo'sh list `[]` qaytarsin. `saqla(royxat)` — ro'yxatni `baza.json` ga yozsin. Tekshiruv: `yukla()` (fayl yo'q) → `[]`; `saqla([1, 2])` dan keyin `yukla()` → `[1, 2]`.
""", section='practice', difficulty='hard', points=5, starter_code='import json\n', tests=[T('output_equals', "[]\n[1, 2]\n[1, 2, 3]", "Natija", harness='print(yukla())\nsaqla([1, 2])\nprint(yukla())\nr = yukla()\nr.append(3)\nsaqla(r)\nprint(yukla())')], hint="`try: with open(...)...  except FileNotFoundError: return []`.", partial_solution='import json\n\ndef yukla():\n    try:\n        with open("baza.json", "r", encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return []\n\n# saqla() ni yozing\n', full_solution='import json\n\ndef yukla():\n    try:\n        with open("baza.json", "r", encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return []\n\ndef saqla(royxat):\n    with open("baza.json", "w", encoding="utf-8") as f:\n        json.dump(royxat, f, ensure_ascii=False)\n', explanation="Yuklash/saqlash funksiyalari — kundalik loyihasining asosi."),
    ])

LESSONS = [LESSON_66, LESSON_67, LESSON_68, LESSON_69]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("10-modul yakuniy nazorati: Fayllar va JSON", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **shaxsiy elektron kundalik**.
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).

> Platformada fayllar vaqtincha ishchi papkada yaratiladi va ishga tushish tugagach o'chiriladi — shuning uchun loyihani bir ishga tushish ichida sinaysiz.
""", [
    single('m10_a_t1', "Rejim", "Faylga mavjud ma'lumotni saqlab, oxiriga qo'shish uchun qaysi rejim?", section='assessment', points=2, options=[opt("`\"a\"`", True), opt("`\"w\"`", False), opt("`\"r\"`", False)], explanation="`\"a\"` — append."),
    single('m10_a_t2', "with", "`with open(...)` nimasi bilan qulay?", section='assessment', points=2, options=[opt("Faylni avtomatik yopadi", True), opt("Tezroq o'qiydi", False), opt("Xotirani oshiradi", False)], explanation="Avtomatik yopish."),
    single('m10_a_t3', "read turi", "Fayldan o'qilgan qiymat qanday turda bo'ladi?", section='assessment', points=2, options=[opt("`str` (matn)", True), opt("`int`", False), opt("`list`", False)], explanation="Matn; songa aylantirish kerak."),
    single('m10_a_t4', "JSON", "JSON matnini Python obyektiga aylantiruvchi funksiya?", section='assessment', points=2, options=[opt("`json.loads()`", True), opt("`json.dumps()`", False), opt("`json.write()`", False)], explanation="`loads` — matndan obyekt."),
    multiple('m10_a_t5', "FileNotFoundError", "Qaysi holatlarda `open(\"x.txt\", \"r\")` `FileNotFoundError` beradi?", section='assessment', points=2, options=[opt("`x.txt` mavjud bo'lmasa", True), opt("Rejim `\"w\"` bo'lsa va fayl yo'q bo'lsa", False), opt("Rejim `\"a\"` bo'lsa va fayl yo'q bo'lsa", False), opt("Papka mavjud bo'lmasa", True)], explanation="`\"w\"` va `\"a\"` faylni yaratadi."),
    predict('m10_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("1\\n2\\n3\\n")\nwith open("a.txt", encoding="utf-8") as f:\n    j = 0\n    for q in f:\n        j = j + int(q)\nprint(j)\n', answer="6", explanation="`1 + 2 + 3`; `int(\"1\\n\")` ishlaydi."),
    predict('m10_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='with open("a.txt", "w") as f:\n    f.write("a")\nwith open("a.txt", "w") as f:\n    f.write("b")\nwith open("a.txt") as f:\n    print(f.read())\n', answer="b", explanation="`\"w\"` har safar tozalaydi."),
    predict('m10_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='import json\nd = json.loads(json.dumps({"a": (1, 2)}))\nprint(d)\n', answer="{'a': [1, 2]}", explanation="JSON'da tuple list bo'ladi."),
    fix_task('m10_a_f1', "Xatoni tuzating (1)", "Dastur faylga `Salom` yozib, o'qishi kerak, lekin faylni o'qishda xato (`io.UnsupportedOperation`) beryapti.", section='assessment', points=4, starter_code='with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("Salom")\n    print(f.read())\n', tests=[T('output_equals', "Salom", "Natija: Salom")], hint="Yozish rejimida o'qib bo'lmaydi: o'qish uchun faylni alohida oching.", full_solution='with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("Salom")\nwith open("a.txt", "r", encoding="utf-8") as f:\n    print(f.read())\n', explanation="`\"w\"` rejimida o'qib bo'lmaydi."),
    fix_task('m10_a_f2', "Xatoni tuzating (2)", "Dastur dictionary'ni JSON faylga yozib, qayta o'qishi kerak (`5`), lekin `TypeError` beryapti.", section='assessment', points=4, starter_code='import json\nwith open("a.json", "w", encoding="utf-8") as f:\n    json.dump({"x": 5})\nwith open("a.json", encoding="utf-8") as f:\n    print(json.load(f)["x"])\n', tests=[T('output_equals', "5", "Natija: 5")], hint="`json.dump` ga ikkinchi argument — fayl.", full_solution='import json\nwith open("a.json", "w", encoding="utf-8") as f:\n    json.dump({"x": 5}, f)\nwith open("a.json", encoding="utf-8") as f:\n    print(json.load(f)["x"])\n', explanation="`json.dump(obyekt, fayl)`."),
    code_task('m10_a_project', "Mini-loyiha: Shaxsiy elektron kundalik", r"""
**`kundalik.json`** faylida yozuvlar **list**i saqlanadi; har yozuv — `{"sana": ..., "matn": ...}` dictionary. Dastur **menyu** orqali boshqariladi (`0` kiritilguncha):

| Buyruq | Amal | Chiqadigan xabar |
|---|---|---|
| `1` | keyingi qatorlarda **sana** va **matn** o'qib, yozuv qo'shadi va **darhol faylga saqlaydi** | `Saqlandi` |
| `2` | barcha yozuvlarni `1. [sana] matn` shaklida chiqaradi | yozuv yo'q bo'lsa `Kundalik bo'sh` |
| `3` | keyingi qatorda **so'z** o'qib, matnida shu so'z bor yozuvlarni (kichik/katta harfga e'tiborsiz) chiqaradi | `[sana] matn` qatorlari yoki `Topilmadi` |
| `4` | fayldan qayta o'qiydi | `Fayldan o'qildi: <N> ta yozuv` |
| `0` | tugatadi | `Xayr! Yozuvlar: <N>` |

Talablar:
- Dastur boshida `kundalik.json` ni **yuklang** (`yukla()` funksiyasi); fayl yo'q bo'lsa — bo'sh list.
- `saqla()` funksiyasi: `with` va `json.dump(..., ensure_ascii=False, indent=2)`.
- Fayl bilan ishlashda xatolarni (`FileNotFoundError`) `try/except` bilan ushlang.

Misol: `1`,`2026-01-01`,`Yangi yil`, `1`,`2026-01-02`,`Python o'rgandim`, `2`, `3`,`python`, `0` →
```
Saqlandi
Saqlandi
1. [2026-01-01] Yangi yil
2. [2026-01-02] Python o'rgandim
[2026-01-02] Python o'rgandim
Xayr! Yozuvlar: 2
```
""", section='project', points=25, difficulty='hard', unlock=3, starter_code='import json\n\n# Shaxsiy elektron kundalik\n',
        expected_output_example="Saqlandi\nSaqlandi\n1. [2026-01-01] Yangi yil\n2. [2026-01-02] Python o'rgandim\n[2026-01-02] Python o'rgandim\nXayr! Yozuvlar: 2",
        tests=[T('output_equals', "Saqlandi\nSaqlandi\n1. [2026-01-01] Yangi yil\n2. [2026-01-02] Python o'rgandim\n[2026-01-02] Python o'rgandim\nXayr! Yozuvlar: 2", "Misol ssenariy", stdin="1\n2026-01-01\nYangi yil\n1\n2026-01-02\nPython o'rgandim\n2\n3\npython\n0\n"),
               T('output_equals', "Kundalik bo'sh\nTopilmadi\nXayr! Yozuvlar: 0", "Bo'sh kundalik", stdin="2\n3\nsalom\n0\n"),
               T('output_equals', "Saqlandi\nFayldan o'qildi: 1 ta yozuv\nXayr! Yozuvlar: 1", "Qayta o'qish", stdin="1\n2026-02-01\nBugun\n4\n0\n"),
               T('output_equals', "[{'sana': '2026-03-01', 'matn': \"O'zbekiston\"}]", "Fayl mazmuni to'g'ri saqlangan (JSON)", stdin="1\n2026-03-01\nO'zbekiston\n0\n", harness='import json\nwith open("kundalik.json", encoding="utf-8") as f:\n    print(json.load(f))', hidden=True),
               T('code_contains', 'json.dump', "`json.dump` ishlatilgan"), T('code_contains', 'with open', "`with open` ishlatilgan"), T('code_contains', 'FileNotFoundError', "`FileNotFoundError` ushlangan")],
        hint="1) `yukla()` — `try: with open(...): return json.load(f)`; `except FileNotFoundError: return []`. 2) `saqla(yozuvlar)` — `json.dump(yozuvlar, f, ensure_ascii=False, indent=2)`. 3) `while True:` ichida menyu. 4) Qidirishda `so_z.lower() in yozuv[\"matn\"].lower()`.",
        partial_solution='import json\n\ndef yukla():\n    try:\n        with open("kundalik.json", "r", encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return []\n\ndef saqla(yozuvlar):\n    with open("kundalik.json", "w", encoding="utf-8") as f:\n        json.dump(yozuvlar, f, ensure_ascii=False, indent=2)\n\nyozuvlar = yukla()\nwhile True:\n    buyruq = input()\n    if buyruq == "0":\n        break\n    # 1, 2, 3, 4 buyruqlarini yozing\nprint("Xayr! Yozuvlar:", len(yozuvlar))\n',
        full_solution='import json\n\ndef yukla():\n    try:\n        with open("kundalik.json", "r", encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return []\n\ndef saqla(yozuvlar):\n    with open("kundalik.json", "w", encoding="utf-8") as f:\n        json.dump(yozuvlar, f, ensure_ascii=False, indent=2)\n\nyozuvlar = yukla()\nwhile True:\n    buyruq = input()\n    if buyruq == "0":\n        break\n    elif buyruq == "1":\n        sana = input()\n        matn = input()\n        yozuvlar.append({"sana": sana, "matn": matn})\n        saqla(yozuvlar)\n        print("Saqlandi")\n    elif buyruq == "2":\n        if len(yozuvlar) == 0:\n            print("Kundalik bo\'sh")\n        else:\n            for n, y in enumerate(yozuvlar, start=1):\n                print(f"{n}. [{y[\'sana\']}] {y[\'matn\']}")\n    elif buyruq == "3":\n        soz = input().lower()\n        topildi = False\n        for y in yozuvlar:\n            if soz in y["matn"].lower():\n                print(f"[{y[\'sana\']}] {y[\'matn\']}")\n                topildi = True\n        if not topildi:\n            print("Topilmadi")\n    elif buyruq == "4":\n        yozuvlar = yukla()\n        print(f"Fayldan o\'qildi: {len(yozuvlar)} ta yozuv")\nprint("Xayr! Yozuvlar:", len(yozuvlar))\n',
        explanation="Loyiha fayl yozish/o'qish, with, JSON, try/except, funksiyalar, list va dictionary — hammasini birlashtiradi."),
])
