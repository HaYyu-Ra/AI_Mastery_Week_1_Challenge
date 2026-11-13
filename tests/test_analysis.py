import numpy as np,pandas as pd
from src.analysis import add_technical_indicators,financial_summary
def sample():
 d=pd.bdate_range("2023-01-01",periods=100); c=np.linspace(100,150,100)
 return pd.DataFrame({"Date":d,"Open":c,"High":c+1,"Low":c-1,"Close":c,"Adj Close":c,"Volume":10000,"Ticker":"TEST"})
def test_indicators():
 x=add_technical_indicators(sample()); assert "RSI_14" in x and pd.isna(x.Daily_Return.iloc[0])
def test_summary():
 s=financial_summary(sample()); assert s["observations"]==100 and s["total_return_pct"]>0
