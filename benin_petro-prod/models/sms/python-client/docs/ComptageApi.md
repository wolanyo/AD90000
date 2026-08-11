# swagger_client.ComptageApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**comptage**](ComptageApi.md#comptage) | **POST** /comptage | Compter le nombre de caractère 


# **comptage**
> ComptageReponse comptage(comptagerequest)

Compter le nombre de caractère 

Compte le nombre de SMS necessaire à un envoi

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComptageApi()
comptagerequest = swagger_client.ComptageRequest() # ComptageRequest | sms request

try:
    # Compter le nombre de caractère 
    api_response = api_instance.comptage(comptagerequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComptageApi->comptage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comptagerequest** | [**ComptageRequest**](ComptageRequest.md)| sms request | 

### Return type

[**ComptageReponse**](ComptageReponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

