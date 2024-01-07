import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from ...models import Links


class LinksParser:
    @staticmethod
    def country_links_parser(url):
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        continents = soup.find(class_="continents")
        continents_links = []
        for continent_link in continents.find_all("a"):
            continents_links.append(url.strip(" \n") + continent_link.get("href").strip(" \n"))
        return continents_links

    def station_links_parser(links):
        url = "https://mytuner-radio.com"
        with alive_bar(149) as bar:
            for continent_link in links:
                pages_req = BeautifulSoup(requests.get(continent_link).text, "html.parser")
                try:
                    pages_tag = pages_req.find("div", class_="pages")
                    pages = len(pages_tag.find_all("a"))
                except AttributeError:  ### Переписать
                    pages = 0
                for page in range(1, pages + 1):
                    req = requests.get(continent_link + f"?page={page}").text
                    stations = (
                        BeautifulSoup(req, "html.parser").find("div", class_="radio-list").find("ul").find_all("a")
                    )
                    for station in stations:
                        Links.objects.get_or_create(link=url + station.get("href"))
                bar()


class SoupObjectParser:
    @staticmethod
    def get_station_name(soup):
        name = soup.find("div", class_="radio-player")
        return name.find("h1").get_text() if name else ""

    @staticmethod
    def get_genres(soup):
        genres = soup.find("div", class_="categories")
        return [genre.get_text() for genre in genres.find_all("a")] if genres else []

    @staticmethod
    def get_contacts(soup):
        contacts = soup.find("div", class_="contacts")
        return {contacts[i].get_text(): contacts[i + 1].get_text() for i in range(0, len(contacts), 2)} if contacts else {}

    @staticmethod
    def get_frequency(soup):
        li_tags = soup.find("div", class_="frequencies")
        if not li_tags:
            return {}
        li = [i.get_text().strip("\n") for i in li_tags.find_all("div")]
        return dict(zip(li[::2], li[1::2]))

    @staticmethod
    def get_socials(soup):
        extra = soup.find("div", class_="extra")
        if not extra:
            return {}
        return dict(
            zip([i.get("aria-label") for i in extra.find_all("a")], [i.get("href") for i in extra.find_all("a")])
        )

    @staticmethod
    def get_country(soup):
        ul = soup.find("ul", class_="breadcrumbs")
        country = ul.find("a", {"name": "radio_country_list"})
        return country.get_text() if country else ""

    @staticmethod
    def get_state(soup):
        ul = soup.find("ul", class_="breadcrumbs")
        state = ul.find("a", {"name": "radio_state_list"})
        return state.get_text() if state else ""  ## Исправить

    @staticmethod
    def get_city(soup):
        ul = soup.find("ul", class_="breadcrumbs")
        city = ul.find("a", {"name": "radio_city_list"})
        return city.get_text() if city else "" ## Исправить
