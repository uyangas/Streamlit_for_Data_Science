import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from utils import process_data

PATH = os.getcwd()

pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(layout='wide')

def load_data():
    df = pd.read_excel(os.path.join(PATH, "Coffee Shop Sales.xlsx"))
    df = process_data(df)

    return df

# өгөгдлийг оруулж ирэх
coffee_df = load_data()

st.title("КОФЕ ШОП-Н БОРЛУУЛАЛТЫН АНАЛИЗ")
st.header("КОФЕ ШОП-Н ДАТАНЫ ШИНЖ ЧАНАР")

# Өгөгдлийн шинж чанар

st.write("Өгөгдлийн ерөнхий шинж чанарын дүгнэлт")
st.markdown(f"Кофе шопны өгөгдөл нь {coffee_df.shape[1]} багана, {coffee_df.shape[0]} мөрөөс бүрдсэн")

st.markdown("**1. Кофе шопны дата-ны харагдах байдал:**")
st.code(coffee_df.head())

st.write("**2. Датаны шинж чанар:**")
st.markdown(f"- Датаны мөрийн тоо: **{coffee_df.shape[0]}**")
st.markdown(f"- Датаны баганы тоо: **{coffee_df.shape[1]}**")

st.write("**3. Баганын өгөгдлийн төрлүүд:**")
col_dtype = {}
col_dtype['columns'] = list(coffee_df.columns)
col_dtype['dtype'] = [coffee_df[col].dtype for col in coffee_df.columns]
col_dtype['na_cnt'] = [coffee_df[col].isna().sum() for col in coffee_df.columns]
st.code(pd.DataFrame(col_dtype))

st.write("**4. Баганын төвийн үзүүлэлтүүд:**")
st.write("4.1. Тоон үзүүлэлтүүд:")
st.code(coffee_df.describe())
st.write("4.2. Чанарын үзүүлэлтүүд:")
for col in coffee_df.columns:
    if coffee_df[col].dtype in ['object','category']:
        st.write(f"- Баганын нэр: **{col}**")
        st.code(coffee_df[col].value_counts())

st.write("**5. Давхардсан утга байгаа эсэх:**")
st.code(coffee_df.duplicated().sum())


st.caption("Анализыг бэлтгэн танилцуулсан: Уянга.С")