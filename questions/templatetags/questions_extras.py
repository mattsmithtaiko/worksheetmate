from django import template

register = template.Library()

@register.filter
def alph(value):
    return chr(value + 96)
