from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin
from django.views.generic import ListView
# from django.contrib import auth

import json
from account.form import RegistarationForm
from account.models import User, Groups_of_users


def remove_urls_nodes(path, n:int):
    if n <= 0:
        raise Exception('invalid counter parameter.')

    if path[-1] != '/' or path[0] != '/':
        raise Exception('invalid path (url).')

    path = path[:-1].split('/')
    path = '/'.join(path[:-min(n, len(path))])

    return '/' if path == '' else path


class PageManager:
    active_page = None

    def get_active_page(self):
        return self.active_page


class Group:
    def get_groups(self, request):
        # user = auth.get_user(request)
        groups = Groups_of_users.objects.filter(users=request.user)
        return groups

    def get_active_group(self, request):
        active_group = request.GET.get("groups")

        if active_group is None:
            groups = self.get_groups(request)

            try:
                active_group = request.COOKIES['active_group']
                if active_group == 'None':
                    active_group = groups[0].name if groups else None
            except:
                active_group = groups[0].name if groups else None

        return active_group

    def set_active_group(self, response):
        request = self.request
        # active_group = self.args['active_group']
        active_group = self.active_group

        try:
            if active_group != request.COOKIES['active_group'] and active_group is not None:
                response.set_cookie('active_group', active_group)
        except:
            response.set_cookie('active_group', active_group)


class Theme:
    def get_custom_them(self, request):
        try:
            custom_theme = json.loads(request.COOKIES['custom_theme'])
        except:
            custom_theme = dict()

        print('new_castom: ', custom_theme)
        return custom_theme

    def get_theme_name(self, request):
        try:
            theme_name = request.COOKIES['theme']
        except:
            theme_name = 'light'

        return theme_name


class StatsBaseView(LoginRequiredMixin, Group, Theme, TemplateResponseMixin, ContextMixin, View):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def set_cokies(self, response):
        self.set_active_group(response)

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        self.set_cokies(response)
        return response

    def get_context_data(self, **kwargs):
        self.active_group = self.get_active_group(self.request)
        self.groups = self.get_groups(self.request)
        self.theme_name = self.get_theme_name(self.request)

        context = {
            "groups": self.groups,
            "active_group": self.active_group,
            "theme_name": self.theme_name,
        }

        if self.theme_name == 'custom':
            context.update(self.get_custom_them(self.request))

        context.update(kwargs)
        return super().get_context_data(**context)


class StatsListView(LoginRequiredMixin, Group, Theme, ListView):

    def set_cokies(self, response):
        self.set_active_group(response)

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        self.set_cokies(response)
        return response

    def get_context_data(self):
        self.active_group = self.get_active_group(self.request)
        self.groups = self.get_groups(self.request)

        args = {
            "groups": self.groups,
            "active_group": self.active_group,
            "theme_name": self.get_theme_name(self.request),
        }

        return super(ListView, self).get_context_data(**args)



class AccountView(StatsBaseView):
    template_name = "account/index.html"

    def get(self, *args, **kwargs):
        context = self.get_context_data()
        try:
            slug = kwargs['slug']
            member = User.objects.get(url=slug)
            context['member'] = member
        except:
            print('no user with slug: ' + slug)

        return self.render_to_response(context)


def is_auth(request):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("/login/")
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


@staff_member_required(redirect_field_name='', login_url='/login/')
def registaration_view(request):
    args = {}
    if request.POST:
        form = RegistarationForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password1')
            account = authenticate(password=password)
            redirect('/home/')
        else:
            args['registaration_form'] = form
    else:
        form = RegistarationForm()
        args['registaration_form'] = form
    return render(request, 'profile/registration.html', args)
