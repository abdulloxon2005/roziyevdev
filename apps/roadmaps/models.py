from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
from apps.users.models import CustomUser
from apps.courses.models import Course, Lesson


class RoadmapTrack(TimeStampedModel):
    title = models.CharField(max_length=150, verbose_name="Yo'nalish nomi")
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        default='fa-solid fa-route',
        verbose_name="Belgi (FontAwesome)",
        help_text="Masalan: fa-solid fa-mobile-screen, fa-brands fa-python, fa-solid fa-code-branch"
    )
    accent_color = models.CharField(
        max_length=30,
        default='blue',
        verbose_name="Rang uslubi (Tailwind color)",
        help_text="blue, emerald, purple, amber, indigo, rose"
    )
    short_description = models.TextField(blank=True, verbose_name="Qisqa tavsif")
    estimated_months = models.PositiveSmallIntegerField(default=6, verbose_name="O'rtacha o'rganish muddati (oy)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Dasturchi Yo'nalishi"
        verbose_name_plural = "Dasturchi Yo'nalishlari"
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def total_nodes_count(self):
        return RoadmapNode.objects.filter(stage__track=self).count()


class RoadmapStage(TimeStampedModel):
    track = models.ForeignKey(RoadmapTrack, on_delete=models.CASCADE, related_name='stages', verbose_name="Yo'nalish")
    title = models.CharField(max_length=200, verbose_name="Bosqich nomi")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartibi (1, 2, 3...)")
    description = models.TextField(blank=True, verbose_name="Bosqich haqida ma'lumot")

    class Meta:
        verbose_name = "Yo'l Bosqichi"
        verbose_name_plural = "Yo'l Bosqichlari"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.track.title} -> #{self.order}: {self.title}"


class NodeImportance(models.TextChoices):
    ESSENTIAL = 'essential', 'Majburiy (Asosiy Poydevor)'
    RECOMMENDED = 'recommended', 'Tavsiya etiladi (Chuqurlashtirilgan)'
    OPTIONAL = 'optional', 'Qo\'shimcha (Kengaytma)'


class RoadmapNode(TimeStampedModel):
    stage = models.ForeignKey(RoadmapStage, on_delete=models.CASCADE, related_name='nodes', verbose_name="Bosqich")
    title = models.CharField(max_length=200, verbose_name="Bekat / Mavzu nomi")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartibi")
    summary = models.TextField(verbose_name="Mavzu mohiyati va nima uchun kerakligi")
    importance = models.CharField(
        max_length=20,
        choices=NodeImportance.choices,
        default=NodeImportance.ESSENTIAL,
        verbose_name="Muhimlik darajasi"
    )
    linked_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roadmap_nodes',
        verbose_name="Platformadagi bog'liq kurs"
    )
    linked_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roadmap_nodes',
        verbose_name="Platformadagi bog'liq dars"
    )
    external_docs_url = models.URLField(blank=True, null=True, verbose_name="Rasmiy hujjatlar yoki resurs havolasi")

    class Meta:
        verbose_name = "Yo'l Bekati (Mavzu)"
        verbose_name_plural = "Yo'l Bekatlari (Mavzular)"
        ordering = ['stage__order', 'order', 'id']

    def __str__(self):
        return f"{self.stage.track.title} | {self.stage.title} - {self.title}"

    @property
    def target_url(self):
        if self.linked_lesson:
            return reverse('course_learn_lesson', kwargs={'slug': self.linked_lesson.module.course.slug, 'lesson_id': self.linked_lesson.id})
        elif self.linked_course:
            return reverse('course_detail', kwargs={'slug': self.linked_course.slug})
        return ""



class UserRoadmapProgress(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='roadmap_progress', verbose_name="O'quvchi")
    node = models.ForeignKey(RoadmapNode, on_delete=models.CASCADE, related_name='user_progress', verbose_name="Bekat")
    status = models.CharField(
        max_length=20,
        choices=[('locked', 'Qulflangan'), ('in_progress', 'Jarayonda'), ('completed', 'Tugatildi')],
        default='in_progress',
        verbose_name="Holati"
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tugatilgan vaqt")

    class Meta:
        verbose_name = "O'quvchi Yo'l Progressi"
        verbose_name_plural = "O'quvchilar Yo'l Progresslari"
        unique_together = ('user', 'node')

    def __str__(self):
        return f"{self.user.email} -> {self.node.title} ({self.status})"
