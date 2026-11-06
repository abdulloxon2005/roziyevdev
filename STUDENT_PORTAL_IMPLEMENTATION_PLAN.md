# RoziyevDev — O'quvchi Paneli (Student Portal)

> Joriy holat hujjati. Eski reja (Musobaqalar, Kurs reytingi, Dasturchi yo'li) bekor qilingan va koddan olib tashlangan.

## Sidebar bo'limlari

| Bo'lim | URL | Vazifasi |
| :--- | :--- | :--- |
| Bosh sahifa | `/student/` | Asosiy oyna: salom, tezkor havolalar, yangi kurslar, maqolalar |
| Dashboard | `/student/dashboard/` | Hozir o'qilayotgan kurslar, progress, oxirgi natijalar. Kurs yo'q bo'lsa kurslar sahifasiga yo'naltiradi |
| Vazifalar Studiyasi | `/student/assignments/` | Kurs vazifalarini yechish va yuborish |
| Kurslar | `/courses/` | Katalog (sidebar saqlanadi) |
| Duel | `/student/duel/` | Kursdoshlar bilan bellashuv |
| Loyihalar | `/student/projects/` | Loyiha yaratish va brauzer IDE |
| Blog | `/blog/` | Maqolalar |
| Profil | `/profile/` | Ma'lumotlar, parol, rasm, sertifikatlar, kurs tarixi |
| Biz haqimizda | `/student/about/` | Roziyev System, aloqa, maxfiylik va foydalanish shartlari |

## Duel (`apps/duels`)

- Modellar: `DuelChallenge` (topshiriq va testlar), `Duel` (holat: pending, active, finished, declined, cancelled), `DuelStats` (ochko, g'alaba, mag'lubiyat, oxirgi faollik).
- Raqiblar: kamida bitta umumiy kursga yozilgan talabalar. Online holati: oxirgi 60 soniya ichida faol.
- Oqim: so'rov yuborish (`/send/`) -> raqib qabul qiladi (`/<id>/respond/`) -> ikkalasi `/<id>/` xonasida yozadi -> `/<id>/submit/`.
- Tekshiruv: talaba kodi `solve` funksiyasi bo'yicha testlardan o'tkaziladi (mavjud Python sandbox). Birinchi to'liq o'tgan g'olib, ochko: oson +10, o'rta +20, qiyin +30. G'olib tanlash `select_for_update` bilan bir martalik.
- Boshlang'ich topshiriqlar `apps/duels/challenges.py` da, admin orqali qo'shish mumkin.

## Loyihalar IDE

- Qo'llab-quvvatlanadigan tillar: Python, C#, Java, C++, JavaScript, Dart, Go, PHP.
- Chapda qisqargan sidebar va fayl daraxti, o'rtada daftar kataklari fonidagi muharrir. Kod taklifi (autocomplete) o'chirilgan.
- Faqat Python kodi haqiqatan bajariladi (cheklangan sandbox), boshqa tillar simulyatsiya.

## Ma'lumotlar bazasi

`apps.contests` va `apps.roadmaps` o'chirildi. Lokal bazadan jadvallar olib tashlangan. Ishlayotgan serverda eski jadvallar qoladi; ularni olib tashlash uchun yangi kodni qo'yishdan oldin o'sha serverda `migrate contests zero` va `migrate roadmaps zero` ni bajaring.
