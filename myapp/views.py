import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render, redirect
import json
from math import sin, cos, sqrt, atan2, radians, acos
import math

def index(request):

    if request.method == 'POST':

        if request.POST['faddress']!="" and request.POST['taddress']!="":

            addressFrom  = request.POST['faddress'].replace(' ', '+')
            addressTo    = request.POST['taddress'].replace(' ', '+')

            from_data = {}
            to_data = {}

            from_address_url = 'https://maps.google.com/maps/api/geocode/json?address={}&sensor=false&key=AIzaSyD8WxtdMy2WyTuL766V9TwA7PL-BP8S5Fs'.format(addressFrom)
            to_address_url = 'https://maps.google.com/maps/api/geocode/json?address={}&sensor=false&key=AIzaSyD8WxtdMy2WyTuL766V9TwA7PL-BP8S5Fs'.format(addressTo)

            from_address_result = requests.get(from_address_url).json()
            to_address_result = requests.get(to_address_url).json()

            from_latitude = from_address_result['results'][0]['geometry']['location']['lat']
            from_longitude = from_address_result['results'][0]['geometry']['location']['lng']

            to_latitude = to_address_result['results'][0]['geometry']['location']['lat']
            to_longitude = to_address_result['results'][0]['geometry']['location']['lng']

            #Getting Distance

            slat = radians(float(from_latitude))
            slon = radians(float(from_longitude))
            elat = radians(float(to_latitude))
            elon = radians(float(to_longitude))

            dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
       


            
            from_eleVation = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key=AIzaSyD8WxtdMy2WyTuL766V9TwA7PL-BP8S5Fs'.format(from_latitude,from_longitude)
            from_alt_result = requests.get(from_eleVation).json()
            
            from_altitude = from_alt_result['results'][0]['elevation']


            to_eleVation = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key=AIzaSyD8WxtdMy2WyTuL766V9TwA7PL-BP8S5Fs'.format(to_latitude,to_longitude)
            to_alt_result = requests.get(to_eleVation).json()
            
            to_altitude = to_alt_result['results'][0]['elevation']

            from_weather_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,daily&appid=911cae2203fbec110bce1ac2fec7c1b8'.format(from_latitude,from_longitude)
            from_weather_result = requests.get(from_weather_url).json()

            to_weather_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,daily&appid=911cae2203fbec110bce1ac2fec7c1b8'.format(to_latitude,to_longitude)
            to_weather_result = requests.get(to_weather_url).json()

            from_data = {
                'from'          :  addressFrom,
                'alt'           :  round(from_altitude,10),
                'lat'           :  from_latitude,
                'long'          :  round(from_longitude,6),
                'wind_speed'    :  from_weather_result['current']['wind_speed'],
                'wind_deg'      :  from_weather_result['current']['wind_deg'],
                'temp'          :  from_weather_result['current']['temp'],
                'humidity'      :  from_weather_result['current']['humidity'], 
                'pressure'      :  from_weather_result['current']['pressure'],
                'weather'       :  from_weather_result['current']['weather'][0]['main']
            }

            to_data = {
                'to'            :  addressTo,
                'alt'           :  round(to_altitude,13),
                'lat'           :  to_latitude,
                'long'           :  round(to_longitude,7),
                'wind_speed'    :  to_weather_result['current']['wind_speed'],
                'wind_deg'      :  to_weather_result['current']['wind_deg'],
                'temp'          :  to_weather_result['current']['temp'],
                'humidity'      :  to_weather_result['current']['humidity'], 
                'pressure'      :  to_weather_result['current']['pressure'],
                'weather'       :  to_weather_result['current']['weather'][0]['main']
            }

            context = {
                'distance'         :  dist,
                'fromApiData'      :  from_data,
                'toApiData'        :  to_data,
            }
    else:

        context = {
            'distance'         :  '',
            'fromApiData'      :  '',
            'toApiData'        :  '',
        }

    return render(request, 'index.html',context)
