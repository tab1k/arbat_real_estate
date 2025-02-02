from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('code_requested', 'Запрос кода'),
        ('code_confirmed', 'Подтверждение кода'),
        ('new_application', 'Новая заявка'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Уведомление для {self.user} - {self.get_notification_type_display()}"

    def mark_as_read(self):
        self.is_read = True
        self.save()
