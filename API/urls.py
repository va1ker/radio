from django.urls import path

from API.views import StationList, GenreList

urlpatterns = [
    path("stations/", StationList.as_view()),
    path("genres/",GenreList.as_view()),
    
]
