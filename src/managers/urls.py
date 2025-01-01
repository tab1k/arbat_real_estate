from .views import *
from django.urls import path

app_name = 'managers'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('settings/', AppSettingsView.as_view(), name='app_settings'),
    path('my-listings/', MyListingsView.as_view(), name='my_listings'),

]
