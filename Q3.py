# "INFY.NS": 15, 
# "TCS.NS": 10, 
# "RELIANCE.NS": 12

import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.pyplot import style

style.use('ggplot')

data1 = yf.download('INFY.NS',period='1mo',interval='1d')
data2 = data = yf.download('TCS.NS',period='1mo',interval='1d')
data3 = data = yf.download('RELIANCE.NS',period='1mo',interval='1d')


df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)

df1.dropna(inplace=True)
df2.dropna(inplace=True)
df3.dropna(inplace=True)

df1['Dates'] = data1.index
df1['Total_price'] = df1['Close']*15
df2['Total_price'] = df2['Close']*10
df3['Total_price'] = df3['Close']*12

df1['Total_portfolio value'] = df1['Total_price'] + df2['Total_price'] + df3['Total_price']

fig,ax = plt.subplots()
ax.plot(df1['Dates'],df1['Total_portfolio value'],color = 'blue', label = 'Total portfolio value')
plt.xlabel('Dates')
plt.ylabel('Total porfolio value')
locator = mdates.AutoDateLocator(maxticks=10)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter( mdates.DateFormatter('%d-%m-%Y'))
fig.autofmt_xdate()
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()

print(df1['Total_portfolio value'].iloc[-1])

plt.show()


