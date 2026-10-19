from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.core.rendering import reading_time_minutes
from apps.core.utils import unique_slugify
from apps.users.models import CustomUser


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Tavsif")

    class Meta:
        verbose_name = 'Blog kategoriyasi'
        verbose_name_plural = 'Blog kategoriyalari'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Teg nomi")
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name = 'Teg'
        verbose_name_plural = 'Teglar'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.name}"


class Post(TimeStampedModel):
    title = models.CharField(max_length=250, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Muallif"
    )
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name="Kategoriya"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="Teglar")
    cover_image = models.ImageField(
        upload_to='blog/covers/%Y/%m/', blank=True, null=True, verbose_name="Muqova rasmi"
    )
    summary = models.CharField(
        max_length=400, verbose_name="Qisqa anons", help_text="Maqola haqida qisqacha mazmun"
    )
    content = models.TextField(verbose_name="Maqola matni (Markdown)")
    reading_time = models.PositiveSmallIntegerField(default=5, verbose_name="O'qish vaqti (daqiqa)")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    is_published = models.BooleanField(default=True, verbose_name="E'lon qilinganmi?")
    published_at = models.DateTimeField(default=timezone.now, verbose_name="Nashr qilingan vaqt")

    class Meta:
        verbose_name = 'Maqola'
        verbose_name_plural = 'Maqolalar'
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        if self.content:
            self.reading_time = reading_time_minutes(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])

    @property
    def cover_url(self):
        if self.cover_image and hasattr(self.cover_image, 'url'):
            return self.cover_image.url
        return "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80"


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Maqola")
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_comments', verbose_name="Foydalanuvchi"
    )
    author_name = models.CharField(max_length=100, blank=True, verbose_name="Ism (mehmonlar uchun)")
    content = models.TextField(verbose_name="Fikr / Izoh")
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="Javob qilingan izoh"
    )
    is_approved = models.BooleanField(default=True, verbose_name="Tasdiqlanganmi?")

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
        ordering = ['created_at']

    def __str__(self):
        name = self.user.display_name if self.user else (self.author_name or 'Mehmon')
        return f"{name}: {self.content[:30]}..."

    @property
    def display_author(self):
        if self.user:
            return self.user.display_name
        return self.author_name or "Mehmon"

    @property
    def avatar_url(self):
        if self.user:
            return self.user.profile.avatar_url
        name = self.display_author.replace(' ', '+')
        return f"https://ui-avatars.com/api/?name={name}&background=334155&color=fff&size=64"
