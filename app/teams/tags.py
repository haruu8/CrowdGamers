from django import template
from django.template.defaultfilters import stringfilter
from markdown as md

register = template.Library()

@register.filter
@stringfilter
def markdown_html(value):
    return md.markdown(value)
