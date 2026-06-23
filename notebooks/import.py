import pandas as pd
import requests
import json

"""with open("data\customers.json") as f:
    data = json.load(f)

df = pd.json_normalize(
                data,
                record_path = "orders",
                meta = ["customer_id", "name", "country"]
)
print(df)

# Total spend per customer
total_spend_per_cust = df.pivot_table(
    index = "customer_id",
    values = "price",
    aggfunc = "sum"
)

print(total_spend_per_cust)

df.to_json('outputs/flattened_orders.json', orient = 'records', indent = 2)"""

"""url = "https://api.open-meteo.com/v1/forecast"
params = {
    'latitude': 0.5143,
    'longitude': 35.2698,
    'daily': 'temperature_2m_max,temperature_2m_min',
    'timezone': 'Africa/Nairobi'
}
response = requests.get(url, params = params)
data = response.json()

df = pd.DataFrame(data['daily'])

print(df)"""


# Task 1 — Facilities table

with open("data\county_data.json") as f:
    data = json.load(f)

df = pd.json_normalize(
    data,
    record_path = 'facilities'
)
print(df)

# Task 2 — Rainfall table

df = pd.DataFrame(data['monthly_rainfall_mm'])
print(df)

# Task 3 — Leadership info

print(f'The governor\'s name is {data['leadership']['governor']} and their term start date was {data['leadership']['term_start']}')


