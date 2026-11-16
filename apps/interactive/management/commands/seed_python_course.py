from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course
from apps.interactive.content import python_module1
from apps.interactive.content.registry import COURSE_FULL, load_modules
from apps.interactive.seeding import seed_course, seed_module


class Command(BaseCommand):
    help = ("«Python — 0 dan boshlash» kursini bazaga kiritadi: 1-modul (6 dars) va 2–11-modullar. "
            "Takroran ishga tushirilsa, mavjud modullar o'zgartirilmaydi (dublikat yaratilmaydi).")

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true',
                            help="1-modulni o'chirib qayta yaratadi (o'quvchi natijalari ham o'chadi!).")
        parser.add_argument('--modules', default='', help="Faqat shu modullar (vergul bilan), masalan: 2,3. Bo'sh — hammasi.")
        parser.add_argument('--keep-course-info', action='store_true',
                            help="Kurs nomi/tavsifini o'zgartirmaydi.")
        parser.add_argument('--reset-modules', default='',
                            help="Ko'rsatilgan modullarni (2,3) o'chirib qayta yaratadi (shu modullar bo'yicha o'quvchi natijalari o'chadi!).")

    def handle(self, *args, **options):
        wanted = {int(x) for x in options['modules'].split(',') if x.strip()}
        resets = {int(x) for x in options['reset_modules'].split(',') if x.strip()}
        course, created = seed_course(python_module1, reset=options['reset'], stdout=self.stdout)
        if created:
            self.stdout.write(self.style.SUCCESS(f"1-modul tayyor: «{course.title}»"))
        course = Course.objects.filter(slug=python_module1.COURSE['slug']).first()
        if not course:
            raise CommandError("Kurs topilmadi.")
        created_any = False
        for content in load_modules():
            order = content.MODULE['order']
            if wanted and order not in wanted:
                continue
            self.stdout.write(f"{order}-modul: «{content.MODULE['title']}»")
            _, made = seed_module(course, content, reset=order in resets, stdout=self.stdout)
            if made:
                created_any = True
                self.stdout.write(self.style.SUCCESS(f"  {order}-modul yaratildi."))
        if created_any and not options['keep_course_info']:
            for field, value in COURSE_FULL.items():
                setattr(course, field, value)
            course.save()
            self.stdout.write("Kurs kartochkasi (nom, tavsif, davomiylik) 11 modulli kursga moslab yangilandi.")
        self.stdout.write(self.style.SUCCESS(f"Tayyor → /learn/{course.slug}/"))
