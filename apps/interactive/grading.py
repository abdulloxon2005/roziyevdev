"""
Topshiriqlarni avtomatik tekshirish.

Muhim tamoyil: kod topshirig'i "ishga tushdi" degani "to'g'ri" degani emas. Har bir kod
topshirig'i oldindan tayyorlangan testlar (TaskTest) bilan tekshiriladi. Dastur chiqishi
web-server tomonida (sandbox'dan tashqarida) taqqoslanadi, shuning uchun o'quvchi kodi
test natijasini soxtalashtira olmaydi.
"""
import re
from dataclasses import dataclass, field

from apps.core.code_runner import RunResult, RunStatus, run_python

from .models import BLANK_TOKEN, TaskKind, TestCheck


def normalize_output(text):
    """Satr oxiridagi bo'sh joylar va boshi/oxiridagi bo'sh qatorlarni hisobga olmaydi."""
    lines = [line.rstrip() for line in (text or '').replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return '\n'.join(lines)


def _norm_case(text, ignore_case):
    return text.casefold() if ignore_case else text


@dataclass
class GradeResult:
    is_correct: bool = False
    score: float = 0
    max_score: float = 0
    message: str = ''
    test_results: list = field(default_factory=list)
    run: RunResult | None = None
    option_feedback: list = field(default_factory=list)
    infrastructure_error: bool = False

    def tests_summary(self):
        total = len(self.test_results)
        passed = sum(1 for t in self.test_results if t['passed'])
        return passed, total


def evaluate_test(test, code, run):
    """Bitta testni baholaydi. run — shu test stdin'i bilan bajarilgan RunResult (yoki None)."""
    ctype = test.check_type
    expected = test.expected or ''
    if ctype in (TestCheck.CODE_CONTAINS, TestCheck.CODE_NOT_CONTAINS, TestCheck.CODE_REGEX):
        haystack = _norm_case(code, test.ignore_case)
        needle = _norm_case(expected, test.ignore_case)
        if ctype == TestCheck.CODE_CONTAINS:
            return needle in haystack, ''
        if ctype == TestCheck.CODE_NOT_CONTAINS:
            return needle not in haystack, ''
        flags = re.MULTILINE | (re.IGNORECASE if test.ignore_case else 0)
        return re.search(expected, code, flags) is not None, ''

    # Ishga tushirishni talab qiladigan testlar
    if run is None or not run.ok:
        if run is not None and run.status != RunStatus.OK:
            return False, "Dastur xato bilan tugadi, shuning uchun bu test o'tmadi."
        return False, ''
    out = normalize_output(run.stdout)
    if ctype == TestCheck.RUNS_OK:
        return True, ''
    if ctype == TestCheck.OUTPUT_EQUALS:
        return _norm_case(out, test.ignore_case) == _norm_case(normalize_output(expected), test.ignore_case), ''
    if ctype == TestCheck.OUTPUT_CONTAINS:
        return _norm_case(expected, test.ignore_case) in _norm_case(out, test.ignore_case), ''
    if ctype == TestCheck.OUTPUT_NOT_CONTAINS:
        return _norm_case(expected, test.ignore_case) not in _norm_case(out, test.ignore_case), ''
    if ctype == TestCheck.OUTPUT_REGEX:
        flags = re.MULTILINE | (re.IGNORECASE if test.ignore_case else 0)
        return re.search(expected, out, flags) is not None, ''
    if ctype == TestCheck.OUTPUT_LINES_MIN:
        need = int(expected.strip() or 0)
        have = sum(1 for line in out.split('\n') if line.strip())
        return have >= need, ''
    return False, "Noma'lum test turi."


def grade_code(task, code):
    """Kodni topshiriq testlari bilan tekshiradi."""
    tests = list(task.tests.all())
    result = GradeResult(max_score=float(task.points))
    code = code or ''
    if not code.strip():
        result.message = "Kod bo'sh. Avval yechimingizni yozing."
        return result

    # Bir xil stdin'li testlar uchun kod bir marta bajariladi
    runs = {}
    needs_run = [t for t in tests if t.needs_run] or ([] if tests else [None])
    for t in needs_run:
        stdin = t.stdin if t is not None else ''
        if stdin not in runs:
            runs[stdin] = run_python(code, stdin=stdin)
            if runs[stdin].is_infrastructure_problem:
                result.infrastructure_error = True
                result.run = runs[stdin]
                result.message = runs[stdin].stderr or "Kod bajarish xizmati vaqtincha mavjud emas. Keyinroq urinib ko'ring."
                return result

    primary_run = runs.get('') or (next(iter(runs.values())) if runs else None)
    result.run = primary_run

    if not tests:
        ok = primary_run is not None and primary_run.ok
        result.test_results = [{
            'description': "Dastur xatosiz ishlaydi", 'passed': ok, 'hidden': False, 'message': '',
        }]
    else:
        for t in tests:
            run = runs.get(t.stdin) if t.needs_run else None
            passed, note = evaluate_test(t, code, run)
            message = ''
            if not passed:
                message = t.failure_message or note
            result.test_results.append({
                'description': "Yashirin test" if t.is_hidden else t.description,
                'passed': passed,
                'hidden': t.is_hidden,
                'message': message,
            })

    passed, total = result.tests_summary()
    result.score = round(task.points * passed / total, 2) if total else 0
    result.is_correct = total > 0 and passed == total
    if result.is_correct:
        result.message = "Barcha testlardan o'tdingiz! Ajoyib."
    elif primary_run is not None and primary_run.status != RunStatus.OK:
        result.message = "Dastur xato bilan tugadi. Xato xabarini o'qing va kodni tuzating."
    else:
        result.message = f"{total} ta testdan {passed} tasidan o'tdingiz. Shartni qayta o'qib chiqing."
    return result


def _fill_code(snippet, blanks):
    parts = snippet.split(BLANK_TOKEN)
    out = [parts[0]]
    for i, rest in enumerate(parts[1:]):
        out.append(blanks[i] if i < len(blanks) else '')
        out.append(rest)
    return ''.join(out)


def _norm_blank(value):
    return re.sub(r'\s+', ' ', (value or '').strip())


def grade_task(task, answer, code=''):
    """
    Topshiriqni baholaydi.

    answer:
      * single/multiple choice: {"options": [id, ...]}
      * predict_output:         {"text": "..."}
      * fill_blank:             {"blanks": ["...", "..."]}
    code: find_error / code turlari uchun.
    """
    answer = answer or {}
    kind = task.kind

    if kind in (TaskKind.SINGLE_CHOICE, TaskKind.MULTIPLE_CHOICE):
        result = GradeResult(max_score=float(task.points))
        try:
            selected = {int(x) for x in (answer.get('options') or [])}
        except (TypeError, ValueError):
            selected = set()
        options = list(task.options.all())
        valid_ids = {o.id for o in options}
        selected &= valid_ids
        correct = {o.id for o in options if o.is_correct}
        if not selected:
            result.message = "Javob variantini tanlang."
            return result
        if kind == TaskKind.SINGLE_CHOICE and len(selected) > 1:
            selected = {next(iter(selected))}
        result.is_correct = selected == correct
        result.score = float(task.points) if result.is_correct else 0
        result.option_feedback = [
            {'id': o.id, 'feedback': o.feedback} for o in options if o.id in selected and o.feedback
        ]
        if result.is_correct:
            result.message = "To'g'ri!"
        elif kind == TaskKind.MULTIPLE_CHOICE and selected < correct:
            result.message = "Qisman to'g'ri: yana to'g'ri variant(lar) bor."
        else:
            result.message = "Noto'g'ri. Maslahatni ko'rib, qayta urinib ko'ring."
        return result

    if kind == TaskKind.PREDICT_OUTPUT:
        result = GradeResult(max_score=float(task.points))
        given = normalize_output(answer.get('text', ''))
        if not given:
            result.message = "Javobni yozing."
            return result
        result.is_correct = given == normalize_output(task.correct_answer)
        result.score = float(task.points) if result.is_correct else 0
        result.message = "To'g'ri! Dastur aynan shu natijani chiqaradi." if result.is_correct else \
            "Noto'g'ri. Har bir print() alohida qatorga chiqishini va bo'sh joylarni hisobga oling."
        return result

    if kind == TaskKind.FILL_BLANK:
        blanks = [str(b) for b in (answer.get('blanks') or [])][:task.blank_count]
        if len(blanks) < task.blank_count or not all(b.strip() for b in blanks):
            return GradeResult(max_score=float(task.points), message="Barcha bo'sh joylarni to'ldiring.")
        if task.tests.exists():
            res = grade_code(task, _fill_code(task.code_snippet, blanks))
            return res
        result = GradeResult(max_score=float(task.points))
        accepted = task.accepted_blank_answers
        per_blank = []
        for i, value in enumerate(blanks):
            options = [_norm_blank(a) for a in (accepted[i] if i < len(accepted) else [])]
            per_blank.append(_norm_blank(value) in options)
        result.is_correct = all(per_blank) and len(per_blank) == task.blank_count
        correct_count = sum(per_blank)
        result.score = round(task.points * correct_count / max(1, task.blank_count), 2)
        result.test_results = [
            {'description': f"{i + 1}-bo'sh joy", 'passed': ok, 'hidden': False, 'message': ''}
            for i, ok in enumerate(per_blank)
        ]
        result.message = "To'g'ri!" if result.is_correct else f"{task.blank_count} ta bo'sh joydan {correct_count} tasi to'g'ri."
        return result

    if kind in (TaskKind.FIND_ERROR, TaskKind.CODE):
        return grade_code(task, code)

    return GradeResult(message="Noma'lum topshiriq turi.")
