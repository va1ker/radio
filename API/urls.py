from django.urls import path

from API.views import StationList, GenreList, UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("stations/", StationList.as_view()),
    path("genres/", GenreList.as_view()),
    path("register/", UserCreateView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
