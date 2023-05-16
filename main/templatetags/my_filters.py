from django import template
import django
register = template.Library()

@register.filter
def set_id(field, id):
    print(id)
    if isinstance(field, django.forms.Field):
        return field.as_widget(attrs={'id': id})
    return field

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True
