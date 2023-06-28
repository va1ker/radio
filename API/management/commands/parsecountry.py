from django.core.management.base import BaseCommand
from ...models import Country, State, City, Genre, Station
import alive_progress
import json


class Command(BaseCommand):
    pass

    def handle(self, *args, **option):
        from bs4 import BeautifulSoup
        from requests import get

        url = get("https://mytuner-radio.com/" + "radio/")
        soup = BeautifulSoup(url.text, "lxml")
        with alive_progress.alive_bar(1) as bar:
            print("Parsing countries...")
            all_href = soup.find("div", class_="continents").find_all("a")
            countries_links = [item.get("href") for item in all_href]
            bar()
        for link in countries_links:
            url = get("https://mytuner-radio.com" + link)
            soup = BeautifulSoup(url.text, "lxml")
            try:
                options = soup.find("div", class_="styled-select").find_all("option")
            except AttributeError:
                options = [1]
            for i in range(len(options)):
                url = get(
                    "https://mytuner-radio.com"
                    + countries_links[countries_links.index(link)]
                    + f"?page={i}"
                )
                soup = BeautifulSoup(url.text, "lxml")
                all_stations = soup.find("ul", class_="radio-list").find_all("a")
                all_stations = [i.get("href") for i in all_stations]
                for station in all_stations:
                    url = get("https://mytuner-radio.com" + station)
                    soup = BeautifulSoup(url.text, "lxml")
                    container = soup.find("div", id="left-container")
                    location = container.find("div", class_="breadcrumbs").find_all("a")
                    location = [item.text for item in location]
                    try:
                        Country.objects.filter(country_name=location[0]).exists()
                        country_id = Country.objects.get(country_name=location[0]).id
                    except Country.DoesNotExist:
                        Country.objects.create(country_name=location[0])
                        country_id = Country.objects.get(country_name=location[0]).id
                    if len(location) > 1:
                        try:
                            State.objects.filter(state_name=location[1]).exists()
                            state_id = State.objects.get(state_name=location[1])
                        except State.DoesNotExist:
                            State.objects.create(
                                country_id=country_id, state_name=location[1]
                            )
                            state_id = State.objects.get(state_name=location[1])
                        try:
                            City.objects.filter(city_name=location[2]).exists()
                            city_id = City.objects.get(city_name=location[2])
                        except City.DoesNotExist:
                            City.objects.create(
                                country_id=country_id,
                                state_id=state_id,
                                city_name=location[2],
                            )
                            city_id = City.objects.get(city_name=location[2])
                    categories = container.find("div", class_="categories").find_all(
                        "a"
                    )
                    genres = []
                    for c in categories:
                        try:
                            Genre.objects.filter(genre=c.text).exists()
                            genres.append(Genre.objects.get(genre=c.text))
                        except Genre.DoesNotExist:
                            Genre.objects.create(genre=c.text)
                            genres.append(Genre.objects.get(genre=c.text))
                    station_name = container.find("h1", class_="title").text
                    fdiv = container.find("div", class_="frequencies")
                    fname = fdiv.find_all("div", class_="name")
                    fvalue = fdiv.find_all("div", class_="frequency")
                    frequencies = {}
                    if fname:
                        for i, k in fname, fvalue:
                            frequencies[i.text] = k.text
                    contacts = soup.find("contacts").find_all("p")
                    if contacts:
                        for contact in contacts:
                            contact.text.replace("&nbsp", " ").split()
