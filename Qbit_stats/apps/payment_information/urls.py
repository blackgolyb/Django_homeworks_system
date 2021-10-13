from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentInformationView.as_view(), name = 'payment_information'),
]
