from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

dow = pdr.get_data_yahoo("^DJI", "2000-01-04")
kospi = pdr.get_data_yahoo("^KS11", "2000-01-04")

import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))
plt.plot(dow.index, dow.Close, "r--", label="Dow Jones Industrial")
plt.plot(kospi.index, kospi.Close, "b", label="KOSPI")
plt.grid(True)
plt.legend(loc="best")
plt.show()
