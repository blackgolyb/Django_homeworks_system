from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views
from account.views import registaration_view

urlpatterns = [
    path('', views.ProfileView.as_view(), name = 'profile'),
    path('set_theme/', views.SetThemeView.as_view(), name = 'set_theme'),
    path('set_custom_theme/', views.SetCustomThemeView.as_view(), name = 'set_custom_theme'),

    path('registration/', registaration_view, name = 'registration'),

    path('password_change/done/', views.BasePasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_change/', views.BasePasswordChangeView.as_view(), name='password_change'),

    path('password_reset/done/',
    auth_views.PasswordResetCompleteView.as_view(template_name='profile/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(),
    name='password_reset_confirm'),

    path('password_reset/',
    auth_views.PasswordResetView.as_view(template_name="profile/password_reset_form.html"),
    name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='profile/password_reset_complete.html'),
     name='password_reset_complete'),
]
