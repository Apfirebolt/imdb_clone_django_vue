from django.db import models
from imdb_clone.settings import AUTH_USER_MODEL
    

class Movie(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movies_created')
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    primary_image = models.URLField(blank=True, null=True)
    trailer = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    metascore = models.IntegerField(blank=True, null=True)
    genres = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' ' + self.created_by.username
    

class PlayList(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists_created')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    movies = models.ManyToManyField('Movie', related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
