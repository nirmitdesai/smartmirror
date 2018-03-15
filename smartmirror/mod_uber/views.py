# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, session, redirect, request
import requests,json
import utils
from flask_assistant import tell
from smartmirror.extensions import assist

uberBlueprint = Blueprint('uber', 
                             __name__,
                             static_folder='../static')

@uberBlueprint.route('/authorize', methods=['GET', 'POST'])
def home():
	pass
	
