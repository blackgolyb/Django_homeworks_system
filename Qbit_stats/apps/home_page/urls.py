from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('home/', views.MainHomeView.as_view(), name = 'home_page'),
]
