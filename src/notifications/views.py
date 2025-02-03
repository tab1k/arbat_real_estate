from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .models import Notification
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from applications.models import MortgageApplication



class NotificationsPageView(LoginRequiredMixin, View):
    template_name = 'notifications/index.html'

    def get(self, request):
        # Получаем уведомления для текущего пользователя
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

        # Передаем уведомления в контекст
        context = {
            'notifications': notifications
        }
        return render(request, self.template_name, context)


@login_required
def mark_notification_as_read(request, notification_id):
    # Получаем уведомление
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)

    # Помечаем как прочитанное
    notification.mark_as_read()

    # Получаем заявку, к которой относится уведомление (например, ID заявки передаем в сообщении)
    application_id = notification.message.split()[-1]  # Получаем ID заявки из текста уведомления
    application = get_object_or_404(MortgageApplication, pk=application_id)

    # Отправляем JSON ответ, чтобы обновить фронтенд
    return JsonResponse({"message": "Уведомление отмечено как прочитанное"})




@login_required
def delete_notification(request, notification_id):
    # Получаем уведомление
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)

    # Удаляем уведомление
    notification.delete()

    # Возвращаем успешный ответ в формате JSON
    return JsonResponse({'message': 'Уведомление удалено'})
