from rest_framework import serializers
from .models import MortgageApplication
from users.models import CustomUser


class MortgageApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageApplication
        fields = '__all__'  # Вы можете указать конкретные поля, если не хотите передавать все данные


class MortgageApplicationAssignManagerSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def validate_manager_id(self, value):
        try:
            return CustomUser.objects.get(id=value, role='manager')  # Предположим, что менеджеры имеют роль 'manager'
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Менеджер с таким ID не существует.")
