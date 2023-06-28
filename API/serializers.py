from rest_framework import serializers
from .models import Station, Country, City


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("station_name", "frequency", "city", "genres", "contacts", "socials")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("country_name",)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
