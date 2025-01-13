from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import MortgageApplication
from .serializers import MortgageApplicationSerializer, MortgageApplicationAssignManagerSerializer
from rest_framework.permissions import IsAuthenticated


class MortgageApplicationListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        applications = MortgageApplication.objects.all()
        serializer = MortgageApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = MortgageApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MortgageApplicationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            application = MortgageApplication.objects.get(pk=pk)
        except MortgageApplication.DoesNotExist:
            return Response({"detail": "Заявка не найдена."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MortgageApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        try:
            application = MortgageApplication.objects.get(pk=pk)
        except MortgageApplication.DoesNotExist:
            return Response({"detail": "Заявка не найдена."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MortgageApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MortgageApplicationAssignManagerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            application = MortgageApplication.objects.get(pk=pk)
        except MortgageApplication.DoesNotExist:
            return Response({"detail": "Заявка не найдена."}, status=status.HTTP_404_NOT_FOUND)

        # Проверка роли пользователя, чтобы назначать менеджера
        if request.user.role != 'manager':
            return Response({"detail": "У вас нет прав для этой операции."}, status=status.HTTP_403_FORBIDDEN)

        serializer = MortgageApplicationAssignManagerSerializer(data=request.data)
        if serializer.is_valid():
            manager = serializer.validated_data['manager_id']
            application.assign_manager(manager)
            return Response({"detail": "Менеджер успешно назначен."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MortgageApplicationUnassignManagerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            application = MortgageApplication.objects.get(pk=pk)
        except MortgageApplication.DoesNotExist:
            return Response({"detail": "Заявка не найдена."}, status=status.HTTP_404_NOT_FOUND)

        # Проверка роли пользователя, чтобы снять назначение менеджера
        if request.user.role != 'manager':
            return Response({"detail": "У вас нет прав для этой операции."}, status=status.HTTP_403_FORBIDDEN)

        application.unassign_manager()
        return Response({"detail": "Менеджер успешно удален."}, status=status.HTTP_200_OK)
