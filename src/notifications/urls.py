from .views import *
from django.urls import path

from applications.views import AllApplicationsView

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsPageView.as_view(), name='notifications'),

]
