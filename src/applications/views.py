from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MortgageApplication
from .forms import MortgageApplicationForm
from django.views.generic import TemplateView, ListView



class MortgageApplicationCreateView(LoginRequiredMixin, CreateView):
    model = MortgageApplication
    form_class = MortgageApplicationForm
    template_name = 'app/realtors/create-request.html'
    success_url = reverse_lazy('applications:success')

    def form_valid(self, form):
        form.instance.realtor = self.request.user
        return super().form_valid(form)


class SuccessfulApplicationCreatedView(LoginRequiredMixin, TemplateView):
    template_name ='app/success.html'


class BaseApplicationsView(LoginRequiredMixin, ListView):
    model = MortgageApplication
    context_object_name = 'applications'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    def filter_queryset(self, queryset):
        return queryset


class AllApplicationsView(BaseApplicationsView):
    template_name = 'app/managers/all-applications.html'

    def filter_queryset(self, queryset):
        # Фильтруем заявки, у которых поле manager пустое (т.е. не прикреплены к менеджеру)
        return queryset.filter(manager__isnull=True).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        application_id = request.POST.get('application_id')
        if application_id:
            try:
                application = MortgageApplication.objects.get(id=application_id)
                if request.user.role == 'manager':  # Проверяем роль
                    application.assign_manager(request.user)
                    application.status = 'in_work'  # Обновляем статус, если нужно
                    application.save()
                    # Можно добавить сообщение об успешном принятии (например, с использованием messages)
            except MortgageApplication.DoesNotExist:
                pass  # Обрабатываем ошибку в случае, если заявка не найдена
        return redirect('managers:all-applications')




class MyApplicationsView(BaseApplicationsView):
    template_name = 'app/realtors/my-applications.html'

    def filter_queryset(self, queryset):
        return queryset.filter(realtor=self.request.user, realtor__role='realtor').order_by('-created_at')


