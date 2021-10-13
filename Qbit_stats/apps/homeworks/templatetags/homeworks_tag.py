from django import template
from account.models import Groups_of_users, User
from homeworks.models import Topic, Homework, CompliteHomework

register = template.Library()

@register.simple_tag()
def get_topics(group_name):
    group = Groups_of_users.objects.get(name=group_name)
    homeworks = list(Homework.objects.filter(group=group))

    topics = set()
    for homework in homeworks:
        topics.add(Topic.objects.get(homework=homework))

    return topics

@register.simple_tag()
def get_status(homework_id, user_id):
    homework = Homework.objects.get(id=homework_id)
    user = User.objects.get(id=user_id)

    try:
        complite_homework = CompliteHomework.objects.get(homework=homework, student=user)
        return complite_homework.status + 1
    except:
        return 0
        
    return 0
