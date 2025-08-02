from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import (
    CustomUserSerializer,
    ListCustomUserSerializer,
    CustomTokenObtainPairSerializer,
    PlayListSerializer,
    MovieSerializer,
    PlayListDetailSerializer,
    MovieReviewSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser
from movies.models import PlayList, Movie


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

    def get_queryset(self):
        return PlayList.objects.filter(created_by=self.request.user)


class RetrieveUpdateDestroyPlayListApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, id=self.kwargs["pk"], created_by=self.request.user
        )
        return obj

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PlayListDetailSerializer
        return PlayListSerializer


class AddMovieToPlayListApiView(UpdateAPIView):
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    permission_classes = [IsAuthenticated]

    # Override the update method directly for custom logic
    def update(self, request, *args, **kwargs):
        playlist = self.get_object()  # Get the specific playlist by pk

        movie_data = request.data.get(
            "movie", {}
        )  # Expecting movie details under a 'movie' key
        imdb_id = movie_data.get("imdb_id")

        if not imdb_id:
            return Response(
                {"detail": "movie_id is required within the 'movie' data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # 1. Get or Create the Movie object
            movie_serializer = MovieSerializer(data=movie_data)
            movie_serializer.is_valid(raise_exception=True)

            try:
                # Try to get existing movie by imdb_id
                movie_obj = Movie.objects.get(imdb_id=imdb_id)
                for attr, value in movie_data.items():
                    if (
                        hasattr(movie_obj, attr) and attr != "created_by"
                    ):  # Prevent changing creator
                        setattr(movie_obj, attr, value)
                movie_obj.save()  # Save updates if any
                created_new_movie = False
            except Movie.DoesNotExist:
                # If not found, create a new movie
                movie_obj = movie_serializer.save(created_by=self.request.user)
                created_new_movie = True

            playlist.movies.add(movie_obj)
            playlist.save()

        updated_playlist_serializer = PlayListSerializer(playlist)
        return Response(updated_playlist_serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        # Your existing get_object remains the same
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, pk=self.kwargs["pk"], created_by=self.request.user
        )
        return obj

    def get_queryset(self):
        # Your existing get_queryset remains the same
        return PlayList.objects.filter(created_by=self.request.user)


class RemoveMovieFromPlayListApiView(UpdateAPIView):

    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        playlist = self.get_object()  # Get the specific playlist by pk
        movie_id = request.data.get("movie_id")

        if not movie_id:
            return Response(
                {"detail": "movie_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            print('Movie ID:', movie_id)
            movie_obj = Movie.objects.get(id=movie_id)
            playlist.movies.remove(movie_obj)
            playlist.save()
            return Response(
                {"detail": "Movie removed from playlist."}, status=status.HTTP_200_OK
            )
        except Movie.DoesNotExist:
            return Response(
                {"detail": "Movie not found in this playlist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, pk=self.kwargs["pk"], created_by=self.request.user
        )
        return obj

    def get_queryset(self):
        return PlayList.objects.filter(created_by=self.request.user)
    

class MovieReviewApiView(UpdateAPIView):
    serializer_class = MovieReviewSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, id=self.kwargs["pk"], created_by=self.request.user
        )
        return obj

    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_movie = serializer.save()
        return Response(MovieSerializer(updated_movie).data, status=status.HTTP_200_OK)
