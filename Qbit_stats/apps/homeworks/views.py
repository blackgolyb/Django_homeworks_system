from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic import ListView
from django.contrib import auth
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin

#from bs4 import BeautifulSoup
#import requests
#import os

from account.views import is_auth, Group, StatsListView, StatsBaseView, PageManager
from .models import Homework, Topic, CompliteHomework
from account.models import User, Groups_of_users
from datetime import datetime, timedelta

class UploadHomeworksView(View):
    def post(self, request, id):
        context = dict()

        if 'homework_file' in request.FILES:
            file = request.FILES['homework_file']
            homework = Homework.objects.get(id=id)
            user = auth.get_user(self.request)


            if homework:
                complite_homework = None
                try:
                    complite_homework = CompliteHomework.objects.get(homework=homework, student=user)
                    complite_homework.file = file
                    complite_homework.status = 0
                except:
                    try:
                        complite_homework = CompliteHomework(
                            student=request.user,
                            homework=homework,
                            file=file, task_comment='')
                    except:
                        print('error in creating comp homewroks')

                try:
                    homework.save()
                    complite_homework.save()
                except Exception as e:
                    print('error in uploading to db')
                    print(e)

            else:
                context['errors'] = 'homework'
        else:
            context['errors'] = 'file'

        return redirect(reverse('homeworks'), context=context)

class HomeworksView(StatsBaseView, PageManager):
    template_name = "homeworks/index.html"
    active_page = 1


    def get_queryset(self):
        user = auth.get_user(self.request)
        group = Groups_of_users.objects.filter(name=self.get_active_group(self.request))
        homeworks = Homework.objects.filter(groups__in=group).order_by('-date')
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
                    complite_homeworks |= CompliteHomework.objects.filter(homework=homework).order_by('-date')

            context['complite_homeworks'] = complite_homeworks
            try:
                pass
            except:
                print("no complite homeworks")
        else:
            individual_homeworks_exist = False
            if user.homeworks.exists():
                individual_homeworks_exist = True
                context['individual_homeworks'] = user.homeworks.all().order_by('-date')
            try:
                group = Groups_of_users.objects.get(name=self.get_active_group(self.request))
                homeworks = group.homeworks.all()
                context['homeworks'] = homeworks.order_by('-date')
            except Exception as e:
                print(e)

            print(context)
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
        groups = Groups_of_users.objects.filter(name=self.get_active_group(self.request))
        homeworks = None
        for group in groups:
            if homeworks is None:
                homeworks = group.homeworks.all()
                continue
            homeworks |= group.homeworks.all()
        individual_homeworks = user.homeworks.all()

        '''if len(status) != 0:
            homeworks = homeworks.filter(status__in=status)
            individual_homeworks = individual_homeworks.filter(status__in=status)'''

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
            "id", "name", "file", "date", "teacher", "topic")
        individual_homeworks = individual_homeworks.order_by(
            '-date').distinct().values(
                "id", "name", "file", "date", "teacher", "topic")

        for homework in homeworks:
            self.convert_to_JSON_format(homework)

        for homework in individual_homeworks:
            self.convert_to_JSON_format(homework)

        #print({'homeworks': list(homeworks), 'individual_homeworks': list(individual_homeworks)})
        return JsonResponse({'homeworks': list(homeworks),
            'individual_homeworks': list(individual_homeworks)}, safe=False)


class CreateHomeworksView(View, PermissionRequiredMixin):
    def post(self, request):
        context = dict()
        context['err'] = list()

        if 'new_homework_file' in request.FILES:
            file = request.FILES['new_homework_file']
            if name := request.POST.get("name", None) is None:
                context['err'].append(f"wrong input data if field {name=}")
            if name := request.POST.get("name", None) is None:
                context['err'].append(f"wrong input data if field {name=}")
            homework = Homework()
            user = auth.get_user(self.request)


            if homework:
                complite_homework = None
                try:
                    complite_homework = CompliteHomework.objects.get(homework=homework, student=user)
                    complite_homework.file = file
                except:
                    try:
                        complite_homework = CompliteHomework(
                            student=request.user,
                            homework=homework,
                            file=file, task_comment='')
                    except:
                        print('error in creating comp homewroks')

                homework.status = 1
                homework.save()
                complite_homework.save()
                try:
                    homework.status = 1
                    homework.save()
                    complite_homework.save()
                except Exception as e:
                    print('error in uploading to db')
                    print(e)

            else:
                context['errors'] = 'homework'
        else:
            context['errors'] = 'file'

        return redirect(reverse('homeworks'), context=context)


        if id := request.POST.get("complite_homework_id", None) is not None:
            complite_homework = Homework.objects.get(id=id)
            if comment := request.POST.get("commet", None):
                if complite_homework != complite_homework.comment:
                    try:
                        complite_homework.set_comment(comment)
                        complite_homework.save()
                    except Exception as e:
                        print("comment unupdated")

class GetGroupsAndUsersView(View, PermissionRequiredMixin):
    permission_required = 'is_teacher'

    def get(self, request):
        groups_queryset = Groups_of_users.objects.all()
        groups = []
        for group in groups_queryset:
            group_dict = {
                'id': group.id,
                'name': str(group),
                'users': [user["id"] for user in group.users.all().distinct().values("id")],
            }
            groups.append(group_dict)
        users = list(User.objects.filter(
            is_teacher=False,
            is_admin=False,
            is_superuser=False,
            is_staff=False)
            .distinct().values("id", "username"))

        return JsonResponse({'groups': list(groups), 'users': list(users)}, safe=False)




class UpdateCompliteHomeworkCommentView(View):
    def post(self, request, id):
        context = dict()

        try:
            complite_homework = CompliteHomework.objects.get(id=id)
            if comment := request.POST.get("comment", None):
                if comment != complite_homework.task_comment:
                    complite_homework.task_comment = comment
                    complite_homework.save()
        except Exception as e:
            print("err in UpdateCompliteHomeworkCommentView")
            print(e)
        return redirect(reverse('homeworks'), context=context)

class DeleteCompliteHomeworkCommentView(View):
    def post(self, request, id):
        context = dict()

        try:
            complite_homework = CompliteHomework.objects.get(id=id)
            complite_homework.task_comment = ''
            complite_homework.save()
        except Exception as e:
            print("err in DeleteCompliteHomeworkCommentView")
            print(e)

        return redirect(reverse('homeworks'), context=context)

class UpdateCompliteHomeworkStatusView(View):
    def post(self, request, id):
        context = dict()
        status = request.POST.get("status", False)
        try:
            complite_homework = CompliteHomework.objects.get(id=id)
            if status != complite_homework.status and status in [False, True, 'on']:
                complite_homework.status = bool(status)
                complite_homework.save()
        except Exception as e:
            print("err in UpdateCompliteHomeworkStatusView")
            print(e)

        return redirect(reverse('homeworks'), context=context)


'''{% for complite_homework in complite_homeworks %}
{% include "homeworks/complite_homework_template.html" %}
{% endfor %}'''
