# swagger_client.CampagneApi

All URIs are relative to *https://apirest.isendpro.com/cgi-bin*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_campagne**](CampagneApi.md#get_campagne) | **GET** /campagne | Retourne les SMS envoyés sur une période donnée


# **get_campagne**
> file get_campagne(keyid, rapport_campagne, date_deb, date_fin)

Retourne les SMS envoyés sur une période donnée

Retourne les SMS envoyés sur une période donnée en fonction d'une date de début et d'une date de fin.   Les dates sont au format YYYY-MM-DD hh:mm.   Le fichier rapport de campagne est sous la forme d'un fichier zip + contenant un fichier csv contenant le détail des envois. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CampagneApi()
keyid = 'keyid_example' # str | Clé API
rapport_campagne = 'rapport_campagne_example' # str | Doit valoir \"1\"
date_deb = 'date_deb_example' # str | date de debut au format YYYY-MM-DD hh:mm
date_fin = 'date_fin_example' # str | date de fin au format YYYY-MM-DD hh:mm

try:
    # Retourne les SMS envoyés sur une période donnée
    api_response = api_instance.get_campagne(keyid, rapport_campagne, date_deb, date_fin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CampagneApi->get_campagne: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyid** | **str**| Clé API | 
 **rapport_campagne** | **str**| Doit valoir \&quot;1\&quot; | 
 **date_deb** | **str**| date de debut au format YYYY-MM-DD hh:mm | 
 **date_fin** | **str**| date de fin au format YYYY-MM-DD hh:mm | 

### Return type

[**file**](file.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json, file

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

