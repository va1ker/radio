from typing import Any
from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand
from .parsers import SoupObjectParser
from alive_progress import alive_bar
from django.db import transaction

from ...models import City, Country, Genre, Links, State, Station


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links = Links.objects.filter(is_parsed=False)
        with alive_bar(len(links)) as bar:
            for link in links.iterator(chunk_size=200):
                req = requests.get(link.link)
                soup = BeautifulSoup(req.text).find("div", class_="left-container")  ## Сделать проверку на статус код
                station_name = SoupObjectParser.get_station_name(soup)
                country = SoupObjectParser.get_country(soup)
                state = SoupObjectParser.get_state(soup)
                city = SoupObjectParser.get_city(soup)  ## Инициализировать объект и выполнять метод
                genres = SoupObjectParser.get_genres(soup)
                socials = SoupObjectParser.get_socials(soup)
                contacts = SoupObjectParser.get_contacts(soup)
                frequencies = SoupObjectParser.get_frequency(soup)


                country_obj, _ = Country.objects.get_or_create(country_name=country)
                state_obj, _ = State.objects.get_or_create(country=country_obj, state_name=state)
                city_obj, _ = City.objects.get_or_create(country=country_obj, state=state_obj, city_name=city)
                station_data = {
                    "station_name": station_name,
                    "city": city_obj,
                    "socials": socials,
                    "contacts": contacts,
                    "frequency": frequencies,
                }
                station = Station(**station_data)
                station.save()
                print(station_data)
                for genre in genres:
                    genre, _ = Genre.objects.get_or_create(genre=genre)
                    station.genres.add(genre)
                station.save()
                link.is_parsed = True
                link.save()
                bar()
