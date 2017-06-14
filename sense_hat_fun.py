import os
import requests
import json
import time

from sense_hat import SenseHat
from gpiozero  import CPUTemperature
from yahoo_finance import Share
from datetime import datetime, timedelta

sense = SenseHat()
speed = 0.17

seconds = 60
minutes = 30

green  = (50,205,50)
blue   = (0,0,255)
yellow = (238,232,170)
red    = (178,34,34)

sleep_time = 2

OWM_ID = os.environ['OWM_ID']

# ==========================================================================
def display_msg(msg, color):
    time.sleep(sleep_time)
    
    sense.show_message(msg, scroll_speed = speed, text_colour=color)
# ==========================================================================


# ==========================================================================
def get_temperature(weather_location, friendly_name):

    time.sleep(sleep_time)
    
    url         = 'http://api.openweathermap.org/data/2.5/weather?q={' + str(weather_location) + '}'
    parameters  = {'appid':OWM_ID,'units':'imperial'}
    head        = {'Accept':'application//json','Content-Type':'application/json'}

    try:
        response    = requests.get(url,params=parameters,headers=head)

        if response.ok:

            data      = str(response.content,'utf-8')
            json_data = json.loads(data)
            location  = json_data['name']
            temp      = json_data['main']['temp']
            humidity  = json_data['main']['humidity']

            if friendly_name != "":
                location_name = friendly_name
            else:
                location_name = location

            msg = "...  " + location_name.lower() + " " + str(round(temp, 1)) + "F  " + str(humidity) + "%  ...   "
        else:
            msg = "...  weather data unavailable  ..."

    except:
        msg = "...  error retreiving weather data  ..."
            

    return msg
# ==========================================================================


# ==========================================================================
def get_stock_price(ticker):

    time.sleep(sleep_time)
    
    try:
        stock = Share(ticker)
        price = stock.get_price()
        price_open = stock.get_open()
        msg = "...  " + ticker.lower() + " " + str(round(float(price), 2)) + "  ..."

        if float(price) - float(price_open) > 0:
            color = green
        else:
            color = red
    except:
        msg   = "...  error retreiving stock data  ..."
        color = red

    return (msg, color)
# ==========================================================================


# ==========================================================================
def get_cpu_temp():

    time.sleep(sleep_time)
    
    return "...  cpu = " + str(round(CPUTemperature().temperature, 2)) + "C  ..."
# ==========================================================================


# ==========================================================================
def get_earthquake():

    time.sleep(sleep_time)
    
    start_time = datetime.utcfromtimestamp(time.time() - seconds * minutes).isoformat()
    
    url         = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
    parameters  = {'format':'geojson','orderby':'time','eventtype':'earthquake','starttime':start_time}

    try:
        response    = requests.get(url,params=parameters)

        msg = "...  earthquake data unavailable  ..."
        if response.ok:
            data      = str(response.content,'utf-8')
            json_data = json.loads(data)
            if json_data['metadata']['count'] > 0:
                msg = "...   latest earthquake "  + json_data['features'][0]['properties']['title'] + "  ..."
    except:
        msg = "...  error retreiving earthquake data  ..."

    return msg
# ==========================================================================

# ==========================================================================


while True:

    sense.set_rotation(270)

    msg, color = get_stock_price('baba')
    display_msg(msg, color)

    msg, color = get_stock_price('tcehy')
    display_msg(msg, color)

    display_msg(get_earthquake(), red)
    
    display_msg(get_temperature("Broken Arrow,OK", "broken arrow"), blue)
    display_msg(get_temperature("Pflugerville,TX", "pflugerville"), blue)
    display_msg(get_temperature("San Jose, CA", "san jose"), blue)
    
    display_msg(get_cpu_temp(), green)



    
