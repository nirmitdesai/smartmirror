# -*- coding: utf-8 -*-
from flask import Blueprint
import requests,json
import utils

weatherBlueprint = Blueprint('weather', 
                             __name__,
                             static_folder='../static')

@weatherBlueprint.route('/', methods=['GET', 'POST'])
def home():
    print "in home.."
    
    weather = utils.getWeather('Santa Clara')
    val = "Temperature in Santa Clara is " + str(weather["currentTemperature"])
    return val

@weatherBlueprint.route("/train",methods=["GET"])
def train():
    return "train"