# swagger_client.SmsApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**send_sms**](SmsApi.md#send_sms) | **POST** /sms | Envoyer un sms
[**send_sms_multi**](SmsApi.md#send_sms_multi) | **POST** /smsmulti | Envoyer des SMS


# **send_sms**
> SMSReponse send_sms(smsrequest)

Envoyer un sms

Envoi un sms vers un unique destinataire

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SmsApi()
smsrequest = swagger_client.SmsUniqueRequest() # SmsUniqueRequest | sms request

try:
    # Envoyer un sms
    api_response = api_instance.send_sms(smsrequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SmsApi->send_sms: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **smsrequest** | [**SmsUniqueRequest**](SmsUniqueRequest.md)| sms request | 

### Return type

[**SMSReponse**](SMSReponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_sms_multi**
> SMSReponse send_sms_multi(smsrequest)

Envoyer des SMS

Envoi de SMS vers 1 ou plusieurs destinataires 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SmsApi()
smsrequest = swagger_client.SMSRequest() # SMSRequest | sms request

try:
    # Envoyer des SMS
    api_response = api_instance.send_sms_multi(smsrequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SmsApi->send_sms_multi: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **smsrequest** | [**SMSRequest**](SMSRequest.md)| sms request | 

### Return type

[**SMSReponse**](SMSReponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

