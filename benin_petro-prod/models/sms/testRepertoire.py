#!/usr/bin/python
# -*- coding: utf-8 -*-
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

api_instance = swagger_client.RepertoireApi()
repertoirecreaterequest = swagger_client.REPERTOIREcreaterequest() # REPERTOIREcreaterequest | Creation repertoire
repertoirecreaterequest.keyid=keyid
repertoirecreaterequest.repertoire_edit="create"
repertoirecreaterequest.repertoire_nom="Repertoire de test"
try:
    # Gestion repertoire (creation)
    api_response = api_instance.repertoire_crea(repertoirecreaterequest)
    pprint(api_response)
except ApiException as e:
    print "Exception when calling RepertoireApi->repertoire_crea: %s\n" % e
    pprint (e)

repertoire_id=api_response.etat.etat[0].repertoire_id
repertoiremodifrequest = swagger_client.REPERTOIREmodifrequest() # REPERTOIREmodifrequest | Requete de creation repertoire
repertoiremodifrequest.keyid=keyid
repertoiremodifrequest.repertoire_edit="add"
repertoiremodifrequest.repertoire_id=repertoire_id
repertoiremodifrequest.num=["0612345678"]
try:
    # Gestion repertoire (modification)
    api_response = api_instance.repertoire(repertoiremodifrequest)
    pprint(api_response)
except ApiException as e:
    print "Exception when calling RepertoireApi->repertoire: %s\n" % e
    pprint (e)

