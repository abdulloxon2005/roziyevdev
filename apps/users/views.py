from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import time
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .models import CustomUser, Profile
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProfileUpdateSerializer,
    ChangePasswordSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ==============================================================================
# REST API VIEWS
# ==============================================================================

class RegisterAPIView(APIView):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish API'si.
    Muvaffaqiyatli ro'yxatdan o'tgach darhol JWT tokenlar qaytariladi.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            user_data = UserSerializer(user).data
            return Response(
                {
                    "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz!",
                    "user": user_data,
                    "tokens": tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Tizimga kirish API'si (Email yoki Username orqali).
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                },
                "required": ["email", "password"],
            }
        },
        responses={200: UserSerializer},
    )
    def post(self, request):
        identifier = request.data.get('email', '').strip()
        password = request.data.get('password', '')

        if not identifier or not password:
            return Response(
                {"detail": "Email/Username va parol kiritilishi shart."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Foydalanuvchini email yoki username orqali topish
        user = None
        if '@' in identifier:
            try:
                u = CustomUser.objects.get(email__iexact=identifier)
                user = authenticate(request, username=u.email, password=password)
            except CustomUser.DoesNotExist:
                user = None
        else:
            try:
                u = CustomUser.objects.get(username__iexact=identifier)
                user = authenticate(request, username=u.email, password=password)
            except CustomUser.DoesNotExist:
                user = None

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "Tizimga muvaffaqiyatli kirdingiz!",
                    "user": UserSerializer(user).data,
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Email yoki parol noto'g'ri kiritildi."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class CurrentUserProfileAPIView(APIView):
    """
    Joriy kirgan foydalanuvchining profiling ma'lumotlarini olish va tahrirlash API'si.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(request=ProfileUpdateSerializer, responses={200: UserSerializer})
    def put(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.update(request.user, serializer.validated_data)
            return Response(
                {
                    "message": "Profil ma'lumotlari muvaffaqiyatli yangilandi.",
                    "user": UserSerializer(user).data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=ProfileUpdateSerializer, responses={200: UserSerializer})
    def patch(self, request):
        return self.put(request)


class ChangePasswordAPIView(APIView):
    """
    Parolni o'zgartirish API'si.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        }
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Hozirgi parol noto'g'ri kiritildi."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Parol muvaffaqiyatli o'zgartirildi!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==============================================================================
# WEB TEMPLATE VIEWS (Server-rendered UI)
# ==============================================================================

def web_login_view(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Email yoki username bo'yicha CustomUser ni topamiz
        user_obj = None
        if '@' in identifier:
            user_obj = CustomUser.objects.filter(email__iexact=identifier).first()
        else:
            user_obj = CustomUser.objects.filter(username__iexact=identifier).first()

        if user_obj:
            user = authenticate(request, username=user_obj.email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.display_name}!")
                next_url = request.GET.get('next') or request.POST.get('next') or 'student_dashboard'
                return redirect(next_url)

        messages.error(request, "Email yoki parol xato kiritildi!")

    return render(request, 'auth/login.html')


def web_register_view(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Validatsiya
        if not email or not username or not password:
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring.")
        elif password != password_confirm:
            messages.error(request, "Kiritilgan parollar bir-biriga mos kelmadi.")
        elif len(password) < 6:
            messages.error(request, "Parol kamida 6 ta belgidan iborat bo'lishi kerak.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu elektron pochta bilan allaqachon ro'yxatdan o'tilgan.")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi (username) band qilingan.")
        else:
            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
            )
            login(request, user)
            messages.success(request, "Hisobingiz muvaffaqiyatli yaratildi!")
            return redirect('student_dashboard')

    return render(request, 'auth/register.html')


def web_logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('home')


@login_required
def web_profile_view(request):
    from apps.learning.models import Enrollment, LessonProgress, CoinTransaction, AssignmentSubmission
    from apps.certificates.models import Certificate

    enrollments = Enrollment.objects.filter(user=request.user).select_related('course__category', 'last_lesson').order_by('-updated_at')
    certificates = Certificate.objects.filter(user=request.user).select_related('course').order_by('-issued_at')
    completed_lessons_count = LessonProgress.objects.filter(enrollment__user=request.user).count()

    coin_transactions = CoinTransaction.objects.filter(student=request.user).order_by('-created_at')[:10]
    my_submissions = AssignmentSubmission.objects.filter(student=request.user).select_related('assignment__lesson__module__course').order_by('-created_at')[:10]
    approved_submissions_count = AssignmentSubmission.objects.filter(student=request.user, status='approved').count()

    context = {
        'user': request.user,
        'enrollments': enrollments,
        'certificates': certificates,
        'enrollments_count': enrollments.count(),
        'completed_lessons_count': completed_lessons_count,
        'certificates_count': certificates.count(),
        'coin_transactions': coin_transactions,
        'my_submissions': my_submissions,
        'approved_submissions_count': approved_submissions_count,
        'active_menu': 'profile',
    }
    return render(request, 'profile/detail.html', context)


@login_required
def web_profile_settings_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            user = request.user
            if 'first_name' in request.POST:
                user.first_name = (request.POST.get('first_name') or '').strip()
            if 'last_name' in request.POST:
                user.last_name = (request.POST.get('last_name') or '').strip()
            if 'phone' in request.POST:
                user.phone = (request.POST.get('phone') or '').strip()
            user.save()

            if 'headline' in request.POST:
                profile.headline = (request.POST.get('headline') or '').strip()
            if 'bio' in request.POST:
                profile.bio = (request.POST.get('bio') or '').strip()
            if 'github' in request.POST:
                profile.github = (request.POST.get('github') or '').strip() or None
            if 'linkedin' in request.POST:
                profile.linkedin = (request.POST.get('linkedin') or '').strip() or None
            if 'telegram' in request.POST:
                profile.telegram = (request.POST.get('telegram') or '').strip() or None
            if 'website' in request.POST:
                profile.website = (request.POST.get('website') or '').strip() or None

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            messages.success(request, "Profil ma'lumotlari muvaffaqiyatli yangilandi!")
            return redirect('profile_settings')

        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password_confirm = request.POST.get('new_password_confirm')

            if not request.user.check_password(old_password):
                messages.error(request, "Hozirgi parol noto'g'ri kiritildi.")
            elif new_password != new_password_confirm:
                messages.error(request, "Yangi parollar bir-biriga mos kelmadi.")
            elif len(new_password) < 6:
                messages.error(request, "Yangi parol kamida 6 ta belgidan iborat bo'lishi kerak.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                # Update session so user stays logged in
                login(request, request.user)
                messages.success(request, "Parolingiz muvaffaqiyatli yangilandi!")
                return redirect('profile_settings')

    return render(request, 'profile/settings.html', {'user': request.user, 'profile': profile, 'active_menu': 'profile_settings'})


@require_POST
def web_quick_unlock_view(request):
    """
    Ekran qulflanganda parolni tezkor tekshirib, sahifani yangilamasdan
    seansni davom ettirish (Unlock) endpointi.
    """
    if not request.user.is_authenticated:
        next_url = request.POST.get('next', '/')
        return JsonResponse({
            'success': False,
            'expired': True,
            'error': "Seans vaqti tugagan. Qaytadan tizimga kiring.",
            'redirect': f"{settings.LOGIN_URL}?next={next_url}"
        }, status=401)

    password = request.POST.get('password', '')
    if not password:
        return JsonResponse({'success': False, 'error': "Parolni kiriting!"}, status=400)

    # Parolni tekshirish
    if request.user.check_password(password):
        # Faollik vaqtini yangilash
        request.session['last_activity'] = time.time()
        return JsonResponse({
            'success': True,
            'message': "Xush kelibsiz! Qulf muvaffaqiyatli ochildi."
        })
    else:
        return JsonResponse({
            'success': False,
            'error': "Kiritilgan parol noto'g'ri!"
        }, status=400)
