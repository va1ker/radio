from django.shortcuts import render
from rest_framework import generics, serializers

from .models import City, Country, Station
from .serializers import CitySerializer, CountrySerializer, StationSerializer


class StationAPI(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class CountryAPI(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityAPI(generics.ListAPIView):
    queryset = City.objects.select_related("country", "state")
    serializer_class = CitySerializer
