# swagger_client.CreditApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_credit**](CreditApi.md#get_credit) | **GET** /credit | Interrogation credit


# **get_credit**
> CreditResponse get_credit(keyid, credit)

Interrogation credit

Retourne le credit existant associe au compte. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CreditApi()
keyid = 'keyid_example' # str | Clé API
credit = 'credit_example' # str | Type de reponse demandée, 1 pour euro, 2 pour euro + estimation quantité

try:
    # Interrogation credit
    api_response = api_instance.get_credit(keyid, credit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CreditApi->get_credit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyid** | **str**| Clé API | 
 **credit** | **str**| Type de reponse demandée, 1 pour euro, 2 pour euro + estimation quantité | 

### Return type

[**CreditResponse**](CreditResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

