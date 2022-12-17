# Custom tag
# https://pythoncircle.com/post/42/creating-custom-template-tags-in-django/

from django import template

register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)
