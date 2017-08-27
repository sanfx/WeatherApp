""" this module contains generic utility functions for the weather app.
"""

import json
import urllib2
import string
import random


cityNameMap = {
    "Bengaluru" : "Bangalore",

}

def getplace(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng={},{}&sensor=false".format(lat, lon)
    v = urllib2.urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "political" in c['types'] and "locality" in c['types']:
            town = c['long_name']
    return town, country



def getJsonFromURL(url, timeout=25):
    try:
        response = urllib2.urlopen(url, timeout=timeout).read()
    except Exception, er:
        # raise ValueError("Failed to load URL")
        return {"status": "fail", "Description": "this is manually forced due to {}".format(er.message)}
    return json.loads(response)


def getCityDateTime(timezone):
    url = "https://script.google.com/macros/s/AKfycbyd5AcbAnWi2Yn0xhFRbyzS4qMq1VucMVgVvhul5XqS9HkAyJY/exec?tz={}".format(timezone)
    data = getJsonFromURL(url)
    if data.get("status"):
        return (
            "{} : {}:{}".format(data.get("hours"), data.get("minutes"), data.get("seconds")),
            "{}/{}".format(data.get("day"), data.get("monthName"))
                )

def getVisitorAddressFromLatLong(lat, lng):
    """ provides address based on latitude and longitude
    """
    return getJsonFromURL("http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}".format(lat, lng))

def getWeatherURL(city, count=2):
	return "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt={}&mode=json&units=metric&appid=c0d8761ca979157a45651a5c7f12a6be".format(city, count)

# http://weathers.co/api.php?city=Bangalore # try this for weather table header

def getSunriseSunsetURL(lat, lng, date):
	return "https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}".format(lat, lng, date)

def getTimeZoneURL(latitude, longitude):
	return "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username=seaurchin".format(
        latitude,
        longitude)

def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getTimezoneFromIP(ip):
    data = getJsonFromURL("http://ip-api.com/json/{}".format(ip))
    tz = "Asia/Kolkata" if ip == "127.0.0.1" else "UTC"
    if data["status"] == "success":
        tz = data["timezone"]
    return tz

def getHostIp():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
    except Exception:
        print("Network not reachable. defaulting to Home")
        return "127.0.0.1"
    ip = s.getsockname()[0]
    s.close()
    return ip
