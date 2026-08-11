#!/usr/bin/python
# -*- coding: utf-8 -*
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SetListeNoireApi()
setliste_noire = '1' # str |
num = '0612345678' # str | numéro de mobile à insérer en liste noire

try:
    # Ajoute un numero en liste noire
    api_response = api_instance.set_liste_noire(keyid, setliste_noire, num)
    pprint(api_response)
except ApiException as e:
    print "Exception when calling SetListeNoireApi->set_liste_noire: %s\n" % e
