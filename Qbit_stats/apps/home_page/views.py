from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView

import os

from account.views import is_auth, StatsBaseView, PageManager

class HomeView(StatsBaseView, PageManager):
    template_name = "home_page/index.html"
    active_page = 0
    #redirect_field_name = "home_page"
    redirect_field_name = None
    redirect_url = '/home/'

    def get_login_url(self):
        redirect_url = self.redirect_url or settings.LOGIN_URL
        return str(redirect_url)

class MainHomeView(TemplateView):
    template_name = "home_page/home_page.html"

def not_found(request, exception):
    return render(request, "errors/404.html")
