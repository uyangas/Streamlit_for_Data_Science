import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import sys

import altair as alt

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error


# ---------------------

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

alt.themes.enable("dark")

color_names = ['aqua','torq', 'teal','powder_blue','blue1','blue3', 'forest_green','light_orange','light_gray','blood_orange']
color_hex = ["#00C4A6", "#00EACD","#00CFE7","#008696","#006996","#005194","#FFCD00","#FF8000","#B0B0B0"]


# ---------------------

# өгөгдлийг оруулж ирэх ба боловсруулах
@st.cache_data
def load_data(extend_cols):
    df = pd.read_excel(os.path.join(PATH, "Coffee Shop Sales.xlsx"))
    df = process_data(df, extend_cols=extend_cols)

    return df

coffee_df = load_data(extend_cols=True)

# ---------------------

with st.sidebar:
    st.title("Дашбоардын удирдлага")
    selected_model = st.multiselect(
        "Загварын төрөл",
        ["Linear Regression","Random Forest","Decision Tree"],
        default="Linear Regression"
        )
    
    train_size = st.slider(label="Сургалтын өгөгдлийн хэмжээ",
                           min_value=0.1,
                           max_value=0.9,
                           value=0.8
                           )
    
# ---------------------

st.header("Кофе Шоп-н Борлуулалтын Таамаглал")

st.markdown("### Зорилго")
st.markdown("**Өдрийн борлуулалтыг таамаглах**")

dayofweek = {v:e for e, v in enumerate(coffee_df.dayofweek.unique(),1)}

daily_sales = coffee_df.groupby(['transaction_date']).agg({'sales':'sum',
                                                             'transaction_qty':'sum',
                                                             'dayofweek':'max',
                                                             'month':'max',
                                                             'day':'max'})\
                                                    .reset_index()

daily_sales['dayofweek'] = daily_sales['dayofweek'].replace(dayofweek)

chart = alt.Chart(daily_sales)\
    .mark_line().encode(
    x=alt.X('transaction_date:T', title="Сар, Өдөр"),
    y=alt.Y('sales:Q', title="Борлуулалт, $")
).properties(width=800,
             title="Өдрийн борлуулалтын бодит утга")

st.altair_chart(chart)


# ---------------------

for col in ['sales', 'transaction_qty', 'dayofweek']:
    lag1 = col+"_lag1"
    lag3 = col+"_lag3"
    daily_sales[lag1] = daily_sales[col].shift(1)
    daily_sales[lag3] = daily_sales[col].shift(3)

daily_sales = daily_sales.dropna(axis=0)


scaler_sales = StandardScaler()
scaler_qty = StandardScaler()
daily_sales_scaled = daily_sales.copy()
daily_sales_scaled[['sales']] = scaler_sales.fit_transform(daily_sales[['sales']])
daily_sales_scaled[['transaction_qty']] = scaler_qty.fit_transform(daily_sales[['transaction_qty']])

split_idx = int(train_size*len(daily_sales_scaled))

train = daily_sales_scaled.iloc[:split_idx,:]
test = daily_sales_scaled.iloc[split_idx:,:]
X_train = train.drop(['sales','transaction_date'],axis=1)
X_test = test.drop(['sales','transaction_date'],axis=1)
y_train = train[['sales']]
y_test = test[['sales']]


model_results = {"model":[],
                 "RMSE":[],
                 "pred":[],
                 "col_name":[]
                 }

for model_name in selected_model:

    if model_name == "Linear Regression":
        model = LinearRegression()
        suffix="lr"

    elif model_name == "Random Forest":
        model = RandomForestRegressor()
        suffix="rf"

    elif model_name == "Decision Tree":
        model = DecisionTreeRegressor()
        suffix="dt"
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    model_results["model"].append(model_name)
    model_results['RMSE'].append(np.sqrt(mean_squared_error(y_test, y_pred)))
    model_results["pred"].append(y_pred)

    col_name = "sales_pred"+suffix

    model_results['col_name'].append(col_name)
    test[col_name] = y_pred


st.markdown("### Загварын үр дүн")
st.markdown(f"Тестийн өгөгдлийн RMSE")
st.write(pd.DataFrame(model_results).drop(["pred","col_name"],axis=1))
# st.write(model_results)


chart1 = alt.Chart(test)\
    .mark_line().encode(
    x=alt.X('transaction_date:T', title="Сар, Өдөр"),
    y=alt.Y('sales:Q', title="Борлуулалт, $"),
    color=alt.value("blue"),
    tooltip=['transaction_date','sales']
).properties(width=800,
             title="Өдрийн борлуулалт")

for e, col_name in enumerate(model_results['col_name']):
    chart1 += alt.Chart(test)\
    .mark_line().encode(
    x=alt.X('transaction_date:T', title="Сар, Өдөр"),
    y=alt.Y(col_name, title="Борлуулалт, $"),
    color=alt.value(color_hex[e+1]),
    tooltip=['transaction_date','sales']
    )


st.altair_chart(chart1
                )