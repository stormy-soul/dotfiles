#!/usr/bin/env python

import time
import json
import requests
from datetime import datetime
from requests.exceptions import RequestException

WEATHER_CODES = {
    '113': '',
    '116': '',
    '122': '',
    '119': '',
    '143': '',
    '176': '',
    '179': '',
    '182': '',
    '185': '',
    '200': '',
    '227': '',
    '230': '',
    '248': '',
    '260': '',
    '263': '',
    '266': '',
    '281': '',
    '284': '',
    '293': '',
    '296': '',
    '299': '',
    '302': '',
    '305': '',
    '308': '',
    '311': '',
    '314': '',
    '317': '',
    '320': '',
    '323': '',
    '326': '',
    '329': '',
    '332': '',
    '335': '',
    '338': '',
    '350': '',
    '353': '',
    '356': '',
    '359': '',
    '362': '',
    '365': '',
    '368': '',
    '371': '',
    '374': '',
    '377': '',
    '386': '',
    '389': '',
    '392': '',
    '395': ''
}
        
data = {}

MAX_RETRIES = 3
BACKOFF = 30.0  

city = "Anuradhapura"
url = f"https://wttr.in/{city}?format=j1"

for attempt in range(1, MAX_RETRIES + 1):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        weather = r.json()
        break
    except RequestException as e:
        if attempt == MAX_RETRIES:
            weather = None
        else:
            time.sleep(BACKOFF * attempt)

if not weather:
    data['text'] = "󰅛 N/A"
    data['tooltip'] = "unavailable"
    print(json.dumps(data))
    raise SystemExit(0)

def format_time(time):
    return time.replace("00", "").zfill(2)

def format_temp(temp):
    return f"{temp}".ljust(3)


def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }

    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)

tempint = int(weather['current_condition'][0]['FeelsLikeC'])
extrachar = ''
if tempint > 0 and tempint < 10:
    extrachar = '+'


data['text'] = ''+WEATHER_CODES[weather['current_condition'][0]['weatherCode']] + f" {tempint}°"
data['tooltip'] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} {weather['current_condition'][0]['temp_C']}°</b>\n"
data['tooltip'] += f"Feels like: {weather['current_condition'][0]['FeelsLikeC']}°\n"
data['tooltip'] += f"Wind: {weather['current_condition'][0]['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"

print(json.dumps(data))
