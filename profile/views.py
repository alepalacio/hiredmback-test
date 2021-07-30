from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from profile.models import Developer
from profile.serializers import (
    DeveloperSerializer,
    DeveloperAchievementsSerializer,
    AchievementsSerializer,
)

# from achievements.models import Achievement
from .models import Achievement
from django.http import Http404


# Create your views here.


class DetailAchievement(APIView):
    # Obtener objetos
    def get_object(self, pk):
        try:
            return Achievement.objects.get(pk=pk)
        except Achievement.DoesNotExist:
            raise Http404

    # MOSTRAR LOGRO
    def get(self, request, ck, pk):
        achievements = self.get_object(pk)
        achievements_json = AchievementsSerializer(achievements)
        return Response(achievements_json.data)

    # MODIFICAR LOGROS
    def put(self, request, ck, pk):
        achievements = self.get_object(pk)
        achievements_json = AchievementsSerializer(achievements, data=request.data)
        if achievements_json.is_valid():
            achievements_json.save()
            return Response(achievements_json.data)
        return Response(achievements_json.errors, status=400)

    # ELIMINAR LOGROS
    def delete(self, request, ck, pk):
        achievements = self.get_object(pk)
        achievements.delete()
        return Response(status=204)


class UserAchievements(APIView):
    def get(self, request, pk):
        achievements = Achievement.objects.filter(
            user_id=pk
        )  # Buscar como se hace un filtro
        achivements_json = AchievementsSerializer(achievements, many=True)
        return Response(achivements_json.data)

    # Agregar un nuevo logro
    def post(self, request, pk):
        achievement_json = AchievementsSerializer(data=request.data)
        if achievement_json.is_valid():
            achievement_json.save()
            return Response(achievement_json.data, status=201)
        return Response(achievement_json.errors, status=400)


class DevelopersListAPIViews(APIView):
    def get(self, request):
        developers = Developer.objects.all()
        serializer = DeveloperSerializer(developers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Clase que devuelve el perfil completo
class DeveloperAPIView(APIView):
    def get(self, request, pk):
        developer_obj = get_object_or_404(Developer, pk=pk)
        developer_obj.achievements = Achievement.objects.filter(user_id=pk)
        serializer = DeveloperAchievementsSerializer(developer_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Clase que devuelve datos del perfil
class DeveloperDetailView(APIView):
    def get(self, request, pk):
        developer_obj = get_object_or_404(Developer, pk=pk)
        serializer = DeveloperSerializer(developer_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        developer_obj = get_object_or_404(Developer, pk=pk)
        serializer = DeveloperSerializer(
            instance=developer_obj, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        developer_obj = get_object_or_404(Developer, pk=pk)
        developer_obj.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
