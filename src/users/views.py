from django.contrib.auth import authenticate, login

from django.shortcuts import render

from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from .forms import *

from django.views.generic.edit import FormView, UpdateView

from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()


class SignInView(FormView):
    form_class = UserSignInForm
    template_name = 'users/signin.html'

    def form_valid(self, form):
        phone_number = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=phone_number, password=password)
        if user is not None:
            login(self.request, user)
            print(f'User role (after login): {user.role}')

            print(f'User role (before redirect): {user.role}')  # Отладочный вывод роли
            if user.role == 'manager':
                return redirect('managers:index')
            elif user.role == 'realtor':
                return redirect('realtors:index')
            else:
                print(f'Role not defined for user {user.username}, redirecting to /')
                return redirect('/')  # Для неизвестной роли
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


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/settings.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user=self.request.user)  # Добавляем форму пароля
        return context

    def form_valid(self, form):
        messages.success(self.request, "Ваш профиль успешно обновлен!")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()  # Объявляем form перед логикой

        if 'password-change' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = request.user
                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Ваш пароль был успешно изменен!')
                return redirect(self.success_url)
            else:
                messages.error(request, "Ошибка смены пароля. Проверьте введенные данные.")
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                messages.error(request, "Ошибка обновления профиля. Проверьте введенные данные.")

        return self.render_to_response(
            self.get_context_data(form=form, password_form=PasswordChangeForm(user=request.user)))


class ForgotPasswordView(View):

    def get(self, request):
        return render(request, 'users/forgot-password.html')


class RoleExistsPageView(TemplateView):
    template_name =  'users/role_exists.html'
