from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from users.models import CustomUser
from applications.models import MortgageApplication
from django.db.models import Case, When, IntegerField

from applications.views import BaseApplicationsView


class IndexView(TemplateView):
    template_name = 'app/managers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = CustomUser.objects.count()
        context['applications'] = MortgageApplication.objects.annotate(
            priority=Case(
                When(status='in_work', then=0),  # Заявки со статусом 'in_work' имеют наивысший приоритет
                When(status='first_approved', then=1),  # Затем идут 'first_approved'
                When(status='approved', then=2),  # Затем 'approved'
                When(status='rejected', then=3),  # Наконец, 'rejected'
                default=4,  # Если вдруг есть другие статусы, они идут последними
                output_field=IntegerField(),
            )
        ).order_by('priority', '-created_at')[:7]  # Сортировка по приоритету, затем по дате
        context['applications_count'] = MortgageApplication.objects.all().count()
        return context


class ApplicationDetailView(BaseApplicationsView):
    template_name = 'app/managers/application-detail.html'

    def get(self, request, *args, **kwargs):
        # Получаем заявку по первичному ключу (id)
        application = get_object_or_404(MortgageApplication, pk=kwargs['pk'])
        return render(request, self.template_name, {'application': application})


class AcceptedApplicationView(ListView):
    template_name = 'app/managers/accepted_applications.html'
    model = MortgageApplication
    context_object_name = 'accepted_applications'

    def get_queryset(self):
        return MortgageApplication.objects.filter(manager=self.request.user)

