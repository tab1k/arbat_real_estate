from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView
from users.models import CustomUser
from applications.models import MortgageApplication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from notifications.models import Notification



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


class RealtorApplicationDetailView(DetailView):
    model = MortgageApplication
    template_name = 'app/realtors/application-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = get_object_or_404(
            MortgageApplication.objects.select_related('realtor'),
            pk=self.kwargs['pk']
        )
        context['application'] = application
        return context

    def post(self, request, *args, **kwargs):
        application = get_object_or_404(MortgageApplication, pk=self.kwargs['pk'])

        if request.user != application.realtor:
            return JsonResponse({"error": "Нет доступа"}, status=403)

        code = request.POST.get("code")
        if code:
            application.code = code
            application.save()

            # Уведомляем менеджера о подтверждении кода
            manager = application.manager
            notification = Notification.objects.create(
                user=manager,
                notification_type='code_confirmed',
                message=f"Риэлтор подтвердил код для заявки {application.pk}."
            )
            # Отправляем уведомление в UI, если используется система сообщений
            messages.info(request, f"Код для заявки {application.pk} был подтверждён.")

            return HttpResponseRedirect(reverse('realtors:application-detail', kwargs={'pk': application.pk}))

        return JsonResponse({"error": "Некорректный запрос"}, status=400)



class CreateRequestView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'app/realtors/create-request.html')
