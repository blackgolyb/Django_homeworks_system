from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_calendar_view, name = 'lessons'),
    path('<int:year>/<int:month>/', views.LessonsView.as_view(), name = 'month'),
]
