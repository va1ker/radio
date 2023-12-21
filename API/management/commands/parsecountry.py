from typing import Any
from bs4 import BeautifulSoup
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from .parsers import LinksParser, SoupObjectParser

from ...models import City, Country, Genre, Links, State, Station


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links, url = LinksParser.country_links_parser("https://mytuner-radio.com")
        LinksParser.station_links_parser(links, url)
        for obj in Links.objects.filter(is_parsed=False):
            soup = BeautifulSoup(requests.get(obj.link)).find("div", id="left-container")
            station_name = SoupObjectParser.get_station_name(soup)
            country = SoupObjectParser.get_country(soup)
            state = SoupObjectParser.get_state(soup)
            city = SoupObjectParser.get_city(soup)  ## Инициализировать объект и выполнять метод
            genres = SoupObjectParser.get_genres(soup)
            socials = SoupObjectParser.get_socials(soup)
            contacts = SoupObjectParser.get_contacts(soup)
            frequencies = SoupObjectParser.get_frequency(soup)

            country_obj = Country.objects.get_or_create(country)
            state_obj = State.objects.get_or_create(country_obj, state)
            city_obj = City.objects.get_or_create(country_obj, state_obj, city)
            genres_obj = Genre.objects.get_or_create(genres)
            station_obj = {
                "station_name": station_name,
                "city": city_obj,
                "genres": genres_obj,
                "social": socials,
                "contacts": contacts,
                "frequencies": frequencies,
            }
            Station.objects.get_or_create(station_obj)


LinksParser.country_links_parser("https://mytuner-radio.com")
