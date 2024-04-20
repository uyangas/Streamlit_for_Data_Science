import streamlit as st
import pandas as pd
import os
import json
import sys

import altair as alt

# -----------------

with open("../utils/config.json","r") as f:
    config = json.load(f)

sys.path.insert(0, config['UTIL_PATH'])

from utils import process_data, color_dict, format_number, alt_make_donut, alt_line_chart, sidebar_filter

PATH = config['DATA_PATH']

pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(
    page_title="Кофе Шоп-н Борлуулалтын Дашбоард",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

color_names = ['aqua','torq', 'teal','powder_blue','blue1','blue3', 'forest_green','light_orange','light_gray','blood_orange']
color_hex = ["#00C4A6", "#00EACD","#00CFE7","#008696","#006996","#005194","#FFCD00","#FF8000","#B0B0B0"]

# -----------------

# өгөгдлийг оруулж ирэх ба боловсруулах
@st.cache_data
def load_data(extend_cols):
    df = pd.read_excel(os.path.join(PATH, "Coffee Shop Sales.xlsx"))
    df = process_data(df, extend_cols=extend_cols)

    return df

coffee_df = load_data(extend_cols=True)

product_category_list = ['All']
product_category_list.extend(list(coffee_df['product_category'].unique()))
month_list = ["All"]
month_list.extend(list(coffee_df['monthname'].unique()))

monthly_sales_product = coffee_df.groupby(['monthname_numbered',
                                           'product_category'])\
                                .agg({'sales':'sum', 
                                      'transaction_qty':'sum'})\
                                .reset_index()

month_name_dict = {"January":"01_Jan","February":"02_Feb","March":"03_Mar","April":"04_Apr","May":"05_May","June":"06_June"}

st.header("Кофе Шоп-н Борлуулалтын Дашбоард")

# -----------------

# >>> Sidebar үүсгэх
with st.sidebar:
    st.title("Дашбоардын удирдлага")
    month = st.multiselect(
        "Тайлагнах сар",
        month_list,
        default=month_list[0]
        )

    product_category = st.multiselect(
        "Бүтээгдэхүүний төрөл",
        product_category_list,
        default=product_category_list[0]
        )


# -----------------


# >>> Багана үүсгэх
# Баганы тоог бичих
# col1, col2, col3 = st.columns(3)
# Баганы хэмжээг зааж өгөх
col1, col2, col3, col4 = st.columns((10,20,10,1))

with col1:
    st.markdown("#### Нийт борлуулалт")
    st.markdown("Тухайн сар, бүтээгдэхүүний хувьд")

    # Сарын борлуулалтын орлого
    monthly_sales = sum(sidebar_filter(coffee_df, month, product_category, type="Орлого")['sales'])
    monthly_sales = format_number(monthly_sales)
    st.metric(label="Орлого", value=monthly_sales)

    # Сарын борлуулсан бүтээгдэхүүн
    monthly_product = sum(sidebar_filter(coffee_df, month, product_category, type="Ширхэг")['transaction_qty'])
    monthly_product = "{:,}".format(monthly_product)
       
    st.metric(label="Ширхэг", value=monthly_product)

    # Борлуулалтын орлогод эзлэх хувь
    st.markdown("")
    st.markdown("#### Нийт борлуулалтын %")
    st.markdown("Орлого")

    monthly_sales = sum(sidebar_filter(coffee_df, month, product_category, type="Орлого")['sales'])
    total_sales = sum(coffee_df['sales'])
    sales_percent = round(monthly_sales*100/total_sales,1)

    st.altair_chart(alt_make_donut(sales_percent,"Борлуулалтын орлого","blue"))

    # Борлуулсан бүтээгдэхүүний тоонд эзлэх хувь
    st.markdown("Ширхэг")

    monthly_product = sum(sidebar_filter(coffee_df, month, product_category, type="Ширхэг")['transaction_qty'])
    total_qty = sum(coffee_df['transaction_qty'])
    sales_percent = round(monthly_product*100/total_qty,1)

    st.altair_chart(alt_make_donut(sales_percent,"Борлуулсан бүтээгдэхүүний тоо","green"))



with col2:
    st.markdown("#### Борлуулалт, сараар")
    temp_df = monthly_sales_product.groupby(['monthname_numbered','product_category'])\
                                .agg({'sales':'sum', 
                                      'transaction_qty':'sum'})\
                                .reset_index()
    
    if ((len(month)==1) & (month[0]=='All')):
        month_name = list(month_name_dict.keys())
    else:
        month_name = [month_name_dict[m] for m in month]
    
    if ((len(product_category)==1)&(product_category[0]=='All')):
        product_category = product_category_list[1:]
        st.write(f"Бүх бүтээгдэхүүний хувьд")
    else:
        st.write(f"{', '.join(product_category)}-н хувьд")

    temp_df = coffee_df[coffee_df['product_category'].isin(product_category)]
    
    st.markdown("Борлуулалтын орлого")
    chart1 = alt_line_chart(temp_df, 
                            x_axis='monthname_numbered',
                            agg_col='sales',
                            x_title='Сар',
                            y_title='USD ($)',
                            color="#004EAF")

    st.altair_chart(chart1)


    temp_df = coffee_df[coffee_df['product_category'].isin(product_category)]

    st.markdown("Борлуулсан бүтээгдэхүүн")
    chart2 = alt_line_chart(temp_df, 
                            x_axis='monthname_numbered',
                            agg_col='transaction_qty',
                            x_title='Сар',
                            y_title='ширхэг',
                            color="#009CAF")

    st.altair_chart(chart2)



with col3:
    st.markdown("#### Бүтээгдэхүүний төрөл")
    st.markdown("Хамгийн өндөр борлуулалттай")

    if ((len(month)==1) & (month[0]=='All')) & ((len(product_category)==1)&(product_category[0]=='All')):
        product_sales = coffee_df.groupby('product_type').agg({'sales':'sum'}).reset_index()
    elif ((len(month)==1) & (month[0]=='All')) & ('All' not in product_category):
        product_sales = coffee_df[coffee_df['product_category'].isin(product_category)]\
            .groupby('product_type').agg({'sales':'sum'}).reset_index()
    elif ('All' not in month) & ((len(product_category)==1)&(product_category[0]=='All')):
        product_sales = coffee_df[(coffee_df['monthname'].isin(month))]\
            .groupby('product_type').agg({'sales':'sum'}).reset_index()
    elif ('All' not in month) & ('All' not in product_category):
        product_sales = coffee_df[(coffee_df['monthname'].isin(month))&(coffee_df['product_category'].isin(product_category))]\
            .groupby('product_type').agg({'sales':'sum'}).reset_index()
    
    chart = alt.Chart(product_sales).mark_bar(color="#163356").encode(
        x=alt.X('sales:Q', title="Борлуулалт ($)"),
        y=alt.Y('product_type:N', title="Бүтээгдэхүүний нэр").sort('-x')
    ).properties(
        height=700
    )

    st.altair_chart(chart)