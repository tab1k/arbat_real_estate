from django.shortcuts import render
from django.views.generic import TemplateView


class AppIndexView(TemplateView):
    template_name = 'app/index.html'