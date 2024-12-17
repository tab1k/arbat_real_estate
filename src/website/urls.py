from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'website'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('calculator/', CalculatorView.as_view(), name='calculator'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
