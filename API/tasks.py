import requests
from bs4 import BeautifulSoup
from celery import shared_task

from API.management.commands.parsers import SoupObjectParser
from API.models import City, Country, Genre, Links, State, Station
from radioAPI.celery import app


@app.task
def create_station(link):
    request = requests.get(link)
    soup = BeautifulSoup(request.text).find("div", class_="left-container")
    station_name = SoupObjectParser.get_station_name(soup)
    country = SoupObjectParser.get_country(soup)
    state = SoupObjectParser.get_state(soup)
    city = SoupObjectParser.get_city(soup)  ## Инициализировать объект и выполнять метод
    genres = SoupObjectParser.get_genres(soup)
    socials = SoupObjectParser.get_socials(soup)
    contacts = SoupObjectParser.get_contacts(soup)
    frequencies = SoupObjectParser.get_frequency(soup)

    country_obj, _ = Country.objects.get_or_create(country_name=country)
    state_obj, _ = State.objects.get_or_create(country=country_obj, state_name=state)
    city_obj, _ = City.objects.get_or_create(country=country_obj, state=state_obj, city_name=city)
    station_data = {
        "station_name": station_name,
        "city": city_obj,
        "socials": socials,
        "contacts": contacts,
        "frequency": frequencies,
    }
    station = Station(**station_data)
    station.save()
    print(station_data)
    for genre in genres:
        genre, _ = Genre.objects.get_or_create(genre=genre)
        station.genres.add(genre)
    station.save()
    Links.objects.filter(link=link).update(is_parsed=True)


@app.task
def country_parse(continent_link):
    url = "https://mytuner-radio.com"
    pages_req = BeautifulSoup(requests.get(continent_link).text, "html.parser")
    try:
        pages_tag = pages_req.find("div", class_="pages")
        pages = len(pages_tag.find_all("a"))
    except AttributeError:  ### Переписать
        pages = 0
    for page in range(1, pages + 1):
        req = requests.get(continent_link + f"?page={page}").text
        stations = BeautifulSoup(req, "html.parser").find("div", class_="radio-list").find("ul").find_all("a")
        for station in stations:
            Links.objects.get_or_create(link=url + station.get("href"))


@app.task
def update_country(link):
    req = requests.get(link).text
    soup = BeautifulSoup(req)
    station_name = SoupObjectParser.get_station_name(soup)
    country_name = SoupObjectParser.get_country(soup)
    state_name = SoupObjectParser.get_state(soup)
    try:
        country_obj = Country.objects.get(country_name=country_name)
        state_obj = State.objects.get(state_name=state_name)
        station_obj = Station.objects.get(station_name=station_name)
        station_obj.country = country_obj
        station_obj.state = state_obj
        station_obj.save()
    except:
        pass

@app.task
def update_genres(link):
    req = requests.get(link).text
    soup = BeautifulSoup(req)
    station_name = SoupObjectParser.get_station_name(soup)
    genres = SoupObjectParser.get_genres(soup)
    try:
        station_obj = Station.objects.get(station_name=station_name)
        for genre in genres:
            genre, _ = Genre.objects.get_or_create(genre=genre)
            station_obj.genres.add(genre)
        station_obj.save()
    except:
        pass
