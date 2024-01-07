from typing import Any
from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand
from .parsers import LinksParser, SoupObjectParser
from alive_progress import alive_bar
from ...models import City, Country, Genre, Links, State, Station
from API.tasks import update_country

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links = Links.objects.all()
        for link in links:
            update_country.delay(link.link)