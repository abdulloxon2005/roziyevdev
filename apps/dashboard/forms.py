from django import forms
from apps.courses.models import Course, CourseModule, Lesson, Category
from apps.learning.models import Assignment


class TailwindFormMixin:
    """Barcha forma maydonlariga chiroyli Tailwind CSS klasslarini avtomatik biriktiradi."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({
                    'class': 'w-5 h-5 text-blue-600 bg-slate-100 dark:bg-slate-800 border-slate-300 dark:border-slate-700 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer'
                })
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.update({
                    'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors'
                })
            elif isinstance(widget, forms.FileInput):
                widget.attrs.update({
                    'class': 'block w-full text-sm text-slate-500 dark:text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 dark:file:bg-blue-900/30 dark:file:text-blue-300 hover:file:bg-blue-100 cursor-pointer'
                })
            else:
                widget.attrs.update({
                    'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-slate-400 dark:placeholder-slate-500 transition-colors'
                })


class CourseForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'category',
            'level',
            'price',
            'is_free',
            'duration_hours',
            'thumbnail',
            'short_description',
            'description',
            'what_you_will_learn',
            'requirements',
            'is_published',
            'is_featured',
        ]
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 2, 'placeholder': "Kurs haqida qisqacha ma'lumot (kartochkalar uchun)..."}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': "Kursning to'liq dasturi, mavzulari va afzalliklari (Markdown qo'llab-quvvatlanadi)..."}),
            'what_you_will_learn': forms.Textarea(attrs={'rows': 4, 'placeholder': "Har bir o'rganiladigan bilimlarni yangi qatordan yozing:\n- Dart dasturlash tili sintaksisi\n- Flutter UI vidjetlari\n- REST API integratsiyasi"}),
            'requirements': forms.Textarea(attrs={'rows': 3, 'placeholder': "Har bir talabni yangi qatordan yozing:\n- Dasturlash asoslaridan xabardorlik\n- Shaxsiy kompyuter va internet"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_free = cleaned_data.get('is_free')
        price = cleaned_data.get('price') or 0
        if is_free:
            cleaned_data['price'] = 0
        elif price < 0:
            self.add_error('price', "Kurs narxi musbat son bo'lishi kerak.")
        return cleaned_data


class CourseModuleForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = CourseModule
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Masalan: 1-bo'lim: Kirish va asosiy tushunchalar"}),
            'order': forms.NumberInput(attrs={'min': 1}),
        }


class LessonForm(TailwindFormMixin, forms.ModelForm):
    # Darsga biriktirilgan Vazifa (Assignment) parametrlari
    has_assignment = forms.BooleanField(
        required=False,
        label="Ushbu darsga amaliy vazifa biriktirish",
        help_text="Belgilansa, talaba dars oxirida topshirishi uchun amaliy topshiriq faollashadi."
    )
    assignment_title = forms.CharField(
        required=False,
        max_length=250,
        label="Vazifa nomi",
        widget=forms.TextInput(attrs={'placeholder': "Masalan: Algoritmik ifodalarni kodda yozish"})
    )
    assignment_description = forms.CharField(
        required=False,
        label="Vazifa sharti va topshiriq ko'rsatmasi (Markdown)",
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': "Vazifaning to'liq sharti, kiritish/chiqarish ma'lumotlari..."})
    )
    starter_code = forms.CharField(
        required=False,
        label="Boshlang'ich kod shabloni (Starter Code)",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': "void main() {\n  // kodingizni bu yerga yozing\n}"})
    )
    coin_reward = forms.IntegerField(
        required=False,
        initial=50,
        min_value=0,
        label="Mukofot tangachalari (Coins)",
        help_text="Vazifa qabul qilinganda o'quvchiga beriladigan tangalar soni"
    )
    max_score = forms.IntegerField(
        required=False,
        initial=100,
        min_value=1,
        max_value=1000,
        label="Maksimal ball"
    )
    passing_score = forms.IntegerField(
        required=False,
        initial=70,
        min_value=1,
        max_value=1000,
        label="O'tish bali"
    )
    allow_code = forms.BooleanField(
        required=False,
        initial=True,
        label="Kod orqali topshirish yoqilgan"
    )
    allow_flowchart = forms.BooleanField(
        required=False,
        initial=True,
        label="Blok-sxema (Flowgorithm) orqali topshirish yoqilgan"
    )
    allow_file_upload = forms.BooleanField(
        required=False,
        initial=True,
        label="Fayl yuklash (arxiv, kod, hujjat) orqali topshirish yoqilgan"
    )
    assignment_is_active = forms.BooleanField(
        required=False,
        initial=True,
        label="Vazifa faolmi?"
    )

    class Meta:
        model = Lesson
        fields = [
            'module',
            'title',
            'lesson_type',
            'video_file',
            'video_url',
            'content',
            'attachment',
            'source_code_url',
            'duration_minutes',
            'is_preview',
            'order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Masalan: 1.1. Dart dasturlash tiliga kirish"}),
            'video_url': forms.URLInput(attrs={'placeholder': "https://www.youtube.com/watch?v=... yoki Vimeo"}),
            'source_code_url': forms.URLInput(attrs={'placeholder': "https://github.com/foydalanuvchi/loyiha"}),
            'content': forms.Textarea(attrs={'rows': 6, 'placeholder': "Dars konspekti, formulalar, izohlar (Markdown)..."}),
            'duration_minutes': forms.NumberInput(attrs={'min': 1}),
            'order': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, course=None, **kwargs):
        super().__init__(*args, **kwargs)
        if course:
            self.fields['module'].queryset = CourseModule.objects.filter(course=course).order_by('order')

        # Agar dars allaqachon mavjud bo'lsa va unga assignment biriktirilgan bo'lsa, qiymatlarini to'ldirish
        if self.instance and self.instance.pk:
            try:
                assignment = getattr(self.instance, 'assignment', None)
            except Exception:
                assignment = None
            if assignment:
                self.fields['has_assignment'].initial = True
                self.fields['assignment_title'].initial = assignment.title
                self.fields['assignment_description'].initial = assignment.description
                self.fields['starter_code'].initial = assignment.starter_code
                self.fields['coin_reward'].initial = assignment.coin_reward
                self.fields['max_score'].initial = assignment.max_score
                self.fields['passing_score'].initial = assignment.passing_score
                self.fields['allow_code'].initial = assignment.allow_code
                self.fields['allow_flowchart'].initial = assignment.allow_flowchart
                self.fields['allow_file_upload'].initial = assignment.allow_file_upload
                self.fields['assignment_is_active'].initial = assignment.is_active

    def clean(self):
        cleaned_data = super().clean()
        has_assignment = cleaned_data.get('has_assignment')
        if has_assignment:
            title = cleaned_data.get('assignment_title')
            desc = cleaned_data.get('assignment_description')
            if not title:
                self.add_error('assignment_title', "Vazifa nomini kiritish majburiy.")
            if not desc:
                self.add_error('assignment_description', "Vazifa shartini (tavsifini) kiritish majburiy.")

            allow_code = cleaned_data.get('allow_code')
            allow_flowchart = cleaned_data.get('allow_flowchart')
            allow_file_upload = cleaned_data.get('allow_file_upload')
            if not (allow_code or allow_flowchart or allow_file_upload):
                self.add_error('allow_code', "Kamida bitta topshirish usulini (kod, blok-sxema yoki fayl) yoqishingiz kerak.")
        return cleaned_data

    def save_assignment(self, lesson):
        """Dars saqlangandan so'ng unga tegishli vazifani saqlash yoki yangilash."""
        has_assignment = self.cleaned_data.get('has_assignment')
        try:
            assignment = getattr(lesson, 'assignment', None)
        except Exception:
            assignment = None

        if has_assignment:
            if not assignment:
                assignment = Assignment(lesson=lesson)
            assignment.title = self.cleaned_data.get('assignment_title') or f"{lesson.title} - Vazifasi"
            assignment.description = self.cleaned_data.get('assignment_description') or ""
            assignment.starter_code = self.cleaned_data.get('starter_code') or ""
            assignment.coin_reward = self.cleaned_data.get('coin_reward') or 50
            assignment.max_score = self.cleaned_data.get('max_score') or 100
            assignment.passing_score = self.cleaned_data.get('passing_score') or 70
            assignment.allow_code = self.cleaned_data.get('allow_code', True)
            assignment.allow_flowchart = self.cleaned_data.get('allow_flowchart', True)
            assignment.allow_file_upload = self.cleaned_data.get('allow_file_upload', True)
            assignment.is_active = self.cleaned_data.get('assignment_is_active', True)
            assignment.save()
            return assignment
        else:
            # Agar mavjud bo'lsa va o'chirilgan bo'lsa, is_active=False qilib qo'yish (yechimlarni yo'qotmaslik uchun)
            if assignment:
                assignment.is_active = False
                assignment.save()
            return None
