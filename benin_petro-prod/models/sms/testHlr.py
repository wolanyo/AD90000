#!/usr/bin/python
# -*- coding: utf-8 -*-
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.HlrApi()
hlrrequest = swagger_client.HLRrequest() # HLRrequest | Clee de compte sms low cost
hlrrequest.keyid=keyid
hlrrequest.num=["0671820318"]
hlrrequest.get_hlr="1"
try:
    # Vérifier la validité d'un numéro
    pprint(hlrrequest)
    api_response = api_instance.get_hlr(hlrrequest)
    pprint(api_response)
except ApiException as e:
    print "Exception when calling HlrApi->get_hlr: %s\n" % e

