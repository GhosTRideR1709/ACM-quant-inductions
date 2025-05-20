import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.pyplot import style
import datetime

def interpolate(x51,x52,y51,y52,y201,y202):
    m1 = (y51-y52)/(x51-x52)
    m2 = (y201-y202)/(x51-x52)

    c1 = y51-m1*x51
    c2 = y201-m2*x51

    x = (c2-c1)/(m1-m2)
    y = m1*x+c1



    return (x,y)


style.use('ggplot')

data = yf.download('NVDA',period='6mo',interval='1d')
df = pd.DataFrame(data)

df['Dates'] = data.index.map(lambda x:x.timestamp())



buy_price = []
buy_date = []
sell_price = []
sell_date = []

df['20_SMA'] = df['Close'].rolling(window=20).mean()
df['5_SMA'] = df['Close'].rolling(window=5).mean()



for i in range(1,len(df['20_SMA'])-1):
    if df['5_SMA'].iloc[i]<df['20_SMA'].iloc[i] and df['5_SMA'].iloc[i+1]>df['20_SMA'].iloc[i+1]:
        buy_price.append(interpolate(df['Dates'].iloc[i],df['Dates'].iloc[i+1],df['5_SMA'].iloc[i],df['5_SMA'].iloc[i+1],df['20_SMA'].iloc[i],df['20_SMA'].iloc[i+1])[1])
        buy_date.append(datetime.datetime.fromtimestamp(interpolate(df['Dates'].iloc[i],df['Dates'].iloc[i+1],df['5_SMA'].iloc[i],df['5_SMA'].iloc[i+1],df['20_SMA'].iloc[i],df['20_SMA'].iloc[i+1])[0]))
    
    elif df['5_SMA'].iloc[i-1]<df['20_SMA'].iloc[i-1] and df['5_SMA'].iloc[i]>df['20_SMA'].iloc[i]:
        buy_price.append(interpolate(df['Dates'].iloc[i-1],df['Dates'].iloc[i],df['5_SMA'].iloc[i-1],df['5_SMA'].iloc[i],df['20_SMA'].iloc[i-1],df['20_SMA'].iloc[i])[1])
        buy_date.append(datetime.datetime.fromtimestamp(interpolate(df['Dates'].iloc[i-1],df['Dates'].iloc[i],df['5_SMA'].iloc[i-1],df['5_SMA'].iloc[i],df['20_SMA'].iloc[i-1],df['20_SMA'].iloc[i])[0]))
    
    elif df['5_SMA'].iloc[i-1]<df['20_SMA'].iloc[i-1] and df['5_SMA'].iloc[i+1]>df['20_SMA'].iloc[i+1] and df['5_SMA'].iloc[i]==df['20_SMA'].iloc[i]:
        buy_price.append(df['20_SMA'].iloc[i])
        buy_date.append(df['Dates'].iloc[i])
    
    elif df['5_SMA'].iloc[i]>df['20_SMA'].iloc[i] and df['5_SMA'].iloc[i+1]<df['20_SMA'].iloc[i+1]:
        sell_price.append(interpolate(df['Dates'].iloc[i],df['Dates'].iloc[i+1],df['5_SMA'].iloc[i],df['5_SMA'].iloc[i+1],df['20_SMA'].iloc[i],df['20_SMA'].iloc[i+1])[1])
        sell_date.append(datetime.datetime.fromtimestamp(interpolate(df['Dates'].iloc[i],df['Dates'].iloc[i+1],df['5_SMA'].iloc[i],df['5_SMA'].iloc[i+1],df['20_SMA'].iloc[i],df['20_SMA'].iloc[i+1])[0]))

    elif df['5_SMA'].iloc[i-1]>df['20_SMA'].iloc[i-1] and df['5_SMA'].iloc[i]<df['20_SMA'].iloc[i]:
        sell_price.append(interpolate(df['Dates'].iloc[i-1],df['Dates'].iloc[i],df['5_SMA'].iloc[i-1],df['5_SMA'].iloc[i],df['20_SMA'].iloc[i-1],df['20_SMA'].iloc[i])[1])
        sell_date.append(datetime.datetime.fromtimestamp(interpolate(df['Dates'].iloc[i-1],df['Dates'].iloc[i],df['5_SMA'].iloc[i-1],df['5_SMA'].iloc[i],df['20_SMA'].iloc[i-1],df['20_SMA'].iloc[i])[0]))
    
    elif df['5_SMA'].iloc[i-1]>df['20_SMA'].iloc[i-1] and df['5_SMA'].iloc[i+1]<df['20_SMA'].iloc[i+1] and df['5_SMA'].iloc[i]==df['20_SMA'].iloc[i]:
        sell_price.append(df['20_SMA'].iloc[i])
        sell_date.append(df['Dates'].iloc[i])



df['Dates'] = df['Dates'].map(lambda x:datetime.datetime.fromtimestamp(x))

fig,ax = plt.subplots()
#ax.plot(df['Dates'],df['Close'],color = 'black',label = 'Close price')
ax.scatter(buy_date,buy_price,color = 'green',label = 'buy points')
ax.scatter(sell_date,sell_price,color = 'red',label = 'sell points')
ax.plot(df['Dates'],df['20_SMA'],color = 'yellow',label = '20sma')
ax.plot(df['Dates'],df['5_SMA'],color = 'blue',label = '5sma')
plt.xlabel('Dates')
plt.legend()
locator = mdates.AutoDateLocator(maxticks=10)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter( mdates.DateFormatter('%d-%m-%Y'))
fig.autofmt_xdate()
plt.xticks(rotation=45)
plt.tight_layout()


plt.show()
