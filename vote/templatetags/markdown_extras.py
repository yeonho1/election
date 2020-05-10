from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown as md

register = template.Library()

@register.filter()
@stringfilter
def safe_markdown(text):
    p = '<p>'
    np = '</p>'
    res = md.markdown(text)
    if res.startswith(p) and res.endswith(np):
        res = res[len(p):-len(np)]
    return res.replace('\n', '<br>')