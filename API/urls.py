from API.views import StationList
from django.urls import path

urlpatterns = [
    path("stations/", StationList.as_view()),
]
