from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

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
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    contacts = models.JSONField()
    socials = models.JSONField()

    def __str__(self):
        return self.station_name

    # @property
    # def total_likes(self):
    #     return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "station")


# class Podcats(models.Model):
#     podcast_name = models.CharField(max_length=100)
#     category = models.ForeignKey(max_length=100)
#     station = models.ForeignKey(Station)
#     contacts = models.JSONField()
#     socials = models.JSONField()
#     likes = models.PositiveIntegerField()
