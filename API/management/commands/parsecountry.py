from typing import Any

import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from API.tasks import country_parse

from ...models import City, Country, Genre, Links, State, Station
from .parsers import LinksParser, SoupObjectParser


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        links = LinksParser.country_links_parser("https://mytuner-radio.com")
        for continent_link in links:
            country_parse.delay(continent_link)