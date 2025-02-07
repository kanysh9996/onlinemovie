from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

STATUS_CHOICES = (
    ('pro', 'Pro'),
    ('simple', 'Simple')
)

class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators= [MinValueValidator(18), MaxValueValidator(65)], null=True, blank=True)
    phone_number =  PhoneNumberField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=32, default='simple')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=32)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField()
    director_image = models.ImageField(upload_to='director_image', null=True, blank=True)

    def __str__(self):
        return self.director_name

class Actor(models.Model):
    actor_name = models.CharField(max_length=32)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(default=0)
    actor_image = models.ImageField(upload_to='actor_images', null=True, blank=True)

    def __str__(self):
        return self.actor_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=32)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='country')
    director = models.ManyToManyField(Director, related_name='director')
    actor = models.ManyToManyField(Actor, related_name='actor')
    genre = models.ManyToManyField(Genre, related_name='genre')
    TYPES_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p')
    )
    types = models.CharField(choices=TYPES_CHOICES, max_length=32, default='360 p')
    movie_time = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    movie_trailer = models.FileField(upload_to='trailer/', null=True, blank=True)
    movie_image = models.ImageField(upload_to='image/', null=True, blank=True)
    status_movie = models.CharField(max_length=12, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return self.movie_name


class MovieLanguages(models.Model):
    language = models.CharField(max_length=16)
    video = models.FileField(upload_to='movie_languages/', null=True, blank=True)
    movie_language = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_languages')


class Moments(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_moments')
  movie_moments = models.FileField(upload_to='moments/', null=True, blank=True)


class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='rating')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range (1, 11)])
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.movie}'


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='user')


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='cart')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie')


class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie_history = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
