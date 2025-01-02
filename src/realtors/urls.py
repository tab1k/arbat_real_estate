from .views import *
from django.urls import path
from applications.views import MortgageApplicationCreateView

from applications.views import MyApplicationsView

app_name = 'realtors'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('create-request/', MortgageApplicationCreateView.as_view(), name='create-request'),

]
