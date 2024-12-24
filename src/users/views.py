from django.contrib.auth import authenticate, login

from django.shortcuts import render

from django.shortcuts import redirect
from django.views import View

from .forms import *

from django.views.generic.edit import FormView

from django.urls import reverse_lazy

User = get_user_model()


class SignInView(FormView):
    form_class = UserSignInForm
    template_name = 'users/signin.html'
    success_url = reverse_lazy('app:app_index')

    def form_valid(self, form):
        phone_number = form.cleaned_data['username']  # username теперь соответствует phone_number
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=phone_number, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            form.add_error(None, "Неверный номер телефона или пароль.")
            return self.form_invalid(form)


class SignUpView(FormView):
    form_class = UserSignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:signin')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.username = form.cleaned_data['phone_number']  # Set phone_number as username
        user.save()

        return super().form_valid(form)


class ForgotPasswordView(View):

    def get(self, request):
        return render(request, 'users/forgot-password.html')
