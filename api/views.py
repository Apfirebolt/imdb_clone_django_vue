from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from . serializers import CustomUserSerializer, ListCustomUserSerializer, CustomTokenObtainPairSerializer, PlayListSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser
from movies.models import PlayList


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ChangeSettingsApiView(UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class ListCreatePlayListApiView(ListCreateAPIView):
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RetrieveUpdateDestroyPlayListApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs['pk'], created_by=self.request.user)
        return obj


