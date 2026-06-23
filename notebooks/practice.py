# Part 1 — Clean the CSV
#---------------------------------------
import pandas as pd
import numpy as np

df = pd.read_csv('data\\retail_orders.csv', sep=',')

# Inspect Data
#---------------------------------------
df.info()
df.describe()
#---------------------------------------

# Errors
#---------------------------------------
# Data type - Age(Float/Int), Order_date(Str/Date)- DONE
# Null values - Age, Payment_method- DONE
# Case - Age, Vip_status- DONE
# Format - Order_date- DONE
# Duplicates - Order_id(5005/5011)- DONE
# Drop zero quantity 
#---------------------------------------

#---------------------------------------
# Clean Dataset
#---------------------------------------
df.drop_duplicates(subset = ["customer_name","email", "age", "order_date"], keep = "first", inplace = True)

df[['customer_name','vip_status']] = df[['customer_name','vip_status']].apply(lambda x: x.str.title())

df['order_date'] = pd.to_datetime(df['order_date'].str.replace('/','-'))

median = df.loc[(df['age'].isnull() == False) & (df['age'] < 100), 'age'].median()
conditions = [df['age'].isna(), df['age'] > 100]
choices = [median, median]

df['age'] = np.select(conditions, choices, default = df['age']).astype('int')

df['payment_method'] = np.where(df['payment_method'].isna(),'Unknown', df['payment_method'])

df.drop(df[df['quantity'] <= 0].index, inplace = True)


#---------------------------------------
# Part 2 — Database round trip
#---------------------------------------
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:1234@localhost:5432/analytics_practice')
orders_raw = pd.read_csv('data\\retail_orders.csv', sep = ',')

orders_raw.to_sql('orders_raw', engine, if_exists = 'replace', index = False)

query = "SELECT * FROM orders_raw"
df = pd.read_sql(query, engine)

df.drop_duplicates(subset = ["customer_name","email", "age", "order_date"], keep = "first", inplace = True)

df[['customer_name','vip_status']] = df[['customer_name','vip_status']].apply(lambda x: x.str.title())

df['order_date'] = pd.to_datetime(df['order_date'].str.replace('/','-'))

median = df.loc[(df['age'].isnull() == False) & (df['age'] < 100), 'age'].median()
conditions = [df['age'].isna(), df['age'] > 100]
choices = [median, median]

df['age'] = np.select(conditions, choices, default = df['age']).astype('int')

df['payment_method'] = np.where(df['payment_method'].isna(),'Unknown', df['payment_method'])

df.drop(df[df['quantity'] <= 0].index, inplace = True)

orders_clean = df.to_sql('orders_clean', engine, if_exists = 'replace', index = False)

check = pd.read_sql("SELECT * FROM orders_clean", engine)

#---------------------------------------
# Part 3 — JSON flattening (two shapes)
#---------------------------------------
import json

with open('data\warehouse_stock.json') as f:
    data = json.load(f)
df = pd.json_normalize(
    data['warehouses'],
    record_path = 'stock',
    meta = ['name', 'region']
)
print(df)
print()

with open('data\\rainfall.json') as g:
    info = json.load(g)
df = pd.DataFrame(info['rainfall_mm'])

#---------------------------------------
# Part 4 — Pivot table analysis
#---------------------------------------
check['revenue'] = check['quantity'] * check['unit_price']
pivot = check.pivot_table(
    index = 'region',
    columns = 'product',
    values = ['quantity', 'revenue'],
    aggfunc = 'sum', 
    fill_value = 0
)
#---------------------------------------
# Part 5 — The business question
#---------------------------------------
"""
1. There are 150 bags of maize seeds are stocked in Kisumu Depot - Nyanza Region but we noticed the 150 bags have not been sold. 
Nyanza region is not a top maize producer in Kenya and therefore a lack of demand might be causing the zero sales. 

Recommendation: The unsold bags should be sold at a discounted rate or the stock be relocated to the Western or Eldoret Central depot, whichever is closest.

2. Pesticides are selling well in Kisumu Depot, stocked units are not sufficicient and at a risk of stockout. 

Recommendation: The procurement team and logistics team should ensure more units are stocked up in the depot before the end of the week.

3. The stock data for Coast and Central need to be collected to allow analysis.
 
 Recommendation:The procurement/ inventory department should follow up on this.

"""


#---------------------------------------
# Part 6 — SQL aggregation
#---------------------------------------
data = pd.read_sql(
   "SELECT region, product, total_quantity, (total_quantity * unit_price) AS total_revenue FROM "
   "(SELECT region, product, unit_price, SUM(quantity) AS total_quantity FROM orders_clean GROUP BY region, product, unit_price) AS sb" \
   " ORDER BY region" 
   ,engine
)
print(data)
