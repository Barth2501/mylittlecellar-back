import os
import requests


def get_first_wine_from_hachette(payload):
    if os.environ.get('USE_NGROK')=='True':
        wine_data = requests.post(os.environ.get('NGROK_SCRAP') + '/hachette', json=payload)    
    else:
        wine_data = requests.post("http://localhost:8001/hachette", json=payload)
    return wine_data.json()['wines']