#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

This sample script leverages the Flask web service micro-framework
(see http://flask.pocoo.org/).  By default the web server will be reachable at
port 5500 you can change this default if desired (see `app.run(...)`).

"""

from dotenv import load_dotenv

__author__ = "Gerardo Chaves"
__author_email__ = "gchaves@cisco.com"
__copyright__ = "Copyright (c) 2016-2022 Cisco and/or its affiliates."
__license__ = "Cisco"

from requests_oauthlib import OAuth2Session

from flask import Flask,request, render_template, jsonify
import requests
import os
import json

# load all environment variables
load_dotenv()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize the environment
# Create the web application instance
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def sendsms():
    result_response=''
    error_response=''
    if request.method == "POST":
        sms_name = request.form.get("SMS-Name")
        sms_number = request.form.get("SMS-Number")
        sms_message = request.form.get("SMS-Message")

        msgSnd=sms_message
        theDestNumber=sms_number
        print(msgSnd)
        #Only send out SMS if IMI Service is configured
        if os.getenv('IMI_SERVICE_KEY')!="":
            #send message via SMS to mobile number (if available)
            if theDestNumber!=None and theDestNumber!="":
                print(f'Sending SMS to {theDestNumber} ')
                url = "https://api-sandbox.imiconnect.io/v1/sms/messages"
                payload = json.dumps({
                    "from": os.getenv('SMS_ORIGIN'),
                    "to": theDestNumber,
                    "content": msgSnd,
                    "contentType": "TEXT"
                })
                headers = {
                    'Authorization': os.getenv('IMI_SERVICE_KEY'),
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                response_dict=json.loads(response.text)
                if ('acceptedTime' in response_dict):
                    result_response=f"Sent on {response_dict['acceptedTime']}"
                    print("Sent SMS: ", response.text)
                else:
                    error_response="Error sending: "+response.text
                    print("Failed sending SMS: ", response.text)

        return render_template("index.html",result_response=result_response, error_response=error_response)
    else:
        return render_template("index.html",result_response='', error_response='')


# Start the Flask web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)


