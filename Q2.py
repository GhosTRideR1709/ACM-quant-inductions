import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import style
import numpy as np

style.use('ggplot')

data = yf.download('NVDA',period='6mo',interval='1d')
df = pd.DataFrame(data)



df['Daily_returns'] = df['Close'].pct_change()
df['Rolling_AVG_7'] = df['Daily_returns'].rolling(window=7).mean()
df['Rolling_STD_7'] = df['Daily_returns'].rolling(window=7).std()
df['Dates'] = data.index




fig,ax = plt.subplots()
ax.plot(df['Dates'],df['Daily_returns'],color = 'blue', label = 'Daily returns')
ax.plot(df['Dates'],df['Rolling_AVG_7'],color = 'red',label = 'Rolling average')
ax.plot(df['Dates'],df['Rolling_STD_7'],color = 'green',label = 'Rolling standard deviation')
plt.xlabel('Dates')
locator = mdates.AutoDateLocator(maxticks=10)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter( mdates.DateFormatter('%d-%m-%Y'))
fig.autofmt_xdate()
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()