import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from ...models import Links


class LinksParser:
    @staticmethod
    def country_links_parser(url):
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        continents = soup.find(class_="continents")
        continents_links = []
        for continent_link in continents.find_all("a"):
            continents_links.append(url + continent_link.get("href"))
        return continents_links, url

    @staticmethod
    def station_links_parser(links, url):
        with alive_bar(149) as bar:
            for continent_link in links:
                option_text = BeautifulSoup(requests.get(continent_link).text, "lxml").find_all("option")
                for page in range(1, len(option_text) + 1):
                    stations = (
                        BeautifulSoup(requests.get(continent_link + f"?page={page}").text, "lxml")
                        .find("ul", class_="radio-list")
                        .find_all("a")
                    )
                    for station in stations:
                        Links.objects.get_or_create(link=url + station.get("href"))
                bar()


class StationPageSoupParser:
    @staticmethod
    def get_station_name(soup):
        try:
            h1 = soup.find("h1", class_="title")
            return h1.get_text()
        except AttributeError:
            return ""

    @staticmethod
    def get_genres(soup):
        try:
            genres = soup.find("div", class_="categories").find_all("a")
            return [genre.get_text() for genre in genres]
        except AttributeError:
            return ""

    @staticmethod
    def get_contacts(soup):
        try:
            contacts = soup.find("div", class_="contacts").find_all("p")
            return dict([p.get_text().split("&nbsp") for p in contacts])
        except AttributeError:
            return {}

    @staticmethod
    def get_frequency(soup):
        try:
            li_tags = soup.find("div", class_="frequencies").find_all("div")
            li = [i.get_text().strip("\n") for i in li_tags]
            return dict(zip(li[::2], li[1::2]))
        except AttributeError:
            return {}

    @staticmethod
    def get_socials(soup):
        try:
            socials = soup.find("div", class_="extra").find_all("a")
            return dict(zip([i.get("aria-label") for i in socials], [i.get("href") for i in socials]))
        except AttributeError:
            return {}

    @staticmethod
    def get_country(soup):
        try:
            country = soup.find("a", class_="radio_country_list")
            return country.get_text()
        except AttributeError:
            return ""

    @staticmethod
    def get_state(soup):
        try:
            state = soup.find("a", class_="radio_state_list")
            return state.get_text()
        except AttributeError:
            return ""

    @staticmethod
    def get_city(soup):
        try:
            city = soup.find("a", class_="radio_city_list")
            return city.get_text()
        except AttributeError:
            return ""
