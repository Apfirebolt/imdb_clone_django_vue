from django.urls import path
from api.views import (
    CreateCustomUserApiView,
    UserDetailApiView,
    CustomTokenObtainPairView,
    ListCreatePlayListApiView,
    RetrieveUpdateDestroyPlayListApiView,
    UserProfileApiView,
    ListCustomUsersApiView,
    AddMovieToPlayListApiView,
    RemoveMovieFromPlayListApiView,
    MovieReviewApiView,
    AuditLogListApiView
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    path("register", CreateCustomUserApiView.as_view(), name="api-register"),
    path("login", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile", UserProfileApiView.as_view(), name="user-settings"),
    path("users", ListCustomUsersApiView.as_view(), name="list-custom-users"),
    path("users/<int:pk>", UserDetailApiView.as_view(), name="user-detail"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("movies/<int:pk>/review", MovieReviewApiView.as_view(), name="movie-review"),
    path(
        "playlists",
        ListCreatePlayListApiView.as_view(),
        name="list-create-playlist",
    ),
    path(
        "playlists/<int:pk>",
        RetrieveUpdateDestroyPlayListApiView.as_view(),
        name="retrieve-update-destroy-playlist",
    ),
    path(
        "playlists/<int:pk>/add-movie",
        AddMovieToPlayListApiView.as_view(),
        name="add-movie-to-playlist",
    ),
    path(
        "playlists/<int:pk>/remove-movie",
        RemoveMovieFromPlayListApiView.as_view(),
        name="remove-movie-from-playlist",
    ),
    path(
        "audit-logs",
        AuditLogListApiView.as_view(),
        name="audit-log-list",
    ),
]
