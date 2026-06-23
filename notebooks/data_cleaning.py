import pandas as pd
df = pd.read_csv('data/clean_sales_data.csv')

# What is the total revenue per country?
revenue_by_country = df.pivot_table(
    index = 'country',
    values = 'total_revenue',
    aggfunc = 'sum',
    columns = 'product',
    fill_value = 0
).round(2)

with pd.ExcelWriter('outputs/report.xlsx') as writer:
    df.to_excel(writer, sheet_name = 'clean_sales_data', index = False)
    revenue_by_country.to_excel(writer, sheet_name = 'revenue_by_country', index = True)

"""l = []
data = pd.read_excel("data\practice_data.xlsx", sheet_name=None)
for sheet_name,df in data.items():
    l.append(df)
print(pd.concat(l, ignore_index = True))"""

"""from urllib.request import urlretrieve
url = 'https://assets.datacamp.com/production/course_1606/datasets/winequality-red.csv'
urlretrieve(url, 'winequality-red.csv')

df = pd.read_csv('winequality-red.csv', sep = ';')
print(df)"""

"""from urllib.request import urlopen, Request

url = "https://campus.datacamp.com/courses/1606/4135?ex=2"

request = Request(url)
response = urlopen(request)
html = response.read()

print(html)

response.close()"""
"""import requests
from bs4 import BeautifulSoup

url = 'https://www.python.org/~guido/'
data = requests.get(url)
d = data.text
soup = BeautifulSoup(d)
pretty = soup.prettify()
title = soup.title
text = soup.get_text()
print(title)
print(text)

a_tags = soup.find_all('a')
for link in a_tags:
    print(link.get('href'))"""