import pandas as pd
import requests

url = 'https://geocoding-api.open-meteo.com/v1/search'
params = {'name': 'Eldoret', 'count': 5}
response = requests.get(url, params=params)

data = response.json()

df = pd.json_normalize(
    data,
    record_path = 'results'
)
print(df)