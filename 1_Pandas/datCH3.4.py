from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt

yf.pdr_override()
sec = pdr.get_data_yahoo("005930.KS", start="2018-05-04")
msft = pdr.get_data_yahoo("MSFT", start="2018-05-04")

plt.plot(sec.index, sec.Close, "b", label="Samsung Electronics")
plt.plot(msft.index, msft.Close, "r--", label="Microsoft")
plt.legend(loc="best")
plt.show()
