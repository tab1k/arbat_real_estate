from .views import *
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', AppIndexView.as_view(), name='app_index'),
    path('settings/', AppSettingsView.as_view(), name='app_settings')

]
