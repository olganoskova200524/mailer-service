from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css):
    """
    Добавляет CSS-класс к виджету поля формы.
    Пример в шаблоне: {{ field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css})
