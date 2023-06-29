from typing import Any

import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from ...models import City, Country, Genre, Links, State, Station


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        Parser.station_links_parser()


url = "https://mytuner-radio.com"


class Parser:
    @staticmethod
    def station_links_parser():
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        continents = soup.find(class_="continents")
        continents_links = []
        for continent_link in continents.find_all("a"):
            continents_links.append(url + continent_link.get("href"))
        with alive_bar(149) as bar:
            for continent_link in continents_links:
                option = BeautifulSoup(requests.get(continent_link).text, "lxml").find_all("option")
                for page in range(1, len(option) + 1):
                    stations = (
                        BeautifulSoup(requests.get(continent_link + f"?page={page}").text, "lxml")
                        .find("ul", class_="radio-list")
                        .find_all("a")
                    )
                    for station in stations:
                        try:
                            Links.objects.get(link=url + station.get("href"))
                        except ObjectDoesNotExist:
                            obj = Links.objects.create(link=url + station.get("href"))
                            obj.save()
                bar()

    def station_name_parser(link):
        return BeautifulSoup(requests.get(link).text, "lxml").find("h1", class_="title").get_text()

    def genres_parser(link):
        genres = BeautifulSoup(requests.get(link).text, "lxml").find("div", class_="categories").find_all("a")
        return [genre.get_text() for genre in genres]

    def contacts_parser(link):
        p_tags = BeautifulSoup(requests.get(link).text, "lxml").find("div", class_="contacts").find_all("p")
        return dict([p.get_text().split("&nbsp") for p in p_tags])

    def frequency_parser(link):
        li_tags = BeautifulSoup(requests.get(link).text, "lxml").find("div", class_="frequencies").find_all("div")
        li = [i.get_text().strip("\n") for i in li_tags]
        return dict(zip(li[::2], li[1::2]))

    def social_parser(link):
        extra = BeautifulSoup(requests.get(link).text, "lxml").find("div", class_="extra").find_all("a")
        return dict(zip([i.get("aria-label") for i in extra], [i.get("href") for i in extra]))

    def country_parser(link):
        return BeautifulSoup(requests.get(link).text, "lxml").find("a", class_="radio_country_list").get_text()

    def state_parser(link):
        return BeautifulSoup(requests.get(link).text, "lxml").find("a", class_="radio_state_list").get_text()

    def town_parser(link):
        return BeautifulSoup(requests.get(link).text, "lxml").find("a", class_="radio_city_list").get_text()
