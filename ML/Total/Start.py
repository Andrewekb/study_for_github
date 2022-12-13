import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st






@st.cache(allow_output_mutation=True)
def get_flights():
    url = "flights.csv"
    return pd.read_csv(url)


@st.cache(allow_output_mutation=True)
def get_airport():
    url = "airports.csv"
    return pd.read_csv(url)




a = get_flights()
b = get_airport()


all_airport = a.columns

airport = st.text_input('airport')

if airport == 'ALL':
    ll = a
else:
   ll = a.query("ORIGIN_AIRPORT == '{}'".format(airport))


#ll = a
ll['DATE_DAY'] = pd.to_datetime(ll[['YEAR', 'MONTH', 'DAY']])
ll['HOUR'] = ll['SCHEDULED_DEPARTURE']//100
ll['MINUTE'] = ll['SCHEDULED_DEPARTURE']%100
ll['DATE_HOUR'] = pd.to_datetime(ll[['YEAR', 'MONTH', 'DAY', 'HOUR']])
ll['DEPARTURE_DELAY'].fillna(1, inplace=True)
ll['PROBABILITY'] = np.where(ll['DEPARTURE_DELAY']>0, 0, 1)
ll['AIRLINE'] = ll['AIRLINE'].astype(str)
B = ll.groupby(['ORIGIN_AIRPORT', 'DATE_HOUR'])['DATE_DAY'].count().reset_index().rename(columns={'DATE_DAY': 'COUNT_HOUR'})
ll = ll.merge(B, how='left', left_on=['ORIGIN_AIRPORT', 'DATE_HOUR'], right_on = ['ORIGIN_AIRPORT', 'DATE_HOUR'])
B = ll.groupby(['ORIGIN_AIRPORT', 'DATE_DAY'])['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR': 'COUNT_DAY'})
ll = ll.merge(B, how='left', left_on=['ORIGIN_AIRPORT', 'DATE_DAY'], right_on = ['ORIGIN_AIRPORT', 'DATE_DAY'])
ll = ll.merge(b, how='right', left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')
ll['AIRLINE'] = ll['AIRLINE'].astype(str)



fig = pd.DataFrame(ll.isna().sum()).rename(columns={0:'Пропуски'})
st.bar_chart(fig)



st.text('Добавлены данные')



code = '''
flights['HOUR'] = flights['SCHEDULED_DEPARTURE']//100
flights['MINUTE'] = flights['SCHEDULED_DEPARTURE']%100
flights['DATE_DAY'] = pd.to_datetime(flights[['YEAR', 'MONTH', 'DAY']])
flights['DATE_HOUR'] = pd.to_datetime(flights[['YEAR', 'MONTH', 'DAY', 'HOUR']])

flights['PROBABILITY'] = np.where(flights['DEPARTURE_DELAY']>0, 0, 1)


B = flights.groupby(['ORIGIN_AIRPORT', 'DATE_HOUR'])['DATE_DAY'].count().reset_index().rename(columns={'DATE_DAY': 'COUNT_HOUR'})
flights = flights.merge(B, how='left', left_on=['ORIGIN_AIRPORT', 'DATE_HOUR'], right_on = ['ORIGIN_AIRPORT', 'DATE_HOUR'])
B = flights.groupby(['ORIGIN_AIRPORT', 'DATE_DAY'])['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR': 'COUNT_DAY'})
flights = flights.merge(B, how='left', left_on=['ORIGIN_AIRPORT', 'DATE_DAY'], right_on = ['ORIGIN_AIRPORT', 'DATE_DAY'])
 '''
st.code(code, language='python')






st.text("Количество рейсов в день")
fig = ll.groupby('DATE_DAY')['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR':'Количество рейсов'}).set_index('DATE_DAY')
st.line_chart(fig)

ll = ll.loc[ll['DATE_DAY'].between('2015-01-01', '2015-09-30')]

st.text("Количество рейсов в день")
fig = ll.groupby('DATE_DAY')['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR':'Количество рейсов'}).set_index('DATE_DAY')
st.line_chart(fig)

st.text("Количество рейсов в разрезе аэропорта вылета")
fig = ll.groupby('ORIGIN_AIRPORT')['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR':'Количество рейсов'}).set_index('ORIGIN_AIRPORT')
st.bar_chart(fig)


st.text("Количество рейсов в различные пункты назначения")
A = ll.groupby('DESTINATION_AIRPORT')['DATE_HOUR'].count().sort_values(ascending=False).reset_index()
A = b.merge(A, how='right', left_on='IATA_CODE', right_on='DESTINATION_AIRPORT') 

fig = px.scatter_mapbox(A,
                    lon = A.LONGITUDE,
                    lat = A.LATITUDE,
                    zoom = 2,
                    hover_name="IATA_CODE",
                    size = A.DATE_HOUR,
                    color = A.DATE_HOUR
                    #width = 800,
                    #height = 600,
                                )
fig.update_layout(mapbox_style='open-street-map')
fig.show()
st.plotly_chart(fig, use_container_width=True)

st.text("Количество рейсов для авиакомпаний")
fig = ll.groupby('AIRLINE')['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR':'Количество рейсов'}).set_index('AIRLINE')
st.bar_chart(fig)

st.text("Количество рейсов в разрезе года по месяцам")
fig = ll.groupby('MONTH')['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR':'Количество рейсов'}).set_index('MONTH')
st.line_chart(fig)
st.bar_chart(fig)

st.text("Количество рейсов в разрезе года по дням недели")
fig = ll.groupby('DAY_OF_WEEK')['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR':'Количество рейсов'}).set_index('DAY_OF_WEEK')
st.line_chart(fig)
st.bar_chart(fig)

st.text("Количество рейсов в разрезе года в зависимости от часа вылета")
fig = ll.groupby('HOUR')['DATE_HOUR'].count().reset_index().rename(columns={'DATE_HOUR':'Количество рейсов'}).set_index('HOUR')
st.line_chart(fig)
st.bar_chart(fig)

st.text("Количество вылетов, положительная вероятность прилета")
A = ll.groupby('DATE_DAY')['DATE_HOUR'].count().reset_index()
A['DATE_HOUR'] = A['DATE_HOUR']/A['DATE_HOUR'].max()
B = ll.groupby('DATE_DAY')['PROBABILITY'].mean().reset_index()
fig = B.merge(A, how='right', left_on='DATE_DAY', right_on='DATE_DAY').set_index('DATE_DAY')
fig = fig.rename(columns={'DATE_HOUR':'Рейсы', 'PROBABILITY':'Вероятность'})
st.line_chart(fig)


st.text('Количество отмененных рейсов (причина)') 

fig = ll.groupby('CANCELLATION_REASON')['DATE_DAY'].count()
st.bar_chart(fig)



st.text('Средняя вероятность прилета в срок, количество вылетов, задержка из-за погоды') 

A = ll.groupby('DATE_DAY')['DATE_HOUR'].count().reset_index()
A['DATE_HOUR'] = A['DATE_HOUR']/A['DATE_HOUR'].max()
B = ll.groupby('DATE_DAY')['PROBABILITY'].mean().reset_index()
df = B.merge(A, how='right', left_on='DATE_DAY', right_on='DATE_DAY').set_index('DATE_DAY')
B = ll.groupby('DATE_DAY')['WEATHER_DELAY'].count().reset_index()
B['WEATHER_DELAY'] = B['WEATHER_DELAY']/B['WEATHER_DELAY'].max()
fig = df.merge(B, how='right', left_on='DATE_DAY', right_on='DATE_DAY').set_index('DATE_DAY')
fig = fig.rename(columns={'DATE_HOUR':'Рейсы', 'PROBABILITY':'Вероятность', 'WEATHER_DELAY':'Задержка погода'})
st.line_chart(fig)



