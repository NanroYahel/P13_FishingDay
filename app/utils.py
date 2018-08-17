"""File containing the function called by the views"""

from datetime import datetime
import calendar
import time
import arrow
import requests as req
from flask import current_app
from app import db
from app.models import City, UserSearch


#Constant used to convert wind direction
DIRECTION = {1:'N', 2:'NNE', 3:'NE', 4:'ENE', 5:'E', 6:'ESE', 7:'SE', 8:'SSE', 9:'S', 10:'SSO', \
            11:'SO', 12:'OSO', 13:'O', 14:'ONO', 15:'NO', 16:'NNO', 17:'N'}

####### Function used to get data from differents API

def request_api(url):
    """Request the selected url and return data from the api as json"""
    data = req.get(url)
    return data.json()

def get_meteo_for_city(city):
    """Method to get the meteo data with the api"""
    url = "http://api.openweathermap.org/data/2.5/forecast?q={},fr&mode=json&APPID={}".format(city,\
        current_app.config['OWM_API_KEY'])
    meteo_data = request_api(url)
    list_meteo_day = []
    for element in meteo_data['list']:
        new_meteo_day = MeteoDay(element)
        list_meteo_day.append(new_meteo_day)
    lat = meteo_data['city']['coord']['lat']
    lon = meteo_data['city']['coord']['lon']
    return lat, lon, list_meteo_day


def get_tides_for_city(lat, lon):
    """Method to get the tides data with the api"""
    today = time.time()
    url = "https://www.worldtides.info/api?extremes&start={}&length=259200&lat={}&lon={}&key={}".\
            format(today, lat, lon, current_app.config['WT_API_KEY'])
    tides_data = request_api(url)
    list_tides_extreme = []
    for element in tides_data['extremes']:
        new_tide_extreme = TideExtreme(element)
        list_tides_extreme.append(new_tide_extreme)
    return list_tides_extreme


####### Function used to format MeteoDay attributes #######

def convert_direction(direction):
    """Convert degree direction in cardinal direction"""
    number_direction = round(direction/22.5, 0) + 1
    return DIRECTION[number_direction]

def convert_temp(temp_kelvin):
    """Convert kelvin degrees to celsius degrees"""
    temp_celsius = round(temp_kelvin - 273.15)
    return temp_celsius

def convert_wind_speed(speed_ms):
    """Convert wind speed form m/s to Knots"""
    speed_kts = round(speed_ms/0.514, 0)
    return speed_kts

####### Function used to format TideExtreme attributes #######

def convert_type_fr(type_tide):
    """Convert the type of tide in french notation"""
    if type_tide == "High":
        type_tide = "PM"
    elif type_tide == "Low":
        type_tide = "BM"
    return type_tide

def find_weekday(date_time):
    """Find the day of the week from a datetime"""
    weekdays = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    weekday = calendar.weekday(date_time.year, date_time.month, date_time.day)
    return weekdays[weekday]


###### Functions used to interact with the db ######

def save_user_search(user, city, lat, lon):
    """Save the city if it not exists and then save the search"""
    #Check if the city is already in the database
    city_searched = find_city(city, lat, lon)
    if city_searched is not False:
        #Check if the search has already been made by this user if city exists
        check_search = UserSearch.query.get((user, city_searched))
        if check_search is not None:
            #If the search has already been made, increment the count
            check_search.count += 1
            check_search.timestamp = datetime.utcnow()

            db.session.commit()
        else:
            #Save the search
            save_search(user, city_searched)
    else:
        #Save the city if it doesn't exists and then save the search
        save_city(city, lat, lon)
        city_searched = City.query.filter_by(name=city, lat=lat, lon=lon).first()
        save_search(user, city_searched.id)

def find_city(city, lat, lon):
    """Return False if the city doesn't exists in the database or the id if it does """
    city_to_find = City.query.filter_by(name=city, lat=lat, lon=lon)
    if city_to_find.all() == []:
        city_searched = False
    else:
        city_searched = city_to_find.first().id
    return city_searched

def save_city(city, lat, lon):
    """Save a city in the database"""
    city_to_save = City(name=city, lat=lat, lon=lon)
    db.session.add(city_to_save)
    db.session.commit()

def save_search(user_id, city_id):
    """Save a user search in the database"""
    search_to_save = UserSearch(user_id=user_id, city_id=city_id, count=1)
    db.session.add(search_to_save)
    db.session.commit()


####### Classes #######

class MeteoDay:
    """Class containing all the meteo informations for a period"""

    def __init__(self, meteo):
        self.date = arrow.get(meteo['dt']).to('Europe/Paris')
        self.img = meteo['weather'][0]['icon']
        self.cloud = meteo['clouds']['all']
        self.temp = convert_temp(meteo['main']['temp'])
        self.wind_direction = convert_direction(float(meteo['wind']['deg']))
        self.wind_degree = int(meteo['wind']['deg'])
        self.wind_speed = int(convert_wind_speed(meteo['wind']['speed']))

        #Manages the case where there is no rainy day in the period
        try:
            self.rain = round(meteo['rain']['3h'], 2)
        except KeyError:
            self.rain = 0


class TideExtreme:
    """Class containing all the tide informations for a 'tide extreme' """

    def __init__(self, tides):
        self.time = arrow.get(tides['dt']).to('Europe/Paris')
        self.day = find_weekday(self.time)
        self.type = convert_type_fr(tides['type'])
        self.height = round(tides['height'], 2)
