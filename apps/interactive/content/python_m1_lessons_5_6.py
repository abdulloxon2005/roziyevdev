"""Python — 0 dan boshlash · 1-modul · 5–6-darslar va modul yakuniy nazorati."""
from .builders import T, callout, code_task, example, exercise, fill, fix_task, multiple, opt, predict, single, text

# ==============================================================================
# 5-DARS. Xato nima? Birinchi xato xabarini o'qish
# ==============================================================================
LESSON_5 = {
    'order': 5,
    'title': "Xato nima? Birinchi xato xabarini o'qish",
    'duration': 14,
    'objective': "Xatolardan qo'rqmaslik, Python xato xabari (traceback) tuzilishini o'qiy olish, "
                 "SyntaxError, NameError va IndentationError ni farqlash va ularni mustaqil tuzatish.",
    'concepts': ["Xato (bug)", "Traceback — xato xabari", "SyntaxError", "NameError", "IndentationError", "Xatoni tuzatish (debugging)"],
    'blocks': [
        text(r"""
Dasturchilar har kuni xato qiladi — bu mutlaqo normal holat. Hatto tajribali dasturchining kodi ham
birinchi urinishda kamdan-kam ishlaydi. Dasturdagi xato inglizcha **bug** (qo'ng'iz) deb ataladi,
xatoni topib tuzatish esa **debugging** deyiladi.

Muhimi — xato xabaridan qo'rqmaslik va uni **o'qishni** o'rganish. Python xato haqida juda
foydali ma'lumot beradi: **qayerda**, **qanday** xato va ko'pincha **nima uchun**.
""", title="Xato — o'rganishning bir qismi"),
        callout('analogy', r"""
Xato xabari — **shifokor tashxisiga** o'xshaydi. Shifokor "qayeringiz og'riyapti?" deb so'rab,
aniq joyni va kasallik nomini aytadi. Python ham xuddi shunday: **qaysi qatorda** (joy) va
**qanday xato** (tashxis) ekanini aytadi. Tashxisni o'qimasdan davolab bo'lmaydi.
""", title="Hayotiy o'xshatish: shifokor"),
        text(r"""
Quyidagi kodda bitta xato bor:

```python
print("Salom")
print("Dunyo)
```

Python shunday xabar beradi:

```text
  File "main.py", line 2
    print("Dunyo)
          ^
SyntaxError: unterminated string literal (detected at line 2)
```

Uni **pastdan yuqoriga** o'qing:

1. **Oxirgi qator** — xato turi va izohi: `SyntaxError` — yozilish qoidasi buzilgan; *unterminated string literal* — "matn yopilmagan".
2. **`line 2`** — xato 2-qatorda.
3. **`^` belgisi** — xato taxminan qayerdaligini ko'rsatadi.

Demak: 2-qatordagi qo'shtirnoq yopilmagan. Tuzatish: `print("Dunyo")`.
""", title="Xato xabarini (traceback) o'qish"),
        callout('tip', r"""
Bu platformada xato chiqqanda muharrir xatoli qatorni **qizil rang** bilan belgilaydi va
o'zbek tilida **izoh** beradi. Lekin asl Python xabarini o'qishni ham odat qiling — haqiqiy
loyihalarda u sizning asosiy yordamchingiz bo'ladi.
"""),
        text(r"""
| Xato turi | Qachon chiqadi | Misol | Tuzatish |
|---|---|---|---|
| `SyntaxError` | Yozilish qoidasi buzilgan: qavs/qo'shtirnoq yopilmagan | `print("Salom"` | `print("Salom")` |
| `NameError` | Python bu nomni tanimaydi | `Print("Salom")` yoki `print(Salom)` | `print("Salom")` |
| `IndentationError` | Satr boshida ortiqcha yoki noto'g'ri bo'sh joy | `  print("Salom")` | `print("Salom")` |

`SyntaxError` va `IndentationError` da Python kodni **umuman ishga tushirmaydi**. `NameError` esa dastur
ishlayotganda, xato qatorga yetganda chiqadi — undan oldingi qatorlar bajarilib ulguradi.
""", title="Eng ko'p uchraydigan 3 xato"),
        example(r'''
print("Bu qator bajariladi")
print(salom)
print("Bu qatorga navbat yetmaydi")
''', title="NameError: dastur yarim yo'lda to'xtaydi", body=r"""
Ishga tushiring: birinchi qator chiqadi, keyin 2-qatorda `NameError` paydo bo'ladi va dastur to'xtaydi.
`salom` qo'shtirnoqsiz yozilgani uchun Python uni matn emas, **nom** deb qidirdi va topa olmadi.
Qo'shtirnoq qo'shib tuzating va qayta ishga tushiring.
"""),
        example(r'''
print("Birinchi qator")
    print("Ikkinchi qator")
''', title="IndentationError: ortiqcha bo'sh joy", body=r"""
Ikkinchi qator boshida ortiqcha bo'sh joylar bor. Python'da satr boshidagi bo'sh joylar
(**chekinish**) muhim ahamiyatga ega — hozircha barcha qatorlarni chap chetdan boshlang.
"""),
        exercise('l5_inline_read'),
        text(r"""
Xatoni tuzatishning oddiy algoritmi:

1. Xato xabarining **oxirgi qatorini** o'qing — xato turi nima?
2. **Qator raqamini** toping (`line N`).
3. Shu qatorni diqqat bilan tekshiring: qavslar, qo'shtirnoqlar, harflar.
4. Bitta o'zgartirish kiriting va **qayta ishga tushiring**.
5. Yangi xato chiqsa — xavotir olmang, 1-qadamga qayting. Bu taraqqiyot belgisi!

Ba'zan xato ko'rsatilgan qatordan **oldingi** qatorda bo'ladi (masalan, oldingi qatorda qavs yopilmagan).
""", title="Xatoni tuzatish algoritmi"),
        callout('warning', r"""
Uchinchi tur xatolar ham bor — **mantiqiy xatolar**. Dastur xatosiz ishlaydi, lekin noto'g'ri
natija beradi (masalan, `print("2 + 2 = 5")`). Python ularni topa olmaydi — ularni **testlar** va
diqqatli tekshirish topadi. Shuning uchun bu kursda vazifalaringiz avtomatik testlar bilan tekshiriladi.
""", title="Mantiqiy xatolar"),
        exercise('l5_inline_fix'),
    ],
    'tasks': [
        single('l5_inline_read', "Xabarni o'qing", r"""
Quyidagi xato xabarini o'qing. Xato **qaysi qatorda** va **qanday turdagi**?

```text
Traceback (most recent call last):
  File "main.py", line 3, in <module>
    Print("Natija")
NameError: name 'Print' is not defined. Did you mean: 'print'?
```
""", section='inline', options=[
            opt("1-qatorda, SyntaxError", False, "Qator raqamini `line ...` dan qidiring."),
            opt("3-qatorda, NameError", True),
            opt("3-qatorda, SyntaxError", False, "Xato turi — oxirgi qatorning boshida."),
        ], hint="Oxirgi qator — xato turi; `line N` — qator raqami.",
            explanation="`line 3` va `NameError`: Python `Print` nomini tanimadi. Hatto tuzatishni ham taklif qilgan: *Did you mean: 'print'?*"),
        fix_task('l5_inline_fix', "Qo'shtirnoqni tuzating", r"""
Kodni ishga tushiring, xato xabarini o'qing va tuzating. Natija: `Xatoni topdim!`
""", section='inline', points=2, starter_code='print("Xatoni topdim!)\n',
            tests=[T('output_equals', "Xatoni topdim!", "To'g'ri natija chiqadi")],
            hint="Xabar: unterminated string literal — matn yopilmagan.",
            full_solution='print("Xatoni topdim!")\n',
            explanation="Ochilgan qo'shtirnoq yopilishi shart."),

        single('l5_quiz_1', "SyntaxError sababi", "Qaysi kod `SyntaxError` beradi?", options=[
            opt('`print("Salom")`', False, "Bu to'g'ri kod."),
            opt('`print("Salom"`', True),
            opt('`print(Salom)`', False, "Bu `NameError` beradi — sintaksis to'g'ri, lekin `Salom` nomi yo'q."),
        ], hint="Qaysi kodda qavs yopilmagan?", explanation="Yopilmagan qavs — yozilish qoidasi buzilishi, ya'ni `SyntaxError`."),
        single('l5_quiz_2', "Xabarni o'qish tartibi", "Python xato xabarini qayerdan o'qishni boshlash kerak?", options=[
            opt("Birinchi qatordan", False),
            opt("Oxirgi qatordan — u yerda xato turi va izohi", True),
            opt("O'rtadan", False),
        ], hint="Shifokor tashxisi qayerda yozilgan?", explanation="Oxirgi qator — xato turi va qisqa izoh; undan yuqorida joy (fayl va qator)."),
        predict('l5_quiz_3', "Xatogacha nima chiqadi?", r"""
Dastur 3-qatorda `NameError` bilan to'xtaydi. Xatogacha ekranga nima chiqadi? (Xato xabarini yozmang.)
""", code='print("Bir")\nprint("Ikki")\nprint(uch)\nprint("To\'rt")\n', answer="Bir\nIkki",
            hint="NameError dastur ishlayotganda chiqadi — undan oldingi qatorlar bajarilib ulguradi.",
            explanation="1 va 2-qatorlar bajariladi, 3-qatorda dastur to'xtaydi va 4-qator bajarilmaydi."),

        predict('l5_review_1', "Takrorlash: sep va end", r"""
4-darsni eslang. Dastur nima chiqaradi?
""", section='review', code='print("a", "b", sep="+", end="=")\nprint("ab")\n', answer="a+b=ab",
            hint="sep — orasiga, end — oxiriga.", explanation="`a+b` dan keyin `=` va yangi qator yo'q, so'ng `ab`."),

        fix_task('l5_assignment', "Uchta xatoni tuzating", r"""
Quyidagi dasturda **uchta** xato bor. Xato xabarlarini birma-bir o'qib, hammasini tuzating.
Tuzatilgan dastur aynan quyidagini chiqarishi kerak:

```
Salom!
Men xatolarni tuzatishni o'rganyapman.
Python — ajoyib til.
```

Har bir tuzatishdan keyin kodni ishga tushirib ko'ring — Python keyingi xatoni ko'rsatadi.
""", starter_code='Print("Salom!")\nprint("Men xatolarni tuzatishni o\'rganyapman."\n    print("Python — ajoyib til.")\n',
            expected_output_example="Salom!\nMen xatolarni tuzatishni o'rganyapman.\nPython — ajoyib til.",
            tests=[
                T('runs_ok', description="Dastur xatosiz ishlaydi", failure="Hali xato bor — xabarning oxirgi qatorini o'qing."),
                T('output_equals', "Salom!\nMen xatolarni tuzatishni o'rganyapman.\nPython — ajoyib til.", "Natija aynan mos"),
            ],
            hint="1) Katta harf bilan yozilgan funksiya. 2) Yopilmagan qavs. 3) Satr boshidagi ortiqcha bo'sh joy.",
            partial_solution='print("Salom!")\nprint("Men xatolarni tuzatishni o\'rganyapman."\n    print("Python — ajoyib til.")\n# 1-xato tuzatildi; qolgan ikkitasini toping\n',
            full_solution='print("Salom!")\nprint("Men xatolarni tuzatishni o\'rganyapman.")\nprint("Python — ajoyib til.")\n',
            explanation="`Print` → `print` (NameError), yopilmagan qavs (SyntaxError) va ortiqcha chekinish (IndentationError). Python xatolarni birma-bir ko'rsatadi — sabr bilan har birini tuzatish kerak."),

        single('l5_practice_easy', "Xato turini aniqlang", "`print(Salom)` qanday xato beradi?", section='practice', difficulty='easy', options=[
            opt("SyntaxError", False, "Sintaksis to'g'ri: qavslar joyida."),
            opt("NameError", True),
            opt("IndentationError", False),
        ], hint="Qo'shtirnoqsiz so'zni Python nom deb qidiradi.", explanation="`Salom` qo'shtirnoqsiz — Python uni o'zgaruvchi nomi deb qidiradi va topmaydi."),
        fix_task('l5_practice_medium', "Chiroyli qo'shtirnoqlar", r"""
Bu kod Telegram'dan nusxalangan va ishlamayapti. Tuzating, natija: `Assalomu alaykum`
""", section='practice', difficulty='medium', points=5, starter_code='print(“Assalomu alaykum”)\n',
            tests=[T('output_equals', "Assalomu alaykum", "To'g'ri natija")],
            hint="“ ” — bu Python tushunmaydigan «chiroyli» qo'shtirnoqlar. Oddiy \" bilan almashtiring.",
            full_solution='print("Assalomu alaykum")\n',
            explanation="Python faqat klaviaturadagi oddiy `\"` va `'` qo'shtirnoqlarni tushunadi."),
        fix_task('l5_practice_hard', "Mantiqiy xato", r"""
Dastur xatosiz ishlaydi, lekin **natijasi noto'g'ri**. Python bu xatoni topmaydi — siz topasiz!
Natija aynan bo'lishi kerak:

```
2 + 2 = 4
10 - 3 = 7
```
""", section='practice', difficulty='hard', points=5, starter_code='print("2 + 2 =", 2 + 2)\nprint("10 - 3 =", 10 + 3)\n',
            tests=[T('output_equals', "2 + 2 = 4\n10 - 3 = 7", "Natija to'g'ri")],
            hint="Ikkinchi qatordagi hisob amalini matndagi amal bilan solishtiring.",
            full_solution='print("2 + 2 =", 2 + 2)\nprint("10 - 3 =", 10 - 3)\n',
            explanation="Mantiqiy xato: matnda ayirish, hisobda qo'shish. Bunday xatolarni faqat natijani tekshirish orqali topish mumkin."),
    ],
}


# ==============================================================================
# 6-DARS. Izohlar (#) va toza kod yozish odati
# ==============================================================================
LESSON_6 = {
    'order': 6,
    'title': "Izohlar (#) va toza kod yozish odati",
    'duration': 13,
    'objective': "Kodga izoh (#) yozish, izoh yordamida kod qatorini vaqtincha o'chirish va PEP 8 asosidagi "
                 "toza kod yozish odatlarini (bo'sh joylar, bo'sh qatorlar, tushunarli tuzilish) shakllantirish.",
    'concepts': ["Izoh (#)", "Qator oxiridagi izoh", "Kodni vaqtincha o'chirish", "PEP 8", "O'qilishi oson kod"],
    'blocks': [
        text(r"""
**Izoh** (inglizcha *comment*) — kod ichidagi odamlar uchun yozilgan eslatma. Python izohlarni
**butunlay e'tiborsiz qoldiradi** — ular natijaga ta'sir qilmaydi.

Python'da izoh `#` (panjara) belgisidan boshlanadi va qator oxirigacha davom etadi:

```python
# Bu izoh — Python uni o'qimaydi
print("Salom")  # bu ham izoh: qator oxirida
```
""", title="Izoh nima?"),
        callout('analogy', r"""
Izoh — **darslik chetidagi qalam bilan yozilgan eslatma**. Kitob matni o'zgarmaydi, lekin eslatma
keyinroq sizga (yoki boshqa o'quvchiga) nima muhimligini tushuntiradi. Bir oydan keyin o'z kodingizni
o'qiganingizda izohlarga rahmat aytasiz.
""", title="Hayotiy o'xshatish: kitob chetidagi eslatma"),
        example(r'''
# Dastur: o'zim haqimda qisqa ma'lumot
# Muallif: o'quvchi

print("Ismim: Ali")      # ism
print("Yoshim: 16")      # yosh
# print("Bu qator bajarilmaydi")
print("Shahrim: Buxoro")
''', title="Izohlar amalda", body=r"""
Ishga tushiring: `#` bilan boshlangan qatorlar natijada ko'rinmaydi. Oxiridan oldingi qatordagi `#` ni
o'chirib, qayta ishga tushiring — endi u qator ham bajariladi.
"""),
        text(r"""
Izohlar uch xil maqsadda ishlatiladi:

1. **Tushuntirish** — kod *nima uchun* shunday yozilganini aytish.
2. **Bo'limlarga ajratish** — uzun dasturda qismlarni belgilash: `# --- Hisob-kitob ---`.
3. **Vaqtincha o'chirish** — qatorni o'chirmasdan, oldiga `#` qo'yib bajarilmaydigan qilish.
   Bu xato qidirishda juda qulay.

Yaxshi izoh **"nima uchun"** degan savolga javob beradi. `print("Salom")  # salom chiqaradi` kabi izoh
foydasiz — kodning o'zi buni aytib turibdi.
""", title="Izohlar nima uchun kerak?"),
        exercise('l6_inline_comment'),
        text(r"""
Kod faqat kompyuter uchun emas, **odamlar uchun** ham yoziladi. Python hamjamiyatida kodni
qanday yozish bo'yicha umumiy qoidalar bor — **PEP 8**. Eng asosiylari:

| Qoida | Yaxshi ✅ | Yomon ❌ |
|---|---|---|
| Vergul**dan keyin** bo'sh joy | `print("a", "b")` | `print("a","b")` |
| Qavs ichida chetlarda bo'sh joy yo'q | `print("Salom")` | `print( "Salom" )` |
| Funksiya nomi va qavs yopishgan | `print("Salom")` | `print ("Salom")` |
| `=` atrofida (parametrda) bo'sh joy yo'q | `sep="-"` | `sep = "-"` |
| `#` dan keyin bitta bo'sh joy | `# izoh` | `#izoh` |
| Mantiqiy qismlar orasida bo'sh qator | bloklar ajratilgan | hammasi bir yaxlit |
""", title="Toza kod: PEP 8 asoslari"),
        example(r'''
# --- Sarlavha ---
print("=== Do'kon cheki ===")

# --- Mahsulotlar ---
print("Non", 4000, sep="\t")
print("Sut", 12000, sep="\t")

# --- Yakun ---
print("Rahmat!")
''', title="Toza, o'qilishi oson kod", body=r"""
Izohlar va bo'sh qatorlar dasturni uchta aniq qismga ajratdi. Natija o'zgarmagan, lekin kodni
o'qish ancha oson.
"""),
        callout('important', r"""
Toza kod odati — boshidanoq shakllanadi. Hozir oddiy dasturlarda to'g'ri yozishga o'rganib olsangiz,
katta loyihalarda bu sizga va jamoangizga soatlab vaqt tejaydi.
"""),
        exercise('l6_inline_clean'),
    ],
    'tasks': [
        predict('l6_inline_comment', "Izohli kod natijasi", "Dastur nima chiqaradi?",
                code='# print("A")\nprint("B")  # print("C")\nprint("D")\n', answer="B\nD", section='inline',
                hint="# dan keyingi hamma narsa — izoh, hatto u yerda print bo'lsa ham.",
                explanation="1-qator butunlay izoh; 2-qatorda faqat `print(\"B\")` bajariladi, qolgani izoh."),
        single('l6_inline_clean', "Qaysi kod toza?", "PEP 8 bo'yicha qaysi qator **to'g'ri** yozilgan?", section='inline', options=[
            opt('`print ("Salom","dunyo")`', False, "Funksiya va qavs orasida bo'sh joy, vergul'dan keyin bo'sh joy yo'q."),
            opt('`print("Salom", "dunyo", sep="-")`', True),
            opt('`print( "Salom", "dunyo", sep = "-" )`', False, "Qavs ichidagi chetki va `=` atrofidagi bo'sh joylar ortiqcha."),
        ], hint="Jadvaldagi qoidalarni solishtiring.", explanation="Vergul'dan keyin bo'sh joy, qavs ichida chetki bo'sh joy yo'q, `sep=\"-\"` bo'sh joysiz."),

        single('l6_quiz_1', "Izoh belgisi", "Python'da bir qatorli izoh qaysi belgi bilan boshlanadi?", options=[
            opt("`//`", False, "Bu JavaScript, C++ kabi tillarda."),
            opt("`#`", True),
            opt("`--`", False, "Bu SQL tilida."),
            opt("`<!--`", False, "Bu HTML'da."),
        ], hint="Panjara belgisi.", explanation="Python'da izoh `#` bilan boshlanadi."),
        multiple('l6_quiz_2', "Izohning vazifalari", "Izohlar nima uchun ishlatiladi? Barchasini belgilang.", options=[
            opt("Kod nima uchun shunday yozilganini tushuntirish", True),
            opt("Kodni vaqtincha o'chirib qo'yish", True),
            opt("Dastur tezligini oshirish", False, "Izohlar tezlikka ta'sir qilmaydi."),
            opt("Dasturni bo'limlarga ajratish", True),
        ], hint="Darsda uchta maqsad sanab o'tilgan.", explanation="Tushuntirish, bo'limlarga ajratish va vaqtincha o'chirish."),
        predict('l6_quiz_3', "Qator oxiridagi izoh", "Natijani yozing:", code='print("Python", end="!")  # end — oxiriga\nprint()\n',
                answer="Python!", hint="Izoh natijaga ta'sir qilmaydi.",
                explanation="`end=\"!\"` oxiriga undov qo'yadi, keyingi bo'sh `print()` faqat qatorni yakunlaydi."),

        fix_task('l6_review_1', "Takrorlash: NameError", r"""
5-darsni eslang. Kod xato beryapti — tuzating. Natija: `Takrorlash — bilim onasi`
""", section='review', points=2, starter_code='print(Takrorlash — bilim onasi)\n',
            tests=[T('output_equals', "Takrorlash — bilim onasi", "To'g'ri natija")],
            hint="Matn qanday belgilar ichida yozilishi kerak edi?",
            full_solution='print("Takrorlash — bilim onasi")\n',
            explanation="Matn qo'shtirnoqsiz bo'lsa, Python uni nom sifatida tushunadi va xato beradi."),

        code_task('l6_assignment', "Tartibsiz kodni tozalang", r"""
Muharrirdagi dastur **ishlaydi**, lekin juda tartibsiz yozilgan. Uni PEP 8 qoidalari bo'yicha tozalang.

**Talablar:**

1. Dastur natijasi **o'zgarmasin** (avtomatik tekshiriladi).
2. Kamida **2 ta** mazmunli izoh (`#`) qo'shing — masalan, bo'limlar nomi.
3. `print` va `(` orasida bo'sh joy bo'lmasin; qavs ichida chetki bo'sh joylar bo'lmasin.
4. Har bir vergul'dan keyin bitta bo'sh joy bo'lsin.
5. `sep` va `end` dagi `=` atrofida bo'sh joy bo'lmasin.
""", starter_code='print ( "=== Mening kunim ===" )\nprint("Uyg\'onish:","07:00",sep = " ")\nprint( "Dars:","08:30" )\nprint("Sport:","17:00",end = "\\n")\n',
            expected_output_example="=== Mening kunim ===\nUyg'onish: 07:00\nDars: 08:30\nSport: 17:00",
            tests=[
                T('output_equals', "=== Mening kunim ===\nUyg'onish: 07:00\nDars: 08:30\nSport: 17:00", "Natija o'zgarmagan",
                  failure="Natija asl dasturnikidan farq qilmoqda. Matnlarni o'zgartirmang."),
                T('code_regex', r"(?s)#[^\n]*\S[^\n]*\n.*#[^\n]*\S", "Kamida 2 ta izoh bor",
                  failure="Kamida ikkita # bilan boshlanadigan mazmunli izoh qo'shing (alohida qatorlarda)."),
                T('code_not_contains', 'print (', "«print (» — funksiya va qavs orasida bo'sh joy yo'q"),
                T('code_not_contains', '( ', "Qavs ochilgandan keyin ortiqcha bo'sh joy yo'q"),
                T('code_not_contains', ' )', "Qavs yopilishidan oldin ortiqcha bo'sh joy yo'q"),
                T('code_regex', r'(?s)\A(?!.*,["\d]).*\Z', "Vergul'dan keyin bo'sh joy bor",
                  failure='Har bir verguldan keyin bitta bo\'sh joy qo\'ying: "a", "b"'),
                T('code_regex', r'(?s)\A(?!.*(sep|end) =)(?!.*(sep|end)= ).*\Z', "sep/end da = atrofida bo'sh joy yo'q",
                  failure='sep = " " emas, sep=" " deb yozing.'),
            ],
            hint="Avval natijani eslab qoling (ishga tushiring). Keyin har bir qatorni jadvaldagi qoidalar bo'yicha qayta yozing va tepasiga # izoh qo'shing.",
            partial_solution='# Sarlavha\nprint("=== Mening kunim ===")\n\n# Kun tartibi\nprint("Uyg\'onish:", "07:00", sep=" ")\n# qolgan qatorlarni ham shunday tozalang\n',
            full_solution='# Sarlavha\nprint("=== Mening kunim ===")\n\n# Kun tartibi\nprint("Uyg\'onish:", "07:00", sep=" ")\nprint("Dars:", "08:30")\nprint("Sport:", "17:00", end="\\n")\n',
            explanation="Toza kod natijani o'zgartirmaydi, lekin o'qishni osonlashtiradi. Izohlar dastur qismlarini tushuntiradi."),

        predict('l6_practice_easy', "Hammasi izoh", "Dastur nima chiqaradi? (Agar hech narsa chiqmasa, `bo'sh` deb yozing.)",
                code='print("Ko\'rinadi")\n# print("Ko\'rinmaydi")\n', answer="Ko'rinadi", section='practice', difficulty='easy',
                hint="Ikkinchi qator — izoh.", explanation="Faqat birinchi qator bajariladi."),
        fix_task('l6_practice_medium', "Qatorni o'chiring (izoh bilan)", r"""
Dastur ortiqcha qator chiqaryapti. **Hech bir qatorni o'chirmasdan**, faqat `#` qo'yib, natijani
quyidagicha qiling:

```
Bir
Uch
```
""", section='practice', difficulty='medium', points=5, starter_code='print("Bir")\nprint("Ikki")\nprint("Uch")\n',
            tests=[
                T('output_equals', "Bir\nUch", "Natija «Bir» va «Uch»"),
                T('code_contains', 'Ikki', "«Ikki» qatori o'chirilmagan, faqat izohga aylantirilgan",
                  failure="Qatorni o'chirmang — oldiga # qo'ying."),
            ],
            hint="Ikkinchi qator boshiga # qo'ying.", full_solution='print("Bir")\n# print("Ikki")\nprint("Uch")\n',
            explanation="Izoh bilan «vaqtincha o'chirish» — kodni yo'qotmasdan sinab ko'rishning qulay usuli."),
        code_task('l6_practice_hard', "Bo'limlarga ajratilgan dastur", r"""
Uch bo'limli dastur yozing. Har bir bo'lim oldida `# ---` bilan boshlanadigan izoh bo'lsin
(jami **kamida 3 ta** shunday izoh), bo'limlar orasida bo'sh qator qoldiring. Natija aynan:

```
Kitob: O'tkan kunlar
Muallif: Abdulla Qodiriy
Janr: roman
```
""", section='practice', difficulty='hard', points=5,
            tests=[
                T('output_equals', "Kitob: O'tkan kunlar\nMuallif: Abdulla Qodiriy\nJanr: roman", "Natija aynan mos"),
                T('code_regex', r"(?s)# ---.*# ---.*# ---", "Kamida 3 ta «# ---» bo'lim izohi"),
            ],
            hint="Har bir print oldiga # --- Bo'lim nomi --- kabi izoh yozing.",
            full_solution='# --- Nomi ---\nprint("Kitob: O\'tkan kunlar")\n\n# --- Muallif ---\nprint("Muallif: Abdulla Qodiriy")\n\n# --- Janr ---\nprint("Janr: roman")\n',
            explanation="Bo'lim izohlari uzun dasturlarda navigatsiyani osonlashtiradi."),
    ],
}


# ==============================================================================
# 1-MODUL YAKUNIY NAZORATI
# ==============================================================================
ASSESSMENT = {
    'title': "1-modul yakuniy nazorati: Birinchi qadamlar",
    'description': r"""
Modulda o'rganilgan barcha mavzular bo'yicha nazorat: algoritm, Python, `print()` imkoniyatlari,
xatolar va izohlar. **5 ta nazariy savol, 3 ta natijani aniqlash, 2 ta xatoni tuzatish** va
**mini-loyiha** — o'zingiz haqingizdagi vizitka dasturi.

O'tish mezoni — **70%**. Natija yetmasa, xatolarni ko'rib chiqib qayta topshirishingiz mumkin.
""",
    'pass_percent': 70,
    'tasks': [
        single('m1_a_theory_1', "Algoritm", "Algoritm qanday bo'lishi kerak?", section='assessment', points=2, options=[
            opt("Aniq, ketma-ket va yakunlanadigan", True),
            opt("Uzun va murakkab", False),
            opt("Faqat matematik formulalardan iborat", False),
            opt("Ixtiyoriy tartibda bajariladigan", False),
        ], explanation="Algoritmning uch asosiy xususiyati: aniqlik, ketma-ketlik, yakun.", hint="1-darsni eslang."),
        single('m1_a_theory_2', "Interpretator", "Python interpretatori kodni qanday bajaradi?", section='assessment', points=2, options=[
            opt("Yuqoridan pastga, qatorma-qator", True),
            opt("Avval oxirgi qatorni", False),
            opt("Faqat izohlarni", False),
        ], explanation="Interpretator kodni qatorma-qator, yuqoridan pastga bajaradi.", hint="2-dars."),
        multiple('m1_a_theory_3', "To'g'ri print qatorlari", "Qaysi qatorlar **xatosiz** ishlaydi?", section='assessment', points=2, options=[
            opt('`print("Salom")`', True),
            opt("`print('Salom')`", True),
            opt('`Print("Salom")`', False),
            opt('`print("Salom\')`', False),
        ], explanation="Ikkala qo'shtirnoq turi ham to'g'ri, lekin bir xil turdagisi bilan yopilishi kerak; `Print` — xato.", hint="3-dars."),
        single('m1_a_theory_4', "end parametri", '`print("A", end="")` dan keyin `print("B")` nima chiqaradi?', section='assessment', points=2, options=[
            opt("`AB`", True),
            opt("`A B`", False),
            opt("`A` va `B` alohida qatorlarda", False),
        ], explanation='`end=""` yangi qatorni olib tashlaydi — `A` va `B` yopishib chiqadi.', hint="4-dars."),
        single('m1_a_theory_5', "Izoh", "Quyidagilardan qaysi biri izoh haqida **to'g'ri**?", section='assessment', points=2, options=[
            opt("Izoh dastur natijasini o'zgartiradi", False),
            opt("Python `#` dan keyingi matnni e'tiborsiz qoldiradi", True),
            opt("Izoh faqat qator boshida bo'lishi mumkin", False, "Qator oxirida ham bo'ladi."),
        ], explanation="Izoh — odamlar uchun; Python uni bajarmaydi.", hint="6-dars."),

        predict('m1_a_predict_1', "Natijani aniqlang (1)", "Dastur nima chiqaradi?", section='assessment', points=2,
                code='print("Kod", "yoz", sep="-", end="!")\nprint()\n', answer="Kod-yoz!",
                explanation="`sep=\"-\"` orasiga chiziqcha, `end=\"!\"` oxiriga undov qo'yadi."),
        predict('m1_a_predict_2', "Natijani aniqlang (2)", "Dastur nima chiqaradi?", section='assessment', points=2,
                code='print(3 + 4)\nprint("3 + 4")\n# print(10)\n', answer="7\n3 + 4",
                explanation="Birinchi qator hisoblanadi, ikkinchisi — matn, uchinchisi — izoh."),
        predict('m1_a_predict_3', "Natijani aniqlang (3)", "Dastur nima chiqaradi? Har bir qatorni alohida yozing.",
                section='assessment', points=2, code='print("Salom\\ndunyo")\nprint(1, 2, 3, sep="")\n', answer="Salom\ndunyo\n123",
                explanation="`\\n` yangi qator yaratadi; `sep=\"\"` raqamlarni yopishtiradi."),

        fix_task('m1_a_fix_1', "Xatoni tuzating (1)", r"""
Dastur `Python 2026` ni chiqarishi kerak, lekin xato beryapti. Tuzating.
""", section='assessment', points=4, starter_code='print("Python", 2026\n',
            tests=[T('output_equals', "Python 2026", "Natija «Python 2026»")],
            hint="Qavslarni sanang.", full_solution='print("Python", 2026)\n',
            explanation="Yopilmagan qavs — SyntaxError."),
        fix_task('m1_a_fix_2', "Xatoni tuzating (2)", r"""
Dastur ikki qator chiqarishi kerak:

```
Ism: Ali
Shahar: Samarqand
```
""", section='assessment', points=4, starter_code='print("Ism:", Ali)\n  print("Shahar: Samarqand")\n',
            tests=[T('output_equals', "Ism: Ali\nShahar: Samarqand", "Natija aynan mos")],
            hint="Ikkita xato: qo'shtirnoqsiz so'z va satr boshidagi ortiqcha bo'sh joy.",
            full_solution='print("Ism:", "Ali")\nprint("Shahar: Samarqand")\n',
            explanation="`Ali` qo'shtirnoqsiz — NameError; ikkinchi qatordagi chekinish — IndentationError."),

        code_task('m1_a_project', "Mini-loyiha: O'zim haqimda vizitka", r"""
O'zingiz haqingizda **vizitka** chiqaradigan dastur yozing. Bu loyiha modulda o'rgangan hamma narsani birlashtiradi.

**Talablar (avtomatik tekshiriladi):**

1. Vizitka **ramka** bilan boshlanib, ramka bilan tugasin: birinchi va oxirgi qator kamida 10 ta
   `=`, `-` yoki `*` belgisidan iborat bo'lsin.
2. Quyidagi qatorlar bo'lsin (har biri alohida qatorda, ikki nuqtadan keyin qiymat):
   `Ism: ...`, `Yosh: ...` (raqam bilan), `Shahar: ...`.
3. Jami kamida **7 qator**.
4. Kodda `sep`, `end` yoki `\t` dan **kamida bittasi** ishlatilsin.
5. Kodda kamida **bitta izoh** (`#`) bo'lsin.

Ma'lumotlarni o'zingiznikiga almashtiring — vizitka sizniki!
""", section='project', points=15, difficulty='medium', unlock=3,
            starter_code='# Mening vizitkam\nprint("==============================")\n\n',
            expected_output_example="==============================\n        VIZITKA\n==============================\nIsm: Aziza Karimova\nYosh: 16\nShahar: Toshkent\nQiziqishlarim: Python, kitob\nMaqsadim: dasturchi bo'lish\n==============================",
            tests=[
                T('runs_ok', description="Dastur xatosiz ishlaydi"),
                T('output_lines_min', '7', "Kamida 7 ta qator"),
                T('output_regex', r"\A[=*-]{10,}\s*$", "Birinchi qator — ramka (kamida 10 ta = - yoki *)"),
                T('output_regex', r"(?m)^[=*-]{10,}\s*\Z", "Oxirgi qator — ramka"),
                T('output_regex', r"(?m)^Ism:\s*\S+", "«Ism: ...» qatori bor"),
                T('output_regex', r"(?m)^Yosh:\s*\d+", "«Yosh: ...» qatori raqam bilan"),
                T('output_regex', r"(?m)^Shahar:\s*\S+", "«Shahar: ...» qatori bor"),
                T('code_regex', r"sep=|end=|\\t", r"Kodda sep, end yoki \t ishlatilgan"),
                T('code_regex', r"(?m)#\s*\S", "Kodda kamida bitta izoh bor"),
            ],
            hint="Avval qog'ozda vizitkangiz ko'rinishini chizing. Ramka uchun print(\"=\" ...) ni namunadagidek yozing, ma'lumotlarni print(\"Ism:\", \"...\") ko'rinishida chiqaring.",
            partial_solution='# Mening vizitkam\nprint("==============================")\nprint("\\tVIZITKA")\nprint("==============================")\nprint("Ism:", "...")\n# Yosh va Shahar qatorlarini qo\'shing, oxirida yana ramka\n',
            full_solution='# Mening vizitkam\nprint("==============================")\nprint("\\tVIZITKA")\nprint("==============================")\n\n# Shaxsiy ma\'lumotlar\nprint("Ism:", "Aziza Karimova")\nprint("Yosh:", 16)\nprint("Shahar:", "Toshkent")\nprint("Qiziqishlarim:", "Python", "kitob", sep=" ")\nprint("Maqsadim: dasturchi bo\'lish")\nprint("==============================")\n',
            explanation="Vizitka — `print`, matn/son, `sep`/`end`/`\\t`, izohlar va toza kod yozishning birlashmasi. Tabriklaymiz, siz birinchi to'liq dasturingizni yozdingiz!"),
    ],
}
