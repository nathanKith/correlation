from django.db import models
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import floor
import math
from pandas_datareader import data as pdr
from datetime import timedelta
from scipy.stats import t
import datetime



def correleation(ticker1, ticker2):
    results = []

    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y")
    now = pd.to_datetime(now)

    start_date = now - timedelta(days=200)
    sample3 = pdr.get_data_yahoo(ticker1, start=start_date, end=now)
    sample3 = sample3.tail(100)
    sample4 = pdr.get_data_yahoo(ticker2, start=start_date, end=now)
    sample4 = sample4.tail(100)

    data = {'sample1': sample3['Close'], 'sample2': sample4['Close']}
    data = pd.DataFrame(data=data)

    data['change1'] = data['sample1'].pct_change() * 100
    data['change1'].fillna(0, inplace=True)

    data['change2'] = data['sample2'].pct_change() * 100
    data['change2'].fillna(0, inplace=True)


    def float_round(num, places=0, direction=floor):
        return direction(num * (10 ** places)) / float(10 ** places)


    data['change1'] = float_round(data['change1'], 2, round)
    data['change2'] = float_round(data['change2'], 2, round)

    results.append('Среднее значение по первой выборке ' + str(np.mean(data['change1'])))
    results.append('Среднее значение по второй выборке ' + str(np.mean(data['change2'])))

    def average(x):
        assert len(x) > 0
        return float(sum(x)) / len(x)


    def pearson_def(x, y):
        assert len(x) == len(y)
        n = len(x)
        assert n > 0
        avg_x = average(x)
        avg_y = average(y)
        diffprod = 0
        xdiff2 = 0
        ydiff2 = 0
        for idx in range(n):
            xdiff = x[idx] - avg_x
            ydiff = y[idx] - avg_y
            diffprod += xdiff * ydiff
            xdiff2 += xdiff * xdiff
            ydiff2 += ydiff * ydiff

        return diffprod / math.sqrt(xdiff2 * ydiff2)


    results.append('Значение корреляции по Пирсону ' + str(pearson_def(data['sample1'], data['sample2'])))

    data['sample1'].plot(figsize=(12, 4), x='sample1')
    data['sample2'].plot(figsize=(12, 4), x='sample2')
    plt.title('Распределение цены')
    plt.xlabel('день')
    plt.ylabel('Цена')
    #plt.show()

    t_crit = t.ppf(0.999, len(data['sample1']) + len(data['sample2']) - 2)
    t_nab = pearson_def(data['sample1'], data['sample2']) * math.sqrt((len(data['sample1']) + len(data['sample2']) - 2) / (
                1 - pearson_def(data['sample1'], data['sample2']) * pearson_def(data['sample1'], data['sample2'])))

    if t_nab < t_crit:
        results.append('Коэффициент значим')
    else:
        results.append('Коэффициент не значим')

    return results
