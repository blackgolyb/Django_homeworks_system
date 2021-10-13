from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic import ListView
from django.contrib import auth
from django.http import JsonResponse
from django.urls import reverse

#from bs4 import BeautifulSoup
#import requests
#import os

from account.views import is_auth, Group, StatsListView, PageManager
from .models import Homework, Topic, CompliteHomework
from account.models import User, Groups_of_users
from datetime import datetime, timedelta

class UploadHomeworksView(View):
    def post(self, request, id):
        context = dict()

        if 'homework_file' in request.FILES:
            file = request.FILES['homework_file']
            homework = Homework.objects.get(id=id)

            if homework:
                try:
                    print(homework.complite_homework)
                    complite_homework = homework.complite_homework
                    complite_homework.file = file
                    homework.status = 1
                    homework.save()
                    complite_homework.save()
                except:
                    complite_homework = CompliteHomework(
                        student=request.user,
                        homework=homework,
                        file=file, task_comment='')
                    homework.status = 1
                    homework.save()
                    complite_homework.save()
            else:
                context['errors'] = 'homework'
        else:
            context['errors'] = 'file'

        return redirect(reverse('homeworks'), context=context)

class HomeworksView(StatsListView, PageManager):
    template_name = "homeworks/index.html"
    active_page = 1

    def get_queryset(self):
        user = auth.get_user(self.request)
        group = Groups_of_users.objects.filter(name=self.get_active_group(self.request))
        homeworks = Homework.objects.filter(group__in=group, user=user).order_by('-date')
        #individual_homeworks = Homework.objects.filter(pk__in=homeworks).order_by('-date')

        return homeworks

    def get_context_data(self):
        context = super().get_context_data()
        user = auth.get_user(self.request)

        if user.is_teacher:
            homeworks = Homework.objects.filter(teacher=user)
            complite_homeworks = None
            for homework in homeworks:
                if complite_homeworks is None:
                    complite_homeworks = CompliteHomework.objects.filter(homework=homework).order_by('-date')
                else:
                    complite_homeworks &= CompliteHomework.objects.filter(homework=homework).order_by('-date')

            context['complite_homeworks'] = complite_homeworks
            try:
                pass
            except:
                print("no complite homeworks")
        else:
            context['individual_homeworks'] = Homework.objects.filter(user=user, group=None).order_by('-date')

        return context

class HomeworkSerialize(object):
    def convert_to_JSON_format(self, homework):
        teacher = User.objects.get(id=homework["teacher"])
        topic = Topic.objects.get(id=homework["topic"])

        homework["teacher"] = dict()

        teacher_full_name = teacher.get_full_name()
        homework["teacher"]["full_name"] = teacher_full_name if teacher_full_name else str(teacher)
        homework["teacher"]["url"] = teacher.get_absolute_url()
        homework["topic"] = str(topic)

        return homework

class JsonHomeworkFilter(ListView, Group, HomeworkSerialize):

    def get(self, request, *args, **kwargs):
        user = auth.get_user(self.request)
        date = self.request.GET.getlist('date')
        status = self.request.GET.getlist('status')
        topics = list(Topic.objects.filter(name__in=self.request.GET.getlist('topic')))
        group = Groups_of_users.objects.filter(name=self.get_active_group(self.request))
        homeworks = Homework.objects.filter(group__in=group, user=user)
        individual_homeworks = Homework.objects.filter(user=user, group=None)

        if len(status) != 0:
            homeworks = homeworks.filter(status__in=status)
            individual_homeworks = individual_homeworks.filter(status__in=status)

        if len(topics) != 0:
            homeworks = homeworks.filter(topic__in=topics)
            individual_homeworks = individual_homeworks.filter(topic__in=topics)

        if date == 'week':
            now = datetime.now() - timedelta(minutes=60*24*7)
            homeworks = homeworks.filter(date__gte=now)
            individual_homeworks = individual_homeworks.filter(date__gte=now)
        elif date == 'month':
            now = datetime.now() - timedelta(minutes=60*24*30)
            homeworks = homeworks.filter(date__gte=now)
            individual_homeworks = individual_homeworks.filter(date__gte=now)

        homeworks = homeworks.order_by('-date').distinct().values(
            "id", "name", "file", "date", "status", "teacher", "topic")
        individual_homeworks = individual_homeworks.order_by(
            '-date').distinct().values(
                "id", "name", "file", "date", "status", "teacher", "topic")

        for homework in homeworks:
            self.convert_to_JSON_format(homework)

        for homework in individual_homeworks:
            self.convert_to_JSON_format(homework)

        #print({'homeworks': list(homeworks), 'individual_homeworks': list(individual_homeworks)})
        return JsonResponse({'homeworks': list(homeworks),
            'individual_homeworks': list(individual_homeworks)}, safe=False)



class UploadCompliteHomeworksView(View):
    def post(self, request, id):
        context = dict()

        if 'homework_file' in request.FILES:
            file = request.FILES['homework_file']
            homework = Homework.objects.get(id=id)

            if homework:
                try:
                    print(homework.complite_homework)
                    complite_homework = homework.complite_homework
                    complite_homework.file = file
                    homework.status = 1
                    homework.save()
                    complite_homework.save()
                except:
                    complite_homework = CompliteHomework(
                        student=request.user,
                        homework=homework,
                        file=file,
                        task_comment='')
                    homework.status = 1
                    homework.save()
                    complite_homework.save()
            else:
                context['errors'] = 'homework'
        else:
            context['errors'] = 'file'

        return redirect(reverse('homeworks'), context=context)





'''{% for complite_homework in complite_homeworks %}
{% include "homeworks/complite_homework_template.html" %}
{% endfor %}'''
