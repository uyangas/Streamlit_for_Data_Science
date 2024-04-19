import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import sys

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.models import FactorRange, HoverTool
from bokeh.transform import dodge

import altair as alt

import pydeck as pdk


with open("../utils/config.json","r") as f:
    config = json.load(f)

sys.path.insert(0, config['UTIL_PATH'])

from utils import process_data, color_dict

PATH = config['DATA_PATH']

pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(layout='wide')
sns.set_style('white')
sns.set_palette("Blues")
color_names = ['aqua','torq', 'teal','powder_blue','blue1','blue3', 'forest_green','light_orange','light_gray','blood_orange']
color_hex = ["#00C4A6", "#00EACD","#00CFE7","#008696","#006996","#005194","#FFCD00","#FF8000","#B0B0B0"]


@st.cache_data
def load_data(extend_cols):
    df = pd.read_excel(os.path.join(PATH, "Coffee Shop Sales.xlsx"))
    df = process_data(df, extend_cols=extend_cols)

    return df

# өгөгдлийг оруулж ирэх
coffee_df = load_data(extend_cols=True)

st.title("КОФЕ ШОП-Н БОРЛУУЛАЛТЫН АНАЛИЗ")
st.header("КОФЕ ШОП-Н ДАТА")
st.subheader("**1. НИЙТ БОРЛУУЛАЛТ**")



# >>> streamlit-н chart функцуудыг ашиглах нь
# st.write("1.1. Нийт борлуулалт, сараар")
# temp_df = coffee_df.groupby("monthname").agg({'sales':'sum'}).reset_index()
# # temp_df["month"] = temp_df['month'].astype('int')
# st.line_chart(temp_df, x="monthname", y="sales")

# st.write("1.1. Нийт борлуулалт, өдрөөр")
# temp_df = coffee_df.groupby("day").agg({'sales':'sum'})
# st.area_chart(temp_df)

# st.write("1.1. Нийт борлуулалт, гаригаар")
# temp_df = coffee_df.groupby("dayofweek").agg({'sales':'sum'})
# st.bar_chart(temp_df)




# >>> st.pyplot-г ашиглах нь
st.write("**1.1. Нийт борлуулалт, сараар**")
temp_df = coffee_df.groupby("monthname_numbered").agg({'sales':'sum'}).reset_index()


st.markdown(f'''Сарын нийт борлуулалт зуны саруудад өсөх хандлагатай бөгөөд 1 ба 2-р сарын дундажтай харьцуулахад 
            **`{round(100*np.mean(temp_df[temp_df['monthname_numbered'].isin(['05_May','06_Jun'])]['sales'])/np.mean(temp_df[temp_df['monthname_numbered'].isin(['01_Jan','02_Feb'])]['sales']))}%`**
            -р өндөр байгаа ба сарын дундаж орлого нь **`${round(np.mean(temp_df['sales']))}`** байна.
            ''')
st.markdown('''6-р сарын орлого нь нийт орлогын **`23.8%`**, 5-р сарын орлого **`22.4%`**-г эзэлж байгаа ба 
            хамгийн орлого багатай сар нь 2-р сар буюу **`10.9%`**-г эзэлж байгаа буюу **`$76,145`** орлого орсон байна.''')

fig, ax = plt.subplots(1,3, figsize=(12,3))
bars = ax[0].bar(temp_df['monthname_numbered'], temp_df['sales'], color=color_hex[3])
for bar in bars:
    height = bar.get_height()
    ax[0].text(bar.get_x() + bar.get_width() / 2, height,"{:,.0f}".format(height), ha='center', va='bottom')

temp_df['monthly_increase'] = temp_df['sales'].diff()
temp_df['monthly_increase'] = temp_df['monthly_increase']*100/temp_df['sales']
bars = ax[1].bar(temp_df['monthname_numbered'], temp_df['monthly_increase'], color=color_hex[2])
for bar in bars:
    height = bar.get_height()
    ax[1].text(bar.get_x() + bar.get_width() / 2, height,"{:,.1f}%".format(height), ha='center', va='bottom')

temp_df = coffee_df.groupby("monthname").agg({'sales':'sum'}).reset_index()

ax[2].pie(temp_df['sales'], labels=temp_df['monthname'], autopct='%1.1f%%', colors=color_hex)

ax[0].set_title("Борлуулалтын хэмжээ, сараар $")
ax[1].set_title("Борлуулалтын орлогын өсөлт, сараар")
ax[2].set_title("Борлуулалтанд эзлэх хувь")

ax[0].set_yticks([])
ax[0].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)
ax[0].spines['bottom'].set_visible(False)
ax[0].spines['left'].set_visible(False)
ax[1].set_yticks([])
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)
ax[1].spines['bottom'].set_visible(False)
ax[1].spines['left'].set_visible(False)

plt.tight_layout()
st.pyplot(fig)

st.markdown("Эдгээр саруудын хувьд орлогыг долоо хоног болон өдрийн дундаж орлогыг харъя.")




# >>> plotly-г ашиглан график байгуулах нь
st.write("**1.2. Нийт борлуулалт, бүтээгдэхүүний төрлөөр**")

st.markdown(f'''Бүтээгдэхүүнүүд дундаас хамгийн өндөр борлуулалттай нь **`Coffee - 38.6%`**, **`Tea - 28.1%`**-г эзэлж байна.
            ''')
st.markdown('''6-р сарын орлого нь нийт орлогын **23.8%**, 5-р сарын орлого **22.4%**-г эзэлж байгаа ба 
            хамгийн орлого багатай сар нь 2-р сар буюу **10.9%**-г эзэлж байгаа буюу **$76,145** орлого орсон байна.''')

fig = make_subplots(1,2, 
                    subplot_titles=("Жилийн эхний хагасын борлуулалтад эзлэх хувь","Нийт борлуулалтын хэмжээ ($), бүтээгдэхүүний төрлөөр"),
                    specs=[[{'type': 'domain'}, {'type': 'xy'}]])

temp_df = coffee_df.groupby(["product_category"]).agg({'sales':'sum'}).reset_index()

colors = {i:color_dict[c] for i,c in zip(temp_df['product_category'].unique(),color_names)}

fig.add_trace(go.Pie(labels=temp_df['product_category'],
                     values=temp_df['sales'],
                     textinfo='percent+label',
                     showlegend=False,
                     marker_colors=list(colors.values())
                     ),
                     1,1)


temp_df = coffee_df.groupby(["monthname_numbered","product_category"]).agg({'sales':'sum'}).reset_index()

for i in temp_df['product_category'].unique():
    fig.add_trace(go.Bar(x=temp_df[temp_df['product_category']==i]['monthname_numbered'],
                            y=temp_df[temp_df['product_category']==i]['sales'],
                            marker_color=colors[i],
                            name=str(i),
                            legendgroup='group',
                            ),
                            1,2,
                            )
fig.update_layout(
    plot_bgcolor="white",
    barmode='stack',
    height=400,
    width=1200,
    legend=dict(traceorder='grouped')
    )

st.plotly_chart(fig)




# >>> bokeh-г ашиглан график байгуулах
st.write("**1.3. Нийт борлуулалт, өдрийн цагаар**")
st.markdown(f'''Нийт борлуулалтын **`56%`** нь өглөөний цагуудаар хийгддэг буюу өглөөний **`5:00-11:00`** цагийн хооронд, **`28%`** нь үдээс хойш буюу **`13:00-18:00`** цагийн хооронд хийгддэг байна.
            ''')
st.markdown('''Бүтээгдэхүүний хувьд кофений борлуулалт хэзээ байхаас үл хамааран тухайн үеийн борлуулалтын **`36-40%`**-г эзэлдэг ба цайны борлуулалт **`27-29%`**-г эзэлдэг байна. 
            Бусад бүтээгдэхүүнүүдийн хувьд оройн хоолны үеэр шоколадны борлуулалт бусад үетэй харьцуулахад бага зэргийн нэмэгддэг.''')


# борлуулалтын хэмжээ, өдрийн цагаар, сараар
temp_df = coffee_df.groupby(["timeofday","monthname_numbered"]).agg({'sales':'sum'}).reset_index()\
    .pivot_table(index='timeofday', columns='monthname_numbered', values=['sales'])
temp_df = round(temp_df.div(temp_df.sum(axis=0))*100,2)
temp_df.columns = ['01_Jan','02_Feb','03_Mar','04_Apr','05_May','06_June']
timeofday = list(temp_df.index)
temp_df = temp_df.T.reset_index().rename({'index':'monthname_numbered'},axis=1)
monthname = list(temp_df['monthname_numbered'])

data = {'monthname_numbered':list(temp_df['monthname_numbered']),
        'afternoon':list(temp_df['afternoon']),
        'dinner':list(temp_df['dinner']),
        'lunch':list(temp_df['lunch']),
        'morning':list(temp_df['morning']),
}

p1 = figure(x_range=FactorRange(factors=monthname), 
           plot_width=800, plot_height=400, 
           title="Нийт борлуулалтын хувь, өдрийн цагаар", 
           x_axis_label='Өдрийн цаг', 
           y_axis_label='Борлуулалтад эзлэх хувь')

renderers = p1.vbar_stack(timeofday,
              x='monthname_numbered',
              source=data,
              width=0.7,
              fill_color=color_hex[:4],
              line_color="white",
              legend_label=timeofday)

for r in renderers:
    timeofday = r.name
    hover = HoverTool(tooltips=[
        ("%s" % timeofday, "@%s" % timeofday)
    ], renderers=[r])
    p1.add_tools(hover)

p1.y_range.start = 0
p1.x_range.range_padding = 0.1
p1.xgrid.grid_line_color = None
p1.axis.minor_tick_line_color = None
p1.outline_line_color = None
p1.add_layout(p1.legend[0], 'right')


# борлуулалтын хэмжээ, өдрийн цагаар
temp_df = coffee_df.groupby(["timeofday","product_category"]).agg({'sales':'sum'}).reset_index()\
    .pivot_table(index='product_category', columns='timeofday', values=['sales'])
temp_df = round(temp_df.div(temp_df.sum(axis=0))*100,2)
temp_df.columns = ['afternoon','dinner','lunch','morning']
product_category = list(temp_df.index)
temp_df = temp_df.T.reset_index().rename({'index':'timeofday'},axis=1)
timeofday = list(temp_df['timeofday'])

data = {'timeofday':list(temp_df['timeofday']),
        'Bakery':list(temp_df['Bakery']),
        'Branded':list(temp_df['Branded']),
        'Coffee':list(temp_df['Coffee']),
        'Coffee beans':list(temp_df['Coffee beans']),
        'Drinking Chocolate':list(temp_df['Drinking Chocolate']),
        'Flavours':list(temp_df['Flavours']),
        'Loose Tea':list(temp_df['Loose Tea']),
        'Packaged Chocolate':list(temp_df['Packaged Chocolate']),
        'Tea':list(temp_df['Tea']),
}

p2 = figure(x_range=FactorRange(factors=timeofday), 
            plot_width=600, 
            plot_height=400, 
            title="Бүтээгдэхүүний нийт борлуулалтын хувь, өдрийн цагаар", 
            x_axis_label='Өдрийн цаг', 
            y_axis_label='Борлуулалтад эзлэх хувь')

renderers = p2.vbar_stack(product_category,
              x='timeofday',
              source=data,
              width=0.7,
              fill_color=color_hex,
              line_color="white",
              legend_label=product_category)

for r in renderers:
    product_category = r.name
    hover = HoverTool(tooltips=[
        ("%s" % product_category, "@%s" % product_category)
    ], renderers=[r])
    p2.add_tools(hover)
  
p2.y_range.start = 0
p2.x_range.range_padding = 0.1
p2.xgrid.grid_line_color = None
p2.axis.minor_tick_line_color = None
p2.outline_line_color = None
p2.add_layout(p2.legend[0], 'right')

grid = gridplot([[p1, p2]])

st.bokeh_chart(grid)




# >>> altair-г ашиглан график байгуулах
st.write("**1.4. Дундаж борлуулсан бүтээгдэхүүн, цагаар**")

st.markdown(f'''Дундаж борлуулалтыг цагаар харвал хамгийн өндөр борлуулалттай цаг нь **`өглөөний 10 цаг`** ба **`7-10 цаг`**-н хооронд борлуулсан бүтээгдэхүүний тоо хамгийн өндөр байдаг. Цагт дунджаар **`140`** ширхэг бүтээгдэхүүн борлуулагддаг. 
            ''')
st.markdown('''Бүтээгдэхүүний борлуулалт 11 цагаас эхлэн буурдаг ба ихэнх бүтээгдэхүүний хувьд оройны **`18 цаг`** хүртэл борлуулалт тогтвортой буюу дунджаар **`70`** ширхэг бүтээгдэхүүн борлуулдаг байдаг байна.''')

temp_df = coffee_df.groupby(["month","day","hour"]).agg({'transaction_qty':'sum'}).reset_index()

chart1 = alt.Chart(temp_df,
                   height=300,
                   width=600)\
    .mark_line()\
    .encode(
        x='hour:N',
        y=alt.Y('mean_qty:Q',
                axis=alt.Axis(title="Нийт борлуулсан бүтээгдэхүүний тоо"))
    ).transform_aggregate(
        mean_qty='mean(transaction_qty)',
        groupby=['hour']
    ).properties(
        title="Дундаж борлуулсан бүтээгдэхүүний тоо, цагаар"
    )

temp_df = coffee_df.groupby(["month","day","product_category","hour"]).agg({'transaction_qty':'sum'}).reset_index()

chart2 = alt.Chart(temp_df,
                   height=300,
                   width=600)\
    .mark_line()\
    .encode(
        x='hour:N',
        y=alt.Y('mean_qty:Q', 
                axis=alt.Axis(title="Дундаж борлуулсан бүтээгдэхүүний тоо")),
        color=alt.Color('product_category:N')
    ).transform_aggregate(
        mean_qty='mean(transaction_qty):Q',
        groupby=['hour','product_category']
    ).properties(
        title="Дундаж борлуулсан бүтээгдэхүүний тоо, бүтээгдэхүүний төрлөөр"
    )

st.altair_chart(alt.hconcat(chart1, chart2), use_container_width=True)




# >>> pydeck-г ашиглан график байгуулах
st.write("**1.5. Борлуулалтын хэмжээ, байршлаар**")

st.markdown(f'''Дундаж борлуулалтыг цагаар харвал хамгийн өндөр борлуулалттай цаг нь **`өглөөний 10 цаг`** ба **`7-10 цаг`**-н хооронд борлуулсан бүтээгдэхүүний тоо хамгийн өндөр байдаг. Цагт дунджаар **`140`** ширхэг бүтээгдэхүүн борлуулагддаг. 
            ''')
st.markdown('''Бүтээгдэхүүний борлуулалт 11 цагаас эхлэн буурдаг ба ихэнх бүтээгдэхүүний хувьд оройны **`18 цаг`** хүртэл борлуулалт тогтвортой буюу дунджаар **`70`** ширхэг бүтээгдэхүүн борлуулдаг байдаг байна.''')

temp_df = coffee_df.groupby(['store_location','Longitude','Latitude']).agg({'sales':'sum'}).reset_index()

layer = pdk.Layer(
    'ColumnLayer',
    data=temp_df,
    get_position='[Longitude, Latitude]',
    get_elevation=['sales'],
    auto_highlight=True,
    elevation_scale=0.01,
    extruded=True,
    get_radius=10,
    get_fill_color=[0,156,175],
    pickable=True,
    coverage=0.1
)

view_state = pdk.ViewState(
    latitude=40.743521,
    longitude=-73.990896,
    pitch=45,
    zoom=12
)

# Газрын зургыг render хийх
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"html": "<b>Branch:</b> {store_location} <br> <b>Total Sales:</b> ${sales}", 
             "style": {"color": "white"}}
)

st.pydeck_chart(r)


st.caption("Анализыг бэлтгэн танилцуулсан: Уянга.С")
