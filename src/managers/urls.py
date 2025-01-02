from .views import *
from django.urls import path

from applications.views import AllApplicationsView

app_name = 'managers'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('all-applications/', AllApplicationsView.as_view(), name='all-applications'),

]
