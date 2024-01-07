from typing import Any

import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db import transaction

from API.tasks import create_station

from ...models import City, Country, Genre, Links, State, Station
from .parsers import SoupObjectParser


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links = Links.objects.filter(is_parsed=False)
        for link in links:
            print(link.link)
            create_station.delay(link.link)
