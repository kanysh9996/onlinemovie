from django.db.models import DateField
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language', 'video']


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']
        

class RatingSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    user = ProfileSimpleSerializer()
    class Meta:
        model = Rating
        fields = ['id', 'user', 'text', 'parent', 'stars', 'created_date']


class RatingEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format('%Y'))
    genre = GenreSerializer(many=True)
    country = CountrySerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'year', 'genre', 'country']


class MovieDetailSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format('%d-%m-%Y'))
    genre = GenreSerializer(many=True)
    country = CountrySerializer(many=True)
    director = DirectorSerializer(many=True)
    actor = ActorSerializer(many=True)
    movie_languages = MovieLanguagesSerializer(many=True, read_only=True)
    movie_moments = MomentsSerializer(many=True, read_only=True)
    rating = RatingSerializer(many=True, read_only=True)
    avg_ratings = serializers.SerializerMethodField()
    count_user = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['movie_name', 'movie_image', 'movie_trailer', 'types', 'director', 'actor', 'year', 'genre', 'country',
                  'movie_time', 'description', 'status_movie', 'movie_languages', 'movie_moments',
                  'rating', 'avg_ratings', 'count_user']


    def get_avg_ratings(self, obj):
        return obj.get_avg_ratings()

    def get_count_user(self, obj):
        return obj.get_count_user()


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','country_name']


class CountryDetailSerializer(serializers.ModelSerializer):
    country = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['country_name', 'country']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name']


class DirectorDetailSerializer(serializers.ModelSerializer):
    director = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Director
        fields = ['director_name', 'bio', 'age', 'director_image', 'director']


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name']


class ActorDetailSerializer(serializers.ModelSerializer):
    actor = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Actor
        fields = ['actor_name', 'bio', 'age', 'actor_image', 'actor']


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','genre_name']


class GenreDetailSerializer(serializers.ModelSerializer):
    genre = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ['genre_name', 'genre']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'