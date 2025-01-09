from .views import *
from django.urls import path, include

app_name = 'applications'

urlpatterns = [
    path("success/", SuccessfulApplicationCreatedView.as_view(), name='success'),

]