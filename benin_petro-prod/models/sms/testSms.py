#!/usr/bin/python
# -*- coding: utf-8 -*-
from keyid import keyid
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# create an instance of the API class
api_instance = swagger_client.SmsApi()
smsrequest = swagger_client.SmsUniqueRequest("35b5adc691f54ac5e0827b2292a194d5",None, None, "bonjour! je teste! é à \" ' bla $$ù","0750961586","iSendPro",None,None,None, None, None) # SMSRequest | sms request

try:
    # Envoyer des SMS
    api_response = api_instance.send_sms(smsrequest)
    print(api_response)
except ApiException as e:
    print ("Exception when calling SmsApi->send_sms: %s\n" % e)
