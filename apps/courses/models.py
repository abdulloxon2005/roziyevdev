from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
from apps.users.models import CustomUser


class Category(TimeStampedModel):
    """
    Kurslar kategoriyalari (Mobil dasturlash, Algoritmlar, Ma'lumotlar bazasi va h.k.).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        default="fa-solid fa-code",
        verbose_name="Belgi (FontAwesome / Icon class)",
        help_text="Masalan: fa-solid fa-mobile-screen, fa-solid fa-code-branch, fa-solid fa-database"
    )
    description = models.TextField(blank=True, verbose_name="Kategoriya tavsifi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CourseLevel(models.TextChoices):
    BEGINNER = 'beginner', "Boshlang'ich"
    INTERMEDIATE = 'intermediate', "O'rta daraja"
    ADVANCED = 'advanced', "Yuqori daraja"
    ALL_LEVELS = 'all_levels', "Barcha darajalar"


class Course(TimeStampedModel):
    """
    Asosiy Kurs modeli.
    """
    title = models.CharField(max_length=200, verbose_name="Kurs sarlavhasi")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        verbose_name="Yo'nalish / Kategoriya"
    )
    instructor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='instructed_courses',
        verbose_name="O'qituvchi / Muallif"
    )
    short_description = models.CharField(
        max_length=350,
        verbose_name="Qisqa tavsif",
        help_text="Kartochkalarda ko'rinadigan qisqacha ma'lumot"
    )
    description = models.TextField(verbose_name="To'liq tavsif (Markdown qo'llab-quvvatlanadi)")
    thumbnail = models.ImageField(
        upload_to='courses/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Kurs muqovasi (rasm)"
    )
    level = models.CharField(
        max_length=20,
        choices=CourseLevel.choices,
        default=CourseLevel.BEGINNER,
        verbose_name="Daraja"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Narxi (so'mda)"
    )
    is_free = models.BooleanField(default=False, verbose_name="Bepul kursmi?")
    duration_hours = models.PositiveIntegerField(default=12, verbose_name="Umumiy davomiyligi (soat)")
    what_you_will_learn = models.TextField(
        blank=True,
        verbose_name="Nimalarni o'rganasiz?",
        help_text="Har bir bandni yangi qatordan yozing"
    )
    requirements = models.TextField(
        blank=True,
        verbose_name="Talablar / Boshlang'ich bilimlar",
        help_text="Har bir bandni yangi qatordan yozing"
    )
    is_published = models.BooleanField(default=True, verbose_name="E'lon qilinganmi?")
    is_featured = models.BooleanField(default=False, verbose_name="Bosh sahifada tavsiya etilsinmi?")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="Reyting")
    students_count = models.PositiveIntegerField(default=0, verbose_name="O'quvchilar soni")

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def formatted_price(self):
        if self.is_free or self.price == 0:
            return "Bepul"
        return f"{self.price:,}".replace(",", " ") + " so'm"

    @property
    def learn_points(self):
        if not self.what_you_will_learn:
            return []
        return [point.strip() for point in self.what_you_will_learn.split('\n') if point.strip()]

    @property
    def requirement_points(self):
        if not self.requirements:
            return []
        return [req.strip() for req in self.requirements.split('\n') if req.strip()]

    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        return "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80"


class CourseModule(TimeStampedModel):
    """
    Kurs bo'limi / moduli (masalan: 1-bo'lim: Flutterga kirish).
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name="Kurs")
    title = models.CharField(max_length=200, verbose_name="Bo'lim sarlavhasi")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")

    class Meta:
        verbose_name = 'Kurs bo\'limi'
        verbose_name_plural = 'Kurs bo\'limlari'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(TimeStampedModel):
    """
    Alohida darslik modeli (Video, Matn).
    """
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons', verbose_name="Bo'lim")
    title = models.CharField(max_length=200, verbose_name="Dars sarlavhasi")
    duration_minutes = models.PositiveIntegerField(default=15, verbose_name="Davomiyligi (daqiqa)")
    is_preview = models.BooleanField(default=False, verbose_name="Ochiq darsmi (Preview)?")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")

    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"
