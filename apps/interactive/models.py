"""
Interaktiv ta'lim modellari.

Mavjud jadvallar qayta ishlatiladi:
  * Course / CourseModule / Lesson          — apps.courses
  * Enrollment / LessonProgress (dars tugallanishi) — apps.learning
  * Project / ProjectFile (Loyihalar bo'limi)       — apps.projects

Yangi jadvallar (topshiriqdagi nomlarga mosligi):
  LessonBlock      ≈ LessonContentBlocks + LessonExamples (code turidagi blok — interaktiv misol)
  Task             ≈ Assignments + QuizQuestions (barcha topshiriq turlari uchun yagona jadval)
  TaskOption       ≈ QuizOptions
  TaskTest         ≈ AssignmentTests
  TaskAttempt      ≈ StudentSubmissions + StudentQuizAttempts (har bir urinish alohida yozuv)
  TaskProgress     — o'quvchining har bir topshiriq bo'yicha umumiy holati (urinishlar soni, yechilganmi)
  CodeDraft        — muharrirdagi kodni avtomatik saqlash
  ModuleAssessment ≈ ModuleAssessments
  AssessmentItem   — nazoratga kiritilgan topshiriqlar (tartib bilan)
  AssessmentAttempt ≈ StudentModuleResults
"""
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.courses.models import CourseModule, Lesson
from apps.users.models import CustomUser


# ==============================================================================
# DARS KONTENT BLOKLARI
# ==============================================================================

class BlockType(models.TextChoices):
    TEXT = 'text', "Matn (Markdown: sarlavha, ro'yxat, jadval, rasm, kod bloki)"
    CALLOUT = 'callout', "Ajratilgan eslatma (muhim, maslahat, ogohlantirish)"
    CODE = 'code', "Interaktiv kod misoli"
    IMAGE = 'image', "Rasm"
    VIDEO = 'video', "Video"
    TASK = 'task', "Dars ichidagi mashq (topshiriqqa havola)"


class CalloutStyle(models.TextChoices):
    INFO = 'info', "Ma'lumot"
    TIP = 'tip', "Maslahat"
    IMPORTANT = 'important', "Muhim"
    WARNING = 'warning', "Ogohlantirish"
    ANALOGY = 'analogy', "Hayotiy misol / o'xshatish"


class LessonBlock(TimeStampedModel):
    """Dars nazariyasining tartiblangan qismi. Admin bloklarni qo'shadi, tahrirlaydi va tartiblaydi."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='blocks', verbose_name="Dars")
    block_type = models.CharField(max_length=20, choices=BlockType.choices, default=BlockType.TEXT, verbose_name="Blok turi")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")
    title = models.CharField(max_length=200, blank=True, verbose_name="Sarlavha (ixtiyoriy)")
    body = models.TextField(blank=True, verbose_name="Matn (Markdown)")
    callout_style = models.CharField(
        max_length=20, choices=CalloutStyle.choices, default=CalloutStyle.INFO, blank=True,
        verbose_name="Eslatma uslubi"
    )
    code = models.TextField(blank=True, verbose_name="Kod (interaktiv misol uchun)")
    is_runnable = models.BooleanField(default=True, verbose_name="Ishga tushirish va muharrirga yuklash mumkinmi?")
    image = models.ImageField(upload_to='lessons/blocks/%Y/%m/', blank=True, null=True, verbose_name="Rasm")
    video_url = models.URLField(blank=True, verbose_name="Video havolasi (YouTube/Vimeo)")
    task = models.ForeignKey(
        'Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='embedded_blocks',
        verbose_name="Mashq (topshiriq)"
    )

    class Meta:
        verbose_name = "Dars bloki"
        verbose_name_plural = "Dars bloklari"
        ordering = ['lesson', 'order', 'id']
        indexes = [models.Index(fields=['lesson', 'order'], name='lessonblock_lesson_order_idx')]

    def __str__(self):
        return f"{self.lesson.title} — #{self.order} {self.get_block_type_display()}"

    def clean(self):
        errors = {}
        if self.block_type in (BlockType.TEXT, BlockType.CALLOUT) and not (self.body or '').strip():
            errors['body'] = "Bu blok turi uchun matn kiritilishi shart."
        if self.block_type == BlockType.CODE and not (self.code or '').strip():
            errors['code'] = "Kod misoli bo'sh bo'lmasligi kerak."
        if self.block_type == BlockType.IMAGE and not self.image:
            errors['image'] = "Rasm yuklang."
        if self.block_type == BlockType.VIDEO and not self.video_url:
            errors['video_url'] = "Video havolasini kiriting."
        if self.block_type == BlockType.TASK:
            if not self.task_id:
                errors['task'] = "Mashqni tanlang."
            elif self.task.lesson_id and self.lesson_id and self.task.lesson_id != self.lesson_id:
                errors['task'] = "Tanlangan mashq boshqa darsga tegishli."
        if errors:
            raise ValidationError(errors)

    @property
    def embed_url(self):
        from apps.courses.models import VIMEO_RE, YOUTUBE_RE
        if not self.video_url:
            return ''
        m = YOUTUBE_RE.search(self.video_url)
        if m:
            return f"https://www.youtube-nocookie.com/embed/{m.group(1)}?rel=0&modestbranding=1"
        m = VIMEO_RE.search(self.video_url)
        if m:
            return f"https://player.vimeo.com/video/{m.group(1)}"
        return ''


# ==============================================================================
# TOPSHIRIQLAR (test savollari, mashqlar, vazifalar, nazorat savollari)
# ==============================================================================

class TaskSection(models.TextChoices):
    INLINE = 'inline', "Dars ichidagi mashq"
    QUIZ = 'quiz', "Nazariy test savoli"
    ASSIGNMENT = 'assignment', "Mustaqil amaliy vazifa"
    PRACTICE = 'practice', "Qo'shimcha mashq"
    REVIEW = 'review', "Takrorlash savoli"
    ASSESSMENT = 'assessment', "Modul nazorati savoli"
    PROJECT = 'project', "Mini-loyiha"


SECTION_LABEL_SHORT = {
    TaskSection.INLINE: 'Mashq',
    TaskSection.QUIZ: 'Test',
    TaskSection.ASSIGNMENT: 'Vazifa',
    TaskSection.PRACTICE: "Qo'shimcha",
    TaskSection.REVIEW: 'Takrorlash',
    TaskSection.ASSESSMENT: 'Savol',
    TaskSection.PROJECT: 'Loyiha',
}


class TaskKind(models.TextChoices):
    SINGLE_CHOICE = 'single_choice', "Bir javobli test"
    MULTIPLE_CHOICE = 'multiple_choice', "Bir nechta javobli test"
    PREDICT_OUTPUT = 'predict_output', "Kod natijasini aniqlash"
    FILL_BLANK = 'fill_blank', "Bo'sh joyni to'ldirish"
    FIND_ERROR = 'find_error', "Xatoni topish va tuzatish"
    CODE = 'code', "Python kod yozish"


CHOICE_KINDS = {TaskKind.SINGLE_CHOICE, TaskKind.MULTIPLE_CHOICE}
CODE_KINDS = {TaskKind.FIND_ERROR, TaskKind.CODE}


class Difficulty(models.TextChoices):
    EASY = 'easy', "Oson"
    MEDIUM = 'medium', "O'rta"
    HARD = 'hard', "Qiyin"


BLANK_TOKEN = '___'


class Task(TimeStampedModel):
    """
    Har qanday topshiriq: test savoli, kod natijasini topish, bo'sh joyni to'ldirish,
    xatoni tuzatish yoki to'liq dastur yozish. Darsga (yoki modul nazoratiga) biriktiriladi.
    """
    module = models.ForeignKey(
        CourseModule, on_delete=models.CASCADE, related_name='tasks', blank=True,
        verbose_name="Modul",
        help_text="Darsga biriktirilgan topshiriqlarda avtomatik to'ldiriladi."
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True,
        verbose_name="Dars",
        help_text="Modul yakuniy nazorati uchun maxsus savollarda bo'sh qoldirilishi mumkin."
    )
    section = models.CharField(max_length=20, choices=TaskSection.choices, default=TaskSection.QUIZ, verbose_name="Bo'lim")
    kind = models.CharField(max_length=20, choices=TaskKind.choices, default=TaskKind.SINGLE_CHOICE, verbose_name="Topshiriq turi")
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY, verbose_name="Qiyinlik darajasi")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")

    title = models.CharField(max_length=200, verbose_name="Topshiriq nomi")
    prompt = models.TextField(verbose_name="Shart / savol (Markdown)")
    code_snippet = models.TextField(
        blank=True, verbose_name="Ko'rsatiladigan kod",
        help_text="«Natijani aniqlash» va «Bo'sh joyni to'ldirish» uchun. Bo'sh joylarni ___ (3 ta pastki chiziq) bilan belgilang."
    )
    starter_code = models.TextField(
        blank=True, verbose_name="Muharrirdagi boshlang'ich kod",
        help_text="«Xatoni tuzatish» uchun — xatoli kod; «Kod yozish» uchun — shablon."
    )
    expected_output_example = models.TextField(blank=True, verbose_name="Kutilayotgan natija namunasi (o'quvchiga ko'rsatiladi)")
    correct_answer = models.TextField(
        blank=True, verbose_name="To'g'ri javob",
        help_text="«Natijani aniqlash»: dasturning to'liq chiqishi. «Bo'sh joy»: har bir bo'sh joy uchun alohida qator, "
                  "muqobil javoblar | bilan ajratiladi (masalan: sep=\"-\" | sep='-')."
    )
    hint = models.TextField(blank=True, verbose_name="Maslahat (hint)")
    partial_solution = models.TextField(blank=True, verbose_name="Qisman yechim")
    full_solution = models.TextField(blank=True, verbose_name="To'liq yechim")
    explanation = models.TextField(blank=True, verbose_name="Tushuntirish (javobdan keyin ko'rsatiladi, Markdown)")

    points = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="Ball")
    solution_unlock_attempts = models.PositiveSmallIntegerField(
        default=2, validators=[MaxValueValidator(20)],
        verbose_name="To'liq yechim ochilishi uchun urinishlar soni",
        help_text="O'quvchi shuncha marta mustaqil urinib ko'rgach to'liq yechimni ko'ra oladi (0 — darhol)."
    )
    is_published = models.BooleanField(default=True, verbose_name="Nashr qilinganmi?")

    class Meta:
        verbose_name = "Topshiriq"
        verbose_name_plural = "Topshiriqlar"
        ordering = ['module__order', 'lesson__order', 'section', 'order', 'id']
        indexes = [
            models.Index(fields=['lesson', 'section', 'order'], name='task_lesson_section_idx'),
            models.Index(fields=['module', 'section'], name='task_module_section_idx'),
        ]

    def __str__(self):
        return f"{self.logical_name} — {self.title}"

    # ---- yordamchi xususiyatlar ----
    @property
    def is_choice(self):
        return self.kind in CHOICE_KINDS

    @property
    def is_code(self):
        return self.kind in CODE_KINDS

    @property
    def uses_editor(self):
        return self.kind in CODE_KINDS

    @property
    def blank_count(self):
        return (self.code_snippet or '').count(BLANK_TOKEN)

    @property
    def accepted_blank_answers(self):
        """[[muqobil1, muqobil2], [..], ...] — har bir bo'sh joy uchun."""
        rows = [r for r in (self.correct_answer or '').splitlines() if r.strip()]
        return [[alt.strip() for alt in row.split('|') if alt.strip()] for row in rows]

    @property
    def logical_name(self):
        """Masalan: «Python / 1-modul / 3-dars / Vazifa-1»."""
        course_title = self.module.course.title if self.module_id else ''
        course_label = course_title.split('—')[0].split('-')[0].strip() or course_title
        module_part = f"{self.module.order}-modul" if self.module_id else '?-modul'
        label = SECTION_LABEL_SHORT.get(self.section, 'Topshiriq')
        if self.lesson_id:
            siblings = Task.objects.filter(lesson_id=self.lesson_id, section=self.section).order_by('order', 'id')
            middle = f"{self.lesson.order}-dars"
        else:
            siblings = Task.objects.filter(module_id=self.module_id, lesson__isnull=True, section=self.section).order_by('order', 'id')
            middle = "Yakuniy nazorat"
        ids = list(siblings.values_list('id', flat=True))
        number = ids.index(self.id) + 1 if self.id in ids else len(ids) + 1
        return f"{course_label} / {module_part} / {middle} / {label}-{number}"

    def clean(self):
        errors = {}
        if self.lesson_id:
            self.module_id = self.lesson.module_id
        if not self.module_id:
            errors['module'] = "Modul yoki darsni tanlang."
        if self.kind in (TaskKind.PREDICT_OUTPUT,) and not (self.code_snippet or '').strip():
            errors['code_snippet'] = "Natijasi aniqlanadigan kodni kiriting."
        if self.kind == TaskKind.PREDICT_OUTPUT and not (self.correct_answer or '').strip():
            errors['correct_answer'] = "Kodning to'g'ri natijasini kiriting."
        if self.kind == TaskKind.FILL_BLANK:
            if self.blank_count == 0:
                errors['code_snippet'] = "Kodda kamida bitta ___ bo'sh joy bo'lishi kerak."
        if self.kind == TaskKind.FIND_ERROR and not (self.starter_code or '').strip():
            errors['starter_code'] = "Tuzatiladigan (xatoli) kodni kiriting."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.lesson_id and not self.module_id:
            self.module_id = Lesson.objects.filter(pk=self.lesson_id).values_list('module_id', flat=True).first()
        elif self.lesson_id:
            lesson_module = Lesson.objects.filter(pk=self.lesson_id).values_list('module_id', flat=True).first()
            if lesson_module:
                self.module_id = lesson_module
        super().save(*args, **kwargs)

    def validate_configuration(self):
        """Saqlangandan keyingi tekshiruv (variantlar/testlar mavjudligi). Xatolar ro'yxatini qaytaradi."""
        problems = []
        if self.is_choice:
            options = list(self.options.all())
            correct = [o for o in options if o.is_correct]
            if len(options) < 2:
                problems.append("Testda kamida 2 ta javob varianti bo'lishi kerak.")
            if not correct:
                problems.append("Kamida bitta to'g'ri javob belgilanishi kerak.")
            if self.kind == TaskKind.SINGLE_CHOICE and len(correct) > 1:
                problems.append("Bir javobli testda faqat bitta to'g'ri javob bo'lishi mumkin.")
        if self.is_code and not self.tests.exists():
            problems.append("Kod topshirig'i uchun kamida bitta avtomatik test qo'shing.")
        if self.kind == TaskKind.FILL_BLANK and not self.tests.exists():
            if len(self.accepted_blank_answers) != self.blank_count:
                problems.append("Har bir ___ bo'sh joy uchun to'g'ri javob qatori bo'lishi kerak (yoki testlar qo'shing).")
        return problems


class TaskOption(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='options', verbose_name="Topshiriq")
    text = models.TextField(verbose_name="Javob varianti")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javobmi?")
    feedback = models.CharField(max_length=500, blank=True, verbose_name="Shu variant tanlanganda izoh")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib")

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"
        ordering = ['task', 'order', 'id']

    def __str__(self):
        return f"{'✔' if self.is_correct else '✘'} {self.text[:60]}"


class TestCheck(models.TextChoices):
    OUTPUT_EQUALS = 'output_equals', "Chiqish aynan teng"
    OUTPUT_CONTAINS = 'output_contains', "Chiqishda matn bor"
    OUTPUT_NOT_CONTAINS = 'output_not_contains', "Chiqishda matn yo'q"
    OUTPUT_REGEX = 'output_regex', "Chiqish regex'ga mos"
    OUTPUT_LINES_MIN = 'output_lines_min', "Kamida N ta bo'sh bo'lmagan qator"
    CODE_CONTAINS = 'code_contains', "Kodda matn bor"
    CODE_NOT_CONTAINS = 'code_not_contains', "Kodda matn yo'q"
    CODE_REGEX = 'code_regex', "Kod regex'ga mos"
    RUNS_OK = 'runs_ok', "Dastur xatosiz ishlaydi"


RUN_CHECKS = {
    TestCheck.OUTPUT_EQUALS, TestCheck.OUTPUT_CONTAINS, TestCheck.OUTPUT_NOT_CONTAINS,
    TestCheck.OUTPUT_REGEX, TestCheck.OUTPUT_LINES_MIN, TestCheck.RUNS_OK,
}


class TaskTest(TimeStampedModel):
    """Kod topshirig'ini avtomatik tekshirish uchun test holati."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tests', verbose_name="Topshiriq")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib")
    description = models.CharField(max_length=300, verbose_name="Test tavsifi (o'quvchiga ko'rinadi)")
    check_type = models.CharField(max_length=30, choices=TestCheck.choices, default=TestCheck.OUTPUT_EQUALS, verbose_name="Tekshirish turi")
    stdin = models.TextField(blank=True, verbose_name="Kiritish (input) ma'lumotlari")
    expected = models.TextField(blank=True, verbose_name="Kutilgan qiymat")
    ignore_case = models.BooleanField(default=False, verbose_name="Katta-kichik harf farqlanmasin")
    is_hidden = models.BooleanField(default=False, verbose_name="Yashirin test", help_text="O'quvchi faqat o'tdi/o'tmadi natijasini ko'radi.")
    failure_message = models.CharField(max_length=500, blank=True, verbose_name="Test o'tmaganda maslahat")

    class Meta:
        verbose_name = "Avtomatik test"
        verbose_name_plural = "Avtomatik testlar"
        ordering = ['task', 'order', 'id']

    def __str__(self):
        return f"{self.task.title}: {self.description}"

    @property
    def needs_run(self):
        return self.check_type in RUN_CHECKS

    def clean(self):
        import re
        if self.check_type in (TestCheck.OUTPUT_REGEX, TestCheck.CODE_REGEX):
            try:
                re.compile(self.expected)
            except re.error as exc:
                raise ValidationError({'expected': f"Regex noto'g'ri: {exc}"})
        if self.check_type == TestCheck.OUTPUT_LINES_MIN:
            if not (self.expected or '').strip().isdigit():
                raise ValidationError({'expected': "Qatorlar sonini butun son sifatida kiriting."})
        if self.check_type not in (TestCheck.RUNS_OK,) and not (self.expected or '') and self.check_type != TestCheck.OUTPUT_EQUALS:
            raise ValidationError({'expected': "Kutilgan qiymatni kiriting."})


# ==============================================================================
# O'QUVCHI NATIJALARI
# ==============================================================================

class TaskProgressStatus(models.TextChoices):
    ATTEMPTED = 'attempted', "Urinilgan"
    SOLVED = 'solved', "Yechilgan"


class TaskProgress(TimeStampedModel):
    """O'quvchining topshiriq bo'yicha umumiy holati (har bir o'quvchi uchun alohida)."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_progress', verbose_name="O'quvchi")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress_records', verbose_name="Topshiriq")
    status = models.CharField(max_length=20, choices=TaskProgressStatus.choices, default=TaskProgressStatus.ATTEMPTED, verbose_name="Holati")
    attempts_count = models.PositiveIntegerField(default=0, verbose_name="Urinishlar soni")
    best_score = models.FloatField(default=0, verbose_name="Eng yaxshi ball")
    solved_at = models.DateTimeField(null=True, blank=True, verbose_name="Yechilgan vaqt")
    hint_viewed = models.BooleanField(default=False, verbose_name="Maslahat ko'rilgan")
    partial_viewed = models.BooleanField(default=False, verbose_name="Qisman yechim ko'rilgan")
    solution_viewed = models.BooleanField(default=False, verbose_name="To'liq yechim ko'rilgan")

    class Meta:
        verbose_name = "Topshiriq holati"
        verbose_name_plural = "Topshiriq holatlari"
        constraints = [models.UniqueConstraint(fields=['user', 'task'], name='unique_task_progress_per_user')]

    def __str__(self):
        return f"{self.user.email}: {self.task.title} ({self.get_status_display()})"

    @property
    def is_solved(self):
        return self.status == TaskProgressStatus.SOLVED


class AttemptContext(models.TextChoices):
    LESSON = 'lesson', "Dars"
    ASSESSMENT = 'assessment', "Modul nazorati"


class TaskAttempt(TimeStampedModel):
    """Har bir topshirish (urinish) alohida saqlanadi: kod/javob, vaqt, test natijalari."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_attempts', verbose_name="O'quvchi")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attempts', verbose_name="Topshiriq")
    context = models.CharField(max_length=20, choices=AttemptContext.choices, default=AttemptContext.LESSON, verbose_name="Qayerda")
    assessment_attempt = models.ForeignKey(
        'AssessmentAttempt', on_delete=models.CASCADE, null=True, blank=True, related_name='answers',
        verbose_name="Nazorat urinishi"
    )
    attempt_number = models.PositiveIntegerField(default=1, verbose_name="Urinish raqami")
    answer = models.JSONField(default=dict, blank=True, verbose_name="Javob (variantlar / matn)")
    code = models.TextField(blank=True, verbose_name="Yuborilgan kod")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'rimi?")
    score = models.FloatField(default=0, verbose_name="Olingan ball")
    max_score = models.FloatField(default=0, verbose_name="Maksimal ball")
    test_results = models.JSONField(default=list, blank=True, verbose_name="Test natijalari")
    output = models.TextField(blank=True, verbose_name="Dastur chiqishi (qisqartirilgan)")

    class Meta:
        verbose_name = "Topshiriq urinishi"
        verbose_name_plural = "Topshiriq urinishlari"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'task', '-created_at'], name='attempt_user_task_idx')]

    def __str__(self):
        return f"{self.user.email} → {self.task.title} #{self.attempt_number} ({'✔' if self.is_correct else '✘'})"


class CodeDraft(TimeStampedModel):
    """Muharrirdagi kodni avtomatik saqlash (dars maydoni, misollar, vazifalar)."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='code_drafts')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='code_drafts', null=True, blank=True)
    key = models.CharField(max_length=60, verbose_name="Muharrir kaliti")
    code = models.TextField(blank=True)

    class Meta:
        verbose_name = "Kod qoralamasi"
        verbose_name_plural = "Kod qoralamalari"
        constraints = [models.UniqueConstraint(fields=['user', 'lesson', 'key'], name='unique_code_draft')]

    def __str__(self):
        return f"{self.user.email}: {self.key}"


# ==============================================================================
# MODUL YAKUNIY NAZORATI
# ==============================================================================

class ModuleAssessment(TimeStampedModel):
    module = models.OneToOneField(CourseModule, on_delete=models.CASCADE, related_name='assessment', verbose_name="Modul")
    title = models.CharField(max_length=200, verbose_name="Nazorat nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif (Markdown)")
    pass_percent = models.PositiveSmallIntegerField(
        default=70, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="O'tish foizi (%)"
    )
    max_attempts = models.PositiveSmallIntegerField(default=0, verbose_name="Maksimal urinishlar (0 — cheksiz)")
    require_all_lessons = models.BooleanField(
        default=True, verbose_name="Barcha darslar tugallangandan keyin ochilsin"
    )
    is_published = models.BooleanField(default=True, verbose_name="Nashr qilinganmi?")
    tasks = models.ManyToManyField(Task, through='AssessmentItem', related_name='assessments', blank=True)

    class Meta:
        verbose_name = "Modul yakuniy nazorati"
        verbose_name_plural = "Modul yakuniy nazoratlari"

    def __str__(self):
        return f"{self.module} — {self.title}"

    def ordered_items(self):
        return self.items.select_related('task').prefetch_related('task__options', 'task__tests').order_by('order', 'id')

    @property
    def max_score(self):
        return sum(item.task.points for item in self.items.select_related('task'))


class AssessmentItem(models.Model):
    assessment = models.ForeignKey(ModuleAssessment, on_delete=models.CASCADE, related_name='items')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assessment_items')
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib")

    class Meta:
        verbose_name = "Nazorat savoli"
        verbose_name_plural = "Nazorat savollari"
        ordering = ['order', 'id']
        constraints = [models.UniqueConstraint(fields=['assessment', 'task'], name='unique_assessment_task')]

    def clean(self):
        if self.task_id and self.assessment_id and self.task.module_id != self.assessment.module_id:
            raise ValidationError({'task': "Topshiriq shu modulga tegishli bo'lishi kerak."})

    def __str__(self):
        return f"{self.assessment.title}: {self.task.title}"


class AssessmentAttempt(TimeStampedModel):
    """O'quvchining modul nazoratidagi har bir urinishi va natijasi."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assessment_attempts', verbose_name="O'quvchi")
    assessment = models.ForeignKey(ModuleAssessment, on_delete=models.CASCADE, related_name='attempts', verbose_name="Nazorat")
    attempt_number = models.PositiveIntegerField(default=1)
    score = models.FloatField(default=0, verbose_name="Ball")
    max_score = models.FloatField(default=0, verbose_name="Maksimal ball")
    percent = models.FloatField(default=0, verbose_name="Foiz")
    pass_percent = models.PositiveSmallIntegerField(default=70, verbose_name="O'tish foizi (urinish paytida)")
    passed = models.BooleanField(default=False, verbose_name="O'tdimi?")

    class Meta:
        verbose_name = "Nazorat natijasi"
        verbose_name_plural = "Nazorat natijalari"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'assessment', '-created_at'], name='assess_attempt_user_idx')]

    def __str__(self):
        verdict = "o'tdi" if self.passed else "o'tmadi"
        return f"{self.user.email}: {self.assessment.title} — {self.percent:.0f}% ({verdict})"
