from django.shortcuts import render
from django.views import View


class NotificationsPageView(View):
    template_name = 'notifications/index.html'