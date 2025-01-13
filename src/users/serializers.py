from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        if not phone_number or not password:
            raise serializers.ValidationError("Номер телефона и пароль обязательны.")

        user = authenticate(username=phone_number, password=password)
        if not user:
            raise serializers.ValidationError("Неверный номер телефона или пароль.")

        if not user.is_active:
            raise serializers.ValidationError("Ваш аккаунт заблокирован.")

        data['user'] = user
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email', ''),
            password=validated_data['password1'],
            role=validated_data.get('role', 'realtor'),  # Роль по умолчанию
        )
        return user
