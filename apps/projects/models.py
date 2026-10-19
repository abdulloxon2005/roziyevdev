from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
from apps.users.models import CustomUser
from apps.courses.models import Course


class ProjectType(models.TextChoices):
    CAPSTONE = 'capstone', 'Kurs Bitiruv Loyihasi'
    PERSONAL = 'personal', 'Shaxsiy Portfolio Loyiha'
    OPEN_SOURCE = 'open_source', 'Ochiq Kodli Loyiha'


class ProjectStatus(models.TextChoices):
    DRAFT = 'draft', 'Qoralama'
    UNDER_REVIEW = 'under_review', 'Ko\'rib chiqilmoqda'
    APPROVED = 'approved', 'Tasdiqlangan & Nashr etilgan'
    FEATURED = 'featured', 'Sara Loyiha (Top Pick)'


class ProjectLanguage(models.TextChoices):
    PYTHON = 'python', 'Python'
    CSHARP = 'csharp', 'C#'
    JAVA = 'java', 'Java'
    CPP = 'cpp', 'C++'
    JAVASCRIPT = 'javascript', 'JavaScript'
    DART = 'dart', 'Dart'
    GO = 'go', 'Go'
    PHP = 'php', 'PHP'


class ProjectMode(models.TextChoices):
    MULTI_FILE = 'multi_file', "Ko'p faylli loyiha"
    CONSOLE = 'console', 'Konsol dastur'


class Project(TimeStampedModel):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="Muallif / O'quvchi"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_projects',
        verbose_name="Bog'langan Kurs (ixtiyoriy)"
    )
    title = models.CharField(max_length=200, verbose_name="Loyiha nomi")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    language = models.CharField(
        max_length=30,
        choices=ProjectLanguage.choices,
        default=ProjectLanguage.PYTHON,
        verbose_name="Dasturlash tili"
    )
    project_mode = models.CharField(
        max_length=30,
        choices=ProjectMode.choices,
        default=ProjectMode.MULTI_FILE,
        verbose_name="Loyiha tuzilishi"
    )
    tagline = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Qisqa shior / bir jumlali tavsif",
        help_text="Masalan: Flutter va Clean Architecture asosida qurilgan yetkazib berish ilovasi"
    )
    description = models.TextField(blank=True, default="", verbose_name="Batafsil tavsif (Markdown qo'llanadi)")
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Loyiha muqovasi (Skrinshot)"
    )
    tech_stack = models.CharField(
        max_length=300,
        blank=True,
        default="",
        verbose_name="Texnologiyalar to'plami",
        help_text="Vergul bilan ajratilgan holda: Flutter, BLoC, Django REST, PostgreSQL, Docker"
    )
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub repozitoriy havolasi")
    demo_url = models.URLField(blank=True, null=True, verbose_name="Jonli Demo / APK / Sayt havolasi")
    project_type = models.CharField(
        max_length=30,
        choices=ProjectType.choices,
        default=ProjectType.PERSONAL,
        verbose_name="Loyiha turi"
    )
    status = models.CharField(
        max_length=30,
        choices=ProjectStatus.choices,
        default=ProjectStatus.DRAFT,
        verbose_name="Holati"
    )
    is_submitted = models.BooleanField(default=False, verbose_name="Ustozga yuborilganmi")
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Yuborilgan vaqti")
    score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Ustoz bahosi (0-100)")
    instructor_review = models.TextField(blank=True, verbose_name="Ustoz taqrizi va tavsiyalari")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Yoqtirishlar soni")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")

    class Meta:
        verbose_name = "O'quvchi loyihasi"
        verbose_name_plural = "O'quvchilar loyihalari"
        ordering = ['-created_at']

    @property
    def is_featured_ordering(self):
        return 1 if self.status == ProjectStatus.FEATURED else 0

    @property
    def tags_list(self):
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        return "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80"

    def get_language_mode_for_ace(self):
        mapping = {
            'python': 'python',
            'csharp': 'csharp',
            'java': 'java',
            'cpp': 'c_cpp',
            'javascript': 'javascript',
            'dart': 'dart',
            'go': 'golang',
            'php': 'php',
        }
        return mapping.get(self.language, 'python')

    def create_default_files(self):
        """Loyiha uchun boshlang'ich fayllarni avtomatik yaratish."""
        if self.files.exists():
            return self.files.filter(is_folder=False).first()

        author_name = getattr(self.author, 'get_full_name', None)
        author_str = author_name() if callable(author_name) and author_name() else self.author.email

        if self.language == ProjectLanguage.PYTHON:
            if self.project_mode == ProjectMode.CONSOLE:
                starter = (
                    f'# {self.title} - Konsol Dasturi\n'
                    f'# Muallif: {author_str}\n\n'
                    'def main():\n'
                    '    print("=== Dastur ishga tushdi ===")\n'
                    '    ism = input("Ismingizni kiriting: ")\n'
                    '    print(f"Salom, {ism}! Xush kelibsiz.")\n\n'
                    '    yosh = int(input("Yoshingizni kiriting: "))\n'
                    '    if yosh >= 18:\n'
                    '        print("Siz voyaga yetgansiz.")\n'
                    '    else:\n'
                    '        print("Siz hali voyaga yetmagansiz.")\n\n'
                    '    print("=== Dastur yakunlandi ===")\n\n'
                    'if __name__ == "__main__":\n'
                    '    main()\n'
                )
            else:
                starter = (
                    f'# {self.title} - Asosiy kirish nuqtasi\n'
                    f'# Muallif: {author_str}\n\n'
                    'from utils import salom_ber\n\n'
                    'def main():\n'
                    f'    print("Loyiha: {self.title}")\n'
                    '    natija = salom_ber("Foydalanuvchi")\n'
                    '    print(natija)\n\n'
                    'if __name__ == "__main__":\n'
                    '    main()\n'
                )
            main_file = ProjectFile.objects.create(project=self, name='main.py', content=starter, is_folder=False)
            if self.project_mode == ProjectMode.MULTI_FILE:
                ProjectFile.objects.create(
                    project=self,
                    name='utils.py',
                    content='def salom_ber(ism):\n    return f"Assalomu alaykum, {ism}!"\n',
                    is_folder=False
                )
                ProjectFile.objects.create(
                    project=self,
                    name='README.md',
                    content=f'# {self.title}\n\nUshbu loyiha Python dasturlash tilida yozilgan ko\'p faylli ilova.',
                    is_folder=False
                )
        elif self.language == ProjectLanguage.CSHARP:
            starter = (
                f'// {self.title} - C# Dasturi\n'
                'using System;\n\n'
                'namespace Application\n'
                '{\n'
                '    class Program\n'
                '    {\n'
                '        static void Main(string[] args)\n'
                '        {\n'
                f'            Console.WriteLine("Salom, {self.title}!");\n'
                '            Console.Write("Ismingizni kiriting: ");\n'
                '            string name = Console.ReadLine();\n'
                '            Console.WriteLine($"Xush kelibsiz, {name}!");\n'
                '        }\n'
                '    }\n'
                '}\n'
            )
            main_file = ProjectFile.objects.create(project=self, name='Program.cs', content=starter, is_folder=False)
            if self.project_mode == ProjectMode.MULTI_FILE:
                ProjectFile.objects.create(
                    project=self,
                    name='README.md',
                    content=f'# {self.title}\n\nC# dasturlash tilida tuzilgan loyiha.',
                    is_folder=False
                )
        elif self.language == ProjectLanguage.JAVA:
            starter = (
                f'// {self.title} - Java Dasturi\n'
                'import java.util.Scanner;\n\n'
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                f'        System.out.println("Salom, {self.title}!");\n'
                '        Scanner scanner = new Scanner(System.in);\n'
                '        System.out.print("Ismingiz: ");\n'
                '        String ism = scanner.nextLine();\n'
                '        System.out.println("Xush kelibsiz, " + ism);\n'
                '    }\n'
                '}\n'
            )
            main_file = ProjectFile.objects.create(project=self, name='Main.java', content=starter, is_folder=False)
            if self.project_mode == ProjectMode.MULTI_FILE:
                ProjectFile.objects.create(
                    project=self,
                    name='README.md',
                    content=f'# {self.title}\n\nJava ilovasi.',
                    is_folder=False
                )
        elif self.language == ProjectLanguage.CPP:
            starter = (
                f'// {self.title} - C++ Dasturi\n'
                '#include <iostream>\n'
                '#include <string>\n\n'
                'using namespace std;\n\n'
                'int main() {\n'
                f'    cout << "Salom, {self.title}!" << endl;\n'
                '    cout << "Ismingiz: ";\n'
                '    string ism;\n'
                '    cin >> ism;\n'
                '    cout << "Salom, " << ism << "!" << endl;\n'
                '    return 0;\n'
                '}\n'
            )
            main_file = ProjectFile.objects.create(project=self, name='main.cpp', content=starter, is_folder=False)
            if self.project_mode == ProjectMode.MULTI_FILE:
                ProjectFile.objects.create(
                    project=self,
                    name='README.md',
                    content=f'# {self.title}\n\nC++ dasturi.',
                    is_folder=False
                )
        elif self.language == ProjectLanguage.JAVASCRIPT:
            starter = (
                f'// {self.title} - JavaScript Loyihasi\n'
                'function main() {\n'
                f'    console.log("=== {self.title} ===");\n'
                '    console.log("JavaScript dasturi ishga tushdi!");\n'
                '}\n\n'
                'main();\n'
            )
            main_file = ProjectFile.objects.create(project=self, name='index.js', content=starter, is_folder=False)
            if self.project_mode == ProjectMode.MULTI_FILE:
                ProjectFile.objects.create(
                    project=self,
                    name='package.json',
                    content='{\n  "name": "' + self.slug + '",\n  "version": "1.0.0"\n}\n',
                    is_folder=False
                )
                ProjectFile.objects.create(
                    project=self,
                    name='README.md',
                    content=f'# {self.title}\n\nJavaScript loyihasi.',
                    is_folder=False
                )
        else:
            filename = 'main.dart' if self.language == ProjectLanguage.DART else ('main.go' if self.language == ProjectLanguage.GO else 'index.php')
            starter = f'// {self.title}\nvoid main() {{\n  print("Salom, {self.title}!");\n}}\n'
            main_file = ProjectFile.objects.create(project=self, name=filename, content=starter, is_folder=False)
            if self.project_mode == ProjectMode.MULTI_FILE:
                ProjectFile.objects.create(
                    project=self,
                    name='README.md',
                    content=f'# {self.title}',
                    is_folder=False
                )

        return main_file

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author.email}"


class ProjectFile(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name="Tegishli loyiha"
    )
    name = models.CharField(max_length=150, verbose_name="Fayl yoki papka nomi")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Ota papka"
    )
    is_folder = models.BooleanField(default=False, verbose_name="Papka ekanligi")
    content = models.TextField(blank=True, default="", verbose_name="Fayl kodi / matni")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Loyiha fayli"
        verbose_name_plural = "Loyiha fayllari"
        ordering = ['-is_folder', 'name', 'order']
        unique_together = ('project', 'parent', 'name')

    def __str__(self):
        return f"{self.project.title}: {self.get_full_path()}"

    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name

    @property
    def extension(self):
        if self.is_folder:
            return 'folder'
        if '.' in self.name:
            return self.name.split('.')[-1].lower()
        return ''


class ProjectLike(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='project_likes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = "Loyiha yoqtirishi"
        verbose_name_plural = "Loyiha yoqtirishlari"
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.email} -> {self.project.title}"
