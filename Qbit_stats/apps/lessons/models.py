from django.db import models

# Create your models here.

class LessonRepeat(models.Model):
    #name =
    status = models.IntegerField(verbose_name = "статус повторения", default=0)

    '''once = models.BooleanField(default = False)
    once_a_year = models.BooleanField(default = False)
    once_a_month = models.BooleanField(default = False)
    two_weeks_in_month = models.BooleanField(default = False)'''

    class Meta:
        verbose_name        = u"Повторение урока"
        verbose_name_plural = u"Повторение уроков"


class Lesson(models.Model):
    time_start  = models.TimeField(verbose_name = "время начала", auto_now = False, auto_now_add = False, blank = True)
    time_end    = models.TimeField(verbose_name = "время окончания", auto_now = False, auto_now_add = False, blank = True)
    status      = models.IntegerField(verbose_name = "статус урока", default=0)

    teacher     = models.ForeignKey('account.User', on_delete = models.CASCADE)
    group       = models.ForeignKey('account.Groups_of_users', on_delete = models.CASCADE)
    topic       = models.ForeignKey('homeworks.Topic', on_delete = models.CASCADE)
    repeat      = models.ForeignKey(LessonRepeat, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.group.name + ' | ' + self.topic.name

    class Meta:
        verbose_name        = u"Урок"
        verbose_name_plural = u"Уроки"
