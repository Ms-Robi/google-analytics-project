# ============================================
# Google Merchandise Store — Funnel Analysis
# Author: Cindy Robina
# Date: June 2026
# Goal: Analyze customer journey from cart to purchase
# Key finding: 49% of cart users never reach checkout
# ============================================

import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ── DATA LOADING ───────────────────────────────
# Load the events dataset with dates parsed upfront
# to avoid conversion issues later in the analysis

df = pd.read_csv("data\events", parse_dates=['date'])

# ── EVENT TYPE FILTER FUNCTION ─────────────────
# Reusable function to filter by event type
# Avoids repeating df[df['type']==...] throughout
# What % of add_to_cart users started checkout

def get_event(event_type, dataframe = df):
   event_type = dataframe[dataframe['type'] == event_type]
   return(event_type)
   
purchase = get_event('purchase')
add_to_cart = get_event('add_to_cart')
begin_checkout = get_event('begin_checkout')

checkout_purchase = np.intersect1d(begin_checkout['user_id'], purchase['user_id']).size
cart_checkout = np.intersect1d(add_to_cart['user_id'],begin_checkout['user_id']).size
cart_purchase = np.intersect1d(add_to_cart['user_id'],purchase['user_id']).size

perc_purchase = round(checkout_purchase / begin_checkout['user_id'].nunique() * 100, 2)
perc_cart = round(cart_checkout / add_to_cart['user_id'].nunique() * 100, 2)
per_cart = round(cart_purchase / add_to_cart['user_id'].nunique() * 100, 2)

print(f'{perc_purchase} % of checkout users purchased the merchandise.')
print(f'{perc_cart} % of add_to_cart users checked out.')
print(f'{per_cart} % of add_to_cart users purchased the merchandise.')

# Which device converts better?
purchases = get_event('purchase').groupby('device')['user_id'].nunique()
total = df.groupby('device')['user_id'].nunique()
conversion = round(purchases / total * 100, 2)


conversion = pd.DataFrame({'purchases': purchases, 'total': total, 'conversion%': conversion})
print(conversion)

# Which country has the most purchases?
country = get_event('purchase')['country'].value_counts().head(10).reset_index()
print(get_event('purchase')[['country','item_id']].value_counts(ascending = False).groupby(by = 'country').head(1))

# ── FUNNEL ANALYSIS ────────────────────────────
# Count unique users per event type
# Key finding: only 4,066 of 12,545 cart users purchased
# That's a 67% overall drop off rate

unique_users = df.groupby('type')['user_id'].nunique()
unique_users['cart_dropped'] = unique_users.loc['add_to_cart'] - unique_users.loc['begin_checkout']
unique_users['cart_abandoned'] = unique_users.loc['begin_checkout'] - unique_users.loc['purchase']
print(unique_users)


# Sankey Chart
fig = go.Figure(go.Sankey(
   node = dict(
      label = ['add_to_cart', 'begin_checkout', 'purchase', 'cart_dropped', 'cart_abandoned'],
      color = ['blue', 'green', 'orange', 'gray', 'gray']
     
   ),
   link = dict(
       source = [0,0,1,1],
       target = [1,3,2,4],
       value = [6404, 6141, 4066, 2338]


   )
)

)

fig.update_layout(title='Customer Funnel', font_size=12)
fig.write_html("outputs/sankey.html")
fig.show()

# Bar Chart
f = go.Figure(
   go.Bar(
      x = conversion.index,
      y = conversion['conversion%']
)
)
f.update_layout(title="Conversion rate per device", 
                font_size = 12,
                xaxis_title = "Device",
                yaxis_title = "% Conversion",
                yaxis_range = [25, 29]
               )
f.write_html("outputs/bar.html")
f.show()

# Horizontal Bar
fig = go.Figure(
   go.Bar(
      x = country['count'],
      y = country['country'],
      orientation='h'
   )
)
fig.update_layout(title = "Top countries by purchases",
                  font_size = 12,
                  yaxis={"categoryorder": "total ascending"},
                  xaxis_title = "Total Purchases",
                  yaxis_title = "Countries"
                  )
fig.write_html("outputs/countries.html")
fig.show()

# Date Column Conversion
df['date_only'] = df['date'].dt.date
dates = get_event('purchase').groupby('date_only')['user_id'].count().reset_index()
dates.columns = ['date', 'purchase_count']
print(dates)

# Line Chart
fig = go.Figure(
   [go.Scatter(
      x = dates['date'],
      y = dates['purchase_count'],
      mode = 'lines'
   )]
)
fig.update_layout(title = "Total purchases per day",
                  font_size = 12,
                  xaxis_title = "Date",
                  yaxis_title = "Purchases")

fig.write_html("outputs/line.html")
fig.show()

