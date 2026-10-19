from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
from apps.users.models import CustomUser


class ContestCategory(models.TextChoices):
    ALGORITHMIC = 'algorithmic', 'Algoritmik Kodlash'
    MOBILE = 'mobile', 'Mobil & Flutter Challenge'
    BACKEND = 'backend', 'Backend & API Hackathon'
    FRONTEND = 'frontend', 'Frontend & Web UI'
    GENERAL = 'general', 'Umumiy IT Xakaton'


class ContestStatus(models.TextChoices):
    UPCOMING = 'upcoming', 'Kutilmoqda'
    ACTIVE = 'active', 'Davom etmoqda'
    FINISHED = 'finished', 'Yakunlangan'


class Contest(TimeStampedModel):
    title = models.CharField(max_length=200, verbose_name="Musobaqa nomi")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(
        max_length=30,
        choices=ContestCategory.choices,
        default=ContestCategory.ALGORITHMIC,
        verbose_name="Yo'nalish / Kategoriya"
    )
    description = models.TextField(verbose_name="Musobaqa tavsifi (Markdown)")
    rules = models.TextField(blank=True, verbose_name="Musobaqa qoidalari va talablari")
    banner = models.ImageField(upload_to='contests/banners/%Y/%m/', blank=True, null=True, verbose_name="Muqova rasmi")
    start_time = models.DateTimeField(verbose_name="Boshlanish vaqti")
    end_time = models.DateTimeField(verbose_name="Tugash vaqti")
    coin_prize_pool = models.PositiveIntegerField(default=500, verbose_name="Mukofot tangalar fondi")
    first_place_reward = models.CharField(max_length=150, default="300 tanga + Maxsus Diplom", verbose_name="1-o'rin mukofoti")
    second_place_reward = models.CharField(max_length=150, default="150 tanga + Diplom", verbose_name="2-o'rin mukofoti")
    third_place_reward = models.CharField(max_length=150, default="50 tanga + Diplom", verbose_name="3-o'rin mukofoti")
    is_published = models.BooleanField(default=True, verbose_name="E'lon qilinganmi?")

    class Meta:
        verbose_name = "Musobaqa"
        verbose_name_plural = "Musobaqalar"
        ordering = ['-start_time']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def current_status(self):
        now = timezone.now()
        if now < self.start_time:
            return ContestStatus.UPCOMING
        elif self.start_time <= now <= self.end_time:
            return ContestStatus.ACTIVE
        return ContestStatus.FINISHED

    @property
    def is_live(self):
        return self.current_status == ContestStatus.ACTIVE

    @property
    def is_upcoming(self):
        return self.current_status == ContestStatus.UPCOMING

    @property
    def is_finished(self):
        return self.current_status == ContestStatus.FINISHED

    @property
    def participants_count(self):
        return self.participants.count()

    @property
    def problems_count(self):
        return self.problems.count()


class ContestProblem(TimeStampedModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='problems', verbose_name="Musobaqa")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartibi (1, 2, 3...)")
    title = models.CharField(max_length=200, verbose_name="Masala sarlavhasi")
    description = models.TextField(verbose_name="Masala sharti va kirish/chiqish formatlari")
    points = models.PositiveIntegerField(default=100, verbose_name="Maksimal ball")
    difficulty = models.CharField(
        max_length=20,
        choices=[('easy', 'Oson'), ('medium', "O'rta"), ('hard', 'Qiyin')],
        default='medium',
        verbose_name="Qiyinlik darajasi"
    )
    starter_code = models.TextField(blank=True, verbose_name="Boshlang'ich kod shabloni")
    time_limit_seconds = models.PositiveIntegerField(default=2, verbose_name="Vaqt chegarasi (soniya)")

    class Meta:
        verbose_name = "Musobaqa masalasi"
        verbose_name_plural = "Musobaqa masalalari"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.contest.title} - #{self.order}: {self.title}"


class ContestParticipant(TimeStampedModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='participants', verbose_name="Musobaqa")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contest_entries', verbose_name="Ishtirokchi")
    total_score = models.PositiveIntegerField(default=0, verbose_name="Jami to'plangan ball")
    rank = models.PositiveIntegerField(null=True, blank=True, verbose_name="Egallagan o'rni")

    class Meta:
        verbose_name = "Musobaqa ishtirokchisi"
        verbose_name_plural = "Musobaqa ishtirokchilari"
        unique_together = ('contest', 'user')
        ordering = ['-total_score', 'created_at']

    def __str__(self):
        return f"{self.user.email} @ {self.contest.title} ({self.total_score} ball)"


class ContestSubmission(TimeStampedModel):
    participant = models.ForeignKey(ContestParticipant, on_delete=models.CASCADE, related_name='submissions', verbose_name="Ishtirokchi")
    problem = models.ForeignKey(ContestProblem, on_delete=models.CASCADE, related_name='submissions', verbose_name="Masala")
    submitted_code = models.TextField(blank=True, verbose_name="Yechim kodi")
    attached_file = models.FileField(upload_to='contests/solutions/%Y/%m/', blank=True, null=True, verbose_name="Biriktirilgan fayl")
    score = models.PositiveIntegerField(default=0, verbose_name="Qo'yilgan ball")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Kutilmoqda'), ('accepted', 'Qabul qilindi'), ('rejected', 'Rad etildi')],
        default='pending',
        verbose_name="Holati"
    )
    reviewer_notes = models.TextField(blank=True, verbose_name="Hakam izohi")

    class Meta:
        verbose_name = "Musobaqa yechimi"
        verbose_name_plural = "Musobaqa yechimlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.participant.user.email} - {self.problem.title} ({self.score} ball)"
