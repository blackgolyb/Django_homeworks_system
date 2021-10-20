from django.db import models

class Topic(models.Model):
    name = models.CharField(verbose_name = "название", max_length = 30)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    class Meta:
        verbose_name        = u"Тема"
        verbose_name_plural = u"Темы"

class Homework(models.Model):
    name        = models.CharField(verbose_name = "название домашнего задания", max_length = 30)
    file        = models.FileField(verbose_name = "файл", upload_to = 'homeworks/', blank = True)
    date        = models.DateField(verbose_name = "дата создания", auto_now_add = True, null = True)

    teacher     = models.ForeignKey('account.User', on_delete = models.CASCADE, related_name = "teacher_homeworks")
    groups      = models.ManyToManyField('account.Groups_of_users', related_name = "homeworks", blank=True, null=True)
    users       = models.ManyToManyField('account.User', related_name = "homeworks", blank=True, null=True)
    topic       = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name = "homework")

    def __str__(self):
        return self.name# + (' | ' + str(self.group)if self.group else '')

    class Meta:
        verbose_name        = u"Домашнее задание"
        verbose_name_plural = u"Домашние задания"

class CompliteHomework(models.Model):
    student = models.ForeignKey('account.User', on_delete = models.CASCADE)
    homework = models.ForeignKey(Homework, related_name = 'complite_homework', on_delete = models.CASCADE)

    file = models.FileField(verbose_name = "файл", upload_to = 'complite_homeworks/', blank = True)# + student.username + '/'
    status = models.BooleanField(verbose_name = "статус задания", default = False, blank = True)
    task_comment = models.CharField(verbose_name = "комментарий к заданию", default = '', max_length = 500)
    date = models.DateTimeField(verbose_name = 'дата создания', auto_now_add = True)

    def __str__(self):
        return self.homework.name + ' | ' + self.student.username

    class Meta:
        verbose_name        = u"Выполненое домашнее задание"
        verbose_name_plural = u"Выполненые Домашние задания"
