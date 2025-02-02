from .views import *
from django.urls import path

from applications.views import AllApplicationsView

app_name = 'managers'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search-applications/', search_applications, name='search-applications'),
    path('application/<int:pk>/', ManagerApplicationDetailView.as_view(), name='application-detail'),
    path('application/<int:pk>/request-code/', request_code, name='request-code'),

    path('all-applications/', AllApplicationsView.as_view(), name='all-applications'),
    path('accepted-application/', AcceptedApplicationView.as_view(), name='accepted-application'),

]
