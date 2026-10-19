# 🚀 RoziyevDev — Serverga Joylash (Production Deployment) Qo'llanmasi

Ushbu qo'llanma **RoziyevDev** ta'lim platformasi va Ustoz Studiyasini real Linux serverga (Ubuntu 22.04 / 24.04 LTS VPS/VDS masalan: Hetzner, DigitalOcean, Reg.ru, UzTelecom, v.h.k.) to'liq, xavfsiz va barqaror joylash bo'yicha batafsil ko'rsatmalarni o'z ichiga oladi.

---

## 📋 Texnik Talablar
* **OS:** Ubuntu 22.04 LTS yoki 24.04 LTS
* **RAM:** Kamida 2 GB (4 GB tavsiya etiladi)
* **Disk:** Kamida 20 GB SSD/NVMe (yuklanadigan dars videolari hajmiga qarab)
* **Domen:** Masalan `roziyev.dev` (DNS A-yozuvi server IP-siga yo'naltirilgan bo'lishi kerak)

---

## 🛠️ 1-QADAM: Serverni Tayyorlash va Paketlarni O'rnatish

Serverga SSH orqali kiring va tizim paketlarini yangilang:
```bash
sudo apt update && sudo apt upgrade -y

# Zaruriy dasturlar: Python, pip, venv, PostgreSQL, Redis, Nginx, Git
sudo apt install -y python3 python3-pip python3-venv \
    postgresql postgresql-contrib libpq-dev \
    redis-server nginx certbot python3-certbot-nginx \
    curl git htop ufw
```

---

## 🗄️ 2-QADAM: PostgreSQL Ma'lumotlar Bazasini Sozlash

```bash
# PostgreSQL konsoliga kirish
sudo -u postgres psql
```

PostgreSQL ichida quyidagi buyruqlarni bajaring (kuchli parol o'rnating):
```sql
CREATE DATABASE roziyev_db;
CREATE USER roziyev_user WITH PASSWORD 'kuchli_parol_123';
ALTER ROLE roziyev_user SET client_encoding TO 'utf8';
ALTER ROLE roziyev_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE roziyev_user SET timezone TO 'Asia/Tashkent';
GRANT ALL PRIVILEGES ON DATABASE roziyev_db TO roziyev_user;
\q
```

---

## 📂 3-QADAM: Loyiha Kodini Joylash va Virtual Muhit

Loyiha katalogini yaratamiz (masalan `/var/www/roziyevdev`):
```bash
sudo mkdir -p /var/www/roziyevdev
sudo chown -R $USER:$USER /var/www/roziyevdev

# Kodni serverga nusxalang yoki Git orqali klonlang:
git clone https://github.com/roziyevdev/roziyevdev.git /var/www/roziyevdev
cd /var/www/roziyevdev

# Python virtual muhitini yaratish
python3 -m venv venv
source venv/bin/activate

# Paketlarni o'rnatish
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ 4-QADAM: Atrof-muhit Sozlamalari (`.env`)

Namuna fayldan `.env` nusxasini yarating:
```bash
cp .env.example .env
nano .env
```

Quyidagi qatorlarni o'zgartiring:
```env
DJANGO_SECRET_KEY=juda-uzun-tasodifiy-kalit-50-belgi
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=roziyev.dev,www.roziyev.dev,SERVER_IP_MANZILI
DJANGO_CSRF_TRUSTED_ORIGINS=https://roziyev.dev,https://www.roziyev.dev
SITE_URL=https://roziyev.dev

# PostgreSQL ulanishi:
DATABASE_URL=postgres://roziyev_user:kuchli_parol_123@localhost:5432/roziyev_db
REDIS_URL=redis://127.0.0.1:6379/1

# Video yuklash chegaralari (500 MB gacha):
DATA_UPLOAD_MAX_MEMORY_SIZE=524288000
FILE_UPLOAD_MAX_MEMORY_SIZE=52428800
```
*(Faylni saqlash uchun: `Ctrl+O`, `Enter`, chiqish uchun: `Ctrl+X`)*

---

## 🏗️ 5-QADAM: Migratsiyalar, Statik Fayllar va Admin Yaratish

```bash
# Migratsiyalarni bazaga qo'llash
python manage.py migrate

# Statik fayllarni yig'ish (CSS, JS, Rasmlar)
python manage.py collectstatic --noinput

# Sayt administratori (Ustoz) profilini yaratish
python manage.py createsuperuser

# Media papkalari huquqlarini www-data foydalanuvchisiga berish
mkdir -p media/lessons/videos media/lessons/attachments media/courses/thumbnails media/avatars
sudo chown -R www-data:www-data media
sudo chmod -R 775 media
```

---

## 🦄 6-QADAM: Gunicorn va Systemd Xizmatini Sozlash

Loyiha ichidagi tayyor `deploy/systemd/roziyevdev.service` faylini tizimga ko'chiramiz:
```bash
sudo cp deploy/systemd/roziyevdev.service /etc/systemd/system/
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn

# Xizmatni yoqish va ishga tushirish:
sudo systemctl daemon-reload
sudo systemctl start roziyevdev
sudo systemctl enable roziyevdev

# Holatini tekshirish:
sudo systemctl status roziyevdev
```

---

## 🌐 7-QADAM: Nginx Veb-Serverini Sozlash

Tayyor Nginx konfiguratsiyasini ulaymiz:
```bash
sudo cp deploy/nginx/roziyevdev.conf /etc/nginx/sites-available/roziyevdev

# Saytni faollashtirish
sudo ln -s /etc/nginx/sites-available/roziyevdev /etc/nginx/sites-enabled/

# Nginx sintaksisini tekshirish
sudo nginx -t

# Nginx-ni qayta yuklash
sudo systemctl reload nginx
```

---

## 🔒 8-QADAM: Bepul SSL (HTTPS) Sertifikatini O'rnatish

Certbot orqali Let's Encrypt bepul SSL sertifikatini 1 ta buyruq bilan yoqing:
```bash
sudo certbot --nginx -d roziyev.dev -d www.roziyev.dev
```
*Elektron pochtangizni kiriting va shartlarga rozilik bering. Certbot Nginx konfiguratsiyasini avtomatik tarzda HTTPS ga moslaydi va muddati tugashidan oldin avtomatik yangilab turadi.*

---

## 🔄 9-QADAM: Keyingi Yangilanishlarni Bir Tugma Bilan Deploy Qilish

Har safar yangi kod yozganingizda yoki o'zgarish kiritganingizda, serverda shunchaki quyidagi bitta skriptni bajarsangiz kifoya:
```bash
bash deploy/deploy.sh
```
*Bu skript avtomatik ravishda: `pip install`, `migrate`, `collectstatic`, `media` huquqlari va `systemctl restart` amallarini xatosiz bajaradi.*

---

## 🐳 Muqobil: Docker orqali Deploy qilish (1-Buyruq bilan)

Agar serverda Docker va Docker Compose o'rnatilgan bo'lsa:
```bash
cp .env.example .env
docker compose up -d --build
```
*Bu PostgreSQL, Redis va Django Gunicorn konteynerlarini avtomatik ravishda birgalikda ishga tushiradi.*

---

## 🛡️ Tekshiruv va Test
Barcha 38 ta test serverga joylash oldidan muvaffaqiyatli o'tgan:
```bash
python manage.py test
# Ran 38 tests -> OK
```

Tabriklaymiz, **roziyevdev** ta'lim platformasi endi serverda xavfsiz va yuqori tezlikda ishlashga 100% tayyor!
