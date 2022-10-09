# В процессе при установки streamlit сломался модуль prophet, поставить не получается

# Импортирую библиотеки
import streamlit as st
import yfinance as yf
import datetime
import pandas as pd

# Функция выгружает данные, преобразует в нужный формат, параметр capusta задается нажатием кнопки
#27 строка
def get_data(capusta):
    end_365 = datetime.date.today() + datetime.timedelta(days=1)
    start_365 = end_365 - datetime.timedelta(days=period)
    data = yf.download(capusta, start = start_365.isoformat(), end = end_365.isoformat())
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date']).dt.date.astype('datetime64[ns]')
    data = data[['Date', 'Close', 'Open']].set_index('Date')
    return data

# Задается количество дней
period = st.slider('Задайте период, дни', 30, 365)


#Информационна строка
st.text("Выберите валюту")


#Еcли выбрана кнопка евро df формируем с помощью ф-ии get_data
if st.button('Euro'):
    df = get_data("EURRUB=X")
    st.line_chart(data=df)

#Если доллар
if st.button('Dollar'):
    df = get_data("USDRUB=X")
    st.line_chart(data=df)



