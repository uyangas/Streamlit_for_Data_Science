import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import json

# -----------------

with open("../utils/config.json","r") as f:
    config = json.load(f)

sys.path.insert(0, config['UTIL_PATH'])

from utils import process_data

PATH = config['DATA_PATH']

pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(layout='wide')

# -----------------

def load_data(extend_cols):
    df = pd.read_excel(os.path.join(PATH, "Coffee Shop Sales.xlsx"))
    df = process_data(df, extend_cols=extend_cols)

    return df

# өгөгдлийг оруулж ирэх
coffee_df = load_data(extend_cols=False)

# -----------------

st.title("КОФЕ ШОП-Н БОРЛУУЛАЛТЫН АНАЛИЗ")
st.header("КОФЕ ШОП-Н ДАТАНЫ ШИНЖ ЧАНАР")

# Өгөгдлийн шинж чанар

st.write("Өгөгдлийн ерөнхий шинж чанарын дүгнэлт")
st.markdown(f"Кофе шопны өгөгдөл нь {coffee_df.shape[1]} багана, {coffee_df.shape[0]} мөрөөс бүрдсэн")

st.markdown("**1. КОФЕ ШОПНЫ ДАТАНЫ ХАРАГДАХ БАЙДАЛ:**")
st.code(coffee_df.head())

st.write("**2. ДАТАНЫ ШИНЖ ЧАНАР:**")
st.markdown(f"- Датаны мөрийн тоо: **{coffee_df.shape[0]}**")
st.markdown(f"- Датаны баганы тоо: **{coffee_df.shape[1]}**")

st.write("**3. БАГАНЫН ӨГӨГДЛИЙН ТӨРЛҮҮД:**")
col_dtype = {}
col_dtype['columns'] = list(coffee_df.columns)
col_dtype['dtype'] = [coffee_df[col].dtype for col in coffee_df.columns]
col_dtype['na_cnt'] = [coffee_df[col].isna().sum() for col in coffee_df.columns]
st.code(pd.DataFrame(col_dtype))

st.write("**4. БАГАНЫН ТӨВИЙН ҮЗҮҮЛЭЛТҮҮД:**")
st.write("4.1. Тоон үзүүлэлтүүд:")
st.code(coffee_df.drop(['store_id','product_id','transaction_id'], axis=1).describe())
st.write("4.2. Чанарын үзүүлэлтүүд:")
for col in coffee_df.columns:
    if coffee_df[col].dtype in ['object','category']:
        st.write(f"- Баганын нэр: **{col}**")
        st.code(coffee_df[col].value_counts())

st.write("**5. ДАВХАРДСАН УТГА БАЙГАА ЭСЭХ:**")
st.code(coffee_df.duplicated().sum())


st.caption("Анализыг бэлтгэн танилцуулсан: Уянга.С")