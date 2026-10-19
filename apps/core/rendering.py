import math
import re

import markdown
import nh3

ALLOWED_TAGS = {
    'p', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'b', 'i', 'u', 's', 'del',
    'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a', 'img', 'table', 'thead', 'tbody', 'tr',
    'th', 'td', 'span', 'div', 'sup', 'sub',
}
ALLOWED_ATTRIBUTES = {
    '*': {'class', 'id'},
    'a': {'href', 'title'},
    'img': {'src', 'alt', 'title', 'width', 'height'},
}


def render_markdown(text):
    """Markdown matnni HTML ga aylantiradi va XSS dan tozalaydi (script, onclick va h.k. olib tashlanadi)."""
    if not text:
        return ''
    html = markdown.markdown(text, extensions=['fenced_code', 'tables', 'sane_lists', 'toc'])
    return nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes={'http', 'https', 'mailto'},
    )


def reading_time_minutes(text, words_per_minute=200):
    words = len(re.findall(r'\w+', text or ''))
    return max(1, math.ceil(words / words_per_minute))
