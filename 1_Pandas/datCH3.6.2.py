from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

dow = pdr.get_data_yahoo("^DJI", "2000-01-04")
kospi = pdr.get_data_yahoo("^KS11", "2000-01-04")

d = (dow.Close / dow.Close.loc["2000-01-04"]) * 100
k = (kospi.Close / kospi.Close.loc["2000-01-04"]) * 100

import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))
plt.plot(d.index, d, "r--", label="Dow Jones Industrial Average")
plt.plot(k.index, k, "b", label="KOSPI Average")
plt.grid(True)
plt.legend(loc="best")
plt.show()
