from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import CustomUser
from applications.models import MortgageApplication



class IndexView(TemplateView):
    template_name = 'app/managers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = CustomUser.objects.count()
        context['applications'] = MortgageApplication.objects.all().order_by('-created_at')[:7]
        context['applications_count'] = MortgageApplication.objects.all().count()
        return context

