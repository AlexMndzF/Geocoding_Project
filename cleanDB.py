import os
from pymongo import MongoClient
import pandas as pd
import json
import requests
from dotenv import load_dotenv
import re
from FunctionsMongo import connectCollection
'''Conexion con base de datos y clase  '''
db,coll = (list(connectCollection('companies','companies')))
'''Query inicial'''
rest = (list(coll.find({'$and':[{'$or':[{"offices.latitude":{'$ne':None}},{"offices.longitude":{'$ne':None}}]},{'deadpooled_year':None}]})))
'''Bucle de limpieza'''
clean_db = []
for i in range(len(rest)):
    value = rest[i].get('total_money_raised') 
    valueM = re.findall(r'\d+[?\.\d]?\d',value)
    if valueM == []:
        valueM = [0]
    diction ={
        'name':rest[i]['name'],
        'category':rest[i]['category_code'],
        #'deadpooled':rest[i]['deadpooled_year'],
        'value': {
            'value':float(valueM[0]),
            'qty':value[-1]
        }
        
    }
    for ind in range(len(rest[i]['offices'])):
        if rest[i]['offices']:
            diction[f'Location-{ind+1}'] = {
                'type':'Point',
                'coordinates':[float(rest[i]['offices'][ind]['longitude']), float(rest[i]['offices'][ind]['latitude'])]
            }
        
    
    clean_db.append(diction)
''' Salva el fichero de la base de datos limpia'''   
with open('Database/database_clean.json', 'w') as fp:
    json.dump(clean_db, fp)
