from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
import re

from .models import CustomUser

User = get_user_model()





class UserSignInForm(AuthenticationForm):
    phone_number = forms.CharField(
        max_length=25,
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Номер телефона',
            'value': '+7 (',  # Начальное значение поля с префиксом +7 и открывающей скобкой
            'oninput': """if (!this.value.startsWith('+7 (')) {
                            this.value = '+7 (' + this.value.replace('+7 (', '');
                        } 
                        if (this.value.length === 8 && this.value[7] !== ')') {
                            this.value = this.value.slice(0, 7) + ')' + this.value.slice(7);
                        }
                        if (this.value.length === 9 && this.value[8] !== ' ') {
                            this.value = this.value.slice(0, 8) + ' ' + this.value.slice(8);
                        }
                        if (this.value.length === 13 && this.value[12] !== ' ') {
                            this.value = this.value.slice(0, 12) + ' ' + this.value.slice(12);
                        }""",  # Скрипт для автоматического добавления скобок и пробелов
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ['phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = self.fields.pop('phone_number')
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        phone_number = self.cleaned_data.get('username')
        # Remove all non-digit characters except the plus sign
        cleaned_phone_number = re.sub(r'[^\d]', '', phone_number)

        # Ensure the number starts with '7' (after the plus sign) and has exactly 10 digits following it
        if not cleaned_phone_number.startswith('7') or len(cleaned_phone_number) != 11:
            raise ValidationError("Введите номер телефона в формате +7 (XXX) XXX-XXXX.")

        # Reformat the number to include the '+7' prefix
        cleaned_phone_number = '+7' + cleaned_phone_number[1:]

        return cleaned_phone_number


class UserSignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=25,
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Номер телефона',
            'value': '+7 (',
            'oninput': """if (!this.value.startsWith('+7 (')) {
                            this.value = '+7 (' + this.value.replace('+7 (', '');
                        } 
                        if (this.value.length === 8 && this.value[7] !== ')') {
                            this.value = this.value.slice(0, 7) + ')' + this.value.slice(7);
                        }
                        if (this.value.length === 9 && this.value[8] !== ' ') {
                            this.value = this.value.slice(0, 8) + ' ' + this.value.slice(8);
                        }
                        if (this.value.length === 13 && this.value[12] !== ' ') {
                            this.value = this.value.slice(0, 12) + ' ' + this.value.slice(12);
                        }""",
        }),
        required=True
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        required=True
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Remove all non-digit characters except the plus sign
        cleaned_phone_number = re.sub(r'[^\d]', '', phone_number)

        # Ensure the number starts with '7' (without the plus sign) and has exactly 10 digits following it
        if not cleaned_phone_number.startswith('7') or len(cleaned_phone_number) != 11:
            raise ValidationError("Номер телефона должен начинаться с +7 и содержать 10 цифр после +7.")

        # Reformat the number to include the '+7' prefix
        cleaned_phone_number = '+7' + cleaned_phone_number[1:]

        return cleaned_phone_number



# Форма для обновления пользователя
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'photo')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and CustomUser.objects.exclude(id=self.instance.id).filter(phone_number=phone_number).exists():
            raise ValidationError("Этот номер телефона уже используется.")
        return phone_number



# Форма смены пароля
class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label='Текущий пароль')
    new_password = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите новый пароль')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError("Новый пароль и подтверждение пароля не совпадают.")

        return cleaned_data


