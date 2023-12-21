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
            continents_links.append(url.strip(" \n") + continent_link.get("href").strip(" \n"))
        print(continents_links)
        return continents_links, url

    def station_links_parser(links, url):
        with alive_bar(149) as bar:
            for continent_link in links:
                pages_req = BeautifulSoup(requests.get(continent_link).text, "lxml")
                try:
                    pages_tag = pages_req.find("div", class_="pages")
                    if pages_tag:
                        pages = len(pages_tag.find_all("a"))
                    else:
                        pages = 0
                except AttributeError:
                    pages = 0
                for page in range(1, pages + 1):
                    req = requests.get(continent_link + f"?page={page}").text
                    stations = BeautifulSoup(req, "lxml").find("div", class_="radio-list").find_all("a")
                    for station in stations:
                        Links.objects.get_or_create(link=url + station.get("href"))
                bar()


class SoupObjectParser:
    def get_station_name(soup):
        return soup.find("h1", class_="title").get_text()

    def get_genres(soup):
        genres = soup.find("div", class_="categories").find_all("a")
        return [genre.get_text() for genre in genres]

    def get_contacts(soup):
        p_tags = soup.find("div", class_="contacts").find_all("p")
        return dict([p.get_text().split("&nbsp") for p in p_tags])

    def get_frequency(soup):
        li_tags = soup.find("div", class_="frequencies").find_all("div")
        li = [i.get_text().strip("\n") for i in li_tags]
        return dict(zip(li[::2], li[1::2]))

    def get_socials(soup):
        extra = soup.find("div", class_="extra").find_all("a")
        return dict(zip([i.get("aria-label") for i in extra], [i.get("href") for i in extra]))

    def get_country(soup):
        return soup.find("a", class_="radio_country_list").get_text()

    def get_state(soup):
        return soup.find("a", class_="radio_state_list").get_text()

    def get_city(soup):
        return soup.find("a", class_="radio_city_list").get_text()
