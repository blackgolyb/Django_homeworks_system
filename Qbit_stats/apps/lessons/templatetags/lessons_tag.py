from django import template
from lessons.models import Lesson
from account.models import Groups_of_users

register = template.Library()

def found_second_iterator(arr, num):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == num:
                return j

@register.simple_tag()
def get_lessons(group_name, days, day):
    lessons = {}
    try:
        group = Groups_of_users.objects.get(name=group_name)
        day_week = found_second_iterator(days, day)
        lessons = Lesson.objects.filter(day=day_week_obj, group=group)
    except Groups_of_users.DoesNotExist:
        #raise Exception('Groups_of_users.DoesNotExist')
        pass

    return lessons

@register.simple_tag()
def month_to_text(month):
    months = [
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь'
    ]
    return months[month-1]#{'text_month': months[month+1]}
