from django.urls import path
from api.views import CreateCustomUserApiView, CustomTokenObtainPairView, ListCreatePlayListApiView, RetrieveUpdateDestroyPlayListApiView, ChangeSettingsApiView, ListCustomUsersApiView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('register', CreateCustomUserApiView.as_view(), name='api-register'),
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/settings', ChangeSettingsApiView.as_view(), name='user-settings'),
    path('users', ListCustomUsersApiView.as_view(), name='list-custom-users'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('playlists', ListCreatePlayListApiView.as_view(), name='list-create-playlist'),
    path('playlists/<int:pk>', RetrieveUpdateDestroyPlayListApiView.as_view(), name='retrieve-update-destroy-playlist'),
]