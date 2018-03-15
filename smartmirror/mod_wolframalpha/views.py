# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, session, redirect, request
import requests,json
import utils
import tungsten
from splitwise.user import ExpenseUser
from flask_assistant import tell
from smartmirror.extensions import assist

wolframalphaBlueprint = Blueprint('wolframalpha', 
                             __name__,
                             static_folder='../static')


