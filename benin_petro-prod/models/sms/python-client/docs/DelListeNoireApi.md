# swagger_client.DelListeNoireApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**del_liste_noire**](DelListeNoireApi.md#del_liste_noire) | **POST** /dellistenoire | Ajoute un numero en liste noire


# **del_liste_noire**
> LISTENOIREReponse del_liste_noire(keyid, del_liste_noire, num)

Ajoute un numero en liste noire

Supprime un numero en liste noire

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DelListeNoireApi()
keyid = 'keyid_example' # str | Clé API
del_liste_noire = 'del_liste_noire_example' # str | Doit valoir \"1\"
num = 'num_example' # str | numéro de mobile à supprimer

try:
    # Ajoute un numero en liste noire
    api_response = api_instance.del_liste_noire(keyid, del_liste_noire, num)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DelListeNoireApi->del_liste_noire: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyid** | **str**| Clé API | 
 **del_liste_noire** | **str**| Doit valoir \&quot;1\&quot; | 
 **num** | **str**| numéro de mobile à supprimer | 

### Return type

[**LISTENOIREReponse**](LISTENOIREReponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

