#!/usr/bin/python
# -*- coding: utf-8 -*-
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CampagneApi()
rapport_campagne = '1' # str |
date_deb = '2016-07-01 00:00' # str | date de debut au format YYYY-MM-DD hh:mm
date_fin = '2016-07-15 14:30' # str | date de fin au format YYYY-MM-DD hh:mm

try:
    # Retourne les SMS envoyés sur une période donnée
    api_response = api_instance.get_campagne(keyid, rapport_campagne, date_deb, date_fin)
    pprint(api_response)
except ApiException as e:
    print "Exception when calling CampagneApi->get_campagne: %s\n" % e
