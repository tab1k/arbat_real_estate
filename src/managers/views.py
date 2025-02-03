from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from users.models import CustomUser
from applications.models import MortgageApplication
from django.db.models import Case, When, IntegerField
from applications.views import BaseApplicationsView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from notifications.models import Notification


class IndexView(TemplateView):
    template_name = 'app/managers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Загрузка заявок с аннотацией приоритета
        applications = (
            MortgageApplication.objects.annotate(
                priority=Case(
                    When(status='in_work', then=0),
                    When(status='first_approved', then=1),
                    When(status='approved', then=2),
                    When(status='rejected', then=3),
                    default=4,
                    output_field=IntegerField(),
                )
            )
            .order_by('priority', '-created_at')
        )

        # Пагинация заявок
        paginator = Paginator(applications, 7)  # 7 заявок на страницу
        page = self.request.GET.get('page', 1)

        try:
            paginated_applications = paginator.page(page)
        except PageNotAnInteger:
            paginated_applications = paginator.page(1)
        except EmptyPage:
            paginated_applications = paginator.page(paginator.num_pages)

        # Подсчёты через Django ORM
        context.update({
            'user_count': CustomUser.objects.count(),
            'applications': paginated_applications,  # Пагинированные заявки
            'applications_count': applications.count(),  # Общее количество заявок
        })

        return context


class ManagerApplicationDetailView(DetailView):
    template_name = 'app/managers/application-detail.html'
    model = MortgageApplication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = get_object_or_404(MortgageApplication, pk=self.kwargs['pk'])
        context['application'] = application
        return context


@login_required
def request_code(request, pk):
    application = get_object_or_404(MortgageApplication, pk=pk)

    if request.user != application.manager:
        return JsonResponse({"error": "Нет доступа"}, status=403)

    if application.code_requested:
        return JsonResponse({"error": "Код уже был запрашивался"}, status=400)

    # Запросил код
    application.code_requested = True
    application.save()

    # Уведомляем риэлтора о запросе кода
    realtor = application.realtor
    notification = Notification.objects.create(
        user=realtor,
        notification_type='code_requested',
        message=f"Менеджер запросил код для заявки {application.pk}."
    )

    return JsonResponse({"message": "Код запроса успешно отправлен"}, status=200)


class AcceptedApplicationView(ListView):
    template_name = 'app/managers/accepted_applications.html'
    model = MortgageApplication
    context_object_name = 'accepted_applications'
    paginate_by = 10  # Количество записей на странице

    def get_queryset(self):
        # Используем select_related для оптимизации запросов
        return (
            MortgageApplication.objects.select_related('manager', 'realtor')
            .filter(manager=self.request.user)
            .order_by('-created_at')
        )


def search_applications(request):
    query = request.GET.get('q', '')

    # Если query — это число, ищем по id
    if query.isdigit():
        applications = MortgageApplication.objects.filter(id=query)
    else:
        applications = MortgageApplication.objects.filter(
            full_name__icontains=query
        ) | MortgageApplication.objects.filter(
            iin__icontains=query
        ) | MortgageApplication.objects.filter(
            phone_number__icontains=query
        ) | MortgageApplication.objects.filter(
            city__icontains=query
        )

    # Сформируем данные для возврата
    results = [{
        'id': application.id,
        'full_name': application.full_name,
        'iin': application.iin,
        'phone_number': application.phone_number,
        'city': application.city,
        'url': reverse('managers:application-detail', args=[application.id])  # URL для перехода
    } for application in applications]

    return JsonResponse(results, safe=False)
