from django import template

register = template.Library()

@register.filter
def get_options(options, question):
    return [
        (1, question.option1),
        (2, question.option2),
        (3, question.option3),
        (4, question.option4)
    ]

@register.filter
def get_item(lst, i):
    try:
        return lst[i]
    except:
        return None