from django.conf import settings
from django.db import models

# class User(models.User):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)


class Links(models.Model):
    link = models.TextField()
    is_parsed = models.BooleanField(default=False)


class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country_name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=100)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)


class Genre(models.Model):
    genre = models.CharField(max_length=100, unique=True)


class Station(models.Model):
    station_name = models.CharField(max_length=100)
    frequency = models.JSONField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    contacts = models.JSONField()
    socials = models.JSONField()

    def __str__(self):
        return self.station_name

    # @property
    # def total_likes(self):
    #     return self.likes.count()


# class Podcats(models.Model):
#     podcast_name = models.CharField(max_length=100)
#     category = models.ForeignKey(max_length=100)
#     station = models.ForeignKey(Station)
#     contacts = models.JSONField()
#     socials = models.JSONField()
#     likes = models.PositiveIntegerField()


# class Like(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="likes", on_delete=models.CASCADE)
