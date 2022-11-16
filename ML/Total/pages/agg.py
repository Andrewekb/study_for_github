
import streamlit as st


st.header('1. Найти аэропорт с минимальной задержкой вылета ')
code = '''
a_1 = flights.groupby('AIRPORT')['DEPARTURE_DELAY'].sum().sort_values().head(1)
b_1 = flights.groupby('AIRPORT')['DEPARTURE_DELAY'].mean().sort_values().head(1)
st.write('Минимальная суммарная задержка рейса в аэропорте',a_1.index[0], 'составляет', round(a_1[0], 2), 'минут')
st.write('Минимальная средняя задержка вылета в аэропорте',b_1.index[0], 'составляет', round(b_1[0], 2), 'минут')'''

st.code(code, language='python')

st.text('''Минимальная суммарная задержка рейса в аэропорте 
Hilo International Airport составляет -4934.0 минут''')
st.text('''Минимальная средняя задержка вылета в аэропорте 
Yakutat Airport составляет -6.29 минут''')



st.header('2. Самая пунктуальная авиакомпания на прилет в Los Angeles International Airport')

st.text('Прибытие точно в срок(ARRIVAL_DELAY == 0)')

st.image('1.png', caption='Самая пунктуальная авиакомпания на прилет в Los Angeles International Airport')



st.text('Если подойти с точки зрения минимального отклонения к рейсу')

st.image('2.png', caption='Самая пунктуальная авиакомпания на прилет в Los Angeles International Airport')



st.header('3. Найти аэропорт, где самолёты проводят больше всего времени на рулении (среднее значение)')

st.image('output.png', caption='Найти аэропорт, где самолёты проводят больше всего времени на рулении (среднее значение)')



