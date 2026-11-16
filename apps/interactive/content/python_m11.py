"""Python — 0 dan boshlash · 11-modul: Modullar va o'z kompyuteringizda ishlash (70–74-darslar) + yakuniy takrorlash."""
from .builders import L, T, callout, code_task, example, exercise, fill, fix_task, module_assessment, multiple, opt, predict, recap, single, text

MODULE = {
    'order': 11,
    'title': "Modullar va o'z kompyuteringizda ishlash",
    'description': "Tayyor modullar (math, random, datetime), o'z modulingizni yaratish, Python va VS Code ni kompyuterga o'rnatish va mustaqil dastur yaratish.",
}

# ==============================================================================
# 70-DARS
# ==============================================================================
LESSON_70 = L(70, "Python modullari nima va import", 12,
    "Modul nima ekanini, import, from ... import va import ... as shakllarini bilish hamda modul ichidagi narsalarga murojaat qilish.",
    ["Modul", "import", "from ... import", "import ... as", "Nuqta bilan murojaat"],
    [
        text(r"""
Har gal yangi dastur yozganda **g'ildirakni qaytadan ixtiro qilish** shartmi? Kvadrat ildiz, tasodifiy son, sana bilan ishlash — bularni minglab dasturchilar allaqachon yozgan. Python ularni **modullar**ga joylagan: kerakli modulni **chaqirsangiz** (`import`), tayyor vositalar sizniki.
""", title="Tayyor vositalar to'plami"),
        text(r"""
**Modul** — tayyor funksiyalar, o'zgaruvchilar va boshqa vositalar saqlangan `.py` fayl. Python bilan birga yuzlab standart modullar keladi.

```python
import math                      # butun modulni chaqirish
print(math.sqrt(25))             # 5.0   — modul.nom

from math import sqrt, pi        # faqat kerakli nomlarni
print(sqrt(16), pi)              # 4.0 3.141592653589793

import math as m                 # qisqa nom berish
print(m.floor(3.9))              # 3
```

- `import modul` — nomga **modul nomi bilan** murojaat: `modul.nom`.
- `from modul import nom` — nomni **to'g'ridan-to'g'ri** ishlatish (modul nomisiz).
- `import modul as qisqa` — qisqa taxallus.
- `import` odatda faylning **boshida** yoziladi.
- Mavjud bo'lmagan modul — `ModuleNotFoundError`.
""", title="import shakllari"),
        callout('analogy', r"""
Modul — **asboblar qutisi**: `math` — hisoblash asboblari, `random` — qur'a asboblari, `datetime` — taqvim asboblari. `import` — qutini ish stoliga qo'yish.
""", title="Hayotiy o'xshatish"),
        example(r'''
import math

print(math.sqrt(49))
print(math.pi)
print(math.ceil(4.1), math.floor(4.9))
''', title="math modulini chaqirish", body="`7.0`, `3.141592653589793`, `5 4`. `ceil` — yuqoriga, `floor` — pastga yaxlitlaydi."),
        example(r'''
from math import sqrt
import math as m

def gipotenuza(a, b):
    return sqrt(a * a + b * b)

print(gipotenuza(3, 4))
print(m.factorial(5))
''', title="Amaliy: from va as", body="Pifagor teoremasi: `5.0`. `m.factorial(5)` — `120`. Ikki xil import shakli birga ishlatildi."),
        exercise('l70_inline_blank'),
        callout('tip', r"""
Modul ichida nimalar borligini bilish uchun `dir(math)` yoki Python hujjatlari (docs.python.org). Odat: standart kutubxona hujjatini ochib, kerakli funksiyani qidirish.
""", title="Dasturchi odati"),
        recap(["`import modul` → `modul.nom`", "`from modul import nom`", "`import modul as qisqa`"], "standart modullar ichida eng foydalilari qaysilar? Matematika, tasodifiy sonlar va sana uchun nima bor?"),
    ],
    [
        fill('l70_inline_blank', "Bo'sh joy", "`math` modulidan kvadrat ildiz oling: `25` → `5.0`", '___ math\nprint(math.sqrt(25))\n', ['import'], section='inline', points=2, tests=[T('output_equals', "5.0", "Natija: 5.0")], hint="Modulni chaqirish kalit so'zi.", explanation="`import math`."),
        predict('l70_quiz_1', "from import", "Dastur nima chiqaradi?", code='from math import floor, ceil\nprint(floor(2.7) + ceil(2.1))\n', answer="5", hint="2 + 3.", explanation="`floor(2.7)` = 2, `ceil(2.1)` = 3."),
        single('l70_quiz_2', "Murojaat", "`import math` dan keyin kvadrat ildiz qanday olinadi?", options=[opt("`math.sqrt(9)`", True), opt("`sqrt(9)`", False, "Bu faqat `from math import sqrt` dan keyin ishlaydi."), opt("`math[sqrt](9)`", False)], hint="Nuqta bilan.", explanation="`modul.nom`."),
        single('l70_quiz_3', "Xato", "Mavjud bo'lmagan modulni chaqirsak qaysi xato chiqadi?", options=[opt("`ModuleNotFoundError`", True), opt("`NameError`", False), opt("`ValueError`", False)], hint="Nomida «module».", explanation="`ModuleNotFoundError`."),
        code_task('l70_assignment', "Doira yuzi", r"""
`math` modulidan `pi` ni ishlatib, foydalanuvchi kiritgan radiusli (kasr bo'lishi mumkin) doira **yuzini** 2 xonali kasr bilan chiqaring: `pi * r ** 2`. `2` → `12.57`; `1` → `3.14`.
""", starter_code='', points=10, tests=[T('output_equals', "12.57", "r = 2", stdin="2\n"), T('output_equals', "3.14", "r = 1", stdin="1\n"), T('output_equals', "78.54", "r = 5", stdin="5\n", hidden=True), T('code_contains', 'import', "`import` ishlatilgan"), T('code_contains', 'pi', "`pi` ishlatilgan")],
            hint="`import math` va `math.pi`.", partial_solution='import math\n\nr = float(input())\n# yuzni hisoblab chiqaring\n', full_solution='import math\n\nr = float(input())\nprint(f"{math.pi * r ** 2:.2f}")\n', explanation="Tayyor `pi` dan foydalandik."),
        single('l70_practice_easy', "Easy: modul nima?", "Modul nima?", section='practice', difficulty='easy', options=[opt("Tayyor vositalar saqlangan `.py` fayl", True), opt("Xato turi", False), opt("O'zgaruvchi turi", False)], hint="Asboblar qutisi.", explanation="Funksiya va o'zgaruvchilar to'plami."),
        code_task('l70_practice_medium', "Medium: gipotenuza", r"""
Foydalanuvchi ikki katetni (kasr) kiritadi. Gipotenuzani `from math import sqrt` bilan hisoblab, 2 xonali chiqaring. `3`, `4` → `5.00`; `1`, `1` → `1.41`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "5.00", "3, 4", stdin="3\n4\n"), T('output_equals', "1.41", "1, 1", stdin="1\n1\n"), T('code_contains', 'from math import', "`from math import` ishlatilgan")], hint="`sqrt(a * a + b * b)`.", full_solution='from math import sqrt\n\na = float(input())\nb = float(input())\nprint(f"{sqrt(a * a + b * b):.2f}")\n', explanation="Faqat kerakli funksiya chaqirildi."),
        code_task('l70_practice_hard', "Hard: kombinatsiyalar", r"""
`math.factorial` bilan n ta elementdan k tasini tanlash usullari sonini hisoblang: `C(n, k) = n! // (k! * (n - k)!)`. Foydalanuvchi `n` va `k` kiritadi. `5`, `2` → `10`; `10`, `3` → `120`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "10", "5, 2", stdin="5\n2\n"), T('output_equals', "120", "10, 3", stdin="10\n3\n"), T('output_equals', "1", "4, 4", stdin="4\n4\n", hidden=True), T('code_contains', 'factorial', "`factorial` ishlatilgan")], hint="`import math as m`, `m.factorial(n)`.", full_solution='import math as m\n\nn = int(input())\nk = int(input())\nprint(m.factorial(n) // (m.factorial(k) * m.factorial(n - k)))\n', explanation="`factorial` tayyor funksiyasi ishni osonlashtirdi."),
    ])

# ==============================================================================
# 71-DARS
# ==============================================================================
LESSON_71 = L(71, "Standart kutubxonalar: math, random, datetime", 14,
    "math (ildiz, daraja, yaxlitlash), random (tasodifiy son va tanlash) va datetime (sana, farq, formatlash) modullarining asosiy vositalarini ishlatish.",
    ["math", "random", "datetime", "date", "timedelta", "strftime"],
    [
        text(r"""
Uchta eng ko'p ishlatiladigan standart modul: **`math`** (matematika), **`random`** (tasodifiylik), **`datetime`** (sana va vaqt). Ularning har biri bilan bir necha tayyor funksiyani o'rganamiz.
""", title="Uchta eng foydali modul"),
        text(r"""
**math**

| | |
|---|---|
| `math.sqrt(x)` | kvadrat ildiz |
| `math.pow(a, b)` / `a ** b` | daraja |
| `math.floor(x)`, `math.ceil(x)` | pastga / yuqoriga yaxlitlash |
| `math.pi`, `math.e` | doimiylar |

**random**

| | |
|---|---|
| `random.randint(a, b)` | `a` dan `b` gacha (ikkalasi ham kiradi) tasodifiy butun son |
| `random.choice(royxat)` | ro'yxatdan tasodifiy element |
| `random.shuffle(royxat)` | ro'yxatni aralashtiradi (joyida) |
| `random.seed(n)` | tasodifiylikni «qotiradi» — bir xil ketma-ketlik (sinash uchun) |

**datetime**

```python
from datetime import date, timedelta
d = date(2026, 3, 15)
print(d.year, d.month, d.day)        # 2026 3 15
print(d.strftime("%d.%m.%Y"))        # 15.03.2026
print(d + timedelta(days=30))        # 2026-04-14
print((date(2026, 12, 31) - d).days) # 291
print(date.today())                  # bugungi sana
```
""", title="Asosiy vositalar"),
        callout('analogy', r"""
`random` — **qur'a tashlash**, `datetime` — **taqvim**, `math` — **kalkulyator**. Bularning hammasi sizning «ish stolingizda» tayyor.
""", title="Hayotiy o'xshatish"),
        example(r'''
import math
import random

print(math.sqrt(2))
random.seed(7)
son = random.randint(1, 6)
print(1 <= son <= 6)
mevalar = ["olma", "nok", "uzum"]
print(random.choice(mevalar) in mevalar)
''', title="math va random", body="`1.4142135623730951`, `True`, `True`. `random.seed()` — natijani qayta-qayta bir xil qilish; tasodifiy son qiymati har safar boshqa, shuning uchun biz **shart** bilan tekshirdik."),
        example(r'''
from datetime import date, timedelta

tugilgan = date(2008, 5, 20)
bugun = date(2026, 3, 15)
yosh_kun = (bugun - tugilgan).days
print("Yashagan kunlar:", yosh_kun)
print("Yosh:", yosh_kun // 365)
print((bugun + timedelta(days=100)).strftime("%d.%m.%Y"))
''', title="Amaliy: sanalar bilan hisob", body="Ikki sana ayirmasi — `timedelta`; `.days` — kunlar soni. Natija: `Yashagan kunlar: 6504`, `Yosh: 17`, `23.06.2026`."),
        exercise('l71_inline_pred'),
        callout('warning', r"""
`random.randint(1, 6)` — **ikkala chegara kiradi** (`range()` dan farqli!). Tasodifiy natijani `print` qilib «to'g'ri» deb tekshirib bo'lmaydi — shart (`1 <= x <= 6`) bilan tekshiring.
""", title="Diqqat"),
        recap(["`math`: sqrt, floor, ceil, pi", "`random`: randint, choice, shuffle, seed", "`datetime`: date, timedelta, strftime"], "o'z funksiyalaringizni alohida faylga yozib, boshqa dasturdan chaqirsa bo'ladimi?"),
    ],
    [
        predict('l71_inline_pred', "datetime", "Dastur nima chiqaradi?", section='inline', code='from datetime import date\nprint((date(2026, 1, 31) - date(2026, 1, 1)).days)\n', answer="30", points=2, hint="Sanalar ayirmasi.", explanation="1-yanvardan 31-yanvargacha 30 kun."),
        predict('l71_quiz_1', "timedelta", "Dastur nima chiqaradi?", code='from datetime import date, timedelta\nprint(date(2026, 2, 27) + timedelta(days=3))\n', answer="2026-03-02", hint="Fevral 2026 da 28 kun.", explanation="27 + 3 = fevralning 30-i → 2 mart."),
        single('l71_quiz_2', "randint", "`random.randint(1, 3)` qaysi qiymatlarni berishi mumkin?", options=[opt("1, 2 yoki 3", True), opt("Faqat 1 yoki 2", False), opt("0, 1, 2 yoki 3", False)], hint="Ikkala chegara kiradi.", explanation="`randint` chegaralarni qo'shadi."),
        predict('l71_quiz_3', "strftime", "Dastur nima chiqaradi?", code='from datetime import date\nprint(date(2026, 7, 4).strftime("%d/%m/%y"))\n', answer="04/07/26", hint="`%d` — kun, `%m` — oy, `%y` — ikki xonali yil.", explanation="Formatlangan sana."),
        code_task('l71_assignment', "Sanagacha necha kun?", r"""
Foydalanuvchi **ikki sanani** kiritadi: yil, oy, kun (har biri alohida qator, jami 6 ta son: birinchi sana yil/oy/kun, keyin ikkinchi sana yil/oy/kun). Dastur ular orasidagi **kunlar sonini** (ikkinchi − birinchi) chiqarsin. `2026`,`1`,`1`, `2026`,`12`,`31` → `364`.
""", starter_code='', points=10, tests=[T('output_equals', "364", "2026-01-01 → 2026-12-31", stdin="2026\n1\n1\n2026\n12\n31\n"), T('output_equals', "1", "ketma-ket kunlar", stdin="2026\n3\n1\n2026\n3\n2\n"), T('output_equals', "366", "kabisa yili", stdin="2024\n1\n1\n2025\n1\n1\n", hidden=True), T('code_contains', 'datetime', "`datetime` ishlatilgan")],
            hint="`from datetime import date`; `date(yil, oy, kun)`; ayirma — `.days`.", partial_solution='from datetime import date\n\nd1 = date(int(input()), int(input()), int(input()))\n# ikkinchi sanani yarating va farqni chiqaring\n', full_solution='from datetime import date\n\nd1 = date(int(input()), int(input()), int(input()))\nd2 = date(int(input()), int(input()), int(input()))\nprint((d2 - d1).days)\n', explanation="Sanalar ayirmasi `timedelta` beradi."),
        single('l71_practice_easy', "Easy: choice", "`random.choice(royxat)` nima qiladi?", section='practice', difficulty='easy', options=[opt("Ro'yxatdan tasodifiy bitta element tanlaydi", True), opt("Ro'yxatni tartiblaydi", False), opt("Ro'yxatni o'chiradi", False)], hint="Qur'a.", explanation="Tasodifiy element."),
        code_task('l71_practice_medium', "Medium: tasodifiy son shartlari", r"""
`random.seed(1)` dan keyin `random.randint(1, 100)` ni 10 marta chaqiring; hamma sonlar `1..100` oralig'ida ekanini tekshirib `Hammasi oraliqda` yoki `Oraliqdan tashqarida` chiqaring (to'g'ri kod — doimo `Hammasi oraliqda`).
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Hammasi oraliqda", "Natija"), T('code_contains', 'randint', "`randint` ishlatilgan")], hint="`bor = True`; siklda tekshirib, noto'g'ri bo'lsa `False`.", full_solution='import random\n\nrandom.seed(1)\nhamma = True\nfor i in range(10):\n    x = random.randint(1, 100)\n    if x < 1 or x > 100:\n        hamma = False\nif hamma:\n    print("Hammasi oraliqda")\nelse:\n    print("Oraliqdan tashqarida")\n', explanation="Tasodifiy natijani shart bilan tekshirdik."),
        code_task('l71_practice_hard', "Hard: hafta kuni", r"""
Foydalanuvchi sana kiritadi: yil, oy, kun (3 ta son). Hafta kunini o'zbekcha chiqaring: `date(...).weekday()` 0 (dushanba)…6 (yakshanba). `2026`,`3`,`15` → `Yakshanba`; `2026`,`3`,`16` → `Dushanba`.
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "Yakshanba", "2026-03-15", stdin="2026\n3\n15\n"), T('output_equals', "Dushanba", "2026-03-16", stdin="2026\n3\n16\n"), T('output_equals', "Payshanba", "2026-01-01", stdin="2026\n1\n1\n", hidden=True)], hint="Kunlar ro'yxatini tuzing va `weekday()` ni indeks sifatida ishlating.", partial_solution='from datetime import date\n\nkunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]\nd = date(int(input()), int(input()), int(input()))\n# weekday() bo\'yicha kun nomini chiqaring\n', full_solution='from datetime import date\n\nkunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]\nd = date(int(input()), int(input()), int(input()))\nprint(kunlar[d.weekday()])\n', explanation="Modul natijasi (son) ro'yxat indeksi sifatida ishlatildi."),
    ])

# ==============================================================================
# 72-DARS
# ==============================================================================
LESSON_72 = L(72, "O'z modulimizni yaratish va undan foydalanish", 14,
    "O'z modulini (.py fayl) yaratish, uni import qilish va if __name__ == \"__main__\" tekshiruvining ma'nosini tushunish.",
    ["O'z moduli", "Fayl = modul", "Import qilish", "__name__", "if __name__ == \"__main__\""],
    [
        text(r"""
Dasturingiz kattalashganda hamma kodni bitta faylga yozish noqulay. Yaxshi usul: tegishli funksiyalarni **alohida `.py` faylga** (modulga) joylab, kerak bo'lganda **import qilish**. Har qanday `.py` fayl — modul!
""", title="O'z asboblar qutimiz"),
        text(r"""
**Ikkita fayl** yaratamiz (bir papkada):

`hisob.py` — modul:
```python
PI = 3.14

def kvadrat(x):
    return x * x

def doira_yuzi(r):
    return PI * kvadrat(r)

if __name__ == "__main__":
    print("Sinov:", kvadrat(4))
```

`asosiy.py` — undan foydalanadi:
```python
import hisob
from hisob import doira_yuzi

print(hisob.kvadrat(5))     # 25
print(doira_yuzi(2))        # 12.56
```

- Modul nomi — **fayl nomi** (`.py` siz). `hisob.py` → `import hisob`.
- Ikkala fayl **bir papkada** bo'lishi kerak.
- **`if __name__ == "__main__":`** — «bu fayl **to'g'ridan-to'g'ri ishga tushirilgandagina** bajar». Boshqa fayldan import qilinsa, bu blok ishlamaydi — modulning o'z sinov kodi import paytida chiqib ketmaydi.
""", title="Modul yaratish"),
        callout('analogy', r"""
`if __name__ == "__main__"` — **do'kon eshigidagi «Faqat egasi uchun»** yozuvi: egasi (siz, faylni to'g'ridan-to'g'ri ishga tushirganda) kiradi; mijoz (boshqa fayl import qilganda) — kirmaydi.
""", title="Hayotiy o'xshatish"),
        text(r"""
> **Bu platformada:** bitta kod muharriri bor, shuning uchun modul faylini dasturning o'zi **yaratadi** (`open(...).write(...)`), so'ng `sys.path.append(".")` bilan joriy papkani Python'ga ko'rsatib, uni `import` qiladi. Kompyuteringizda esa shunchaki ikki fayl yaratasiz — ikkinchi qadam keyingi darsda.
"""),
        example(r'''
import sys

with open("hisob.py", "w", encoding="utf-8") as f:
    f.write("PI = 3.14\n")
    f.write("def kvadrat(x):\n    return x * x\n")

sys.path.append(".")
import hisob

print(hisob.PI)
print(hisob.kvadrat(6))
''', title="Modul yaratib, import qilish", body="Dastur `hisob.py` faylini yaratdi va uni import qildi: `3.14` va `36`. Kompyuteringizda fayl yaratishni muharrirda qilasiz."),
        example(r'''
import sys

with open("moduli.py", "w", encoding="utf-8") as f:
    f.write("def salom():\n    return 'modul ishladi'\n\n")
    f.write("if __name__ == '__main__':\n    print('to`g`ridan-to`g`ri ishga tushdi')\n")

sys.path.append(".")
import moduli
print(moduli.salom())
print(moduli.__name__)
''', title="Amaliy: __name__ tekshiruvi", body="Import paytida modul ichidagi `if __name__ == \"__main__\"` bloki ishlamadi: faqat `modul ishladi` va `moduli` (modul nomi) chiqdi."),
        exercise('l72_inline_pred'),
        callout('warning', r"""
O'z modulingiz nomini standart modul nomi bilan bir xil qo'ymang (`math.py`, `random.py`) — Python o'zingiznikini import qilib, standartini «yashirib» qo'yadi va g'alati xatolar chiqadi.
""", title="Diqqat"),
        recap(["har bir `.py` fayl — modul", "modul nomi = fayl nomi", "`if __name__ == \"__main__\":` — faqat to'g'ridan-to'g'ri ishga tushirilganda"], "endi o'z kompyuteringizda Python bilan ishlashni boshlaymiz. Buning uchun nimalar o'rnatiladi?"),
    ],
    [
        predict('l72_inline_pred', "__name__", "Dastur nima chiqaradi?", section='inline', code='print(__name__)\n', answer="__main__", points=2, hint="Fayl to'g'ridan-to'g'ri ishga tushirilgan.", explanation="To'g'ridan-to'g'ri ishga tushirilgan faylda `__name__` — `\"__main__\"`."),
        single('l72_quiz_1', "Modul nomi", "`kalkulyator.py` faylini qanday import qilamiz?", options=[opt("`import kalkulyator`", True), opt("`import kalkulyator.py`", False), opt("`import \"kalkulyator\"`", False)], hint="`.py` siz.", explanation="Modul nomi — fayl nomi, kengaytmasiz."),
        single('l72_quiz_2', "__main__", "`if __name__ == \"__main__\":` bloki qachon ishlaydi?", options=[opt("Fayl to'g'ridan-to'g'ri ishga tushirilganda", True), opt("Fayl import qilinganda", False), opt("Hech qachon", False)], hint="«Faqat egasi uchun».", explanation="Faqat asosiy fayl sifatida ishga tushirilganda."),
        single('l72_quiz_3', "Bir papka", "Modulni import qilish uchun u qayerda bo'lishi kerak?", options=[opt("Asosiy fayl bilan bir papkada", True), opt("Istalgan joyda", False), opt("Faqat C: diskda", False)], hint="Python avval joriy papkani qidiradi.", explanation="Odatda bir papkada."),
        code_task('l72_assignment', "O'z modulingizni yarating", r"""
Dastur `yordamchi.py` faylini yaratsin: ichida `ikki_baravar(x)` funksiyasi (`x * 2` ni qaytaradi). So'ng `sys.path.append(".")` va `import yordamchi` qiling, foydalanuvchi kiritgan butun sonning ikki baravarini `yordamchi.ikki_baravar(...)` bilan chiqaring. `7` → `14`.
""", starter_code='import sys\n\n', points=10, tests=[T('output_equals', "14", "7", stdin="7\n"), T('output_equals', "-6", "-3", stdin="-3\n"), T('code_contains', 'import yordamchi', "`import yordamchi` ishlatilgan"), T('code_contains', 'yordamchi.py', "`yordamchi.py` yaratilgan")],
            hint="Avval faylni yozing, keyin `sys.path.append(\".\")`, keyin `import`.", partial_solution='import sys\n\nwith open("yordamchi.py", "w", encoding="utf-8") as f:\n    f.write("def ikki_baravar(x):\\n    return x * 2\\n")\n\nsys.path.append(".")\n# yordamchi ni import qiling va natijani chiqaring\n', full_solution='import sys\n\nwith open("yordamchi.py", "w", encoding="utf-8") as f:\n    f.write("def ikki_baravar(x):\\n    return x * 2\\n")\n\nsys.path.append(".")\nimport yordamchi\n\nprint(yordamchi.ikki_baravar(int(input())))\n', explanation="Modul fayli yaratildi va import qilindi."),
        single('l72_practice_easy', "Easy: modul", "Qaysi gap to'g'ri?", section='practice', difficulty='easy', options=[opt("Har qanday `.py` fayl modul bo'la oladi", True), opt("Modul faqat standart kutubxonada bo'ladi", False), opt("Modulni faqat bir marta ishlatish mumkin", False)], hint="O'zingiz yozgan fayl ham.", explanation="`.py` fayl — modul."),
        code_task('l72_practice_medium', "Medium: formulalar moduli", r"""
Dastur `geometriya.py` yaratsin: `kvadrat_yuzi(a)` (`a * a`) va `togri_tortburchak_yuzi(a, b)` (`a * b`) funksiyalari bilan. Import qilib `kvadrat_yuzi(5)` va `togri_tortburchak_yuzi(2, 3)` ni ikki qatorda chiqaring: `25` va `6`.
""", section='practice', difficulty='medium', points=5, starter_code='import sys\n\n', tests=[T('output_equals', "25\n6", "Natija"), T('code_contains', 'geometriya', "`geometriya` moduli ishlatilgan")], hint="Modul matnini `f.write(...)` ga bitta qatorda `\\n` lar bilan yozing.", full_solution='import sys\n\nwith open("geometriya.py", "w", encoding="utf-8") as f:\n    f.write("def kvadrat_yuzi(a):\\n    return a * a\\n\\n")\n    f.write("def togri_tortburchak_yuzi(a, b):\\n    return a * b\\n")\n\nsys.path.append(".")\nimport geometriya\n\nprint(geometriya.kvadrat_yuzi(5))\nprint(geometriya.togri_tortburchak_yuzi(2, 3))\n', explanation="Ikkita funksiyali o'z moduli."),
        code_task('l72_practice_hard', "Hard: __main__ bilan sinov", r"""
Dastur `salomlar.py` modulini yaratsin: `salom(ism)` funksiyasi `Salom, <ism>!` **qaytaradi**; modul oxirida `if __name__ == "__main__": print("modul sinovi")`. Asosiy dastur uni import qilib, `salom("Ali")` natijasini chiqarsin. **«modul sinovi» chiqmasligi** kerak: faqat `Salom, Ali!`.
""", section='practice', difficulty='hard', points=5, starter_code='import sys\n\n', tests=[T('output_equals', "Salom, Ali!", "Natija"), T('code_contains', '__main__', "`__main__` tekshiruvi bor")], hint="Import paytida `__name__` modul nomiga teng — blok ishlamaydi.", full_solution='import sys\n\nwith open("salomlar.py", "w", encoding="utf-8") as f:\n    f.write("def salom(ism):\\n    return \'Salom, \' + ism + \'!\'\\n\\n")\n    f.write("if __name__ == \'__main__\':\\n    print(\'modul sinovi\')\\n")\n\nsys.path.append(".")\nimport salomlar\n\nprint(salomlar.salom("Ali"))\n', explanation="`__main__` bloki import paytida ishlamadi."),
    ])

# ==============================================================================
# 73-DARS
# ==============================================================================
LESSON_73 = L(73, "Python va VS Code dasturlarini kompyuterga o'rnatish, Python faylini ishga tushirish", 15,
    "Python va VS Code ni kompyuterga o'rnatish, birinchi .py faylni yaratish va terminal hamda VS Code orqali ishga tushirish; keng tarqalgan muammolarni hal qilish.",
    ["Python o'rnatish", "PATH", "VS Code", "Python kengaytmasi", ".py fayl", "Terminalda ishga tushirish"],
    [
        text(r"""
Shu paytgacha kodni brauzerda yozdingiz. Haqiqiy dasturchi esa **o'z kompyuterida** ishlaydi: fayllar saqlanadi, dasturlar internetsiz ishlaydi, o'zingiz yaratgan dasturni do'stingizga berishingiz mumkin. Endi shu bosqichga o'tamiz — ikkita dastur kerak: **Python** (til) va **VS Code** (kod yozish uchun qulay muharrir).
""", title="Brauzerdan kompyuterga"),
        text(r"""
## 1-qadam. Python o'rnatish

1. Brauzerda **python.org/downloads** sahifasini oching (rasmiy sayt).
2. «**Download Python 3.x**» tugmasini bosib, o'rnatuvchi faylni yuklab oling.
3. **Windows:** o'rnatuvchini ishga tushiring va **birinchi oynada pastdagi «Add python.exe to PATH» katakchasini albatta belgilang** — keyin «Install Now».
   **macOS:** `.pkg` faylni oching va ko'rsatmalarga amal qiling.
   **Linux:** odatda Python tayyor; kerak bo'lsa `sudo apt install python3 python3-pip`.
4. **Tekshiring:** terminal (Windows: «Win + R» → `cmd`; macOS/Linux: «Terminal») oching va yozing:

```text
python --version
```
Windows va ba'zi tizimlarda `python`, macOS/Linux'da ko'pincha `python3 --version`. `Python 3.12.x` kabi javob chiqsa — tayyor.

## 2-qadam. VS Code o'rnatish

1. **code.visualstudio.com** saytidan o'z tizimingiz uchun o'rnatuvchini yuklab oling va o'rnating.
2. VS Code'ni oching. Chap tomondagi **Extensions** (kvadratchalar belgisi, `Ctrl+Shift+X`) bo'limiga kiring.
3. Qidiruvga `Python` yozing va **Microsoft** tomonidan chiqarilgan «Python» kengaytmasini **Install** qiling.

## 3-qadam. Birinchi dasturingiz

1. Kompyuteringizda `python_kurs` nomli papka yarating (masalan, Hujjatlar ichida).
2. VS Code: **File → Open Folder** → shu papkani tanlang.
3. **New File** tugmasi bilan `salom.py` fayl yarating (kengaytma — **`.py`**!).
4. Quyidagini yozing va `Ctrl+S` bilan saqlang:

```python
ism = input("Ismingiz: ")
print(f"Salom, {ism}! Bu mening birinchi dasturim.")
```

## 4-qadam. Ishga tushirish

- **VS Code orqali:** o'ng yuqoridagi ▶ (**Run Python File**) tugmasini bosing.
- **Terminal orqali:** VS Code'da **Terminal → New Terminal** (`Ctrl+\``), keyin:
```text
python salom.py
```
(macOS/Linux'da `python3 salom.py`.)
""", title="Qadamma-qadam yo'riqnoma"),
        callout('warning', r"""
**Eng ko'p uchraydigan muammolar:**
- `'python' is not recognized...` (Windows) — o'rnatishda **PATH** katakchasi belgilanmagan. Python'ni qayta o'rnating (Modify/Repair) va katakchani belgilang, terminalni yoping-oching.
- Fayl `salom.py.txt` bo'lib qolgan — fayl kengaytmalarini ko'rsating va nomini `salom.py` qiling.
- VS Code ▶ tugmasi chiqmayapti — Python kengaytmasi o'rnatilganini va `.py` fayl ochiqligini tekshiring.
- «No module named ...» — fayl nomini `random.py`, `math.py` kabi qo'ymang.
""", title="Muammolar va yechimlar"),
        callout('analogy', r"""
Python — **tilni biluvchi tarjimon**, VS Code — **qulay yozuv stoli**. Tarjimonsiz stolda yozgan matn ishlamaydi; stolsiz tarjimon ham ishlaydi, lekin noqulay.
""", title="Hayotiy o'xshatish"),
        example(r'''
import sys

print("Python versiyasi:", sys.version_info.major, sys.version_info.minor)
print("Katta versiya 3 mi?", sys.version_info.major == 3)
''', title="Python versiyasini aniqlash", body="Bu kodni o'z kompyuteringizda ham ishga tushirib ko'ring — o'rnatilgan Python versiyasini ko'rsatadi. Bu yerda ham `3` bilan boshlanuvchi versiya chiqadi."),
        example(r'''
import sys

def versiya_matni():
    return f"Python {sys.version_info.major}.{sys.version_info.minor}"

if __name__ == "__main__":
    print(versiya_matni())
''', title="Amaliy: o'z kompyuteringizdagi namuna dastur", body="`if __name__ == \"__main__\":` — VS Code'da ▶ tugmasi yoki `python fayl.py` buyrug'i bilan ishga tushirilganda bajariladi. Shu shablon bilan har bir dasturingizni boshlang."),
        exercise('l73_inline_pick'),
        callout('tip', r"""
**Shu darsning amaliy qismi — o'z kompyuteringizda.** Yuqoridagi qadamlarni bajarib, `salom.py` ni ishga tushiring. Brauzer muharriri bu vazifani tekshira olmaydi, shuning uchun quyidagi test va dastur topshirig'i — o'rnatish jarayonini tushunganingizni tekshiradi.
""", title="Mustaqil amaliyot"),
        recap(["Python — python.org dan, Windows'da PATH katakchasi!", "VS Code + Microsoft Python kengaytmasi", "`.py` fayl; ▶ yoki `python fayl.py` bilan ishga tushiriladi"], "oxirgi darsda hamma o'rganganlarimizni birlashtirib mustaqil dastur yaratamiz. Qanday dastur yaratmoqchisiz?"),
    ],
    [
        single('l73_inline_pick', "PATH", "Windows'da Python'ni o'rnatayotganda qaysi katakchani belgilash juda muhim?", section='inline', points=2, options=[opt("«Add python.exe to PATH»", True), opt("«Install for all fonts»", False), opt("«Open browser»", False)], hint="Terminal `python` buyrug'ini taniy olishi uchun.", explanation="PATH katakchasi — terminaldan `python` ni chaqirish imkonini beradi."),
        single('l73_quiz_1', "Fayl kengaytmasi", "Python dasturi faylining kengaytmasi?", options=[opt("`.py`", True), opt("`.txt`", False), opt("`.python`", False)], hint="Python so'zining qisqartmasi.", explanation="`.py`."),
        single('l73_quiz_2', "Ishga tushirish", "Terminalda `salom.py` ni ishga tushirish buyrug'i?", options=[opt("`python salom.py`", True), opt("`salom.py run`", False), opt("`open salom.py`", False)], hint="`python` + fayl nomi.", explanation="`python salom.py` (macOS/Linux'da ko'pincha `python3`)."),
        single('l73_quiz_3', "VS Code kengaytmasi", "VS Code'da Python bilan qulay ishlash uchun nima o'rnatiladi?", options=[opt("Microsoft'ning «Python» kengaytmasi", True), opt("Yangi brauzer", False), opt("Antivirus", False)], hint="Extensions bo'limi.", explanation="Python kengaytmasi (Extensions)."),
        code_task('l73_assignment', "Versiya tekshiruvchi dastur", r"""
O'z kompyuteringizda ishlatadigan **versiya tekshiruvchi** dastur yozing (`sys` moduli bilan): Python **katta versiyasi 3 va undan yuqori** bo'lsa `Python versiyasi mos`, aks holda `Python eski`. Bu platformada Python 3 ishlaydi — natija: `Python versiyasi mos`. Dastur `if __name__ == "__main__":` bilan boshlansin.
""", starter_code='import sys\n\n', points=10, tests=[T('output_equals', "Python versiyasi mos", "Natija"), T('code_contains', '__main__', "`__main__` tekshiruvi bor"), T('code_contains', 'sys.version_info', "`sys.version_info` ishlatilgan")],
            hint="`sys.version_info.major >= 3`.", partial_solution='import sys\n\nif __name__ == "__main__":\n    if sys.version_info.major >= 3:\n        print("Python versiyasi mos")\n    # aks holda...\n', full_solution='import sys\n\nif __name__ == "__main__":\n    if sys.version_info.major >= 3:\n        print("Python versiyasi mos")\n    else:\n        print("Python eski")\n', explanation="Shu dasturni VS Code'da ham ishga tushirib ko'ring."),
        single('l73_practice_easy', "Easy: tekshirish", "O'rnatilgan Python versiyasini terminalda qanday tekshiramiz?", section='practice', difficulty='easy', options=[opt("`python --version`", True), opt("`python --check`", False), opt("`version python`", False)], hint="Ikki chiziq va «version».", explanation="`python --version`."),
        code_task('l73_practice_medium', "Medium: salomlashuv dasturi", r"""
`salom.py` namunasini takrorlang: ism so'rab (`input`), `Salom, <ism>! Bu mening birinchi dasturim.` deb chiqaring. Dastur `salom()` funksiyasida bo'lsin va `__main__` bilan chaqirilsin. `Ali` → `Salom, Ali! Bu mening birinchi dasturim.`
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Salom, Ali! Bu mening birinchi dasturim.", "Ali", stdin="Ali\n"), T('output_equals', "Salom, Vali! Bu mening birinchi dasturim.", "Vali", stdin="Vali\n"), T('code_contains', '__main__', "`__main__` tekshiruvi bor")], hint="`def salom(): ...` va oxirida `if __name__ == \"__main__\": salom()`.", full_solution='def salom():\n    ism = input()\n    print(f"Salom, {ism}! Bu mening birinchi dasturim.")\n\nif __name__ == "__main__":\n    salom()\n', explanation="Aynan shu shablon bilan har bir dasturni boshlang."),
        code_task('l73_practice_hard', "Hard: o'rnatish bo'yicha tekshiruv ro'yxati", r"""
`qadamlar` listini yarating: o'rnatish qadamlarining qisqa nomlari — `Python`, `PATH`, `VS Code`, `Kengaytma`, `salom.py`, `Run`. Dastur raqamlab chiqarsin: `1. Python`, ..., `6. Run`. (Tartib shu bo'lsin.)
""", section='practice', difficulty='hard', points=5, tests=[T('output_equals', "1. Python\n2. PATH\n3. VS Code\n4. Kengaytma\n5. salom.py\n6. Run", "Natija"), T('code_contains', 'enumerate', "`enumerate` ishlatilgan")], hint="`enumerate(qadamlar, start=1)`.", full_solution='qadamlar = ["Python", "PATH", "VS Code", "Kengaytma", "salom.py", "Run"]\nfor n, q in enumerate(qadamlar, start=1):\n    print(f"{n}. {q}")\n', explanation="O'rnatish tartibini eslab qolish uchun ro'yxat."),
    ])

# ==============================================================================
# 74-DARS
# ==============================================================================
LESSON_74 = L(74, "O'rganilgan mavzularni birlashtirib mustaqil dastur yaratish", 15,
    "Kurs davomida o'rganilganlarni (funksiyalar, list/dict, fayl/JSON, xatolarni boshqarish, modullar) birlashtirib, rejalashtirish orqali mustaqil dastur yaratish.",
    ["Dastur rejasi", "Funksiyalarga bo'lish", "Ma'lumotni saqlash", "Xatolardan himoya", "Sinash va yaxshilash"],
    [
        text(r"""
Siz endi Python'ning asosiy vositalarini bilasiz: o'zgaruvchilar, matnlar, shartlar, sikllar, list/dict, funksiyalar, xatolarni boshqarish, fayllar va modullar. Bu — **mustaqil dastur** yaratish uchun yetarli! Bu darsda dastur yaratishning **tartibli usulini** o'rganamiz.
""", title="Hamma narsani birlashtirish vaqti"),
        text(r"""
**Dastur yaratish — 6 qadam:**

1. **Maqsad:** dastur nima qiladi? (bitta jumlada)
2. **Ma'lumot:** nimani saqlaymiz? (`list`, `dict`, fayl/JSON)
3. **Funksiyalar:** qanday kichik vazifalarga bo'lamiz? (har biri bitta ish)
4. **Menyu / oqim:** foydalanuvchi qanday boshqaradi? (`while True` + buyruqlar)
5. **Xatolardan himoya:** nima noto'g'ri ketishi mumkin? (`try/except`, tekshiruvlar)
6. **Sinash:** har bir qismni alohida, keyin birga sinab ko'ring; xato topilsa — yaxshilang.

**Dastur shabloni:**

```python
import json

def yukla():
    ...                # ma'lumotni fayldan olish

def saqla(malumot):
    ...                # faylga yozish

def qosh(malumot):
    ...                # bitta vazifa

def main():
    malumot = yukla()
    while True:
        buyruq = input()
        if buyruq == "0":
            break
        elif buyruq == "1":
            qosh(malumot)
        ...
    saqla(malumot)

if __name__ == "__main__":
    main()
```
""", title="Reja va shablon"),
        callout('analogy', r"""
Dastur yaratish — **uy qurish**: avval **reja** (chizma), keyin **poydevor** (ma'lumot), **xonalar** (funksiyalar), **eshik** (menyu), **xavfsizlik** (xatolardan himoya) va oxirida **tekshiruv**.
""", title="Hayotiy o'xshatish"),
        example(r'''
def statistika(sonlar):
    if len(sonlar) == 0:
        return None
    return {"soni": len(sonlar), "yigindi": sum(sonlar), "ortacha": sum(sonlar) / len(sonlar), "eng_katta": max(sonlar)}

def main():
    sonlar = []
    for q in ["5", "x", "10", "3"]:
        try:
            sonlar.append(int(q))
        except ValueError:
            print("O'tkazib yuborildi:", q)
    print(statistika(sonlar))

main()
''', title="Kichik dastur: statistika", body="Funksiya (`statistika`), xatolardan himoya (`try/except`), dictionary va sikl birga ishlaydi. Natija: `O'tkazib yuborildi: x` va `{'soni': 3, 'yigindi': 18, 'ortacha': 6.0, 'eng_katta': 10}`."),
        example(r'''
import json

def saqla(royxat, nom="vazifalar.json"):
    with open(nom, "w", encoding="utf-8") as f:
        json.dump(royxat, f, ensure_ascii=False)

def yukla(nom="vazifalar.json"):
    try:
        with open(nom, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

vazifalar = yukla()
vazifalar.append("Python o'rganish")
saqla(vazifalar)
print(yukla())
''', title="Amaliy: saqlash va yuklash funksiyalari", body="Ma'lumotni saqlash va yuklash — alohida funksiyalar, standart parametrli. Natija: `[\"Python o'rganish\"]` (fayl avval bo'lmagani uchun bo'sh listdan boshlandi)."),
        exercise('l74_inline_pick'),
        callout('tip', r"""
Birinchi dasturingizda hamma narsani **mukammal** qilishga urinmang. Avval eng sodda ishlaydigan versiyani yarating, keyin bir-bir yaxshilang. «Ishlaydigan oddiy» — «mukammal yarim tayyor»dan yaxshiroq.
""", title="Maslahat"),
        recap(["6 qadam: maqsad, ma'lumot, funksiyalar, menyu, xatolardan himoya, sinash", "`main()` + `if __name__ == \"__main__\"` shabloni", "oddiy versiyadan boshlang"], "modul loyihasi — o'zingizning mustaqil dasturingiz! Qaysi mavzu sizni ko'proq qiziqtiradi?"),
    ],
    [
        single('l74_inline_pick', "Qadam tartibi", "Dastur yaratishning birinchi qadami nima?", section='inline', points=2, options=[opt("Dastur nima qilishini aniqlash (maqsad)", True), opt("Darhol kod yozish", False), opt("Fayl nomini tanlash", False)], hint="Chizma.", explanation="Avval maqsad va reja."),
        single('l74_quiz_1', "Funksiyalar", "Katta dasturni nima uchun funksiyalarga bo'lamiz?", options=[opt("Har bir qism bitta vazifani bajarib, sinash va tuzatish oson bo'lishi uchun", True), opt("Dastur tezroq ishlashi uchun", False), opt("Kod uzunroq bo'lishi uchun", False)], hint="Xonalar.", explanation="Tushunarlilik va qayta ishlatish."),
        single('l74_quiz_2', "Xatolardan himoya", "Foydalanuvchi noto'g'ri kiritishi mumkin bo'lgan joyga nima qo'yiladi?", options=[opt("`try/except` yoki tekshiruv", True), opt("Hech narsa", False), opt("`import`", False)], hint="Xavfsizlik to'ri.", explanation="Xatolardan himoya."),
        predict('l74_quiz_3', "Funksiyalar birligi", "Dastur nima chiqaradi?", code='def a(x):\n    return x + 1\n\ndef b(x):\n    return a(x) * 2\n\ndef main():\n    print(b(a(1)))\n\nif __name__ == "__main__":\n    main()\n', answer="6", hint="`a(1)` = 2, `b(2)` = (2 + 1) * 2.", explanation="`a(1)` = 2; `b(2)` = 6."),
        code_task('l74_assignment', "Mini dastur: baholar tahlili", r"""
**Reja asosida** mustaqil dastur yozing. Foydalanuvchi baholarni (1–5) kiritadi, `0` kiritilganda tugaydi. Son bo'lmagan yoki 1–5 dan tashqari qiymat — `Noto'g'ri baho: <qiymat>` (qabul qilinmaydi). Oxirida: `Baholar soni: N` va `O'rtacha: X.XX` (baho bo'lmasa — `Baholar yo'q`). Dasturni `statistika(baholar)` funksiyasi (o'rtacha yoki `None` qaytaradi) va `main()` bilan tuzing. `5`, `4`, `x`, `7`, `5`, `0` → `Noto'g'ri baho: x`, `Noto'g'ri baho: 7`, `Baholar soni: 3`, `O'rtacha: 4.67`.
""", starter_code='def statistika(baholar):\n    pass\n\n\ndef main():\n    pass\n\n\nif __name__ == "__main__":\n    main()\n', points=15,
            tests=[T('output_equals', "Noto'g'ri baho: x\nNoto'g'ri baho: 7\nBaholar soni: 3\nO'rtacha: 4.67", "5 4 x 7 5 0", stdin="5\n4\nx\n7\n5\n0\n"), T('output_equals', "Baholar yo'q", "darhol 0", stdin="0\n"), T('output_equals', "Baholar soni: 2\nO'rtacha: 3.00", "2 4 0", stdin="2\n4\n0\n", hidden=True), T('output_equals', "4.0\nNone", "statistika funksiyasi", harness='print(statistika([3, 5]))\nprint(statistika([]))', stdin="0\n"), T('code_contains', 'def main', "`main()` funksiyasi bor")],
            hint="`main()` da `baholar = []`, `while True`, `try: b = int(input())`; tekshiruv `1 <= b <= 5`; `statistika` ichida bo'sh listni tekshiring.", partial_solution='def statistika(baholar):\n    if len(baholar) == 0:\n        return None\n    return sum(baholar) / len(baholar)\n\n\ndef main():\n    baholar = []\n    while True:\n        q = input()\n        if q == "0":\n            break\n        # qiymatni tekshiring va baholarga qo\'shing\n    # natijani chiqaring\n\n\nif __name__ == "__main__":\n    main()\n', full_solution='def statistika(baholar):\n    if len(baholar) == 0:\n        return None\n    return sum(baholar) / len(baholar)\n\n\ndef main():\n    baholar = []\n    while True:\n        q = input()\n        if q == "0":\n            break\n        try:\n            b = int(q)\n            if b < 1 or b > 5:\n                raise ValueError\n            baholar.append(b)\n        except ValueError:\n            print("Noto\'g\'ri baho:", q)\n    o = statistika(baholar)\n    if o is None:\n        print("Baholar yo\'q")\n    else:\n        print("Baholar soni:", len(baholar))\n        print(f"O\'rtacha: {o:.2f}")\n\n\nif __name__ == "__main__":\n    main()\n', explanation="Funksiyalar, sikl, try/except, raise va f-string — hammasi birga."),
        single('l74_practice_easy', "Easy: main()", "Nima uchun dasturni `main()` funksiyasiga joylaymiz?", section='practice', difficulty='easy', options=[opt("Dastur tuzilishi aniq va boshqa fayldan import qilish xavfsiz bo'ladi", True), opt("Aks holda dastur ishlamaydi", False), opt("Xotira tejaladi", False)], hint="Tartib.", explanation="Tartibli tuzilma va `__main__` bilan xavfsiz import."),
        code_task('l74_practice_medium', "Medium: xarajatlar hisobi", r"""
Foydalanuvchi xarajatlarni kiritadi (butun son), `0` bilan tugaydi. `jami(royxat)` funksiyasi yig'indini qaytarsin; dastur `Jami: <yig'indi>` va `Eng katta: <max>` (yo'q bo'lsa `Xarajat yo'q`) chiqarsin. `1000`, `5000`, `300`, `0` → `Jami: 6300` va `Eng katta: 5000`.
""", section='practice', difficulty='medium', points=5, tests=[T('output_equals', "Jami: 6300\nEng katta: 5000", "1000 5000 300", stdin="1000\n5000\n300\n0\n"), T('output_equals', "Xarajat yo'q", "darhol 0", stdin="0\n"), T('output_equals', "Jami: 7\nEng katta: 7", "bitta", stdin="7\n0\n", hidden=True), T('output_equals', "6\n0", "jami funksiyasi", harness='print(jami([1, 2, 3]))\nprint(jami([]))', stdin="0\n")], hint="`jami` — `sum`; sikl `0` gacha.", full_solution='def jami(royxat):\n    return sum(royxat)\n\n\ndef main():\n    xarajatlar = []\n    while True:\n        x = int(input())\n        if x == 0:\n            break\n        xarajatlar.append(x)\n    if len(xarajatlar) == 0:\n        print("Xarajat yo\'q")\n    else:\n        print("Jami:", jami(xarajatlar))\n        print("Eng katta:", max(xarajatlar))\n\n\nif __name__ == "__main__":\n    main()\n', explanation="Funksiya + sikl + list."),
        code_task('l74_practice_hard', "Hard: lug'at va JSON", r"""
`yukla()` (fayl yo'q bo'lsa `{}`), `saqla(d)` — `lugat.json` bilan ishlaydi (`with` va `json`). `qosh(d, so_z, tarjima)` — lug'atga qo'shadi. Tekshiruv: `yukla()` → `{}`; `qosh` va `saqla` dan keyin `yukla()` — saqlangan lug'at: `{'salom': 'hello'}`.
""", section='practice', difficulty='hard', points=5, starter_code='import json\n', tests=[T('output_equals', "{}\n{'salom': 'hello'}", "Natija", harness='print(yukla())\nd = yukla()\nqosh(d, "salom", "hello")\nsaqla(d)\nprint(yukla())')], hint="Oldingi darsdagi `yukla/saqla` shabloni, faqat `[]` o'rniga `{}`.", full_solution='import json\n\ndef yukla():\n    try:\n        with open("lugat.json", "r", encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return {}\n\ndef saqla(d):\n    with open("lugat.json", "w", encoding="utf-8") as f:\n        json.dump(d, f, ensure_ascii=False)\n\ndef qosh(d, so_z, tarjima):\n    d[so_z] = tarjima\n', explanation="Saqlash va yuklash — har qanday dasturning asosi."),
    ])

LESSONS = [LESSON_70, LESSON_71, LESSON_72, LESSON_73, LESSON_74]

# ==============================================================================
# MODUL NAZORATI + MINI-LOYIHA
# ==============================================================================
ASSESSMENT = module_assessment("11-modul yakuniy nazorati: Modullar va mustaqil dastur", r"""
**5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va **mini-loyiha** — **mustaqil ishlaydigan kichik Python dasturi** («Shaxsiy moliya hisobchisi»).
O'tish mezoni — **70%** (admin o'zgartirishi mumkin).
""", [
    single('m11_a_t1', "import", "`from math import sqrt` dan keyin kvadrat ildiz qanday olinadi?", section='assessment', points=2, options=[opt("`sqrt(16)`", True), opt("`math.sqrt(16)`", False), opt("`import sqrt`", False)], explanation="`from` bilan nom to'g'ridan-to'g'ri ishlatiladi."),
    single('m11_a_t2', "randint", "`random.randint(1, 6)` qaysi sonlarni berishi mumkin?", section='assessment', points=2, options=[opt("1 dan 6 gacha (6 ham)", True), opt("1 dan 5 gacha", False), opt("0 dan 6 gacha", False)], explanation="Ikkala chegara kiradi."),
    single('m11_a_t3', "__main__", "`if __name__ == \"__main__\":` nima uchun kerak?", section='assessment', points=2, options=[opt("Kod faqat to'g'ridan-to'g'ri ishga tushirilganda bajarilishi uchun", True), opt("Faylni shifrlash uchun", False), opt("Xatolarni ushlash uchun", False)], explanation="Import qilinganda ishlamaydi."),
    single('m11_a_t4', "PATH", "Windows'da `python` buyrug'i terminalda ishlamasa, ko'pincha sabab?", section='assessment', points=2, options=[opt("O'rnatishda «Add python.exe to PATH» belgilanmagan", True), opt("Kompyuter eski", False), opt("VS Code o'rnatilmagan", False)], explanation="PATH sozlanmagan."),
    multiple('m11_a_t5', "Modullar", "Qaysi gaplar to'g'ri?", section='assessment', points=2, options=[opt("Har qanday `.py` fayl modul bo'la oladi", True), opt("`import math as m` — qisqa nom beradi", True), opt("Modul nomi fayl nomi bilan `.py` qo'shib yoziladi", False), opt("Standart modul nomini o'z modulingizga qo'ymaslik kerak", True)], explanation="Import'da `.py` yozilmaydi."),
    predict('m11_a_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='import math\nprint(math.floor(-2.5), math.ceil(-2.5))\n', answer="-3 -2", explanation="`floor` pastga, `ceil` yuqoriga."),
    predict('m11_a_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='from datetime import date\nd = date(2026, 12, 25)\nprint(d.day + d.month, d.strftime("%Y/%m/%d"))\n', answer="37 2026/12/25", explanation="`25 + 12 = 37`."),
    predict('m11_a_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='import random\nrandom.seed(3)\nx = random.choice([10, 20, 30])\nprint(x in [10, 20, 30])\n', answer="True", explanation="Tanlangan element har doim ro'yxatda."),
    fix_task('m11_a_f1', "Xatoni tuzating (1)", "Kvadrat ildiz `4.0` chiqishi kerak, lekin `NameError` beryapti.", section='assessment', points=4, starter_code='print(sqrt(16))\n', tests=[T('output_equals', "4.0", "Natija: 4.0")], hint="`sqrt` qaysi moduldan?", full_solution='from math import sqrt\nprint(sqrt(16))\n', explanation="`from math import sqrt` yetishmagan."),
    fix_task('m11_a_f2', "Xatoni tuzating (2)", "Dastur `Salom, Ali!` chiqarishi kerak, lekin `salom()` chaqirilmayapti.", section='assessment', points=4, starter_code='def salom(ism):\n    return f"Salom, {ism}!"\n\nif __name__ == "__main__":\n    salom("Ali")\n', tests=[T('output_equals', "Salom, Ali!", "Natija")], hint="Funksiya natija qaytaradi — chiqarish kerak.", full_solution='def salom(ism):\n    return f"Salom, {ism}!"\n\nif __name__ == "__main__":\n    print(salom("Ali"))\n', explanation="`return` qiymati `print` qilinmadi."),
    code_task('m11_a_project', "Mini-loyiha: Mustaqil Python dasturi — Shaxsiy moliya hisobchisi", r"""
**Shaxsiy moliya hisobchisi** dasturini yarating. Ma'lumotlar `moliya.json` faylida saqlanadi: yozuvlar **list**i, har biri `{"tur": "daromad" yoki "xarajat", "summa": <int>, "izoh": <matn>}`.

**Talablar:**
- Funksiyalar: `yukla()` (fayl yo'q bo'lsa `[]`), `saqla(yozuvlar)` (`with` + `json`), `balans(yozuvlar)` (daromadlar − xarajatlar), `main()`; fayl oxirida `if __name__ == "__main__": main()`.
- **Menyu** (`0` gacha takrorlanadi):

| Buyruq | Amal | Xabar |
|---|---|---|
| `1` | **summa** va **izoh** o'qib **daromad** qo'shadi, saqlaydi | `Daromad qo'shildi` |
| `2` | **summa** va **izoh** o'qib **xarajat** qo'shadi, saqlaydi | `Xarajat qo'shildi` |
| `3` | balansni chiqaradi | `Balans: <N>` |
| `4` | barcha yozuvlarni `1. daromad 50000 (maosh)` shaklida chiqaradi | yozuv yo'q bo'lsa `Yozuv yo'q` |
| `0` | tugatadi | `Xayr!` |

- Summa **musbat butun son** bo'lishi kerak: son emas yoki musbat bo'lmasa → `Xato: summa musbat butun son bo'lishi kerak` (yozuv qo'shilmaydi, izoh baribir o'qiladi). Xatoni `try/except` va `raise ValueError` bilan boshqaring.
- Noma'lum buyruq → `Noma'lum buyruq`.

Misol: `1`,`500000`,`maosh`, `2`,`120000`,`ijara`, `3`, `4`, `0` →
```
Daromad qo'shildi
Xarajat qo'shildi
Balans: 380000
1. daromad 500000 (maosh)
2. xarajat 120000 (ijara)
Xayr!
```
""", section='project', points=30, difficulty='hard', unlock=3, starter_code='import json\n\n# Shaxsiy moliya hisobchisi\n',
        expected_output_example="Daromad qo'shildi\nXarajat qo'shildi\nBalans: 380000\n1. daromad 500000 (maosh)\n2. xarajat 120000 (ijara)\nXayr!",
        tests=[T('output_equals', "Daromad qo'shildi\nXarajat qo'shildi\nBalans: 380000\n1. daromad 500000 (maosh)\n2. xarajat 120000 (ijara)\nXayr!", "Misol ssenariy", stdin="1\n500000\nmaosh\n2\n120000\nijara\n3\n4\n0\n"),
               T('output_equals', "Balans: 0\nYozuv yo'q\nXayr!", "Bo'sh holat", stdin="3\n4\n0\n"), T('output_equals', "Xato: summa musbat butun son bo'lishi kerak\nXato: summa musbat butun son bo'lishi kerak\nNoma'lum buyruq\nBalans: 0\nXayr!", "Xato kiritishlar", stdin="1\nabc\nkitob\n2\n-5\nizoh\n9\n3\n0\n"),
               T('output_equals', "Xarajat qo'shildi\nBalans: -2500\nXayr!", "Manfiy balans", stdin="2\n2500\nnon\n3\n0\n", hidden=True),
               T('output_equals', '[{"tur": "daromad", "summa": 100, "izoh": "sovg\'a"}]', "Fayl JSON ko'rinishida saqlangan", stdin="1\n100\nsovg'a\n0\n", harness='import json\nwith open("moliya.json", encoding="utf-8") as f:\n    print(json.dumps(json.load(f), ensure_ascii=False))', hidden=True),
               T('output_equals', "0\n-3\n5", "balans funksiyasi", harness='print(balans([]))\nprint(balans([{"tur": "xarajat", "summa": 3, "izoh": ""}]))\nprint(balans([{"tur": "daromad", "summa": 9, "izoh": ""}, {"tur": "xarajat", "summa": 4, "izoh": ""}]))', stdin="0\n", hidden=True),
               T('code_contains', 'json.dump', "`json.dump` ishlatilgan"), T('code_contains', 'FileNotFoundError', "`FileNotFoundError` ushlangan"), T('code_contains', 'raise', "`raise` ishlatilgan"), T('code_contains', '__main__', "`__main__` tekshiruvi bor")],
        hint="1) `yukla()/saqla()` — 10-moduldagi shablon. 2) `balans`: siklda `tur == \"daromad\"` bo'lsa qo'shing, aks holda ayiring. 3) `qosh(yozuvlar, tur)` yordamchi funksiyasi 1 va 2 buyruqlar uchun umumiy: summa va izohni o'qiydi, `try: summa = int(...)`, `if summa <= 0: raise ValueError`. 4) Izohni summadan keyin **har doim** o'qing (xato bo'lsa ham).",
        partial_solution='import json\n\ndef yukla():\n    try:\n        with open("moliya.json", "r", encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return []\n\ndef saqla(yozuvlar):\n    with open("moliya.json", "w", encoding="utf-8") as f:\n        json.dump(yozuvlar, f, ensure_ascii=False)\n\ndef balans(yozuvlar):\n    # daromad - xarajat\n    pass\n\ndef main():\n    yozuvlar = yukla()\n    while True:\n        buyruq = input()\n        if buyruq == "0":\n            break\n        # buyruqlarni yozing\n    print("Xayr!")\n\nif __name__ == "__main__":\n    main()\n',
        full_solution='import json\n\ndef yukla():\n    try:\n        with open("moliya.json", "r", encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return []\n\ndef saqla(yozuvlar):\n    with open("moliya.json", "w", encoding="utf-8") as f:\n        json.dump(yozuvlar, f, ensure_ascii=False)\n\ndef balans(yozuvlar):\n    jami = 0\n    for y in yozuvlar:\n        if y["tur"] == "daromad":\n            jami = jami + y["summa"]\n        else:\n            jami = jami - y["summa"]\n    return jami\n\ndef qosh(yozuvlar, tur):\n    matn = input()\n    izoh = input()\n    try:\n        summa = int(matn)\n        if summa <= 0:\n            raise ValueError\n    except ValueError:\n        print("Xato: summa musbat butun son bo\'lishi kerak")\n    else:\n        yozuvlar.append({"tur": tur, "summa": summa, "izoh": izoh})\n        saqla(yozuvlar)\n        if tur == "daromad":\n            print("Daromad qo\'shildi")\n        else:\n            print("Xarajat qo\'shildi")\n\ndef main():\n    yozuvlar = yukla()\n    while True:\n        buyruq = input()\n        if buyruq == "0":\n            break\n        elif buyruq == "1":\n            qosh(yozuvlar, "daromad")\n        elif buyruq == "2":\n            qosh(yozuvlar, "xarajat")\n        elif buyruq == "3":\n            print("Balans:", balans(yozuvlar))\n        elif buyruq == "4":\n            if len(yozuvlar) == 0:\n                print("Yozuv yo\'q")\n            else:\n                for n, y in enumerate(yozuvlar, start=1):\n                    print(f"{n}. {y[\'tur\']} {y[\'summa\']} ({y[\'izoh\']})")\n        else:\n            print("Noma\'lum buyruq")\n    print("Xayr!")\n\nif __name__ == "__main__":\n    main()\n',
        explanation="Loyiha kursdagi deyarli hamma narsani birlashtiradi: funksiyalar, list/dict, sikl, shart, fayl+JSON, xatolarni boshqarish (try/except/else, raise), f-string va main()."),
])

# ==============================================================================
# YAKUNIY TAKRORLASH VA BAHOLASH (butun kurs)
# ==============================================================================
FINAL_REVIEW = module_assessment("Yakuniy takrorlash va baholash (butun kurs)", r"""
Butun kurs bo'yicha **yakuniy takrorlash va baholash**: o'zgaruvchilar, matnlar, shartlar, sikllar, list/dict/set, funksiyalar, xatolar, fayllar/JSON va modullar — **aralash** holda.
Natija sizning kurs bo'yicha o'zlashtirish foizingizni ko'rsatadi. O'tish — **70%**; qayta urinish cheksiz.
""", [
    single('f_t1', "Turlar", "`type(3 / 2)` natijasi?", section='assessment', points=2, options=[opt("`<class 'float'>`", True), opt("`<class 'int'>`", False), opt("`<class 'str'>`", False)], explanation="`/` doim float."),
    single('f_t2', "Matn", "`\"Python\".upper()` natijasi?", section='assessment', points=2, options=[opt("`PYTHON`", True), opt("`python`", False), opt("`Python`", False)], explanation="`upper()` — katta harflar."),
    single('f_t3', "Shart", "Qaysi shart `x` 5 dan katta **va** juft ekanini tekshiradi?", section='assessment', points=2, options=[opt("`x > 5 and x % 2 == 0`", True), opt("`x > 5 or x % 2 == 0`", False), opt("`x > 5 and x % 2 = 0`", False)], explanation="`and` va `==`."),
    single('f_t4', "Sikl", "`range(2, 10, 3)` qaysi sonlarni beradi?", section='assessment', points=2, options=[opt("2, 5, 8", True), opt("2, 5, 8, 11", False), opt("3, 6, 9", False)], explanation="Qadam 3."),
    single('f_t5', "To'plam", "Takrorlanmaydigan elementlar to'plami uchun mos tur?", section='assessment', points=2, options=[opt("set", True), opt("list", False), opt("tuple", False)], explanation="Set takrorlarni olib tashlaydi."),
    single('f_t6', "Funksiya", "Funksiya `return` qilmasa nima qaytaradi?", section='assessment', points=2, options=[opt("`None`", True), opt("`0`", False), opt("Bo'sh matn", False)], explanation="`None`."),
    single('f_t7', "Xatolar", "`10 / 0` qaysi xatoni beradi?", section='assessment', points=2, options=[opt("`ZeroDivisionError`", True), opt("`ValueError`", False), opt("`TypeError`", False)], explanation="Nolga bo'lish."),
    single('f_t8', "Fayl", "Faylni o'qishning xavfsiz usuli?", section='assessment', points=2, options=[opt("`with open(...) as f:`", True), opt("`open(...)` va `close()` ni unutish", False), opt("`read(...)`", False)], explanation="`with` faylni avtomatik yopadi."),
    predict('f_p1', "Natija (1)", "Dastur nima chiqaradi?", section='assessment', points=2, code='a = [3, 1, 2]\na.sort()\na.append(a[0] * 10)\nprint(a)\n', answer="[1, 2, 3, 10]", explanation="Saralandi, keyin `1 * 10` qo'shildi."),
    predict('f_p2', "Natija (2)", "Dastur nima chiqaradi?", section='assessment', points=2, code='d = {"a": 1, "b": 2}\nd["c"] = d["a"] + d["b"]\nfor k in d:\n    if d[k] > 1:\n        print(k, d[k])\n', answer="b 2\nc 3", explanation="`c` = 3; faqat qiymati 1 dan katta bo'lganlar."),
    predict('f_p3', "Natija (3)", "Dastur nima chiqaradi?", section='assessment', points=2, code='def f(x, y=2, *a):\n    return x * y + len(a)\n\nprint(f(3), f(3, 4), f(3, 4, 7, 8))\n', answer="6 12 14", explanation="`3*2+0`, `3*4+0`, `3*4+2`."),
    predict('f_p4', "Natija (4)", "Dastur nima chiqaradi?", section='assessment', points=2, code='try:\n    n = int("5")\n    r = 10 // (n - 5)\nexcept ZeroDivisionError:\n    r = -1\nelse:\n    r = r + 100\nfinally:\n    print("tamom")\nprint(r)\n', answer="tamom\n-1", explanation="`ZeroDivisionError` ushlandi; `else` ishlamadi."),
    fix_task('f_f1', "Tuzating: sikl va list", "Dastur 1 dan 5 gacha sonlar kvadratlari listini chiqarishi kerak: `[1, 4, 9, 16, 25]`.", section='assessment', points=4, starter_code='k = []\nfor i in range(1, 5):\n    k.append(i * i)\nprint(k)\n', tests=[T('output_equals', "[1, 4, 9, 16, 25]", "Natija")], hint="`range` oxirgi sonni kiritmaydi.", full_solution='k = []\nfor i in range(1, 6):\n    k.append(i * i)\nprint(k)\n', explanation="`range(1, 6)`."),
    fix_task('f_f2', "Tuzating: funksiya", "`o_rtacha([2, 4])` `3.0` qaytarishi kerak.", section='assessment', points=4, starter_code='def o_rtacha(sonlar):\n    jami = 0\n    for s in sonlar:\n        jami = jami + s\n    print(jami / len(sonlar))\n', tests=[T('output_equals', "3.0\n5.0", "Natija", harness='print(o_rtacha([2, 4]))\nprint(o_rtacha([5]))')], hint="Funksiya qaytarishi kerak, chiqarishi emas.", full_solution='def o_rtacha(sonlar):\n    jami = 0\n    for s in sonlar:\n        jami = jami + s\n    return jami / len(sonlar)\n', explanation="`return`."),
    code_task('f_c1', "Amaliy: matn tahlili", "Foydalanuvchi gap kiritadi (so'zlar probel bilan). Dastur: so'zlar sonini, eng uzun so'zni (teng bo'lsa — birinchisi) va gapdagi **unli harflar** (`a o i u e`) sonini uch qatorda chiqarsin. `men python yozaman` → `3`, `yozaman`, `5`.", section='assessment', points=10, difficulty='medium',
              tests=[T('output_equals', "3\nyozaman\n5", "men python yozaman", stdin="men python yozaman\n"), T('output_equals', "1\nsalom\n2", "salom", stdin="salom\n"), T('output_equals', "2\nkitob\n3", "bu kitob (bu=u, kitob=i,o)", stdin="bu kitob\n", hidden=True)],
              hint="`gap.split()` so'zlarni ajratadi.", partial_solution='gap = input()\nsozlar = gap.split()\nprint(len(sozlar))\n# eng uzun so\'z va unlilar sonini chiqaring\n', full_solution='gap = input()\nsozlar = gap.split()\nprint(len(sozlar))\neng = sozlar[0]\nfor s in sozlar:\n    if len(s) > len(eng):\n        eng = s\nprint(eng)\nn = 0\nfor h in gap:\n    if h in "aoiue":\n        n = n + 1\nprint(n)\n', explanation="Matn, sikl, shart, list."),
    code_task('f_c2', "Amaliy: dictionary va funksiya", "`chastota(matn)` funksiyasi matndagi har bir **so'zning** necha marta uchrashini dictionary sifatida qaytarsin (so'zlar kichik harfga o'tkaziladi). `chastota(\"A b a\")` → `{'a': 2, 'b': 1}`.", section='assessment', points=10, difficulty='hard',
              tests=[T('output_equals', "{'a': 2, 'b': 1}\n{}\n{'x': 3}", "Natija", harness='print(chastota("A b a"))\nprint(chastota(""))\nprint(chastota("x X x"))')],
              hint="`split()`, `lower()` va `get(so_z, 0) + 1`.", full_solution='def chastota(matn):\n    natija = {}\n    for s in matn.lower().split():\n        natija[s] = natija.get(s, 0) + 1\n    return natija\n', explanation="Funksiya + dictionary + matn metodlari."),
    code_task('f_c3', "Amaliy: himoyalangan fayl o'qish", "`kiritilgan_ballar()` — foydalanuvchi 3 ta ball kiritadi; ularni `ballar.json` ga (list sifatida) yozib, fayldan qayta o'qib o'rtachani **2 xonali** chiqarsin. Son bo'lmagan qiymat bo'lsa `Xato: faqat son` chiqarib to'xtasin. `4`,`5`,`3` → `4.00`; `4`,`a`,`3` → `Xato: faqat son`.", section='assessment', points=12, difficulty='hard',
              tests=[T('output_equals', "4.00", "4 5 3", stdin="4\n5\n3\n"), T('output_equals', "Xato: faqat son", "4 a 3", stdin="4\na\n3\n"), T('output_equals', "2.67", "2 3 3", stdin="2\n3\n3\n", hidden=True), T('code_contains', 'json', "`json` ishlatilgan")],
              hint="`try` ichida `int(input())` ni 3 marta; `json.dump`/`json.load`.", partial_solution='import json\n\ntry:\n    ballar = [int(input()), int(input()), int(input())]\nexcept ValueError:\n    print("Xato: faqat son")\nelse:\n    with open("ballar.json", "w", encoding="utf-8") as f:\n        json.dump(ballar, f)\n    # fayldan o\'qib o\'rtachani chiqaring\n', full_solution='import json\n\ntry:\n    ballar = [int(input()), int(input()), int(input())]\nexcept ValueError:\n    print("Xato: faqat son")\nelse:\n    with open("ballar.json", "w", encoding="utf-8") as f:\n        json.dump(ballar, f)\n    with open("ballar.json", "r", encoding="utf-8") as f:\n        y = json.load(f)\n    print(f"{sum(y) / len(y):.2f}")\n', explanation="try/except/else, list, json, f-string — butun kurs."),
], pass_percent=70)

REVIEWS = [FINAL_REVIEW]
