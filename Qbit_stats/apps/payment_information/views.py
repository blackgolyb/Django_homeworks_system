from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import View
import os

from account.views import is_auth, StatsBaseView, PageManager


class PaymentInformationView(StatsBaseView, PageManager):
    template_name = "payment_information/index.html"
    active_page = 4
