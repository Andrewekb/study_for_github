import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns




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


options = st.multiselect(
    'Выбрать необходимые показатели для построения heatmap',
    list(ll.columns))




end = st.date_input('Дата вылета')


if st.button('Попарная корреляция heatmap'):
    A= ll.loc[ll['DATE_DAY'].between('2015-01-01', '{}'.format(end))]
    A =  A[options]

    fig, ax = plt.subplots()  
    sns.heatmap(A.corr(), ax=ax)
    st.write(fig)


if st.button('Boxplot, удаляем выбросы'):

#A = ll.groupby(['DAY_OF_WEEK','AIRLINE'], as_index=False)['DATE_DAY'].count()
    fig = px.box(ll['ARRIVAL_DELAY'])
    fig.show()
    st.plotly_chart(fig, use_container_width=True)

    Q1 = ll['ARRIVAL_DELAY'].quantile(0.25)
    Q3 = ll['ARRIVAL_DELAY'].quantile(0.75)
    IQR = Q3 - Q1
    o = ll[(ll['ARRIVAL_DELAY'] < Q1-1.5*IQR ) | (ll['ARRIVAL_DELAY'] > Q3+1.5*IQR)]['ARRIVAL_DELAY'].reset_index()
    #список с исключениями
    o = list(o.ARRIVAL_DELAY)
    #исключаю выбросы
    A = ll.query("ARRIVAL_DELAY != @o")

    fig = px.box(A['ARRIVAL_DELAY'])
    fig.show()
    st.plotly_chart(fig, use_container_width=True)

    A= ll.loc[ll['DATE_DAY'].between('2015-01-01', '{}'.format(end))]
    A =  A[options]
    fig, ax = plt.subplots()  
    sns.heatmap(A.corr(), ax=ax)
    st.write(fig)