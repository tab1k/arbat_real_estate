from .views import *
from django.urls import path, include
from .views_api import *

app_name = 'applications'

urlpatterns = [
    path("success/", SuccessfulApplicationCreatedView.as_view(), name='success'),

    path('applications/', MortgageApplicationListCreateAPIView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', MortgageApplicationDetailAPIView.as_view(), name='application-detail'),
    path('applications/<int:pk>/assign_manager/', MortgageApplicationAssignManagerAPIView.as_view(), name='application-assign-manager'),
    path('applications/<int:pk>/unassign_manager/', MortgageApplicationUnassignManagerAPIView.as_view(), name='application-unassign-manager'),

]