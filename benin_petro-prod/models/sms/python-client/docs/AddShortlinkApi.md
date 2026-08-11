# swagger_client.AddShortlinkApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_shortlink**](AddShortlinkApi.md#add_shortlink) | **POST** /shortlink | add a shortlink


# **add_shortlink**
> ShortlinkResponse add_shortlink(addshortlinkrequest)

add a shortlink

add a shortlink

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AddShortlinkApi()
addshortlinkrequest = swagger_client.ShortlinkRequest() # ShortlinkRequest | add sub account request

try:
    # add a shortlink
    api_response = api_instance.add_shortlink(addshortlinkrequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AddShortlinkApi->add_shortlink: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **addshortlinkrequest** | [**ShortlinkRequest**](ShortlinkRequest.md)| add sub account request | 

### Return type

[**ShortlinkResponse**](ShortlinkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

