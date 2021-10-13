from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View

from account.views import is_auth, StatsBaseView, PageManager
import calendar, datetime

def redirect_calendar_view(request):
    time_now = datetime.datetime.now()
    return redirect(request.get_full_path()+str(time_now.year)+"/"+str(time_now.month))

def del_one_sigment_of_url(url):
    if url[-1] == '/':
        url = url[:-1]
    for i in range(len(url)-1, -1, -1):
        if url[i] == '/':
            break
        url = url[:i]

    return url

class LessonsView(StatsBaseView, PageManager):
    template_name = "lessons/index.html"
    active_page = 2

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        # found month and year and normolize them
        month = kwargs['month']
        year = kwargs['year']
        path = request.get_full_path()
        path = del_one_sigment_of_url(del_one_sigment_of_url(path))

        if month <= 0:
            return redirect(path+str(year-1)+"/"+str(12))
        elif month >= 13:
            return redirect(path+str(year+1)+"/"+str(1))

        #found day of the week and num of days in the monthrange
        #and init calendar
        day_of_week, days = calendar.monthrange(year, month)
        calendar_list = [[None for i in range(7)] for i in range(6)]

        #generate calendar list
        day = 1
        start = False
        for i in range(6):
            for j in range(7):
                if j == day_of_week:
                    start = True
                if day > days:
                    start = False
                if start:
                    calendar_list[i][j] = day
                    day += 1

        #replace None lines from calendar list
        calendar_list_new = []
        for i in range(len(calendar_list)):
            if calendar_list[i].count(None) != 7:
                calendar_list_new.append(calendar_list[i])

        calendar_list = calendar_list_new
        del(calendar_list_new)

        #add content
        context['calendar'] = calendar_list
        context['month'] = month
        context['year'] = year
        context['year_now'] = datetime.datetime.now().year
        context['month_now'] = datetime.datetime.now().month
        context['day_now'] = datetime.datetime.now().day

        print(context)


        return self.render_to_response(context)



def not_found(request, exception):
    return render(request, "errors/404.html")
