from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic.base import View
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "login/login.html")

def login(request):
    if not request.user.is_authenticated:
        args = {}
        if request.POST:
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                args["login_error"] = "user not found"
                return render(request, "login/login.html", args)
        else:
            return render(request, "login/login.html", args)
    else:
        return redirect("/")

class JsonLogin(View):
    def get(self, request):
        print('go to login get')
        return JsonResponse({}, safe=False)
    def post(self, request):
        print('go to login post')
        if not request.user.is_authenticated:
            args = dict()
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                args["login_error"] = "user not found"
                return JsonResponse(args, safe=False)
        else:
            return redirect("/")
