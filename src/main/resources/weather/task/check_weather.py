#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#

from xlrelease.HttpRequest import HttpRequest
import json

params = {'url': 'http://api.openweathermap.org'}

http_request = HttpRequest(params)

weather_response = http_request.get('/data/2.5/weather?zip={},us&appid=926183652fba05ab14691aa5b6ed1faa'.format(zipcode))
if weather_response.isSuccessful():
    json_data = json.loads(weather_response.getResponse())
    temperature = json_data
else:
    sys.exit(1)


