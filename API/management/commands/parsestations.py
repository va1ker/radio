from typing import Any
from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand
from .parsers import SoupObjectParser
from alive_progress import alive_bar
from django.db import transaction

from ...models import City, Country, Genre, Links, State, Station
from API.tasks import create_station


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links = Links.objects.filter(is_parsed=False)
        for link in links:
            print(link.link)
            create_station.delay(link.link)
