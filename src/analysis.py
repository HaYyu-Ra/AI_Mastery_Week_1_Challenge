import numpy as np,pandas as pd,re
from scipy.stats import pearsonr,spearmanr
REQ={"Date","Open","High","Low","Close","Adj Close","Volume"}
def load_stock(path,ticker=None):
 d=pd.read_csv(path)
 if REQ-set(d): raise ValueError(f"Missing columns: {sorted(REQ-set(d))}")
 d["Date"]=pd.to_datetime(d.Date,errors="coerce",utc=True).dt.tz_convert(None).dt.normalize()
 for c in REQ-{"Date"}: d[c]=pd.to_numeric(d[c],errors="coerce")
 d=d.dropna(subset=["Date","Adj Close"]).sort_values("Date").drop_duplicates("Date"); d=d[d["Adj Close"]>0].reset_index(drop=True); d["Ticker"]=(ticker or "UNKNOWN").upper()
 return d
def add_technical_indicators(d):
 x=d.copy().sort_values("Date").reset_index(drop=True); c=x["Adj Close"].astype(float)
 x["Daily_Return"]=c.pct_change(); x["Daily_Return_Pct"]=x.Daily_Return*100; x["Log_Return"]=np.log(c).diff()
 x["SMA_20"]=c.rolling(20).mean(); x["SMA_50"]=c.rolling(50).mean(); x["EMA_12"]=c.ewm(span=12,adjust=False).mean(); x["EMA_26"]=c.ewm(span=26,adjust=False).mean()
 x["MACD"]=x.EMA_12-x.EMA_26; x["MACD_Signal"]=x.MACD.ewm(span=9,adjust=False).mean()
 delta=c.diff(); g=delta.clip(lower=0).ewm(alpha=1/14,adjust=False,min_periods=14).mean(); l=(-delta.clip(upper=0)).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
 x["RSI_14"]=(100-100/(1+g/l.replace(0,np.nan))).mask((l==0)&(g>0),100).mask((g==0)&(l>0),0)
 x["Volatility_30D_Annualized"]=x.Daily_Return.rolling(30).std()*np.sqrt(252); x["Rolling_Max"]=c.cummax(); x["Drawdown"]=c/x.Rolling_Max-1
 x["Bollinger_Mid"]=x.SMA_20; sd=c.rolling(20).std(); x["Bollinger_Upper"]=x.SMA_20+2*sd; x["Bollinger_Lower"]=x.SMA_20-2*sd
 return x
def financial_summary(d):
 x=add_technical_indicators(d); r=x.Daily_Return.dropna(); years=max((x.Date.iloc[-1]-x.Date.iloc[0]).days/365.25,1/252); tr=x["Adj Close"].iloc[-1]/x["Adj Close"].iloc[0]-1; v=x.RSI_14.dropna()
 return {"ticker":str(x.Ticker.iloc[0]),"observations":len(x),"start_date":str(x.Date.min().date()),"end_date":str(x.Date.max().date()),"total_return_pct":float(tr*100),"cagr_pct":float(((1+tr)**(1/years)-1)*100),"mean_daily_return_pct":float(r.mean()*100),"daily_volatility_pct":float(r.std()*100),"annualized_volatility_pct":float(r.std()*np.sqrt(252)*100),"max_drawdown_pct":float(x.Drawdown.min()*100),"best_day_pct":float(r.max()*100),"worst_day_pct":float(r.min()*100),"average_volume":float(x.Volume.mean()),"latest_rsi_14":float(v.iloc[-1]) if len(v) else None}
def load_news(path):
 n=pd.read_csv(path); a={"headline":"Headline","title":"Headline","date":"Date","published_at":"Date","publication_date":"Date","stock":"Ticker","ticker":"Ticker","symbol":"Ticker","publisher":"Publisher","author":"Publisher","source":"Publisher"}
 n=n.rename(columns={c:a[c.strip().lower()] for c in n.columns if c.strip().lower() in a})
 if not {"Headline","Date","Ticker"}.issubset(n): raise ValueError("News CSV needs headline, date and stock/ticker columns")
 n["Headline"]=n.Headline.fillna("").astype(str); n["Date"]=pd.to_datetime(n.Date,errors="coerce",utc=True).dt.tz_convert(None).dt.normalize(); n=n.dropna(subset=["Date"]); n["Ticker"]=n.Ticker.astype(str).str.upper(); n=n[n.Headline.str.strip().ne("")].copy()
 from textblob import TextBlob
 n["Sentiment"]=n.Headline.map(lambda h:float(TextBlob(h).sentiment.polarity)); n["Sentiment_Label"]=np.select([n.Sentiment>.05,n.Sentiment<-.05],["positive","negative"],default="neutral"); n["Headline_Length"]=n.Headline.str.len(); n["Hour_UTC"]=n.Date.dt.hour
 if "Publisher" not in n:n["Publisher"]="Unknown"
 n["Publisher"]=n.Publisher.fillna("Unknown").astype(str)
 return n
def news_eda(n):
 t=re.findall(r"[a-z]{3,}"," ".join(n.Headline.str.lower())); terms=pd.Series(t).value_counts().head(30).rename_axis("Term").reset_index(name="Frequency")
 return {"descriptive":n[["Headline_Length","Sentiment"]].describe().reset_index(),"publishers":n.groupby("Publisher").agg(Article_Count=("Headline","size"),Mean_Sentiment=("Sentiment","mean")).sort_values("Article_Count",ascending=False).reset_index(),"daily_frequency":n.groupby("Date").size().rename("Article_Count").reset_index(),"hourly_frequency":n.groupby("Hour_UTC").size().rename("Article_Count").reset_index(),"sentiment_distribution":n.groupby(["Ticker","Sentiment_Label"]).size().rename("Article_Count").reset_index(),"top_terms":terms}
def correlate_news_stock(news,stock):
 t=str(stock.Ticker.iloc[0]).upper(); n=news[news.Ticker==t].groupby("Date",as_index=False).agg(Mean_Sentiment=("Sentiment","mean"),Article_Count=("Headline","size")); p=add_technical_indicators(stock)[["Date","Daily_Return"]]; m=p.merge(n,on="Date").dropna(); o={"ticker":t,"matched_days":len(m),"method":"same-day association only"}
 if len(m)>=3 and m.Mean_Sentiment.nunique()>1 and m.Daily_Return.nunique()>1:
  a=pearsonr(m.Mean_Sentiment,m.Daily_Return); b=spearmanr(m.Mean_Sentiment,m.Daily_Return); o.update(pearson_r=float(a.statistic),pearson_p=float(a.pvalue),spearman_rho=float(b.statistic),spearman_p=float(b.pvalue))
 else:o.update(pearson_r=None,pearson_p=None,spearman_rho=None,spearman_p=None)
 return m,o
