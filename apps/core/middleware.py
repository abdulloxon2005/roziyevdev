import time
from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import resolve


class SessionIdleTimeoutMiddleware:
    """
    Harakatsizlik tufayli seansni tugatish va xavfsizlik qulfi middleware'i.
    
    1. Foydalanuvchi tizimga kirgan bo'lsa (authenticated):
       Oxirgi so'rovdan beri o'tgan vaqtni (last_activity) tekshiradi.
       Agar SESSION_IDLE_TIMEOUT (default 15 daqiqa) dan ko'p vaqt harakatsiz
       turgan bo'lsa:
         - Foydalanuvchi tizimdan chiqariladi (logout).
         - Xavfsizlik xabari ko'rsatiladi.
         - Login sahifasiga yo'naltiriladi (?next=...).
       
    2. Agar LOGIN_REQUIRED_FOR_ALL = True bo'lsa:
       Ruxsat berilgan (exempt) yo'llardan tashqari barcha sahifalar uchun
       login talab qilinadi.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.idle_timeout = getattr(settings, 'SESSION_IDLE_TIMEOUT', 15 * 60)
        self.login_required_all = getattr(settings, 'LOGIN_REQUIRED_FOR_ALL', False)
        
        # Ochiq yo'llar (login talab qilinmaydigan prefikslar)
        self.exempt_prefixes = [
            settings.LOGIN_URL,
            '/auth/login/',
            '/auth/register/',
            '/auth/quick-unlock/',
            '/static/',
            '/media/',
            '/api/v1/health/',
            '/api/v1/auth/',
        ]

    def __call__(self, request):
        path = request.path_info
        now = time.time()

        # 1. Autentifikatsiyadan o'tgan foydalanuvchining harakatsizlik taymerini tekshirish
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            # Agar quick-unlock so'rovi bo'lsa, o'tkazib yuboramiz
            if path == '/auth/quick-unlock/':
                return self.get_response(request)

            if last_activity:
                elapsed = now - last_activity
                if elapsed > self.idle_timeout:
                    # Seans vaqti tugadi -> Logout
                    logout(request)
                    request.session.flush()

                    msg = "Harakatsizlik tufayli seans muddati tugadi. Xavfsizlik maqsadida tizimga qaytadan kiring."
                    
                    # AJAX / Fetch so'rovlar uchun JSON javob
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or path.startswith('/api/'):
                        return JsonResponse({
                            'success': False,
                            'session_expired': True,
                            'message': msg,
                            'redirect': f"{settings.LOGIN_URL}?next={path}"
                        }, status=401)

                    messages.warning(request, msg)
                    return redirect(f"{settings.LOGIN_URL}?next={path}")

            # Oxirgi faollik vaqtini yangilash
            request.session['last_activity'] = now

        # 2. Agar butun sayt bo'ylab login majburiy qilingan bo'lsa (LOGIN_REQUIRED_FOR_ALL=True)
        elif self.login_required_all:
            is_exempt = any(path.startswith(prefix) for prefix in self.exempt_prefixes)
            if not is_exempt:
                return redirect(f"{settings.LOGIN_URL}?next={path}")

        response = self.get_response(request)
        return response
