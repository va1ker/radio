from typing import Any

import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from API.tasks import update_country

from ...models import City, Country, Genre, Links, State, Station
from .parsers import LinksParser, SoupObjectParser


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links = Links.objects.all()
        for link in links:
            update_country.delay(link.link)