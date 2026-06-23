from sqlalchemy import create_engine
import pandas as pd

engine = create_engine()
df = pd.read_csv('data\clean_sales_data.csv')

df.to_sql('sales', engine, if_exists = 'replace', index = False)

query = "SELECT * FROM sales WHERE country = 'Uk'"
orders_raw = pd.read_sql(query, engine)
print(orders_raw)
