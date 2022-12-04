
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


code = '''
import pyspark.pandas as ps
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import concat_ws, to_date, desc


import os
os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"

spark = (SparkSession.builder
.master("local[*]")
.appName('Flight_delay')
.getOrCreate()
)

df = spark.read.csv('flights.csv',     
                    sep=',',
                    header=True)


df = df.withColumn('DATE', concat_ws("-", "YEAR", "MONTH", 'DAY')).withColumn('DATE', to_date('DATE'))

df.createOrReplaceTempView("insurance_df")
df2 = spark.sql(''
    SELECT * FROM(
    SELECT ORIGIN_AIRPORT as o, 
    sum(TAXI_OUT) as sum_out,
    count(TAXI_OUT) as count_out  
    FROM insurance_df 
    WHERE DATE BETWEEN '2015-01-01' AND '2015-09-30'
    GROUP BY ORIGIN_AIRPORT) AS OA
    INNER JOIN
    (SELECT
    DESTINATION_AIRPORT as d,
    sum(TAXI_IN) as sum_in, 
    count(TAXI_IN) as count_in
    FROM insurance_df 
    GROUP BY DESTINATION_AIRPORT)
    ON
    o=d
'')

df2 = df2.withColumn('PROB', (df2.sum_out + df2.count_out)/(df2.count_out + df2.count_in))
df2.sort(desc('PROB')).show()
    '''
st.code(code, language='python')

st.image('pyspark_img.png')


st.image('output.png', caption='Найти аэропорт, где самолёты проводят больше всего времени на рулении (среднее значение)')



