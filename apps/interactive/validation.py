"""
Admin kiritgan topshiriqlarni haqiqiy sandbox orqali tekshirish.

* «Kod yozish» — to'liq yechim barcha testlardan o'tishi kerak.
* «Xatoni tuzatish» — boshlang'ich (xatoli) kod testlardan O'TMASLIGI, to'liq yechim esa o'tishi kerak.
* «Natijani aniqlash» — ko'rsatilgan kodning haqiqiy natijasi «To'g'ri javob» bilan bir xil bo'lishi kerak.
* «Bo'sh joy» — to'g'ri javoblar qo'yilgan kod testlardan o'tishi kerak (agar testlar bo'lsa).
"""
from apps.core.code_runner import run_python

from .grading import _fill_code, grade_code, normalize_output
from .models import TaskKind


def check_task(task):
    """Qaytaradi: [(level, message)], level ∈ {'error', 'warning', 'ok'}."""
    report = [('error', p) for p in task.validate_configuration()]

    if task.kind in (TaskKind.CODE, TaskKind.FIND_ERROR):
        if not task.full_solution.strip():
            report.append(('warning', "To'liq yechim kiritilmagan — testlarni avtomatik sinab bo'lmaydi."))
        elif task.tests.exists():
            res = grade_code(task, task.full_solution)
            if res.infrastructure_error:
                report.append(('warning', "Sandbox mavjud emas — yechimni tekshirib bo'lmadi."))
            elif not res.is_correct:
                failed = [t['description'] for t in res.test_results if not t['passed']]
                report.append(('error', "To'liq yechim testlardan o'tmadi: " + '; '.join(failed)))
            else:
                report.append(('ok', "To'liq yechim barcha testlardan o'tdi."))
        if task.kind == TaskKind.FIND_ERROR and task.starter_code.strip() and task.tests.exists():
            res = grade_code(task, task.starter_code)
            if not res.infrastructure_error and res.is_correct:
                report.append(('error', "Xatoli boshlang'ich kod testlardan o'tib ketmoqda — testlar xatoni aniqlamayapti."))

    if task.kind == TaskKind.PREDICT_OUTPUT and task.code_snippet.strip():
        res = run_python(task.code_snippet)
        if res.is_infrastructure_problem:
            report.append(('warning', "Sandbox mavjud emas — javobni tekshirib bo'lmadi."))
        elif normalize_output(res.stdout) != normalize_output(task.correct_answer):
            report.append(('error', "«To'g'ri javob» kodning haqiqiy natijasiga mos emas. Haqiqiy natija:\n" + res.stdout))
        else:
            report.append(('ok', "To'g'ri javob kodning haqiqiy natijasiga mos."))

    if task.kind == TaskKind.FILL_BLANK and task.tests.exists():
        answers = [alts[0] if alts else '' for alts in task.accepted_blank_answers]
        if len(answers) == task.blank_count:
            res = grade_code(task, _fill_code(task.code_snippet, answers))
            if not res.infrastructure_error and not res.is_correct:
                report.append(('error', "To'g'ri javoblar qo'yilgan kod testlardan o'tmadi."))

    return report
