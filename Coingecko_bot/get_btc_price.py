# get_btc_price.py

import requests

async def get_btc_price():
    api_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'bitcoin' in data and 'usd' in data['bitcoin']:
            btc_price = data['bitcoin']['usd']
            return btc_price
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None
