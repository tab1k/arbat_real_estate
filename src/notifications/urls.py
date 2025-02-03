from .views import *
from django.urls import path

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsPageView.as_view(), name='index'),
    path('mark_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
]
