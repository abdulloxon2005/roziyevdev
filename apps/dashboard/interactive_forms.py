"""Ustoz Studiyasi: interaktiv dars kontenti, topshiriqlar va modul nazorati formalari."""
from django import forms
from django.forms import inlineformset_factory

from apps.interactive.models import (
    LessonBlock,
    ModuleAssessment,
    Task,
    TaskOption,
    TaskTest,
)

from .forms import TailwindFormMixin

MONO = 'font-mono text-[13px]'


def _mono(widget):
    widget.attrs['class'] = (widget.attrs.get('class', '') + ' ' + MONO).strip()
    widget.attrs['spellcheck'] = 'false'
    return widget


class LessonBlockForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = LessonBlock
        fields = ['block_type', 'order', 'title', 'callout_style', 'body', 'code', 'is_runnable', 'image', 'video_url', 'task']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 6, 'placeholder': "Markdown: ## Sarlavha, **qalin**, - ro'yxat, | jadval |, ```python kod```, ![rasm](url)"}),
            'code': forms.Textarea(attrs={'rows': 5, 'placeholder': 'print("Salom, dunyo!")'}),
            'order': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, lesson=None, **kwargs):
        super().__init__(*args, **kwargs)
        _mono(self.fields['code'].widget)
        self.fields['task'].required = False
        self.fields['callout_style'].required = False
        if lesson is not None:
            self.fields['task'].queryset = Task.objects.filter(lesson=lesson).order_by('section', 'order')
            self.instance.lesson = lesson


class TaskForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'lesson', 'section', 'kind', 'difficulty', 'order', 'points', 'is_published',
            'title', 'prompt', 'code_snippet', 'starter_code', 'expected_output_example', 'correct_answer',
            'hint', 'partial_solution', 'full_solution', 'solution_unlock_attempts', 'explanation',
        ]
        widgets = {
            'prompt': forms.Textarea(attrs={'rows': 5}),
            'code_snippet': forms.Textarea(attrs={'rows': 5}),
            'starter_code': forms.Textarea(attrs={'rows': 5}),
            'expected_output_example': forms.Textarea(attrs={'rows': 3}),
            'correct_answer': forms.Textarea(attrs={'rows': 3}),
            'hint': forms.Textarea(attrs={'rows': 2}),
            'partial_solution': forms.Textarea(attrs={'rows': 4}),
            'full_solution': forms.Textarea(attrs={'rows': 6}),
            'explanation': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, module=None, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('code_snippet', 'starter_code', 'expected_output_example', 'correct_answer', 'partial_solution', 'full_solution'):
            _mono(self.fields[name].widget)
        if module is not None:
            self.fields['lesson'].queryset = module.lessons.order_by('order', 'id')
            self.instance.module = module
        self.fields['lesson'].required = False
        self.fields['lesson'].empty_label = "— Darsga bog'lanmagan (faqat modul nazorati uchun) —"


TaskOptionFormSet = inlineformset_factory(
    Task, TaskOption,
    fields=['order', 'text', 'is_correct', 'feedback'],
    extra=2, can_delete=True,
    widgets={'text': forms.Textarea(attrs={'rows': 1}), 'order': forms.NumberInput(attrs={'min': 1, 'style': 'width:4.5rem'})},
)

TaskTestFormSet = inlineformset_factory(
    Task, TaskTest,
    fields=['order', 'description', 'check_type', 'stdin', 'expected', 'ignore_case', 'is_hidden', 'failure_message'],
    extra=1, can_delete=True,
    widgets={
        'stdin': forms.Textarea(attrs={'rows': 1}),
        'expected': forms.Textarea(attrs={'rows': 2}),
        'order': forms.NumberInput(attrs={'min': 1, 'style': 'width:4.5rem'}),
    },
)


def style_formset(formset):
    """Inline formset maydonlariga Tailwind klasslarini qo'llash."""
    for form in formset.forms + [formset.empty_form]:
        for name, field in form.fields.items():
            w = field.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs['class'] = 'w-4 h-4 accent-blue-600'
            else:
                w.attrs['class'] = ('w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 '
                                    'text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500')
                if name in ('expected', 'stdin', 'text'):
                    w.attrs['class'] += ' ' + MONO
    return formset


class ModuleAssessmentForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = ModuleAssessment
        fields = ['title', 'description', 'pass_percent', 'max_attempts', 'require_all_lessons', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'pass_percent': forms.NumberInput(attrs={'min': 1, 'max': 100}),
            'max_attempts': forms.NumberInput(attrs={'min': 0}),
        }
