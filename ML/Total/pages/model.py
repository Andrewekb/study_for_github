import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import streamlit as st





st.title("Анализ данных")


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




end = st.date_input('Дата вылета')





if st.button('Летим'):


    A= ll.loc[ll['DATE_DAY'].between('2015-01-01', '{}'.format(end))]

    st.text('Общее количество направлений {}'.format(A.DESTINATION_AIRPORT.nunique()))

    def make_features(data, max_lag, rolling_mean_size):
        data['year'] = data.DATE_DAY.dt.year
        data['month'] = data.DATE_DAY.dt.month
        data['day'] = data.DATE_DAY.dt.day
        data['dayofweek'] = data.DATE_DAY.dt.dayofweek
        for lag in range(1, max_lag + 1):
            data['lag_{}'.format(lag)] = data['ARRIVAL_DELAY'].shift(lag)
        data['y_mean'] = data['ARRIVAL_DELAY'].shift().rolling(rolling_mean_size).mean().copy()



    total = pd.DataFrame(columns=['name', 'RMSE', 'ARRIVAL_DELAY'])

    for d_airport in A['DESTINATION_AIRPORT'].unique():
        d_df = A.query("DESTINATION_AIRPORT == '{}'".format(d_airport))


           #удаляю выбросы - 1,5 межквантильных размаха из колонки с задержкой прилета
        Q1 = d_df['ARRIVAL_DELAY'].quantile(0.25)
        Q3 = d_df['ARRIVAL_DELAY'].quantile(0.75)
        IQR = Q3 - Q1
        a = d_df[(d_df['ARRIVAL_DELAY'] < Q1-1.5*IQR ) | (d_df['ARRIVAL_DELAY'] > Q3+1.5*IQR)]['ARRIVAL_DELAY'].reset_index()
    
    #список с исключениями
        a = list(a.ARRIVAL_DELAY)
    #исключаю выбросы
        d_df = d_df.query("ARRIVAL_DELAY != @a")
        d = d_df.DATE_DAY.max()
        d_df.loc[(d_df.DATE_DAY == d),'ARRIVAL_DELAY']=0

        try:    

        #генерируем показатели
            d_df = d_df.groupby('DATE_DAY')['ARRIVAL_DELAY'].sum().reset_index()
            make_features(d_df,21,7)
            d_df.dropna(inplace=True)
            d_df.set_index('DATE_DAY', inplace=True)


        #формирую выборки - обучающую и тестовую
            X_train,X_test, y_train, y_test = train_test_split(d_df.drop('ARRIVAL_DELAY',axis=1),
                                                        d_df.ARRIVAL_DELAY,
                                                        shuffle = False,# временной ряд, отключаем перемешивание
                                                        test_size = 0.15)

        #обучаю и делаю предсказание
            lr = LinearRegression()
            lr.fit(X_train, y_train)
            pred = lr.predict(X_test)

        #формирую словарь, далее будем накапливать данные в df total
            t = {'name':'{}'.format(d_airport), 'RMSE':round(np.sqrt(mean_squared_error(y_test, pred)), 2), 
            'ARRIVAL_DELAY':round(pred[-1], 2)}
            total = total.append(t, ignore_index=True)

        except Exception as e:
            continue
    t = {'name':'{}'.format(airport), 'RMSE':total.RMSE.mean()*2, 'ARRIVAL_DELAY':0}
    total = total.sort_values(by=['RMSE','ARRIVAL_DELAY'],ascending=[True, True])
    total = total.head(3)
    total = total.append(t, ignore_index=True)

    st.dataframe(total.set_index('name')[:-1])

    total = total.reset_index()
    map_air = b.merge(total, how='right', left_on='IATA_CODE', right_on='name')

    
    fig = px.scatter_mapbox(map_air,
                    lon = map_air.LONGITUDE,
                    lat = map_air.LATITUDE,
                    zoom = 2,
                    color = map_air.RMSE,
                    size = map_air.RMSE,
                    hover_name="name",
                    width = 800,
                    height = 600,
                                )
    fig.update_layout(mapbox_style='open-street-map')
    fig.show()
    st.plotly_chart(fig)

    st.text('Средняя вероятность прилета в срок для аэропортов назначения') 

    fig = ll.groupby('DESTINATION_AIRPORT')['PROBABILITY'].mean().reset_index().set_index('DESTINATION_AIRPORT')
    #st.line_chart(fig)
    st.bar_chart(fig)

    
