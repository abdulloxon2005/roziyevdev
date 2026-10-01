from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class UserRole(models.TextChoices):
    STUDENT = 'student', 'Talaba'
    INSTRUCTOR = 'instructor', "O'qituvchi"
    ADMIN = 'admin', 'Administrator'


class CustomUser(AbstractUser):
    """
    Kengaytirilgan foydalanuvchi modeli.
    Email orqali tizimga kirish va rollar qo'llab-quvvatlanadi.
    """
    email = models.EmailField(unique=True, verbose_name="Elektron pochta")
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name="Telefon raqami")
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        verbose_name="Foydalanuvchi roli"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def display_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.username


class Profile(TimeStampedModel):
    """
    Foydalanuvchi qo'shimcha ma'lumotlari va ijtimoiy profili.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True, verbose_name="Profil rasmi")
    headline = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Mutaxassislik",
        help_text="Masalan: Flutter & Android Developer, Algoritmik dasturchi"
    )
    bio = models.TextField(blank=True, verbose_name="O'zi haqida (Bio)")
    github = models.URLField(blank=True, null=True, verbose_name="GitHub havola")
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn havola")
    telegram = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telegram (@username yoki havola)")
    website = models.URLField(blank=True, null=True, verbose_name="Shaxsiy veb-sayt")

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profillar'

    def __str__(self):
        return f"{self.user.email} profili"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        # Standart avatar rasmi (UI-avatars bepul servisi)
        name = self.user.display_name.replace(' ', '+')
        return f"https://ui-avatars.com/api/?name={name}&background=0D8ABC&color=fff&size=128"
