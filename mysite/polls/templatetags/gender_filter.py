from django import template
from polls.models import GENDER

register = template.Library()


@register.filter
def custom_gender(q):
    for choice in GENDER:
        if choice[0] == q:
            return choice[1]
    return ''
