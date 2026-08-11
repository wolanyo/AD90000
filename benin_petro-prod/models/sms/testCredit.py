#!/usr/bin/python
# -*- coding: utf-8 -*-
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CreditApi()
credit = '1' # str | Type de reponse demandée, 1 pour euro et 2 pour messages

try:
    # Interrogation credit
    api_response = api_instance.get_credit(keyid, credit)
    print str(api_response)
except ApiException as e:
    print "Exception when calling CreditApi->get_credit: %s\n" % e

