from API.views import CityAPI, CountryAPI, StationAPI, LinksForParsingAPI
from django.urls import path

urlpatterns = [
    path("countrys/", CountryAPI.as_view()),
    path("cities/", CityAPI.as_view()),
    path("links/", LinksForParsingAPI.as_view()),
]
