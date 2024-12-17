from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, TemplateView


class SignInView(LoginView):
    template_name = 'users/signin.html'


class SignUpView(TemplateView):
    template_name = 'users/signup.html'


class ForgotPasswordView(View):

    def get(self, request):
        return render(request, 'users/forgot-password.html')
