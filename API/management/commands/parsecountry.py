from typing import Any
from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand
from .parsers import LinksParser, SoupObjectParser
from alive_progress import alive_bar
from ...models import City, Country, Genre, Links, State, Station
from API.tasks import country_parse


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links = LinksParser.country_links_parser("https://mytuner-radio.com")
        for continent_link in links:
            country_parse.delay(continent_link)