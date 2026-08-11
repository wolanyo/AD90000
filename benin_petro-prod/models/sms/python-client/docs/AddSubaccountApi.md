# swagger_client.AddSubaccountApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**subaccount_add**](AddSubaccountApi.md#subaccount_add) | **POST** /subaccount | Ajoute un sous compte


# **subaccount_add**
> SubaccountAddResponse subaccount_add(addsubaccountrequest)

Ajoute un sous compte

Ajoute un sous compte

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AddSubaccountApi()
addsubaccountrequest = swagger_client.SubaccountAddRequest() # SubaccountAddRequest | add sub account request

try:
    # Ajoute un sous compte
    api_response = api_instance.subaccount_add(addsubaccountrequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AddSubaccountApi->subaccount_add: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **addsubaccountrequest** | [**SubaccountAddRequest**](SubaccountAddRequest.md)| add sub account request | 

### Return type

[**SubaccountAddResponse**](SubaccountAddResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

