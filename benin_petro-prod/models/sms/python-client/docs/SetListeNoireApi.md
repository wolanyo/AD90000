# swagger_client.SetListeNoireApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**set_liste_noire**](SetListeNoireApi.md#set_liste_noire) | **POST** /setlistenoire | Ajoute un numero en liste noire


# **set_liste_noire**
> LISTENOIREReponse set_liste_noire(keyid, setliste_noire, num)

Ajoute un numero en liste noire

Ajoute un numero en liste noire. Une fois ajouté, les requêtes d'envoi de SMS marketing vers ce numéro seront refusées.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SetListeNoireApi()
keyid = 'keyid_example' # str | Clé API
setliste_noire = 'setliste_noire_example' # str | Doit valoir \"1\"
num = 'num_example' # str | numéro de mobile à insérer en liste noire

try:
    # Ajoute un numero en liste noire
    api_response = api_instance.set_liste_noire(keyid, setliste_noire, num)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SetListeNoireApi->set_liste_noire: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyid** | **str**| Clé API | 
 **setliste_noire** | **str**| Doit valoir \&quot;1\&quot; | 
 **num** | **str**| numéro de mobile à insérer en liste noire | 

### Return type

[**LISTENOIREReponse**](LISTENOIREReponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

