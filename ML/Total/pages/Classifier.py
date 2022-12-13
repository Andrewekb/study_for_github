import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import mean_squared_error
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler



st.text('Используемые библиотеки')
code = '''
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import mean_squared_error
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
 '''
st.code(code, language='python')


@st.cache(allow_output_mutation=True)
def get_flights():
    url = "flights.csv"
    return pd.read_csv(url)


@st.cache(allow_output_mutation=True)
def get_airport():
    url = "airports.csv"
    return pd.read_csv(url)



@st.cache(allow_output_mutation=True)
def get_weather():
    url = "Atlanta.csv"
    return pd.read_csv(url)



code = '''
!pip install wwo_hist
from wwo_hist import retrieve_hist_data



frequency = 1
start_date = '1-JAN-2015'
end_date = '30-SEP-2015'
api_key = 'd3307ad7a39849fba4a134542221212'
location_list = ['Atlanta']
hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)
 '''
st.code(code, language='python')




a = get_flights()
b = get_airport()


all_airport = a.columns

airport = st.text_input('airport')

if airport == 'ALL':
    ll = a
else:
   ll = a.query("ORIGIN_AIRPORT == '{}'".format(airport))



st.text('Общее количество возможных направлений {}'.format(ll.DESTINATION_AIRPORT.nunique()))


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
ll = ll.loc[ll['DATE_DAY'].between('2015-01-01', '2015-09-30')]


if airport == 'ATL':
    c = get_weather()
    c = c[['precipMM', 'tempC', 'visibility', 'windspeedKmph', 'date_time']]
    c['date_time'] = pd.to_datetime(c['date_time'])
    ll = ll.merge(c, how='left', left_on='DATE_HOUR', right_on='date_time')
    ll.drop('date_time', inplace=True, axis=1)





st.text('Данные для анализа')





code = '''
        [['MONTH', 'DAY_OF_WEEK', 'AIRLINE','SCHEDULED_TIME',
       'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
       'SCHEDULED_DEPARTURE', 'DISTANCE',
       'ARRIVAL_DELAY', 'HOUR', 'MINUTE',
       'DATE_HOUR', 'PROBABILITY', 'COUNT_HOUR', 'COUNT_DAY',
       'precipMM', 'tempC', 'visibility', 'windspeedKmph']]
 '''
st.code(code, language='python')



if airport == 'ATL':
    C = ll[['MONTH', 'DAY_OF_WEEK', 'AIRLINE','SCHEDULED_TIME',
            'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
            'SCHEDULED_DEPARTURE', 'DISTANCE',
            'ARRIVAL_DELAY', 'HOUR', 'MINUTE',
            'DATE_HOUR', 'PROBABILITY', 'COUNT_HOUR', 'COUNT_DAY', 
            'precipMM', 'tempC', 'visibility', 'windspeedKmph'  ]]

else:
    C = ll[['MONTH', 'DAY_OF_WEEK', 'AIRLINE','SCHEDULED_TIME',
            'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
            'SCHEDULED_DEPARTURE', 'DISTANCE',
            'ARRIVAL_DELAY', 'HOUR', 'MINUTE',
            'DATE_HOUR', 'PROBABILITY', 'COUNT_HOUR', 'COUNT_DAY']]


options = st.multiselect(
    'Выбрать необходимые показатели для построения heatmap',
    list(C.columns))

fig = pd.DataFrame(C.isna().sum()).rename(columns={0:'Пропуски'})
st.bar_chart(fig)


C.dropna(inplace=True)


code = '''
C.dropna(inplace=True)
 '''
st.code(code, language='python')




if st.button('Попарная корреляция/ковариация'):
    
    A =  C[options]
    A.set_index('DATE_HOUR', inplace=True)
    le = LabelEncoder()
    for column in A.columns:
        if A.dtypes['{}'.format(column)] == 'object':
            A['{}'.format(column)] = le.fit_transform(A['{}'.format(column)])

    fig, ax = plt.subplots()  
    colormap = plt.cm.viridis
    sns.heatmap(A.corr(), ax=ax, cmap=colormap)
    st.write(fig)

    scaler = MinMaxScaler(feature_range=(0, 1))
    rescaledX = scaler.fit_transform(A)
    col = A.columns
    skalre_df = pd.DataFrame(rescaledX, columns=col )


    code = '''
    scaler = MinMaxScaler(feature_range=(0, 1))
    rescaledX = scaler.fit_transform(A)
    col = A.columns
    skalre_df = pd.DataFrame(rescaledX, columns=col )
    '''
    st.code(code, language='python')

    fig, ax = plt.subplots()  
    colormap = plt.cm.viridis
    sns.heatmap(skalre_df.cov(), ax=ax, cmap=colormap)
    st.write(fig)


if st.button('go!'):
    C =  C[options]
    st.text(C.columns)

    a_list = []
    le = LabelEncoder()
    for column in C.columns:
        if C.dtypes['{}'.format(column)] == 'object':
            a_list.append(column)
            C['{}'.format(column)] = le.fit_transform(C['{}'.format(column)])

    
    code = '''
    Меняю строковые данные числовыми с помощью LabelEncoder
    a_list = []
    le = LabelEncoder()
    for column in C.columns:
        if C.dtypes['{}'.format(column)] == 'object':
            a_list.append(column)
            C['{}'.format(column)] = le.fit_transform(C['{}'.format(column)])
 '''
    st.code(code, language='python')


    C.set_index('DATE_HOUR', inplace=True)





    fig = px.box(C['ARRIVAL_DELAY'], title='Распределение задержки вылета, минуты')
    fig.show()
    st.plotly_chart(fig, use_container_width=True)


    #удаляю выбросы - 1,5 межквантильных размаха из колонки с задержкой прилета
    Q1 = C['ARRIVAL_DELAY'].quantile(0.25)
    Q3 = C['ARRIVAL_DELAY'].quantile(0.75)
    IQR = Q3 - Q1
    a = C[(C['ARRIVAL_DELAY'] < Q1-1.5*IQR ) | (C['ARRIVAL_DELAY'] > Q3+1.5*IQR)]['ARRIVAL_DELAY'].reset_index()


    code = '''
    Удаляю выбросы
    Q1 = C['ARRIVAL_DELAY'].quantile(0.25)
    Q3 = C['ARRIVAL_DELAY'].quantile(0.75)
    IQR = Q3 - Q1
    a = C[(C['ARRIVAL_DELAY'] < Q1-1.5*IQR ) | (C['ARRIVAL_DELAY'] > Q3+1.5*IQR)]['ARRIVAL_DELAY'].reset_index()
    '''
    st.code(code, language='python')


    
    
    #список с исключениями
    a = list(a.ARRIVAL_DELAY)
    #исключаю выбросы
    C_1 = C.query("ARRIVAL_DELAY != @a")


    fig = px.box(C_1['ARRIVAL_DELAY'], title='Распределение задержки вылета, минуты')
    fig.show()
    st.plotly_chart(fig, use_container_width=True)


    C.drop(['PROBABILITY'], axis=1, inplace=True)

    #формирую выборки - обучающую и тестовую
    X_train,X_test, y_train, y_test = train_test_split(C.drop('ARRIVAL_DELAY',axis=1),
                                                        C.ARRIVAL_DELAY,
                                                        shuffle = False,# временной ряд, отключаем перемешивание
                                                        test_size = 0.25)

    

    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    print('Ошибка на обучающей выборке', (mean_squared_error(y_train, dtc.predict(X_train)))**0.5)
    pred = dtc.predict(X_test)
    print('Ошибка на тесте', (mean_squared_error(y_test, pred))**0.5)

    code = '''
    Работа модели
    X_train,X_test, y_train, y_test = train_test_split(C.drop('ARRIVAL_DELAY',axis=1),
                                                        C.ARRIVAL_DELAY,
                                                        shuffle = False,# временной ряд, отключаем перемешивание
                                                        test_size = 0.25)

    

    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    print('Ошибка на обучающей выборке', (mean_squared_error(y_train, dtc.predict(X_train)))**0.5)
    pred = dtc.predict(X_test)
    print('Ошибка на тесте', (mean_squared_error(y_test, pred))**0.5)
    '''
    st.code(code, language='python')


    y_test = y_test.reset_index()
    y_test['PRED'] = list(pred)
    y_test = y_test.set_index('DATE_HOUR')
    X_test['ARRIVAL_DELAY'] = y_test['ARRIVAL_DELAY']
    X_test['PRED'] = y_test['PRED']

    st.text(a_list)
    for column in a_list:
        X_test['{}'.format(column)] = le.inverse_transform(X_test['{}'.format(column)])


    code = '''
    Декодирую данные в строки
    for column in a_list:
        X_test['{}'.format(column)] = le.inverse_transform(X_test['{}'.format(column)])
    '''
    st.code(code, language='python')



    X_test['PROBABILITY'] = np.where(X_test['ARRIVAL_DELAY']>0, 0, 1)
    X_test['PROBABILITY_PRED'] = np.where(X_test['PRED']>0, 0, 1)
    X_test = X_test.reset_index()
    X_test['MSE'] = (X_test['PRED'] - X_test['ARRIVAL_DELAY'])**2
    A = X_test.groupby('DESTINATION_AIRPORT')['ARRIVAL_DELAY'].count().reset_index().rename(columns={'ARRIVAL_DELAY':'COUNT'})
    X_test = X_test.merge(A, how='left', left_on='DESTINATION_AIRPORT', right_on='DESTINATION_AIRPORT' )
    

    X_test = X_test.groupby('DESTINATION_AIRPORT').mean()
    X_test['RMSE'] = round(np.sqrt(X_test['MSE']),0)
    X_test = X_test.query("COUNT > 60")[['ARRIVAL_DELAY', 'PRED',  'PROBABILITY', 'PROBABILITY_PRED', 'RMSE', 'COUNT']]
  
    X_test = X_test.sort_values(by=['RMSE','ARRIVAL_DELAY'],ascending=[True, True])
    st.dataframe(X_test)

    fig = px.bar(X_test,y=['PROBABILITY', 'PROBABILITY_PRED'], barmode = 'group', title='Сравнение вероятностей положительного исхода')
    fig.show()
    st.plotly_chart(fig, use_container_width=True)


    fig = px.bar(X_test,y=['ARRIVAL_DELAY', 'PRED'], barmode = 'group', title='Сравнение задержки вылета')
    fig.show()
    st.plotly_chart(fig, use_container_width=True)

    X_test = X_test.reset_index().head(3)


    t = {'DESTINATION_AIRPORT':'{}'.format(airport), 'ARRIVAL_DELAY':0, 'PRED':0,  'PROBABILITY':0, 'PROBABILITY_PRED':0, 'RMSE':50, 'COUNT':0}
    X_test = X_test.append(t, ignore_index=True)

    X_test = X_test.reset_index().merge(b, how='left', left_on='DESTINATION_AIRPORT', right_on='IATA_CODE')


    fig = px.scatter_mapbox(X_test,
                    lon = X_test.LONGITUDE,
                    lat = X_test.LATITUDE,
                    zoom = 2,
                    color = X_test.RMSE,
                    size = X_test.RMSE ,
                    hover_name="DESTINATION_AIRPORT",
                    width = 800,
                    height = 600,
                    title='Лучшие направления вылета'
                                )
    fig.update_layout(mapbox_style='open-street-map')
    fig.show()
    st.plotly_chart(fig)





# wisout Q13







    C_1.drop(['PROBABILITY'], axis=1, inplace=True)

    #формирую выборки - обучающую и тестовую
    X_train,X_test, y_train, y_test = train_test_split(C_1.drop('ARRIVAL_DELAY',axis=1),
                                                        C_1.ARRIVAL_DELAY,
                                                        shuffle = False,# временной ряд, отключаем перемешивание
                                                        test_size = 0.25)

    

    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    print('Ошибка на обучающей выборке', (mean_squared_error(y_train, dtc.predict(X_train)))**0.5)
    pred = dtc.predict(X_test)
    print('Ошибка на тесте', (mean_squared_error(y_test, pred))**0.5)

  


    y_test = y_test.reset_index()
    y_test['PRED'] = list(pred)
    y_test = y_test.set_index('DATE_HOUR')
    X_test['ARRIVAL_DELAY'] = y_test['ARRIVAL_DELAY']
    X_test['PRED'] = y_test['PRED']

    st.text(a_list)
    for column in a_list:
        X_test['{}'.format(column)] = le.inverse_transform(X_test['{}'.format(column)])




    X_test['PROBABILITY'] = np.where(X_test['ARRIVAL_DELAY']>0, 0, 1)
    X_test['PROBABILITY_PRED'] = np.where(X_test['PRED']>0, 0, 1)
    X_test = X_test.reset_index()
    X_test['MSE'] = (X_test['PRED'] - X_test['ARRIVAL_DELAY'])**2
    A = X_test.groupby('DESTINATION_AIRPORT')['ARRIVAL_DELAY'].count().reset_index().rename(columns={'ARRIVAL_DELAY':'COUNT'})
    X_test = X_test.merge(A, how='left', left_on='DESTINATION_AIRPORT', right_on='DESTINATION_AIRPORT' )
    

    X_test = X_test.groupby('DESTINATION_AIRPORT').mean()
    X_test['RMSE'] = round(np.sqrt(X_test['MSE']),0)
    X_test = X_test.query("COUNT > 60")[['ARRIVAL_DELAY', 'PRED',  'PROBABILITY', 'PROBABILITY_PRED', 'RMSE', 'COUNT']]
  
    X_test = X_test.sort_values(by=['RMSE','ARRIVAL_DELAY'],ascending=[True, True])
    st.dataframe(X_test)

    fig = px.bar(X_test,y=['PROBABILITY', 'PROBABILITY_PRED'], barmode = 'group', title='Сравнение вероятностей положительного исхода')
    fig.show()
    st.plotly_chart(fig, use_container_width=True)


    fig = px.bar(X_test,y=['ARRIVAL_DELAY', 'PRED'], barmode = 'group', title='Сравнение задержки вылета')
    fig.show()
    st.plotly_chart(fig, use_container_width=True)

    X_test = X_test.reset_index().head(3)


    t = {'DESTINATION_AIRPORT':'{}'.format(airport), 'ARRIVAL_DELAY':0, 'PRED':0,  'PROBABILITY':0, 'PROBABILITY_PRED':0, 'RMSE':50, 'COUNT':0}
    X_test = X_test.append(t, ignore_index=True)

    X_test = X_test.reset_index().merge(b, how='left', left_on='DESTINATION_AIRPORT', right_on='IATA_CODE')


    fig = px.scatter_mapbox(X_test,
                    lon = X_test.LONGITUDE,
                    lat = X_test.LATITUDE,
                    zoom = 2,
                    color = X_test.RMSE,
                    size = X_test.RMSE ,
                    hover_name="DESTINATION_AIRPORT",
                    width = 800,
                    height = 600,
                    title='Лучшие направления вылета'
                                )
    fig.update_layout(mapbox_style='open-street-map')
    fig.show()
    st.plotly_chart(fig)

