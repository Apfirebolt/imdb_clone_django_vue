from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import (
    CustomUserSerializer,
    UserProfileSerializer,
    ListCustomUserSerializer,
    CustomTokenObtainPairSerializer,
    PlayListSerializer,
    MovieSerializer,
    PlayListDetailSerializer,
    MovieReviewSerializer,
    AuditLogSerializer,
    PersonalMessagesSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser, PersonalMessages
from movies.models import PlayList, Movie, AuditLog
from django.contrib.auth.hashers import make_password


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    

class UserProfileApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data

        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        profile_picture = data.get("profile_picture")
        is_locked = data.get("is_locked", False)
        if is_locked == 'true':
            is_locked = True
        else:
            is_locked = False
        if profile_picture:
            user.profile_picture = profile_picture # Assuming profile_picture is a FileField or ImageField

            # if size of the image exceeds 5MB, return error
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB
                return Response(
                    {"detail": "Profile picture size exceeds 5MB."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if email:
            user.email = email
        if username:
            user.username = username
        if password:
            user.password = make_password(password)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if is_locked is not None:
            user.is_locked = is_locked

        user.save()
        # Log the action in AuditLog
        AuditLog.objects.create(
            user=self.request.user,
            action="Updated user profile",
            details={
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "is_locked": is_locked
            }
        )   
        return Response({"detail": "Profile updated successfully."}, status=status.HTTP_200_OK)

class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class UserDetailApiView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        return obj


class ListCreatePlayListApiView(ListCreateAPIView):
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

        # Log the action in AuditLog
        AuditLog.objects.create(
            user=self.request.user,
            action="Created a new playlist",
            details={"playlist_name": serializer.validated_data['name']}
        )

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return PlayList.objects.filter(created_by_id=user_id)
        return PlayList.objects.filter(created_by=self.request.user)


class RetrieveUpdateDestroyPlayListApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            obj = get_object_or_404(
                queryset, id=self.kwargs["pk"], created_by=self.request.user
            )
        else:
            obj = get_object_or_404(
                queryset, id=self.kwargs["pk"]
            )
        return obj

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PlayListDetailSerializer
        return PlayListSerializer
    
    def update(self, request, *args, **kwargs):
        playlist = self.get_object()
        serializer = self.get_serializer(playlist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_playlist = serializer.save()

        # Log the action in AuditLog
        AuditLog.objects.create(
            user=self.request.user,
            action="Updated playlist",
            details={"playlist_id": updated_playlist.id, "name": updated_playlist.name}
        )

        return Response(PlayListDetailSerializer(updated_playlist).data, status=status.HTTP_200_OK)
    

    def delete(self, request, *args, **kwargs):
        playlist = self.get_object()
        # Log the action in AuditLog before deletion
        AuditLog.objects.create(
            user=self.request.user,
            action="Deleted playlist",
            details={"playlist_id": playlist.id, "name": playlist.name}
        )
        return super().delete(request, *args, **kwargs) 


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

        # 2. Log the action in AuditLog
        action = "Added movie to playlist" if created_new_movie else "Updated movie in playlist"
        AuditLog.objects.create(
            user=self.request.user,
            action=action,
            details={
                "playlist_id": playlist.id,
                "movie_id": movie_obj.id,
                "imdb_id": imdb_id
            }
        )

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

            # Log the action in AuditLog
            AuditLog.objects.create(
                user=self.request.user,
                action="Removed movie from playlist",
                details={
                    "playlist_id": playlist.id,
                    "movie_id": movie_obj.id,
                    "imdb_id": movie_obj.imdb_id
                }
            )
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

        # Log the action in AuditLog
        AuditLog.objects.create(
            user=self.request.user,
            action="Reviewed movie",
            details={
                "movie_id": updated_movie.id,
                "review": updated_movie.review,
                "is_watched": updated_movie.is_watched,
                "is_favorite": updated_movie.is_favorite
            }
        )
        return Response(MovieSerializer(updated_movie).data, status=status.HTTP_200_OK)
    

class AuditLogListApiView(ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AuditLog.objects.filter(user=self.request.user)
    

class PersonalMessagesListApiView(ListAPIView):
    serializer_class = PersonalMessagesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PersonalMessages.objects.filter(recipient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
