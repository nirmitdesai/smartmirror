# -*- coding: utf-8 -*-
from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
import apiai
import json, requests

endpointsBlueprint = Blueprint('endpoints', 
                             __name__,
                             static_folder='../static')

@endpointsBlueprint.route('/', methods=['GET'])
def homepage():
    return "dashboard"


@endpointsBlueprint.route('/messaging',methods=["POST", "GET"])
def handleMessage():

	message = request.values.get('Body','').strip()
	print("message = " + message)
	url = "http://localhost:8080/syslog"
	params ={"type" : "INFO","message" : message,"alert": True}
	r = requests.get(url, params)
	print r.json()

	
	# ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

	# apiairequest = ai.text_request()

	# apiairequest.lang = 'en'  # optional, default value equal 'en'

	# apiairequest.session_id = "asdasd"

	# apiairequest.query = message
	# response = apiairequest.getresponse()
	# val = response.read()
	# val = json.loads(val)
	# answer = val["result"]["fulfillment"]["speech"]

	resp = MessagingResponse().message("okay")
	return str(resp)
