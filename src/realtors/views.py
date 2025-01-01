from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from users.models import CustomUser

from applications.models import MortgageApplication


class IndexView(TemplateView):
    template_name = 'app/realtors/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = CustomUser.objects.count()
        # Получаем только последние 7 заявок
        context['applications'] = MortgageApplication.objects.filter(
            realtor=self.request.user,
            realtor__role='realtor'
        ).order_by('-created_at')[:7]
        context['applications_count'] = MortgageApplication.objects.filter(
            realtor=self.request.user,
            realtor__role='realtor'
        ).count()
        return context


class SettingsView(TemplateView):
    template_name = 'app/realtors/settings.html'


class CreateRequestView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'managers/realtors/create-request.html')
