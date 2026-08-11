# swagger_client.EditSubaccountApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**subaccount_edit**](EditSubaccountApi.md#subaccount_edit) | **PUT** /subaccount | Edit a subaccount


# **subaccount_edit**
> SubaccountResponse subaccount_edit(editsubaccountrequest)

Edit a subaccount

Edit a subaccount

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EditSubaccountApi()
editsubaccountrequest = swagger_client.SubaccountRequest() # SubaccountRequest | edit sub account request

try:
    # Edit a subaccount
    api_response = api_instance.subaccount_edit(editsubaccountrequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EditSubaccountApi->subaccount_edit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **editsubaccountrequest** | [**SubaccountRequest**](SubaccountRequest.md)| edit sub account request | 

### Return type

[**SubaccountResponse**](SubaccountResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

