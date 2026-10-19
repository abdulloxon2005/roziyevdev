from django import template
from django.utils.safestring import mark_safe

from apps.core.rendering import render_markdown

register = template.Library()


@register.filter(name='markdownify')
def markdownify(value):
    return mark_safe(render_markdown(value))


@register.filter(name='som')
def som(value):
    """12345678 -> '12 345 678'"""
    try:
        return f"{int(value):,}".replace(',', ' ')
    except (TypeError, ValueError):
        return value


@register.filter(name='get_item')
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

