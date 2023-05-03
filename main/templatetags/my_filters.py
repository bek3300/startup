from django import template
import django
register = template.Library()

@register.filter
def set_id(field, id):
    print(id)
    if isinstance(field, django.forms.Field):
        return field.as_widget(attrs={'id': id})
    return field