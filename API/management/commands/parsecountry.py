from typing import Any
from bs4 import BeautifulSoup
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from .parsers import LinksParser, StationPageSoupParser
from alive_progress import alive_bar

from ...models import City, Country, Genre, Links, State, Station


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        # res = LinksParser.country_links_parser("https://mytuner-radio.com")
        # LinksParser.station_links_parser(res[0], res[1])
        with alive_bar(len(Links.objects.filter(is_parsed=False))) as bar:
            for obj in Links.objects.filter(is_parsed=False):
                soup = BeautifulSoup(requests.get(obj.link).text, "lxml").find("div", id="left-container")
                station_name = StationPageSoupParser.get_station_name(soup)
                country = StationPageSoupParser.get_country(soup)
                state = StationPageSoupParser.get_state(soup)
                city = StationPageSoupParser.get_city(soup)
                genres = StationPageSoupParser.get_genres(soup)
                socials = StationPageSoupParser.get_socials(soup)
                contacts = StationPageSoupParser.get_contacts(soup)
                frequencies = StationPageSoupParser.get_frequency(soup)
                country_obj, _ = Country.objects.get_or_create(country_name=country)
                state_obj, _ = State.objects.get_or_create(country=country_obj, state_name=state)
                city_obj, _ = City.objects.get_or_create(country=country_obj, state=state_obj, city_name=city)
                genres = [Genre.objects.get_or_create(genre=genre)[0] for genre in genres]
                station_obj, _ = Station.objects.get_or_create(
                    station_name=station_name,
                    city=city_obj,
                    socials=socials,
                    contacts=contacts,
                    frequency=frequencies,
                )
                station_obj.genres.add(*genres)
                station_obj.save()
                obj.is_parsed = True
                obj.save()
                bar()
