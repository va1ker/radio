from django.shortcuts import render
from rest_framework import generics, serializers
from django.contrib.auth.models import User
from django.db.models import Count

from .models import City, Country, Genre, Links, Station, Like
from .serializers import (
    CitySerializer,
    CountrySerializer,
    GenresSerializer,
    LinksSerializer,
    StationSerializer,
    UserSerializer,
    LikeSerializer,
)

from rest_framework.permissions import IsAuthenticated


class LikeStation(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StationList(generics.ListAPIView):
    serializer_class = StationSerializer

    def get_queryset(self):
        queryset = Station.objects.annotate(likes_count=Count("likes"))
        city_name = self.request.query_params.get("city", None)
        state_name = self.request.query_params.get("state", None)
        country_name = self.request.query_params.get("country", None)
        genre_name = self.request.query_params.getlist("genres[]", None)

        if city_name:
            queryset = queryset.filter(city__city_name__icontains=city_name)

        if state_name:
            queryset = queryset.filter(state__state_name__icontains=state_name)

        if country_name:
            queryset = queryset.filter(country__country_name__icontains=country_name)

        if genre_name:
            queryset = queryset.filter(genres__id__in=genre_name)

        return queryset.all().order_by("-likes_count")


class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class GenreList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer

    def get_queryset(self):
        queryset = Station.objects.all()
        genre_name = self.request.query_params.get("genre", None)
        if genre_name:
            queryset = queryset.filter(genre__icontains=genre_name)


# class StationList(generics.ListAPIView):
#     queryset = Country.objects.all()
#     serializer_class = StationSerializer

#     def get_queryset(self):
#         queryset = Station.objects.all()
#         city_name = self.request.query_params.get("city", None)

#         if city_name:
#             queryset = queryset.filter(city__city_name__icontains=city_name)

#         return queryset
