# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 10:14:35 2021

@author: ashok
"""
import requests

class ForeCastDataHandling:
    def __init__(self):
        pass
    def getoneminutedata(self,lat,lon):
        self.lat=lat
        self.lon=lon
        #appid="5b6de60a001457f618954a5861c665a5"
        #exclude"current,hourly,daily,alerts"
        #lat=18.5204
        #lon=73.8567
        response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,hourly,daily,alerts&appid=5b6de60a001457f618954a5861c665a5".format(lat,lon))
        response= response.json()
        timedata=response["minutely"]
        return timedata
        
        



        
