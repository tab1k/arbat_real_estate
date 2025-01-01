from django import forms
from .models import MortgageApplication
from django.core.exceptions import ValidationError
import re


class MortgageApplicationForm(forms.ModelForm):  # Меняем на ModelForm
    class Meta:
        model = MortgageApplication
        fields = ['full_name', 'iin', 'phone_number', 'amount', 'down_payment', 'mortgage_term', 'city']

    full_name = forms.CharField(
        max_length=255,
        label='Полное имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Полное имя'}),
        required=True
    )

    iin = forms.CharField(
        max_length=255,
        label='ИИН',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ИИН'}),
        required=True
    )

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

    amount = forms.DecimalField(
        label='Сумма ипотеки',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сумма ипотеки'}),
        required=True
    )

    down_payment = forms.DecimalField(
        label='Первоначальный взнос',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Первоначальный взнос'}),
        required=True
    )

    mortgage_term = forms.IntegerField(
        label='Срок ипотеки (в годах)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Срок ипотеки'}),
        required=True
    )

    city = forms.CharField(
        max_length=100,
        label='Город',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
        required=True
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Удаляем все символы, кроме цифр
        cleaned_phone_number = re.sub(r'[^\d]', '', phone_number)

        # Проверяем, что номер начинается с '7' (после знака плюс) и имеет 10 цифр
        if not cleaned_phone_number.startswith('7') or len(cleaned_phone_number) != 11:
            raise ValidationError("Введите номер телефона в формате +7 (XXX) XXX-XXXX.")

        # Форматируем номер с добавлением префикса +7
        cleaned_phone_number = '+7' + cleaned_phone_number[1:]

        return cleaned_phone_number