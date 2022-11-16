import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns



st.title("Визуализация данных")


@st.cache
def get_flights():
    url = "flights.csv"
    return pd.read_csv(url)


@st.cache
def get_airport():
    url = "airports.csv"
    return pd.read_csv(url)

a = get_flights()
b = get_airport()



airport = st.text_input('airport')
print(airport)



ll = a.query("ORIGIN_AIRPORT == '{}'".format(airport))
ll['DATE_DAY'] = pd.to_datetime(ll[['YEAR', 'MONTH', 'DAY']])
ll['HOUR'] = ll['SCHEDULED_DEPARTURE']//100
ll['MINUTE'] = ll['SCHEDULED_DEPARTURE']%100
ll['DEPARTURE_DELAY'].fillna(1, inplace=True)
ll['PROBABILITY'] = np.where(ll['DEPARTURE_DELAY']>0, 0, 1)
ll['AIRLINE'] = ll['AIRLINE'].astype(str)

st.header("Общее количество рейсов {}".format(ll.shape[0]))





A = ll.groupby('DESTINATION_AIRPORT')['DATE_DAY'].count().sort_values(ascending=False).reset_index()
A = b.merge(A, how='right', left_on='IATA_CODE', right_on='DESTINATION_AIRPORT') 


B = b.query("IATA_CODE == '{}'".format(airport))
fig = px.scatter_mapbox(B,
                    lon = B.LONGITUDE,
                    lat = B.LATITUDE,
                    zoom = 5,
                    hover_name="IATA_CODE",
                    #width = 800,
                    #height = 600,
                                )
fig.update_layout(mapbox_style='open-street-map')
fig.show()
st.plotly_chart(fig, use_container_width=True)

st.text('Карта направлений авиаперелетов для аэропорта вылета за год') 
fig = px.scatter_mapbox(A,
                    lon = A.LONGITUDE,
                    lat = A.LATITUDE,
                    zoom = 3,
                    color = A.DATE_DAY,
                    size = A.DATE_DAY,
                    hover_name="DESTINATION_AIRPORT",
                    #width = 800,
                    #height = 600,
                                )
fig.update_layout(mapbox_style='open-street-map')
fig.show()
st.plotly_chart(fig, use_container_width=True)


st.text('Количество перелетов по дням') 

fig = ll.groupby('DATE_DAY')['ARRIVAL_DELAY'].count().reset_index().set_index('DATE_DAY')
st.line_chart(fig)


ll = ll.loc[ll['DATE_DAY'].between('2015-01-01', '2015-09-30')]


st.text('Количество перелетов по месяцам с 2015-01-01 по 2015-09-30') 

fig = ll.groupby('DATE_DAY')['ARRIVAL_DELAY'].count().reset_index().set_index('DATE_DAY')
st.line_chart(fig)

st.text('Количество перелетов для различных авиакомпаний') 


fig = ll.groupby('AIRLINE')['DATE_DAY'].count().reset_index().set_index('AIRLINE')
st.bar_chart(fig)

st.text('Количество перелетов по дням недели за год') 


fig = ll.groupby('DAY_OF_WEEK')['DATE_DAY'].count().reset_index().set_index('DAY_OF_WEEK')
st.line_chart(fig)
st.bar_chart(fig)


st.text('Средняя вероятность прилета для дней недели')

fig = ll.groupby('DAY_OF_WEEK')['PROBABILITY'].mean().reset_index().set_index('DAY_OF_WEEK')
st.line_chart(fig)



st.text('Средняя вероятность прилета в срок для аэропортов назначения') 

fig = ll.groupby('DESTINATION_AIRPORT')['PROBABILITY'].mean().reset_index().set_index('DESTINATION_AIRPORT')
#st.line_chart(fig)
st.bar_chart(fig)


st.text('Количество перелетов для аэропортов прилета') 

fig = ll.groupby('DESTINATION_AIRPORT')['ARRIVAL_DELAY'].count().reset_index().set_index('DESTINATION_AIRPORT')
#st.line_chart(fig)
st.bar_chart(fig)


st.text('Количество вылетов в разрезе суток') 

fig = ll.groupby('HOUR')['DATE_DAY'].count().reset_index().set_index('HOUR')
st.line_chart(fig)

st.text('Средняя вероятность прилета в срок для аэропортов назначения при вылете в разрезе суток') 

fig = ll.groupby('HOUR')['PROBABILITY'].mean().reset_index().set_index('HOUR')
st.line_chart(fig)

st.text('Средняя вероятность прилета в срок и количество вылетов в разрезе года') 

A = ll.groupby('DATE_DAY')['ARRIVAL_DELAY'].count().reset_index()
A['ARRIVAL_DELAY'] = A['ARRIVAL_DELAY']/A['ARRIVAL_DELAY'].max()
B = ll.groupby('DATE_DAY')['PROBABILITY'].mean().reset_index()
fig = B.merge(A, how='right', left_on='DATE_DAY', right_on='DATE_DAY').set_index('DATE_DAY')
st.line_chart(fig)

st.text('Количество отмененных рейсов (причина)') 

fig = ll.groupby('CANCELLATION_REASON')['DATE_DAY'].count()
st.bar_chart(fig)

st.text('Средняя вероятность прилета в срок, количество вылетов, задержка из-за погоды') 

A = ll.groupby('DATE_DAY')['ARRIVAL_DELAY'].count().reset_index()
A['ARRIVAL_DELAY'] = A['ARRIVAL_DELAY']/A['ARRIVAL_DELAY'].max()
B = ll.groupby('DATE_DAY')['PROBABILITY'].mean().reset_index()
df = B.merge(A, how='right', left_on='DATE_DAY', right_on='DATE_DAY').set_index('DATE_DAY')
B = ll.groupby('DATE_DAY')['WEATHER_DELAY'].count().reset_index()
B['WEATHER_DELAY'] = B['WEATHER_DELAY']/B['WEATHER_DELAY'].max()
fig = df.merge(B, how='right', left_on='DATE_DAY', right_on='DATE_DAY').set_index('DATE_DAY')
st.line_chart(fig)


st.text('Средняя вероятность прилета в срок для авиаперевозчиков (месяцы)') 

A = ll.groupby(['MONTH','AIRLINE'], as_index=False)['PROBABILITY'].mean()
fig = px.line(A, x='MONTH', y='PROBABILITY', color='AIRLINE', line_group='AIRLINE')
fig.show()
st.plotly_chart(fig, use_container_width=True)

st.text('Количество перелетов для авиаперевозчиков (месяцы)') 

A = ll.groupby(['MONTH','AIRLINE'], as_index=False)['DATE_DAY'].count()
fig = px.line(A, x='MONTH', y='DATE_DAY', color='AIRLINE', line_group='AIRLINE')
fig.show()
st.plotly_chart(fig, use_container_width=True)


st.text('Количество перелетов для авиаперевозчиков (дни)') 

A = ll.groupby(['DAY_OF_WEEK','AIRLINE'], as_index=False)['DATE_DAY'].count()
fig = px.line(A, x='DAY_OF_WEEK', y='DATE_DAY', color='AIRLINE', line_group='AIRLINE')
fig.show()
st.plotly_chart(fig, use_container_width=True)

st.text('Средняя вероятность прилета в срок для авиаперевозчиков (дни)') 

A = ll.groupby(['DAY_OF_WEEK','AIRLINE'], as_index=False)['PROBABILITY'].mean()
fig = px.line(A, x='DAY_OF_WEEK', y='PROBABILITY', color='AIRLINE', line_group='AIRLINE')
fig.show()
st.plotly_chart(fig, use_container_width=True)
