import pandas as pd
import numpy as np

dirty_df = pd.read_csv("data\dirty_sales_data.csv")
# ============================================
# Dirty Sales Dataset
# Author: Cindy Robina
# Date: June 2026
# Goal: Clean dataset for analysis
# Key finding: 
"""
1. Missing values in age - DONE
2. Age max is 999 - Impossible - DONE
3. Customer name are different cases - DONE
4. Country - USA is in different cases - DONE
5. Purchase dates are in different formats - DONE
7. Purchase date in str dtype - DONE 
8. Missing values - age and payment_method
9. total revenue for order_id 1019 - DONE
10. Duplicate for John Smith 1001/1005 & Emma Moore 1009/1015 - DONE
"""
# ============================================
"""for col in dirty_df.columns:
    print(f'{col}')
    print('-----------------------------')
    print(dirty_df[col].describe())
    print(dirty_df[col].value_counts())
    print('----------------------------')

print(dirty_df.isnull().sum())"""

# ── Revenue Calculation  ─────────────────
dirty_df['total_revenue'] = dirty_df['quantity'] * dirty_df['unit_price']

# ── Change the case for customer_name, country & customer_segment ─────────────────
dirty_df[['customer_name','country','customer_segment']] = dirty_df[['customer_name','country','customer_segment']].apply(lambda col: col.str.title())

# ── Change date format to a uniform format and the datatype from string to datetime ─────────────────
dirty_df['purchase_date'] = pd.to_datetime((dirty_df['purchase_date'].str.replace('/', '-')))

# ── Replace extreme ages with the median ─────────────────
clean_median = dirty_df[(dirty_df['age'] <= 100) & (dirty_df['age'].notnull())]['age'].median()
conditions = [dirty_df.age.isnull(), dirty_df.age > 100]
choices = [clean_median,clean_median]
dirty_df.age = np.select(conditions, choices, default = dirty_df.age).astype(int)

# ── Missing null for payment method ─────────────────
dirty_df['payment_method'] = np.where(dirty_df['payment_method'].isnull(),'Unknown',dirty_df.payment_method)

# ── Dropping duplicate values ─────────────────
dirty_df = dirty_df[dirty_df['quantity'] > 0]
dirty_df.drop_duplicates(subset = ['customer_name', 'email','age'], inplace = True, ignore_index = True)
print(dirty_df)

print(dirty_df.isnull().sum())
print(dirty_df.shape)
print(dirty_df.dtypes)

dirty_df.to_csv('data/clean_sales_data.csv', index=False)
print("Clean data saved")