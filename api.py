import pandas as pd
import requests
import numpy as np

"""url = 'https://geocoding-api.open-meteo.com/v1/search'
params = {'name': 'Eldoret', 'count': 5}
response = requests.get(url, params=params)

data = response.json()

df = pd.json_normalize(
    data,
    record_path = 'results'
)
print(df)"""

df = pd.read_csv('data\\farm_sensor_data.csv',
                 parse_dates = ['timestamp'],
                 sep = ',',
                 encoding = 'utf-8')

print(df.duplicated().sum())
df.drop_duplicates(subset='timestamp', keep='first', inplace=True)
df.loc[df['temperature_c'] == 999, 'temperature_c'] = np.nan
df[['temperature_c', 'soil_moisture_pct']] = df[['temperature_c', 'soil_moisture_pct']].interpolate()
df.set_index('timestamp', inplace = True)
new_df = df.resample('h').agg({
    'temperature_c':'mean',
    'soil_moisture_pct':'mean'
}).round(2)

last = df.resample('h').last()

print(new_df)
farm_sensor = new_df.to_csv('farm_sensor_hourly.csv')
