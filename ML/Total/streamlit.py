import streamlit as st
import pandas as pd
import os
import pickle
import datetime
from neuralprophet import NeuralProphet

df = pd.read_csv('flights_2.csv') # здесь нужен датасет из блокнота total.ipynb
#st.write(df)


#функция для определения периода прогноза исходя из пользовательского ввода
def get_period():
    a = (d - datetime.date(2015, 9, 30)).days
    period = int(a % 365.25)
    return period

  #функция для получения датафрейма для модели  
def get_B():
    A = df.query(f"ORIGIN_AIRPORT == '{airport}'")
    B = A.groupby('Date')['PROBABILITY'].mean().reset_index()
    B.columns = ['ds', 'y']
    return B

# функция для выбора необходимого списка аэропортов прилета, исходя из заданного значения метрики
def change_DESTANATION_AIRPORT():
    os.chdir('/Users/andrejmironov/Documents/study_for_github/ML/Total')#нужно указать путь к текущему каталогу
    os.chdir('{}'.format(airport))
    with open('metrix.pkl', 'rb') as f:
        metrix = pickle.load(f)
    return list(metrix.query("rsme < 0.20")['name'])
    

#функция для предсказанния
def get_best():
    total = pd.DataFrame()
    os.chdir('{}'.format(airport))      
    for airport_1 in change_DESTANATION_AIRPORT():
        with open('{}'.format(airport_1)+'.pkl', 'rb') as f:
            m = pickle.load(f)
        future = m.make_future_dataframe(B, periods=period)
        forecast = m.predict(future)
        probability = float(forecast.yhat1[-1:])
        t = {'name':'{}'.format(airport_1), 'probability':probability}
        total = total.append(t, ignore_index=True)
    os.chdir('/Users/andrejmironov/Documents/study_for_github/ML/Total') #указать текущую директорию
    return total.sort_values(by='probability', ascending=False).head(3)



#пользовательский ввод аэропорта вылета (в примере 5 аэропортов ATL, DEN, DFW, LAX, ORD)
airport = st.text_input(label="airport")

# дата на котрую нужен прогноз, пользовательский ввод, пока можно выбрать октябрь
d = st.date_input(label="When?")

period = get_period()


# вывод аэропортов прилета
if st.button('GO!'):
    B = get_B()
    st.write(get_best())
    os.chdir('/Users/andrejmironov/Documents/study_for_github/ML/Total')


#print(period)

#st.line_chart(A)

