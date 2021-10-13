from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'login'),
    #path('', views.JsonLogin.as_view(), name = 'login'),
]
