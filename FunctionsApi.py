import os
from pymongo import MongoClient
import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
import json
import requests
from dotenv import load_dotenv
import re
load_dotenv()
def requestfoursquare(query):
    '''
    Funcion para hacer peticiones a la api, el parametro de entrada es query que quremos hacer.
    '''
    url = 'https://api.foursquare.com/v2/venues/explore'
    params = dict(
      client_id=os.getenv("CLIENT_ID"),
      client_secret=os.getenv("CLIENT_SECRET"),
      v='20180323',
      ll='40.7243,-74.0018',
      query=query,
      limit=200
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data

def getlocation(data):
    '''
    Devuelve lista de diccionario con el nombre y el geopoint
    '''
    locationslist = []
    for i in range(len(data['response']['groups'][0]['items'])):
        latitude = float((data['response']['groups'][0]['items'][i]['venue'].get('location')).get('lat'))
        longitude = float((data['response']['groups'][0]['items'][i]['venue'].get('location')).get('lng'))
        dictio = {
            'name':(data['response']['groups'][0]['items'][i]['venue']).get('name'),
            'loc':{'type':'Point','coordinates':[longitude,latitude]}            
            }
        locationslist.append(dictio)
    return locationslist