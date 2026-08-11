#!/usr/bin/python
# -*- coding: utf-8 -*-
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComptageApi()
comptagerequest = swagger_client.ComptageRequest() # ComptageRequest | sms request
comptagerequest.keyid=keyid
comptagerequest.num="0750961586"
comptagerequest.emetteur="iSendPro"
comptagerequest.sms="bonjour! je teste! é à"
try:
    # Compter le nombre de caractère
    api_response = api_instance.comptage(comptagerequest)
    print "Nombre de sms nécessaires: "+api_response.etat.etat[0].nb_sms
    pprint(api_response)
except ApiException as e:
    print "Exception when calling ComptageApi->comptage: %s\n" % e

