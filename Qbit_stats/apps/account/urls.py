from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.AccountView.as_view(), name = 'user'),
]
