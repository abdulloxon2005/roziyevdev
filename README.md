# RoziyevDev — Onlayn Ta'lim Platformasi va Shaxsiy IT Blog

Zamonaviy, to'liq funksional onlayn ta'lim platformasi (LMS) va dasturchining shaxsiy blogi.  
Texnologik stack: **Python 3.11+**, **Django 5.x**, **Django REST Framework (DRF)**, **SimpleJWT**, **drf-spectacular (OpenAPI 3.0 / Swagger)**, **Tailwind CSS**.

---

## 🚀 1-Bosqichda Amalga Oshirilgan Imkoniyatlar (MVP)

1. **Foydalanuvchilar Tizimi va Autentifikatsiya (`apps/users`):**
   - Maxsus `CustomUser` modeli (Email orqali avtorizatsiya, rollar: Talaba, O'qituvchi, Admin).
   - `Profile` modeli (Avatar, mutaxassislik, bio, ijtimoiy tarmoqlar: Telegram, GitHub, LinkedIn, Website).
   - **Ro'yxatdan o'tish (Register)**: Validatsiya, xavfsiz hisob yaratish va avtomatik profil bog'lash.
   - **Tizimga kirish (Login)**: JWT Token (access/refresh) va sessiya asosida kirish.
   - **Profilni sozlash (Profile Settings)**: Shaxsiy ma'lumotlarni tahrirlash, avatar rasmini yuklash va parolni yangilash.
   - **Mening Profilim (Profile Detail)**: Shaxsiy kabinet, faol kurslar va progress paneli.

2. **Kurslar Katalogi (`apps/courses`):**
   - **Kategoriyalar**: Mobil dasturlash, Algoritmlar & Ma'lumotlar tuzilmasi, Ma'lumotlar bazasi (SQL), Backend & Python.
   - **Kurslar**: Sarlavha, muqova rasmi, daraja, narx (bepul yoki pullik), o'rganiladigan bilimlar, talablar, modul va darslar mundarijasi.
   - **Qidiruv va Filtrlash**: Kategoriya, daraja (boshlang'ich, o'rta, yuqori) va narx (bepul/pullik) bo'yicha tezkor qidiruv.
   - **Kursning batafsil sahifasi**: O'quv dasturi (modullar, darslar, preview darslar), muallif ma'lumoti va to'liq ma'lumotlar.

3. **Asosiy Sahifa (Landing Page):**
   - Ta'sirli Hero qism, zamonaviy kod terminali vidjeti, platforma statistikasi, yo'nalishlar kartochkalari, sara kurslar, afzalliklar va muallif (Abdulloh Roziyev) bo'limi.

4. **REST API & Swagger Hujjatlari:**
   - OpenAPI 3.0 / Swagger UI interfeysi: `/api/docs/`
   - Redoc interfeysi: `/api/redoc/`
   - Barcha endpointlar to'liq hujjatlashtirilgan.

---

## 🛠️ Loyihani Ishga Tushirish Qo'llanmasi

### 1. Virtual muhitni faollashtirish
Windows PowerShell'da:
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Ma'lumotlar bazasi migratsiyalarini bajarish
```powershell
python manage.py migrate
```

### 3. Demo ma'lumotlarni (Kurslar, Kategoriyalar, O'qituvchi) bazaga kiritish
```powershell
python manage.py seed_data
```

### 4. Serverni ishga tushirish
```powershell
python manage.py runserver
```
Server manzili: **http://127.0.0.1:8000/**

---

## 🔑 Demo Hisob Ma'lumotlari

Sinab ko'rish uchun quyidagi hisoblar bazaga kiritilgan:

| Rol | Email | Parol | Huquq |
| :--- | :--- | :--- | :--- |
| **Admin / O'qituvchi** | `admin@roziyev.dev` | `AdminPassword123!` | To'liq administrator va o'qituvchi huquqi |

*Admin paneliga kirish:* **http://127.0.0.1:8000/admin/**  
*REST API Swagger UI:* **http://127.0.0.1:8000/api/docs/**  

---

## 📡 REST API Asosiy Endpointlari

| Metod | Endpoint | Vazifasi | Ruxsat |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register/` | Yangi foydalanuvchini ro'yxatdan o'tkazish | Har kim (AllowAny) |
| `POST` | `/api/v1/auth/login/` | Kirish va JWT tokenlar (access, refresh) olish | Har kim (AllowAny) |
| `POST` | `/api/v1/auth/token/refresh/` | JWT tokenni yangilash | Har kim (AllowAny) |
| `GET` | `/api/v1/auth/me/` | Joriy foydalanuvchi ma'lumotlarini olish | Faqat tizimga kirganlar |
| `PUT` | `/api/v1/auth/me/` | Profil ma'lumotlarini tahrirlash | Faqat tizimga kirganlar |
| `POST` | `/api/v1/auth/change-password/` | Parolni o'zgartirish | Faqat tizimga kirganlar |
| `GET` | `/api/v1/courses/categories/` | Barcha kategoriyalar ro'yxati | Har kim |
| `GET` | `/api/v1/courses/` | Barcha kurslar ro'yxati (filter & search) | Har kim |
| `GET` | `/api/v1/courses/<slug>/` | Kursning batafsil ma'lumotlari | Har kim |
| `GET` | `/api/v1/health/` | Tizim holati (Health check) | Har kim |

---

## 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish

Barcha unit va integratsion testlarni tekshirish uchun:
```powershell
python manage.py test
```
