from django.shortcuts import render
from rest_framework import generics
from .models import Station, Country, City
from .serializers import (
    StationSerializer,
    CountrySerializer,
    CitySerializer,
)
from rest_framework import serializers


class StationAPI(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class CountryAPI(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityAPI(generics.ListAPIView):
    queryset = City.objects.select_related("country", "state")
    serializer_class = CitySerializer
