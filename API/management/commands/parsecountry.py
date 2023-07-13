from typing import Any
from bs4 import BeautifulSoup
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from parsers import LinksParser, SoupOjbectParser

from ...models import City, Country, Genre, Links, State, Station


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        LinksParser.station_links_parser(LinksParser.country_links_parser)
        for obj in Links.objects.filter(is_parsed=False):
            soup = BeautifulSoup(requests.get(obj.link)).find("div", id="left-container")
            station_name = SoupOjbectParser.get_station_name(soup)
            country = SoupOjbectParser.get_country(soup)
            state = SoupOjbectParser.get_state(soup)
            city = SoupOjbectParser.get_city(soup)
            genres = SoupOjbectParser.get_genres(soup)
            socials = SoupOjbectParser.get_socials(soup)
            contacts = SoupOjbectParser.get_contacts(soup)
            frequencies = SoupOjbectParser.get_frequency(soup)

            country_obj = Country.objects.get_or_create(country)
            state_obj = State.objects.get_or_create(country_obj, state)
            city_obj = City.objects.get_or_create(country_obj,state_obj, city)
            genres_obj = Genre.objects.get_or_create(genres)
            station_obj = {
                "station_name": station_name,
                "city": city_obj,
                "genres": genres_obj,
                "social": socials,
                "contacts": contacts,
                "frequencies": frequencies
            }
            Station.objects.get_or_create(station_obj)



LinksParser.country_links_parser("https://mytuner-radio.com")
