from rest_framework import serializers
from users.models import CustomUser
from movies.models import PlayList, Movie, AuditLog
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('No account exists with these credentials, check password and email')
    }

    def validate(self, attrs):
        
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data 
        data.update({'userData': {
            'email': self.user.email,
            'username': self.user.username,
            'id': self.user.id
        }})
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_staff', 'password', 'access', 'refresh',)
    
    def get_refresh(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def get_access(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token),
        return access

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ListCustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_picture', 'is_staff',)


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('id', 'name', 'created_by', 'created_at', 'description')
        read_only_fields = ('created_at', 'created_by')

    def validate_name(self, value):
        # Access the request user from the context
        request_user = self.context.get('request').user
        if not request_user.is_authenticated:
            raise serializers.ValidationError("Authentication required to create a playlist.")

        if PlayList.objects.filter(name=value, created_by=request_user).exists():
            raise serializers.ValidationError("You already have a playlist with this name.")
        return value
    

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')


class PlayListDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    is_locked = serializers.BooleanField(source='created_by.is_locked', read_only=True)

    class Meta:
        model = PlayList
        fields = ('id', 'name', 'created_by', 'created_at', 'description', 'movies', 'is_locked')


class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'review', 'is_watched', 'is_favorite')
        read_only_fields = ('created_by', 'created_at')

    def update(self, instance, validated_data):
        instance.review = validated_data.get('review', instance.review)
        instance.is_watched = validated_data.get('is_watched', instance.is_watched)
        instance.is_favorite = validated_data.get('is_favorite', instance.is_favorite)
        instance.save()
        return instance
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_locked', 'profile_picture', 'password',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'user', 'action', 'timestamp', 'details')
        read_only_fields = ('id', 'user', 'timestamp', 'details')

