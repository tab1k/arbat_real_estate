from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    path('', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password')

]
