"""Python — 0 dan boshlash · 1-modul · 1–2-darslar."""
from .builders import T, callout, code_task, example, exercise, fill, multiple, opt, predict, single, text

# ==============================================================================
# 1-DARS. Dasturlash nima? Algoritm tushunchasi
# ==============================================================================
LESSON_1 = {
    'order': 1,
    'title': "Dasturlash nima? Algoritm tushunchasi",
    'duration': 12,
    'objective': "Dasturlash va algoritm nima ekanini tushunish, kundalik hayotdagi jarayonni aniq, "
                 "ketma-ket qadamlarga ajrata olish va birinchi tayyor dasturni ishga tushirib ko'rish.",
    'concepts': ["Dastur", "Dasturlash", "Algoritm", "Qadamlar ketma-ketligi", "Aniqlik"],
    'blocks': [
        text(r"""
Kompyuter juda tez ishlaydi — bir soniyada milliardlab amal bajaradi. Lekin u **o'zi o'ylay olmaydi**.
Kompyuter faqat unga aniq aytilgan ishni, aynan aytilgan tartibda bajaradi.

**Dastur** — kompyuter bajarishi kerak bo'lgan buyruqlar ro'yxati.
**Dasturlash** — ana shu buyruqlarni kompyuter tushunadigan tilda yozish jarayoni.

Telefoningizdagi kalkulyator, Telegram, o'yinlar, bank ilovasi — barchasi dasturlar. Ularni
odamlar yozgan, va siz ham shu kursda o'z dasturlaringizni yozishni o'rganasiz.
""", title="Dastur nima?"),
        callout('analogy', r"""
Tasavvur qiling, siz hech qachon oshxonaga kirmagan robotga **choy damlashni** o'rgatyapsiz.
"Choy damla" desangiz, robot hech narsa qilmaydi — u "choy damlash" nimaligini bilmaydi.
Unga har bir qadamni aytishingiz kerak: choynakni ol, suv quy, qaynat, piyolaga choy sol...
Kompyuter ham xuddi shu robotga o'xshaydi.
""", title="Hayotiy o'xshatish: robot-oshpaz"),
        text(r"""
**Algoritm** — biror masalani hal qilish uchun bajariladigan **aniq** va **ketma-ket** qadamlar.

Masalan, *choy damlash algoritmi*:

1. Choynakka suv quy.
2. Suvni qaynat.
3. Choynakka 1 qoshiq choy sol.
4. Ustidan qaynoq suv quy.
5. 5 daqiqa kut.
6. Piyolaga quy.

Algoritm yaxshi bo'lishi uchun uch shart muhim:

| Xususiyat | Ma'nosi | Yomon misol |
|---|---|---|
| **Aniqlik** | Har bir qadam faqat bitta ma'noni bildiradi | "Biroz choy sol" — qancha? |
| **Ketma-ketlik** | Qadamlar to'g'ri tartibda | Avval quyib, keyin qaynatish |
| **Yakun** | Algoritm albatta tugaydi | "Choy tayyor bo'lguncha kutaver" — qachon? |
""", title="Algoritm nima?"),
        callout('important', r"""
Dastur — bu kompyuter tilida yozilgan algoritm. Avval masalani **qadamlarga ajratishni** o'rganing,
keyin bu qadamlarni Python tilida yozish oson bo'ladi. Yaxshi dasturchi avval o'ylaydi, keyin yozadi.
"""),
        text(r"""
Kompyuter buyruqlarni **yuqoridan pastga**, birin-ketin bajaradi. Quyidagi misolda har bir qator —
bitta buyruq. Hozircha `print(...)` nima ekaniga e'tibor bermang (uni 3-darsda batafsil o'rganamiz),
shunchaki u qavs ichidagi matnni ekranga chiqaradi deb biling.

O'ngdagi (telefonda — pastdagi «Muharrir» tugmasi) kod muharririda misolni ishga tushirib ko'ring.
""", title="Kompyuter qadamlarni qanday bajaradi?"),
        example(r'''
print("1. Choynakka suv quy")
print("2. Suvni qaynat")
print("3. Choynakka choy sol")
print("4. Ustidan qaynoq suv quy")
print("5. 5 daqiqa kut")
print("6. Piyolaga quy")
''', title="Choy damlash algoritmi — dastur ko'rinishida", body=r"""
«Ishga tushirish» tugmasini bosing — natija oynasida qadamlar aynan yozilgan tartibda chiqadi.
Endi ikkita qatorning o'rnini almashtirib, qayta ishga tushiring: kompyuter **siz yozgan tartibni**
bajaradi, hatto u mantiqsiz bo'lsa ham.
"""),
        exercise('l1_inline_order'),
        text(r"""
Algoritmlar faqat oshxonada emas, hamma joyda:

- **Navigator** sizga yo'l ko'rsatadi: "200 metrdan keyin o'ngga buriling" — bu algoritm qadamlari.
- **Bankomat**: kartani qo'ying → PIN kiriting → summani tanlang → pulni oling.
- **Darslik masalasi**: avval shartni o'qing → ma'lumlarni yozing → formulani tanlang → hisoblang.

Har safar biror ishni "birinchi... keyin... oxirida..." deb tushuntirganingizda, siz algoritm tuzyapsiz.
""", title="Algoritmlar atrofimizda"),
        callout('tip', r"""
Algoritm yozishda o'zingizga savol bering: **"Buni hech narsa bilmaydigan robot tushunadimi?"**
Agar qadamda "taxminan", "biroz", "kerak bo'lsa" kabi noaniq so'zlar bo'lsa — uni aniqlashtiring.
"""),
        exercise('l1_inline_fill'),
    ],
    'tasks': [
        # ---- Dars ichidagi mashqlar ----
        single('l1_inline_order', "Qaysi tartib to'g'ri?", r"""
Quyidagi qadamlardan **to'g'ri tartiblangan** algoritmni tanlang: *"Telefonda qo'ng'iroq qilish"*.
""", section='inline', options=[
            opt("Raqamni terish → Telefonni ochish → Qo'ng'iroq tugmasini bosish", False,
                "Telefon ochilmasdan raqam terib bo'lmaydi — ketma-ketlik buzilgan."),
            opt("Telefonni ochish → Raqamni terish → Qo'ng'iroq tugmasini bosish", True),
            opt("Qo'ng'iroq tugmasini bosish → Raqamni terish → Telefonni ochish", False,
                "Qo'ng'iroq raqamsiz amalga oshmaydi."),
        ], hint="Har bir qadam oldingi qadam natijasiga tayanishi kerak. Birinchi navbatda nima qilinadi?",
            explanation="Algoritmda **ketma-ketlik** muhim: har bir qadam oldingisi bajarilgandan keyingina ma'noga ega bo'ladi."),
        fill('l1_inline_fill', "Algoritmni to'ldiring", r"""
Choy damlash dasturida 2-qadam tushib qolgan. Bo'sh joyga **qavs ichidagi matnni** yozing
(qo'shtirnoqlar allaqachon bor), shunda algoritm to'g'ri ishlaydi: *2. Suvni qaynat*.
""", snippet='print("1. Choynakka suv quy")\nprint("___")\nprint("3. Choynakka choy sol")\n',
            answers=["2. Suvni qaynat"],
            tests=[
                T('output_equals', "1. Choynakka suv quy\n2. Suvni qaynat\n3. Choynakka choy sol",
                  "Uchta qadam to'g'ri tartibda chiqadi"),
            ],
            hint="Qo'shtirnoq ichiga aynan «2. Suvni qaynat» matnini yozing.",
            explanation="Dastur qadamlarni yuqoridan pastga bajaradi, shuning uchun 2-qadam 1 va 3 orasida turishi kerak."),

        # ---- Nazariy test ----
        single('l1_quiz_1', "Algoritm ta'rifi", "**Algoritm** nima?", options=[
            opt("Kompyuterning ichki qismlari (protsessor, xotira)", False, "Bu kompyuterning apparat qismi (hardware)."),
            opt("Masalani hal qilish uchun aniq va ketma-ket qadamlar", True),
            opt("Faqat matematikaga oid formula", False, "Algoritm har qanday sohada bo'ladi: oshxonada ham, navigatorda ham."),
            opt("Internetdagi sayt", False),
        ], hint="Darsdagi choy damlash misolini eslang.",
            explanation="Algoritm — **aniq**, **ketma-ket** va **yakunlanadigan** qadamlar to'plami. Dastur — algoritmning kompyuter tilidagi ko'rinishi."),
        multiple('l1_quiz_2', "Yaxshi algoritm xususiyatlari", "Yaxshi algoritmga xos xususiyatlarni **barchasini** belgilang.", options=[
            opt("Har bir qadam aniq va bir ma'noli", True),
            opt("Qadamlar to'g'ri tartibda joylashgan", True),
            opt("Algoritm albatta yakunlanadi", True),
            opt("Qadamlarni ixtiyoriy tartibda bajarish mumkin", False, "Tartib buzilsa, natija ham buziladi."),
        ], hint="Darsdagi jadvalda uchta xususiyat ko'rsatilgan.",
            explanation="Uch asosiy xususiyat: **aniqlik**, **ketma-ketlik** va **yakun**."),
        single('l1_quiz_3', "Noaniq qadam", "Qaysi qadam robot uchun **noaniq**?", options=[
            opt("Choynakka 1 litr suv quy", False, "Bu aniq: miqdor ko'rsatilgan."),
            opt("Suvni 100 °C gacha qaynat", False, "Bu ham aniq."),
            opt("Choyni yetarlicha damla", True),
            opt("Piyolaga 200 ml choy quy", False),
        ], hint="Qaysi qadamda o'lchov yoki aniq vaqt yo'q?",
            explanation="«Yetarlicha» so'zi noaniq — robot qancha kutishni bilmaydi. To'g'risi: «5 daqiqa kut»."),

        # ---- Takrorlash ----
        single('l1_review_1', "Takrorlash: dastur nima?", r"""
Darsning boshida o'rgangan tushunchani eslang. **Dastur** — bu...
""", section='review', options=[
            opt("kompyuter bajaradigan buyruqlar ro'yxati", True),
            opt("kompyuterning ekrani", False),
            opt("faqat o'yinlar", False, "O'yinlar dasturning bir turi, lekin dastur tushunchasi kengroq."),
        ], hint="Kompyuter o'zi o'ylay olmaydi — unga nima beriladi?",
            explanation="Dastur — kompyuter tilida yozilgan algoritm, ya'ni buyruqlar ro'yxati."),

        # ---- Mustaqil vazifa ----
        code_task('l1_assignment', "Ertalabki tayyorgarlik algoritmi", r"""
Ertalab uyg'onganingizdan maktabga (yoki ishga) chiqqaningizgacha bo'lgan jarayonni
**kamida 5 qadamli algoritm** sifatida yozing.

**Talablar:**

1. Har bir qadam alohida qatorda chiqsin.
2. Har bir qadam raqam, nuqta va bo'sh joy bilan boshlansin: `1. `, `2. `, `3. ` ...
3. Raqamlar 1 dan boshlanib, ketma-ket kelsin.

Muharrirdagi namunadagi kabi har bir qadamni `print("...")` ichiga yozing — hozircha shu yetarli.
""", starter_code='''print("1. Uyg'onaman")
print("2. ...")
''',
            expected_output_example="1. Uyg'onaman\n2. Yuvinaman\n3. Nonushta qilaman\n4. Kiyinaman\n5. Uydan chiqaman",
            tests=[
                T('runs_ok', description="Dastur xatosiz ishlaydi"),
                T('output_lines_min', '5', "Kamida 5 ta qadam (qator) chiqadi",
                  failure="Qadamlar soni 5 tadan kam. Yana print(...) qatorlarini qo'shing."),
                T('output_regex', r"\A1\. \S.*\n2\. \S.*\n3\. \S.*\n4\. \S.*\n5\. \S", "Qadamlar «1. », «2. », ... ko'rinishida ketma-ket raqamlangan",
                  failure="Raqamlash: 1. 2. 3. 4. 5. — har biridan keyin nuqta va bo'sh joy, keyin qadam matni."),
                T('output_not_contains', '...', "Namunadagi «...» o'rniga haqiqiy qadam yozilgan",
                  failure="«...» o'rniga o'z qadamingizni yozing."),
            ],
            hint="Har bir qatorni namunadagidek yozing: print(\"3. Nonushta qilaman\"). Qo'shtirnoqlarni yopishni unutmang.",
            partial_solution='''print("1. Uyg'onaman")
print("2. Yuvinaman")
print("3. ...")  # davom ettiring
''',
            full_solution='''print("1. Uyg'onaman")
print("2. Yuvinaman")
print("3. Nonushta qilaman")
print("4. Kiyinaman")
print("5. Sumkamni olib, uydan chiqaman")
''',
            explanation="Har bir `print()` bitta qadamni alohida qatorga chiqaradi. Kompyuter ularni siz yozgan tartibda bajaradi — bu algoritmning ketma-ketligi."),

        # ---- Qo'shimcha mashqlar ----
        single('l1_practice_easy', "Algoritmmi yoki yo'qmi?", "Quyidagilardan qaysi biri **algoritm** hisoblanadi?",
               section='practice', difficulty='easy', options=[
                   opt("«Qizil rang chiroyli»", False, "Bu fikr, qadamlar emas."),
                   opt("«Eshikni och → ichkariga kir → eshikni yop»", True),
                   opt("«Ertaga havo yaxshi bo'ladi»", False, "Bu bashorat."),
               ], hint="Algoritmda harakatlar ketma-ketligi bo'ladi.",
               explanation="Faqat ikkinchi variantda aniq harakatlar ketma-ketligi bor."),
        predict('l1_practice_medium', "Tartibni kuzating", r"""
Dastur ekranga nima chiqaradi? Har bir qatorni alohida yozing.
""", code='print("Kiyinaman")\nprint("Uyg\'onaman")\nprint("Nonushta qilaman")\n',
            answer="Kiyinaman\nUyg'onaman\nNonushta qilaman",
            section='practice', difficulty='medium',
            hint="Kompyuter mantiqni tekshirmaydi — u qatorlarni yuqoridan pastga bajaradi.",
            explanation="Natija yozilgan tartibda chiqadi, hatto «uyg'onmasdan kiyinish» mantiqsiz bo'lsa ham. Shuning uchun algoritm tartibi dasturchining mas'uliyati."),
        code_task('l1_practice_hard', "Bankomatdan pul yechish", r"""
Bankomatdan pul yechish algoritmini **aynan 6 qadamda** yozing. Oxirgi qadam aynan
`6. Kartani qaytarib olaman` bo'lsin. Har bir qadam `N. ` bilan boshlansin.
""", section='practice', difficulty='hard', points=5,
            starter_code='print("1. Kartani bankomatga qo\'yaman")\n',
            tests=[
                T('runs_ok', description="Dastur xatosiz ishlaydi"),
                T('output_regex', r"\A1\. \S.*\n2\. \S.*\n3\. \S.*\n4\. \S.*\n5\. \S.*\n6\. Kartani qaytarib olaman\Z",
                  "Aynan 6 ta raqamlangan qadam, oxirgisi «6. Kartani qaytarib olaman»",
                  failure="Qadamlar soni aynan 6 ta bo'lsin va oxirgi qator so'zma-so'z mos kelsin."),
            ],
            hint="Avval qog'ozda qadamlarni yozing: karta, PIN, summa, tasdiqlash, pul, karta.",
            full_solution='''print("1. Kartani bankomatga qo'yaman")
print("2. PIN-kodni kiritaman")
print("3. Pul yechish bo'limini tanlayman")
print("4. Summani kiritaman")
print("5. Pulni olaman")
print("6. Kartani qaytarib olaman")
''',
            explanation="Aniq sonli qadamlar talab qilinganda har bir qadamni rejalashtirish muhim — bu algoritmik fikrlashning asosi."),
    ],
}


# ==============================================================================
# 2-DARS. Python nima va qayerlarda ishlatiladi?
# ==============================================================================
LESSON_2 = {
    'order': 2,
    'title': "Python nima va qayerlarda ishlatiladi?",
    'duration': 12,
    'objective': "Python dasturlash tili nima ekanini, uning afzalliklarini, qaysi sohalarda ishlatilishini "
                 "va Python kodni qanday bajarishini (interpretator) tushunish.",
    'concepts': ["Dasturlash tili", "Python", "Interpretator", "Qo'llanish sohalari", "Kod yuqoridan pastga bajariladi"],
    'blocks': [
        text(r"""
Kompyuter aslida faqat 0 va 1 lardan iborat **mashina tilini** tushunadi. Odam uchun bunday
tilda yozish juda qiyin. Shuning uchun odamlar **dasturlash tillarini** o'ylab topishgan — ular
odam tiliga yaqinroq, lekin kompyuterga tarjima qilinishi mumkin.

Dasturlash tillari ko'p: Python, JavaScript, Java, C++, Go... Har biri o'z vazifasiga mos.
Biz **Python** dan boshlaymiz, chunki u yangi boshlovchilar uchun eng qulay tillardan biri.
""", title="Dasturlash tili nima?"),
        text(r"""
**Python** — 1991-yilda gollandiyalik dasturchi **Gvido van Rossum** tomonidan yaratilgan
dasturlash tili. Nomi ilondan emas, britaniyalik "Monty Python" komediya shousidan olingan.

Python'ning asosiy afzalliklari:

- **Sodda sintaksis** — kod oddiy ingliz tiliga o'xshab o'qiladi.
- **Kam kod — ko'p ish** — boshqa tillarda 10 qator bo'ladigan narsa Python'da 2–3 qator.
- **Bepul va ochiq** — hamma foydalanishi va o'rganishi mumkin.
- **Ulkan hamjamiyat** — savolingizga javob deyarli har doim internetda bor.
- **Tayyor kutubxonalar** — minglab tayyor "asboblar" bilan murakkab ishlarni tez qilish mumkin.
""", title="Python bilan tanishuv"),
        callout('analogy', r"""
Dasturlash tilini **tarjimon** orqali gaplashishga o'xshatish mumkin. Siz o'zbekcha gapirasiz,
tarjimon esa gapingizni boshqa tilga o'giradi. Python'da bu tarjimon — **interpretator**: u siz yozgan
kodni qatorma-qator o'qib, kompyuterga tushunarli buyruqlarga aylantiradi va darhol bajaradi.
""", title="Hayotiy o'xshatish: tarjimon"),
        text(r"""
Bir xil vazifa — ekranga salom chiqarish — turli tillarda qanday yozilishini solishtiring.

**Java** tilida:

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Salom!");
    }
}
```

**Python** tilida:

```python
print("Salom!")
```

Python'da faqat bitta qator! Shuning uchun Python bilan **dasturlash g'oyalariga** tezroq e'tibor
qaratasiz, tilning murakkab qoidalariga emas.
""", title="Python nega oson?"),
        text(r"""
| Soha | Python bilan nima qilinadi | Misollar |
|---|---|---|
| Veb-dasturlash | Saytlarning server qismi | Instagram, Pinterest (Django) |
| Sun'iy intellekt | Neyron tarmoqlar, chat-botlar | ChatGPT kabi modellar o'qitilishi |
| Ma'lumotlar tahlili | Jadval va grafiklar, statistika | Bank va do'konlar hisobotlari |
| Avtomatlashtirish | Takroriy ishlarni dasturga topshirish | Fayllarni saralash, xabar yuborish |
| Telegram botlar | Avtomatik javob beruvchi botlar | Do'kon, test, ob-havo botlari |
| Ta'lim va fan | Hisob-kitob, modellashtirish | Universitet va laboratoriyalar |

Ya'ni Python'ni o'rganib, ko'plab yo'nalishlarga eshik ochasiz.
""", title="Python qayerlarda ishlatiladi?"),
        text(r"""
Python interpretatori kodni **yuqoridan pastga**, qatorma-qator bajaradi. Har bir qator
bajarilgach, keyingisiga o'tadi. Agar biror qatorda xato bo'lsa, dastur shu yerda to'xtaydi
(xatolarni 5-darsda batafsil o'rganamiz).
""", title="Python kodni qanday bajaradi?"),
        example(r'''
print("Python — bu dasturlash tili")
print("U 1991-yilda yaratilgan")
print("Uni Gvido van Rossum yaratgan")
''', title="Qatorma-qator bajarilish", body=r"""
Ishga tushiring va natija tartibini kuzating. So'ng uchinchi qatorni birinchi qator o'rniga
ko'chirib, qayta ishga tushiring.
"""),
        exercise('l2_inline_predict'),
        callout('tip', r"""
Bu kursdagi barcha kodlar serverdagi **xavfsiz, izolyatsiyalangan muhitda** bajariladi —
kompyuteringizga hech narsa o'rnatish shart emas. Keyinchalik Python'ni o'z kompyuteringizga
o'rnatib ([python.org](https://www.python.org)) xuddi shu kodlarni u yerda ham ishlata olasiz.
"""),
        example(r'''
print("Men Python o'rganyapman!")
print("Python bilan sayt, bot va o'yin yozish mumkin.")
''', title="O'zingiz sinab ko'ring", body=r"""
Muharrirga yuklang va qo'shtirnoq ichidagi matnni o'zingizniki bilan almashtiring.
"""),
    ],
    'tasks': [
        predict('l2_inline_predict', "Natijani oldindan toping", r"""
Kod ishga tushirilmasdan oldin o'ylab ko'ring: ekranga nima chiqadi?
""", code='print("Birinchi")\nprint("Ikkinchi")\nprint("Uchinchi")\n',
            answer="Birinchi\nIkkinchi\nUchinchi", section='inline',
            hint="Interpretator qatorlarni yuqoridan pastga bajaradi; har bir print yangi qatorga yozadi.",
            explanation="Uchta `print` — uchta qator, yozilgan tartibda."),

        single('l2_quiz_1', "Python muallifi", "Python dasturlash tilini kim yaratgan?", options=[
            opt("Bill Geyts", False, "Bill Geyts — Microsoft asoschisi."),
            opt("Gvido van Rossum", True),
            opt("Mark Sukerberg", False, "U Facebook asoschisi."),
            opt("Ilon Mask", False),
        ], hint="Darsdagi «Python bilan tanishuv» bo'limiga qarang.",
            explanation="Python'ni 1991-yilda Gvido van Rossum yaratgan."),
        single('l2_quiz_2', "Interpretator vazifasi", "Python'da **interpretator** nima qiladi?", options=[
            opt("Kodni qatorma-qator o'qib, bajaradi", True),
            opt("Kompyuterni internetga ulaydi", False),
            opt("Kodni chiroyli rangga bo'yaydi", False, "Bu muharririning vazifasi (sintaksisni ajratib ko'rsatish)."),
            opt("Faqat xatolarni topadi", False, "Xatolarni ham aytadi, lekin asosiy vazifasi — kodni bajarish."),
        ], hint="Tarjimon o'xshatishini eslang.",
            explanation="Interpretator — «tarjimon»: kodni o'qiydi va darhol bajaradi."),
        multiple('l2_quiz_3', "Qo'llanish sohalari", "Python ishlatiladigan sohalarni belgilang.", options=[
            opt("Veb-saytlarning server qismi", True),
            opt("Sun'iy intellekt va ma'lumotlar tahlili", True),
            opt("Telegram botlar", True),
            opt("Faqat kalkulyator yasash", False, "Python imkoniyatlari ancha keng."),
        ], hint="Darsdagi jadvalni ko'rib chiqing.",
            explanation="Python veb, sun'iy intellekt, tahlil, avtomatlashtirish va botlarda keng qo'llaniladi."),

        single('l2_review_1', "Takrorlash: algoritm", r"""
Oldingi darsni eslang. Quyidagi qadamlarning qaysi biri **aniq** algoritm qadami?
""", section='review', options=[
            opt("Biroz kuting", False, "«Biroz» — noaniq."),
            opt("10 daqiqa kuting", True),
            opt("Kerak bo'lsa kuting", False),
        ], hint="Aniqlik — har bir qadam bir ma'noli bo'lishi.",
            explanation="Aniq qadamda o'lchov (10 daqiqa) bor — robot ham uni bajara oladi."),

        code_task('l2_assignment', "Python qo'llaniladigan sohalar ro'yxati", r"""
Ekranga Python qo'llaniladigan sohalar ro'yxatini chiqaradigan dastur yozing.

**Talablar:**

1. Birinchi qator aynan: `Python qo'llaniladigan sohalar:`
2. Undan keyin **kamida 3 ta** soha, har biri alohida qatorda.
3. Har bir soha qatori chiziqcha va bo'sh joy bilan boshlansin: `- `

Diqqat: birinchi qatorda `o'` harfidagi apostrof bor, shuning uchun matnni **qo'sh qo'shtirnoq** `"..."` ichiga oling.
""", starter_code='print("Python qo\'llaniladigan sohalar:")\n',
            expected_output_example="Python qo'llaniladigan sohalar:\n- Veb-dasturlash\n- Sun'iy intellekt\n- Telegram botlar",
            tests=[
                T('runs_ok', description="Dastur xatosiz ishlaydi"),
                T('output_regex', r"\APython qo'llaniladigan sohalar:\n", "Birinchi qator aynan «Python qo'llaniladigan sohalar:»",
                  failure="Sarlavha qatorini harfma-harf tekshiring (oxirida ikki nuqta bor)."),
                T('output_regex', r"\APython qo'llaniladigan sohalar:(\n- \S.*){3,}\Z", "Kamida 3 ta soha «- » bilan alohida qatorlarda",
                  failure="Har bir soha print(\"- Soha nomi\") ko'rinishida bo'lsin va kamida 3 ta bo'lsin."),
            ],
            hint="Sarlavhadan keyin yana uchta qator qo'shing, masalan: print(\"- Veb-dasturlash\")",
            partial_solution='''print("Python qo'llaniladigan sohalar:")
print("- Veb-dasturlash")
# yana kamida 2 ta soha qo'shing
''',
            full_solution='''print("Python qo'llaniladigan sohalar:")
print("- Veb-dasturlash")
print("- Sun'iy intellekt")
print("- Telegram botlar")
''',
            explanation="Har bir `print` alohida qator chiqaradi. Matnda `'` (apostrof) bo'lsa, uni `\"...\"` ichiga olish kerak — aks holda Python matn qayerda tugashini adashtiradi."),

        single('l2_practice_easy', "Python haqida to'g'ri gap", "Qaysi gap **to'g'ri**?", section='practice', difficulty='easy', options=[
            opt("Python pullik dastur", False, "Python bepul va ochiq kodli."),
            opt("Python bepul va ochiq kodli til", True),
            opt("Python faqat o'yinlar uchun", False),
        ], hint="Afzalliklar ro'yxatini eslang.", explanation="Python bepul va ochiq — uni istalgan kishi ishlatishi mumkin."),
        predict('l2_practice_medium', "Bo'sh print", r"""
`print()` qavslari ichida hech narsa bo'lmasa, u **bo'sh qator** chiqaradi. Dastur natijasini yozing
(bo'sh qatorni ham hisobga oling).
""", code='print("Python")\nprint()\nprint("oson")\n', answer="Python\n\noson",
            section='practice', difficulty='medium',
            hint="Ikkinchi qator bo'sh bo'ladi.", explanation="Bo'sh `print()` faqat yangi qatorga o'tadi — natijada ikki so'z orasida bo'sh qator paydo bo'ladi."),
        code_task('l2_practice_hard', "Python haqida mini-ma'lumotnoma", r"""
Quyidagi natijani **aynan** chiqaring (bo'sh qator ham bor):

```
Python
Muallif: Gvido van Rossum
Yil: 1991

Python sodda va kuchli til!
```
""", section='practice', difficulty='hard', points=5,
            expected_output_example="Python\nMuallif: Gvido van Rossum\nYil: 1991\n\nPython sodda va kuchli til!",
            tests=[T('output_equals', "Python\nMuallif: Gvido van Rossum\nYil: 1991\n\nPython sodda va kuchli til!",
                     "Natija namunaga aynan mos", failure="Har bir harf, ikki nuqta va bo'sh qatorni tekshiring.")],
            hint="Bo'sh qator uchun bo'sh print() ishlating.",
            full_solution='''print("Python")
print("Muallif: Gvido van Rossum")
print("Yil: 1991")
print()
print("Python sodda va kuchli til!")
''',
            explanation="Natijani aynan takrorlash — dasturlashdagi muhim ko'nikma: kompyuter «deyarli to'g'ri»ni qabul qilmaydi."),
    ],
}
