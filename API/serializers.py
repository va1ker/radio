from rest_framework import serializers

from .models import City, Country, Genre, Like, Links, Station

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class StationSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = "__all__"

    def get_likes_count(self, instance):
        return instance.likes.count()


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


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'