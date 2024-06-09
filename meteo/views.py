from datetime import datetime

import geocoder
import requests
from django.http import HttpResponse

from django.shortcuts import render
from django.template import loader

from meteo.models import WorldCities

ENDPOINT = "https://api.open-meteo.com/v1/forecast"


def construct_api_request(endpoint, location_coords, forecast_param='temperature_2m'):
    latitude, longitude = location_coords
    return f"{endpoint}?latitude={latitude}&longitude={longitude}&hourly={forecast_param}"


def get_temp(location):
    meteo_data = None
    try:
        api_request = construct_api_request(ENDPOINT, location)
        meteo_data = requests.get(api_request).json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    now = datetime.now()
    hour = now.hour
    current_temperature = meteo_data['hourly']['temperature_2m'][hour]
    return current_temperature


def temp_somewhere(request):
    random_item = WorldCities.objects.all().order_by('?').first()
    city = random_item.city
    location = [random_item.lat, random_item.lng]
    template = loader.get_template('index.html')
    context = {
        "city": city,
        "temp": get_temp(location)
    }
    return HttpResponse(template.render(context, request))


def temp_here(request):
    location = geocoder.ip('me').latlng
    template = loader.get_template('index.html')
    context = {
        "city": "Your location",
        "temp": get_temp(location)
    }
    return HttpResponse(template.render(context, request))

