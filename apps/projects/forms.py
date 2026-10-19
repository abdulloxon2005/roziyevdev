from django import forms
from .models import Project, ProjectType, ProjectLanguage, ProjectMode


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'language', 'project_mode', 'course']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-purple-500 outline-none text-slate-900 dark:text-white font-semibold',
                'placeholder': 'Masalan: Bank Boshqaruv Tizimi yoki Kalkulyator'
            }),
            'language': forms.Select(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-purple-500 outline-none text-slate-900 dark:text-white font-semibold'
            }),
            'project_mode': forms.Select(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-purple-500 outline-none text-slate-900 dark:text-white font-semibold'
            }),
            'course': forms.Select(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-purple-500 outline-none text-slate-900 dark:text-white font-semibold'
            }),
        }


class ProjectSubmissionForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'title',
            'course',
            'tagline',
            'description',
            'tech_stack',
            'github_url',
            'demo_url',
            'project_type',
            'thumbnail',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white',
                'placeholder': 'Masalan: E-Bozor — Mobil Yetkazib Berish Ilovasi'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white',
                'placeholder': 'Loyihaning qisqacha bir jumlali shiori'
            }),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white',
                'placeholder': 'Loyiha haqida batafsil ma\'lumot, arxitekturasi, imkoniyatlari (Markdown qo\'llab-quvvatlanadi)...'
            }),
            'tech_stack': forms.TextInput(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white',
                'placeholder': 'Flutter, BLoC, Django REST, PostgreSQL, Docker'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white',
                'placeholder': 'https://github.com/username/project-repo'
            }),
            'demo_url': forms.URLInput(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white',
                'placeholder': 'https://my-demo-app.uz yoki Google Play / TestFlight havolasi'
            }),
            'project_type': forms.Select(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white'
            }),
            'course': forms.Select(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 dark:text-white'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-500 cursor-pointer text-slate-900 dark:text-white'
            }),
        }
