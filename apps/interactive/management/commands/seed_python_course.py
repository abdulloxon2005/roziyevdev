from django.core.management.base import BaseCommand

from apps.interactive.content import python_module1
from apps.interactive.seeding import seed_course


class Command(BaseCommand):
    help = "«Python — 0 dan boshlash» kursining 1-modulini (6 dars + nazorat) bazaga kiritadi."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help="1-modulni o'chirib, kontentni qaytadan yaratadi (o'quvchi natijalari ham o'chadi!).",
        )

    def handle(self, *args, **options):
        course, created = seed_course(python_module1, reset=options['reset'], stdout=self.stdout)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Tayyor: «{course.title}» → /learn/{course.slug}/"))
