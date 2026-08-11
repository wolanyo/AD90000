# swagger_client.GetListeNoireApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_liste_noire**](GetListeNoireApi.md#get_liste_noire) | **POST** /getlistenoire | Retourne le liste noire


# **get_liste_noire**
> file get_liste_noire(keyid, get_liste_noire)

Retourne le liste noire

Retourne un fichier csv zippé contenant la liste noire

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GetListeNoireApi()
keyid = 'keyid_example' # str | Clé API
get_liste_noire = 'get_liste_noire_example' # str | Doit valoir \"1\"

try:
    # Retourne le liste noire
    api_response = api_instance.get_liste_noire(keyid, get_liste_noire)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GetListeNoireApi->get_liste_noire: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyid** | **str**| Clé API | 
 **get_liste_noire** | **str**| Doit valoir \&quot;1\&quot; | 

### Return type

[**file**](file.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

