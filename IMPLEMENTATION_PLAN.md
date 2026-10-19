# RoziyevDev — Onlayn Ta'lim Platformasi va Shaxsiy IT Blog
## Texnik Amalga Oshirish Rejasi (Implementation Plan)

---

### 1. Loyiha haqida va Maqsad

**Loyiha nomi:** `roziyevdev` — Zamonaviy Onlayn Ta'lim (LMS) va Shaxsiy IT Blog Platformasi.  
**Maqsad:** Foydalanuvchilarga mobil dasturlash (Flutter, Android, iOS), algoritmlar va ma'lumotlar tuzilmalari, ma'lumotlar bazalari va boshqa dasturlash yo'nalishlarida sifatli online kurslarni taqdim etish hamda muallifning shaxsiy tajribalari, maqolalari va qo'llanmalarini o'z ichiga olgan zamonaviy, tezkor va xavfsiz web platforma yaratish.

---

### 2. Texnologik Stack va Arxitektura

| Qatlam | Texnologiya / Vosita | Tavsif |
| :--- | :--- | :--- |
| **Backend** | Python 3.11+, Django 5.x, Django REST Framework (DRF) | Mustahkam, xavfsiz va kengayuvchan REST API arxitekturasi |
| **Autentifikatsiya** | `djangorestframework-simplejwt` | Xavfsiz JSON Web Token (Access & Refresh tokens) |
| **Hujjatlashtirish** | `drf-spectacular` (Swagger UI & Redoc) | Barcha API endpointlar uchun interaktiv hujjat |
| **Frontend** | Zamonaviy Responsive UI (Django Templates + Tailwind CSS / Alpine.js) | Barcha qurilmalarga to'liq moslashuvchan, tez yuklanuvchi zamonaviy dizayn |
| **Ma'lumotlar bazasi** | PostgreSQL / SQLite | Relatsion ma'lumotlar bazasi |
| **Media / Fayllar** | Django File Storage / Cloudinary | Kurs videolari, rasmlar va o'quv materiallari saqlash |

---

### 3. Bosqichma-bosqich Reja (Project Phases)

#### 🚀 1-BOSQICH: Asosiy Sahifa, Kurslar Katalogi va Foydalanuvchilar Tizimi (MVP)
1. **Loyiha poydevori:** Django 5 + DRF loyihasini sozlash, `users`, `courses`, `core` modullarini yaratish.
2. **Custom User va Profil Tizimi:**
   - CustomUser (Email, Username, Ism-familiya, Rol: Talaba/Instruktor/Admin).
   - Profile modeli (Avatar, mutaxassislik, bio, ijtimoiy tarmoqlar).
   - Ro'yxatdan o'tish (Register).
   - Profilga kirish (Login - JWT & Session).
   - Profilni ko'rish va sozlash (Profile Settings).
3. **Kurslar Katalogi:**
   - Kategoriyalar (Mobil dasturlash, Algoritmlar, Ma'lumotlar bazasi va h.k.).
   - Kurslar modeli, ro'yxati va batafsil sahifasi.
   - Qidiruv va filtrlash tizimi.
4. **Asosiy Sahifa (Landing Page):**
   - Hero qismi, yo'nalishlar kartochkalari, sara kurslar, afzalliklar va aloqa.
5. **Swagger / OpenAPI:** Barcha endpointlar hujjati.

---

#### 📚 2-BOSQICH: Darslar Tuzilmasi, Video Darslar va O'quv Jarayoni
1. Bo'limlar (Sections) va Darslar (Lessons) modeli (Video, Matn, Kod fayllari).
2. Video darslar pleeri va resurslar.
3. Kursga yozilish (Enrollment) va progress tracking (o'tilgan darslar foizi).

---

#### 📝 3-BOSQICH: Shaxsiy IT Blog va Maqolalar Tizimi
1. Blog maqolalari (Markdown, sintaksis yoritgich, ko'rishlar statistikasi).
2. Teglar va kategoriyalar.
3. Izohlar (Comments) tizimi.
4. SEO va ijtimoiy tarmoqlarda ulashish.

---

#### 💳 4-BOSQICH: To'lovlar, Avtomatik Sertifikatlar va Bildirishnomalar
1. Payme, Click, Uzum to'lov integratsiyalari.
2. Kursni tamomlaganlik haqida QR-kodli PDF sertifikat generatsiyasi.
3. Telegram bot / Email xabarnomalar.

---

#### 🛡️ 5-BOSQICH: Admin Dashboard, Xavfsizlik va Deployment
1. Instruktor statistikasi va boshqaruv paneli.
2. Xavfsizlik (CORS, Rate limiting, CSRF).
3. Docker & Production sozlamalari.

---

#### 🎓 6-BOSQICH: O'quvchilar Paneli (Student Portal & Gamification)
Batafsil texnik reja: [STUDENT_PORTAL_IMPLEMENTATION_PLAN.md](file:///d:/BMI/roziyevdev/STUDENT_PORTAL_IMPLEMENTATION_PLAN.md)
1. **Vazifalar Laboratoriyasi:** Platformaning o'zida kod/flowchart muharriri orqali amaliy topshiriqlarni bajarish va o'qituvchiga yuborish, taqriz va qayta ishlash zanjiri.
2. **Kurs Reytingi (Leaderboard):** Talaba o'zi o'qiyotgan kurs bo'yicha jonli reyting, XP/ballar, shaxsiy o'rin ko'rsatkichi va ligalar.
3. **Musobaqalar Bo'limi (Contests):** Haftalik bellashuvlar, algoritmik va xakaton musobaqalari, jonli turnir jadvali va sovrinli tangalar.
4. **Loyihalar Bo'limi (Projects Showcase):** Kurs bitiruv (capstone) loyihalari, shaxsiy portfoliolarni joylash, ustoz code review va jamoatchilik ko'rgazmasi.
5. **Dasturchi Yo'li (Developer Roadmap):** Yo'nalishlar (Flutter, Python, Algoritmlar) bo'yicha chiroyli interaktiv metro liniyasi shaklidagi vizual xarita, mavzular va darslar bilan avtomatik bog'langan progress.

