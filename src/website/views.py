from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


class IndexView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creeping_line'] = CreepingLine.objects.all().order_by('created_at')
        context['exclusive_offer'] = ExclusiveOffer.objects.all().order_by('created_at')
        return context


class AboutView(TemplateView):
    template_name = 'website/about.html'


class CalculatorView(TemplateView):
    template_name = 'website/calculator.html'


class ContactsView(TemplateView):
    template_name = 'website/contacts.html'
