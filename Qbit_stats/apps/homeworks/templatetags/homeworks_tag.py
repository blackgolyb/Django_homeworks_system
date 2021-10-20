from django import template
from account.models import Groups_of_users, User
from homeworks.models import Topic, Homework, CompliteHomework

register = template.Library()

@register.simple_tag()
def get_topics(group_name):
    group = Groups_of_users.objects.get(name=group_name)
    homeworks = list(group.homeworks.all())
    topics = set()
    for homework in homeworks:
        topics.add(Topic.objects.get(homework=homework))

    return topics

@register.simple_tag()
def get_homework_by_complite_homework(complite_homework_id):
    try:
        complite_homework = CompliteHomework.objects.get(id=complite_homework_id)
        homework = Homework.objects.get(id=complite_homework.homework.id)
        return homework
    except Exception as e:
        print(e)
        return None

@register.simple_tag()
def get_complite_homework_by_homework(homework_id, user_id):
    try:
        homework = Homework.objects.get(id=homework_id)
        user = User.objects.get(id=user_id)
        complite_homework = CompliteHomework.objects.get(homework=homework, student=user)
        return complite_homework
    except Exception as e:
        print(e)
        return None


@register.simple_tag()
def get_status(homework_id, user_id):
    '''homework = Homework.objects.get(id=homework_id)
    user = User.objects.get(id=user_id)'''

    try:
        complite_homework = CompliteHomework.objects.get(homework=homework_id, student=user_id)
        return int(complite_homework.status) + 1
    except Exception as e:
        print()

    return 0
