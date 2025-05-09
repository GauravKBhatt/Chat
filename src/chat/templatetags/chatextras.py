from django import template

register = template.Library()

# decorator is used to register a function as a custom filter for Django templates
@register.filter(name='initials')

def initials(value):
    initals=''

    for name in value.split(' '):
        if name and len(initials)<3:
            initals += name[0].upper()

    return initials