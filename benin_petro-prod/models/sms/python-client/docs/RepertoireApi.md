# swagger_client.RepertoireApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**repertoire**](RepertoireApi.md#repertoire) | **PUT** /repertoire | Gestion repertoire (modification)
[**repertoire_crea**](RepertoireApi.md#repertoire_crea) | **POST** /repertoire | Gestion repertoire (creation)


# **repertoire**
> REPERTOIREmodifreponse repertoire(repertoiremodifrequest)

Gestion repertoire (modification)

Ajoute ou supprime une liste de numéros à un répertoire existant.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.RepertoireApi()
repertoiremodifrequest = swagger_client.REPERTOIREmodifrequest() # REPERTOIREmodifrequest | Requête de creation repertoire

try:
    # Gestion repertoire (modification)
    api_response = api_instance.repertoire(repertoiremodifrequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RepertoireApi->repertoire: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repertoiremodifrequest** | [**REPERTOIREmodifrequest**](REPERTOIREmodifrequest.md)| Requête de creation repertoire | 

### Return type

[**REPERTOIREmodifreponse**](REPERTOIREmodifreponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **repertoire_crea**
> REPERTOIREcreatereponse repertoire_crea(repertoirecreaterequest)

Gestion repertoire (creation)

Cree un nouveau répertoire et retourne son identifiant. Cet identifiant pourra être utilisé pour ajouter ou supprimer des numéros via l'API.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.RepertoireApi()
repertoirecreaterequest = swagger_client.REPERTOIREcreaterequest() # REPERTOIREcreaterequest | Creation repertoire

try:
    # Gestion repertoire (creation)
    api_response = api_instance.repertoire_crea(repertoirecreaterequest)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RepertoireApi->repertoire_crea: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repertoirecreaterequest** | [**REPERTOIREcreaterequest**](REPERTOIREcreaterequest.md)| Creation repertoire | 

### Return type

[**REPERTOIREcreatereponse**](REPERTOIREcreatereponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

