# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 20:51:34 2022

@author: luise
"""
import streamlit as st
import pandas as pd

df = pd.DataFrame(columns = ['Teste1', 'Teste2', 'Teste3'])
df = df.append({'Teste1' : "olá", 'Teste2' : 77, 'Teste3': 56}, ignore_index = True)

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)