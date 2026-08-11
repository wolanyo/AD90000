#!/usr/bin/python
# -*- coding: utf-8 -*-
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# create an instance of the API class
api_instance = swagger_client.SmsApi()
smsrequest = swagger_client.SMSRequest() # SMSRequest | sms request
smsrequest.keyid=keyid
smsrequest.num=["0695208432","0695208432"]
smsrequest.emetteur="iSendPro"
smsrequest.sms=["bonjour! je teste!","Coucou!"] #il est possible de laisser 1 seul element dans la liste sms, dans ce cas le meme message est envoye pour tous les destinataires
try:
    # Envoyer des SMS
    api_response = api_instance.send_sms(smsrequest)
    pprint(api_response)
except ApiException as e:
    print "Exception when calling SmsApi->send_sms: %s\n" % e
