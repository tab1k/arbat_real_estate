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


class MyApplicationsView(ListView):
    model = MortgageApplication
    template_name = 'app/realtors/my-applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        # Фильтруем заявки для текущего пользователя, если его роль "rieltor"
        return MortgageApplication.objects.filter(realtor=self.request.user, realtor__role='realtor').order_by(
            '-created_at')

    paginate_by = 10  # Пагинация
    ordering = ['-created_at']