# swagger_client.HlrApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_hlr**](HlrApi.md#get_hlr) | **POST** /hlr | Vérifier la validité d&#39;un numéro


# **get_hlr**
> HLRReponse get_hlr(hlrrequest)

Vérifier la validité d'un numéro

Réalise un lookup HLR sur les numéros  

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.HlrApi()
hlrrequest = swagger_client.HLRrequest() # HLRrequest | 

try:
    # Vérifier la validité d'un numéro
    api_response = api_instance.get_hlr(hlrrequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HlrApi->get_hlr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hlrrequest** | [**HLRrequest**](HLRrequest.md)|  | 

### Return type

[**HLRReponse**](HLRReponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

