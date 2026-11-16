"""
Kontent faylidagi barcha topshiriqlarni HAQIQIY sandbox'da tekshiradi (bazaga hech narsa saqlanmaydi):
  * to'liq yechim barcha testlardan o'tadimi;
  * xatoli boshlang'ich kod testlardan o'tib ketmayaptimi;
  * «natijani aniqlash» javobi kodning haqiqiy natijasiga mosmi;
  * har bir dars strukturasi (nazariya, >=2 kod namunasi, topshiriq, 2-3 mini-test) to'g'rimi.

Ishlatish:  manage.py validate_python_content python_m02 python_m03 ...
"""
import importlib

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.courses.models import Course
from apps.interactive.models import Task, TaskKind, TaskSection
from apps.interactive.seeding import seed_module
from apps.interactive.validation import check_task


class _Rollback(Exception):
    pass


def structure_problems(content):
    problems = []
    for l in content.LESSONS:
        name = f"{l['order']}-dars"
        blocks = l['blocks']
        code_blocks = [b for b in blocks if b['type'] == 'code']
        texts = [b for b in blocks if b['type'] == 'text']
        if not texts:
            problems.append(f"{name}: nazariy matn yo'q")
        if len(code_blocks) < 2:
            problems.append(f"{name}: kod namunalari 2 tadan kam")
        tasks = l['tasks']
        quiz = [t for t in tasks if t['section'] == 'quiz']
        if not 2 <= len(quiz) <= 3:
            problems.append(f"{name}: mini-test savollari {len(quiz)} ta (2-3 bo'lishi kerak)")
        assignments = [t for t in tasks if t['section'] == 'assignment']
        if not assignments:
            problems.append(f"{name}: mustaqil topshiriq yo'q")
        for t in tasks:
            if t['kind'] in ('code', 'find_error') and not (t['hint'] and t['full_solution'] and t['partial_solution'] or t['section'] != 'assignment'):
                problems.append(f"{name}: «{t['title']}» da hint/qisman/to'liq yechim yo'q")
        if not any(t['kind'] == 'code' for t in tasks):
            problems.append(f"{name}: mustaqil kod yozish topshirig'i yo'q")
    return problems


class Command(BaseCommand):
    help = "Kontent modullarini haqiqiy sandbox'da tekshiradi (bazaga saqlanmaydi)."

    def add_arguments(self, parser):
        parser.add_argument('modules', nargs='+', help="masalan: python_m02")

    def handle(self, *args, **opts):
        bad = 0
        total = 0
        course = Course.objects.filter(slug='python-0-dan-boshlash').first()
        if not course:
            raise CommandError("Avval 1-modulni seed qiling (seed_python_course).")
        for name in opts['modules']:
            content = importlib.import_module(f'apps.interactive.content.{name}')
            for p in structure_problems(content):
                bad += 1
                self.stdout.write(self.style.ERROR(f"[STRUKTURA] {p}"))
            try:
                with transaction.atomic():
                    # vaqtincha: bir xil tartib raqamli modul bo'lsa ham tekshirish uchun reset
                    module, _ = seed_module(course, content, reset=True)
                    tasks = list(Task.objects.filter(module=module).select_related('lesson'))
                    for t in tasks:
                        total += 1
                        for level, msg in check_task(t):
                            if level == 'error':
                                bad += 1
                                where = f"{t.lesson.order}-dars" if t.lesson_id else "nazorat"
                                self.stdout.write(self.style.ERROR(f"[{name}] {where} / {t.title}: {msg}"))
                            elif level == 'warning':
                                self.stdout.write(self.style.WARNING(f"[{name}] {t.title}: {msg}"))
                    raise _Rollback()
            except _Rollback:
                pass
            self.stdout.write(f"{name}: tekshirildi")
        self.stdout.write(self.style.SUCCESS(f"Tekshirilgan topshiriqlar: {total}, muammolar: {bad}") if not bad
                          else self.style.ERROR(f"Tekshirilgan topshiriqlar: {total}, MUAMMOLAR: {bad}"))
        if bad:
            raise CommandError("Kontentda muammolar bor.")
