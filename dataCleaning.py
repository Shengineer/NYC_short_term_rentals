# -*- coding: utf-8 -*-
"""
Created on Sat May 20 10:42:30 2023

@author: kit
"""
# pip install xlrd
import pandas as pd
import numpy as np
from scipy import stats

prices = pd.read_csv("C:\\Users\kit\\OneDrive\\Documents\\Masterschool Docs\\NYSE_project\\prices.csv", header=0)
reviews = pd.read_csv("C:\\Users\\kit\\OneDrive\\Documents\\Masterschool Docs\\NYSE_project\\reviews.tsv", sep='\t', header=0)
room_types = pd.read_excel("C:\\Users\\kit\\OneDrive\\Documents\\Masterschool Docs\\NYSE_project\\room_types.xlsx", header=0)

# print(prices.head())
# print(reviews.head())
# print(room_types.head())

'''  Clean price column ''' 
prices[['price', 'unit']] = prices.price.str.split(" ", expand=True)
'''  Making sure to change the data type to a numeric from string, in this case a float '''
prices[['price']] = prices[['price']].astype(float)
''' Rearrage dataframe order to one that makes more sense '''
price_cols = ['listing_id', 'nbhood_full', 'price', 'unit']
prices = prices[price_cols]
''' Exploratory look at highest values '''
prices.sort_values(by=['price'], ascending=False, inplace=True)
# print(prices.head())
''' Exploratory look at lowest values '''
prices.sort_values(by=['price'], ascending=True, inplace=True)
# print(prices.head())
# print(len(prices))

# Remove Outliers that fall outside of the interquartile range
def remove_outliers_iqr(df,column):
    '''
    Parameters
    ----------
    df : Input dataframe
    column : column name to filter within dataframe
    Returns
    -------
    df : filtered dataframe
    '''
    # Remove zero values
    df.drop(df[df[column] == 0].index, inplace=True)
    
    # Detection of upper and lower bounds
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    # print(Q3)
    IQR = Q3 - Q1
    lower_iqr = Q1 - 1.5*IQR
    upper_iqr = Q3 + 1.5*IQR
    
    # Remove outliers
    df.drop(df[(df[column] >= upper_iqr) | (df[column] <= lower_iqr)].index, inplace=True) # Based on upper and lower bounds
    
    return df

# Remove Outliers using the Z-score
def remove_outliers_z(df,column,n_std):
    '''
    Parameters
    ----------
    df : Input dataframe
    column : column name to filter within dataframe
    n_std : number of standard deviations to filter by
    Returns
    -------
    df : filtered dataframe
    '''
    # Remove zero values
    df.drop(df[df[column] == 0].index, inplace=True)
    
    # Detection of upper and lower bounds
    upper_z = df[column].mean() + n_std * df[column].std()
    lower_z = df[column].mean() - n_std * df[column].std()
    
    # Remove outliers
    df.drop(df[(df[column] >= upper_z) | (df[column] <= lower_z)].index, inplace=True) # Based on upper and lower bounds
    
    return df

# Create IQR and z-score filter copies of original dataframe
prices_iqr = prices.copy()
prices_z = prices.copy()

# Filter for outliers
prices_iqr = remove_outliers_iqr(prices_iqr, "price")
prices_z = remove_outliers_z(prices_z, "price",3)           # To 3 standard deviations
# Check it worked
# print("IQR filtered dataframe size", len(prices_iqr))
# print("Z-Score filtered dataframe size", len(prices_z))

''' Different Filters remove different number of values from the dataframe, each is a valid method of filtering for outliers '''

# print(prices_iqr['price'].describe())
# print(prices_z['price'].describe())

# Working out monthly average
avg_price_iqr = round(prices_iqr['price'].mean(), 2)
avg_price_z = round(prices_z['price'].mean(), 2)

def monthly_avg(iqr, z):
    days_in_month = { 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    mon_price_iqr = 0
    mon_price_z = 0
    for days in days_in_month.values():
        mon_price_iqr += days * iqr
        mon_price_z += days * z
    avg_iqr = mon_price_iqr/12
    avg_z = mon_price_z/12
    return(avg_iqr,avg_z)

avg_mon_price_iqr, avg_mon_price_z = monthly_avg(avg_price_iqr, avg_price_z)
# print(avg_mon_price_iqr)
# print(avg_mon_price_z)
print(prices_iqr.count())


