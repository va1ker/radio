from rest_framework import serializers

from .models import City, Country, Station, Links


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


class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = "__all__"
