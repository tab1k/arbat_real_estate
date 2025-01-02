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
    success_url = reverse_lazy('website:index')  # Страница с заявками после успешного создания

    def form_valid(self, form):
        # # Проверяем, является ли пользователь риэлтором
        # if self.request.user.role != 'realtor':
        #     return redirect('/')  # Если не риэлтор, перенаправляем на главную

        # Присваиваем риэлтора как создателя заявки
        form.instance.realtor = self.request.user
        return super().form_valid(form)


class BaseApplicationsView(LoginRequiredMixin, ListView):
    model = MortgageApplication
    context_object_name = 'applications'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    def filter_queryset(self, queryset):
        # Этот метод будет переопределен в дочерних классах
        return queryset


class AllApplicationsView(BaseApplicationsView):
    template_name = 'app/managers/all-applications.html'

    def filter_queryset(self, queryset):
        # Возвращаем все заявки для менеджеров
        return queryset.order_by('-created_at')


class MyApplicationsView(BaseApplicationsView):
    template_name = 'app/realtors/my-applications.html'

    def filter_queryset(self, queryset):
        # Фильтруем заявки для текущего пользователя, если он риэлтор
        return queryset.filter(realtor=self.request.user, realtor__role='realtor').order_by('-created_at')
