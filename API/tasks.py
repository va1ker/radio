from celery import shared_task
import requests
from bs4 import BeautifulSoup
from API.management.commands.parsers import SoupObjectParser
from API.models import Country, State, City, Station, Genre, Links
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
