from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeworksView.as_view(), name='homeworks'),#views.HomeworksView.as_view() views.Homeworks.as_view()
    path('filter/',
        views.JsonHomeworkFilter.as_view(),
        name='homeworks_filter'),

    path('upload/<int:id>',
        views.UploadHomeworksView.as_view(),
        name='homeworks_upload'),

    path('update_complite_homework_comment/<int:id>',
        views.UpdateCompliteHomeworkCommentView.as_view(),
        name='update_complite_homework_comment'),

    path('delete_complite_homework_comment/<int:id>',
        views.DeleteCompliteHomeworkCommentView.as_view(),
        name='delete_complite_homework_comment'),

    path('update_complite_homeworks_status/<int:id>',
        views.UpdateCompliteHomeworkStatusView.as_view(),
        name='update_complite_homeworks_status'),

    path('create/', views.CreateHomeworksView.as_view(), name='homeworks_create'),
    path('get_groups_and_users/', views.GetGroupsAndUsersView.as_view(), name='get_groups_and_users'),
]
