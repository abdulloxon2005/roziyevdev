#!/usr/bin/env bash
# ==============================================================================
# ROZIYEVDEV — SERVERGA AVTOMATIK DEPLOYMENT SKRIPTI
# Ishlatish: bash deploy/deploy.sh
# ==============================================================================

set -e

echo "🚀 [1/6] Loyiha yangilanishi boshlandi..."

# Ishchi katalogga o'tish
PROJECT_DIR="/var/www/roziyevdev"
cd "$PROJECT_DIR"

# Virtual muhitni faollashtirish
source "$PROJECT_DIR/venv/bin/activate"

echo "📦 [2/6] Python paketlarini yangilash..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ [3/6] Ma'lumotlar bazasi migratsiyalarini qo'llash..."
python manage.py migrate --noinput

echo "🎨 [4/6] Statik fayllarni yig'ish (collectstatic)..."
python manage.py collectstatic --noinput

echo "📁 [5/6] Media kataloglari huquqlarini tekshirish..."
mkdir -p media/lessons/videos media/lessons/attachments media/courses/thumbnails media/avatars media/assignments media/certificates
mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data media /var/log/gunicorn
sudo chmod -R 775 media

echo "🔄 [6/6] Gunicorn va Nginx xizmatlarini qayta ishga tushirish..."
sudo systemctl restart roziyevdev
sudo systemctl reload nginx

echo "✅ TABRIKLAYMIZ! RoziyevDev loyihasi muvaffaqiyatli yangilandi va serverda ishga tushdi!"
