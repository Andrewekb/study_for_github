import streamlit as st


st.header('Модель (код)')



code = '''
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
            continue'''
st.code(code, language='python')