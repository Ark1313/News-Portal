from django import template
from ..bad_words import BAD_WORDS

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value):
    """
   value: значение, к которому нужно применить фильтр
    """

    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} Р'


@register.filter(name='censor')
def currency(value):
    """
   value: значение, к которому нужно применить фильтр
    """

    # проверка и замена
    n = value.split()
    for i in n:
        if i.lower() in BAD_WORDS:
            value = value.replace(i, (i[0] + '*' * (len(i) - 1)))

    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value}'
