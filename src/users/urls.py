from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *
from .views_api import *

app_name = 'users'

urlpatterns = [
    path('', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', CustomUserUpdateView.as_view(), name='profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('role_exists/', RoleExistsPageView.as_view(), name='role_exists'),


    # API
    path('api/signin/', SignInAPIView.as_view(), name='api_signin'),
    path('api/signup/', SignUpAPIView.as_view(), name='api_signup'),

]
