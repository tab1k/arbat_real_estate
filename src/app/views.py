from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import CustomUser


class AppIndexView(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = CustomUser.objects.count()
        return context



class AppSettingsView(TemplateView):
    template_name = 'app/settings.html'