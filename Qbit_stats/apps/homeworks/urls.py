from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeworksView.as_view(), name='homeworks'),#views.HomeworksView.as_view() views.Homeworks.as_view()
    path('filter/', views.JsonHomeworkFilter.as_view(), name='homeworks_filter'),
    path('upload/<int:id>', views.UploadHomeworksView.as_view(), name='homeworks_upload'),
    path('create/', views.HomeworksView.as_view(), name='homeworks_create'),
]
