from django.shortcuts import render
from rest_framework import generics, serializers

from .models import City, Country, Station, Links
from .serializers import CitySerializer, CountrySerializer, StationSerializer, LinksSerializer


class StationList(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def get_queryset(self):
        queryset = Station.objects.all()
        city_name = self.request.query_params.get("city", None)

        if city_name:
            queryset = queryset.filter(city__city_name__icontains=city_name)

        return queryset
