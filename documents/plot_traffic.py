# -*- coding: utf-8 -*-
#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import dateutil

file = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/traffic/Wienzeile-271.csv'
col_list = ['Timestamp', 'JamFactor']
tick_spacing = 0.25

with open(file) as csvfile:
    df = pd.read_csv(file, usecols=col_list, delimiter=';')
    print(df['Timestamp'])
    df['Timestamp'] = df['Timestamp'].apply(dateutil.parser.parse)
    plt.title(file)
    plt.plot(df['Timestamp'],df['JamFactor'])
    plt.gcf().autofmt_xdate() 
    myFmt = mdates.DateFormatter('%x %H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    plt.xlabel('Time')
    plt.ylabel('Jam Factor')
    plt.show()