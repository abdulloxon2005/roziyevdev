"""Kontentni ixcham yozish uchun yordamchi konstruktorlar (faqat oddiy dict qaytaradi)."""


# ---- Bloklar ----
def text(body, title=''):
    return {'type': 'text', 'title': title, 'body': body.strip()}


def callout(style, body, title=''):
    return {'type': 'callout', 'style': style, 'title': title, 'body': body.strip()}


def example(code, title='', body='', runnable=True):
    return {'type': 'code', 'title': title, 'code': code.strip('\n') + '\n', 'body': body.strip(), 'runnable': runnable}


def exercise(key):
    return {'type': 'task', 'task': key}


# ---- Testlar ----
def T(check, expected='', description='', stdin='', ignore_case=False, hidden=False, failure=''):
    return {
        'check': check, 'expected': expected, 'description': description, 'stdin': stdin,
        'ignore_case': ignore_case, 'hidden': hidden, 'failure': failure,
    }


# ---- Topshiriqlar ----
def _task(key, kind, section, title, prompt, **kw):
    data = {
        'key': key, 'kind': kind, 'section': section, 'title': title, 'prompt': prompt.strip(),
        'difficulty': kw.pop('difficulty', 'easy'),
        'points': kw.pop('points', 1),
        'code_snippet': kw.pop('code_snippet', ''),
        'starter_code': kw.pop('starter_code', ''),
        'expected_output_example': kw.pop('expected_output_example', ''),
        'correct_answer': kw.pop('correct_answer', ''),
        'hint': kw.pop('hint', '').strip(),
        'partial_solution': kw.pop('partial_solution', ''),
        'full_solution': kw.pop('full_solution', ''),
        'explanation': kw.pop('explanation', '').strip(),
        'solution_unlock_attempts': kw.pop('unlock', 2),
        'options': kw.pop('options', []),
        'tests': kw.pop('tests', []),
    }
    if kw:
        raise TypeError(f"Noma'lum maydonlar: {sorted(kw)}")
    for f in ('code_snippet', 'starter_code', 'partial_solution', 'full_solution'):
        if data[f]:
            data[f] = data[f].strip('\n') + '\n'
    data['expected_output_example'] = data['expected_output_example'].strip('\n')
    data['correct_answer'] = data['correct_answer'].strip('\n')
    return data


def single(key, title, prompt, options, section='quiz', **kw):
    return _task(key, 'single_choice', section, title, prompt, options=options, **kw)


def multiple(key, title, prompt, options, section='quiz', **kw):
    return _task(key, 'multiple_choice', section, title, prompt, options=options, **kw)


def predict(key, title, prompt, code, answer, section='quiz', **kw):
    return _task(key, 'predict_output', section, title, prompt, code_snippet=code, correct_answer=answer, **kw)


def fill(key, title, prompt, snippet, answers, section='inline', **kw):
    """answers: har bir bo'sh joy uchun satr; muqobillar ' | ' bilan."""
    return _task(key, 'fill_blank', section, title, prompt, code_snippet=snippet, correct_answer='\n'.join(answers), **kw)


def code_task(key, title, prompt, section='assignment', **kw):
    kw.setdefault('points', 10)
    return _task(key, 'code', section, title, prompt, **kw)


def fix_task(key, title, prompt, section='assignment', **kw):
    kw.setdefault('points', 10)
    return _task(key, 'find_error', section, title, prompt, **kw)


def opt(text, correct=False, feedback=''):
    return (text, correct, feedback)
