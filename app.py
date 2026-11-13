import tempfile
import pandas as pd
import streamlit as st
import plotly.express as px
from src.analysis import load_stock,add_technical_indicators,financial_summary,load_news,news_eda,correlate_news_stock
st.set_page_config(page_title="Nova Financial Insights",page_icon="📈",layout="wide")
st.title("📈 Nova Financial Insights")
st.caption("10 Academy Week 1 | Historical stock analytics and financial-news sentiment")
st.info("Historical price data only. Supplied files end 2024-07-30; this is not live market data.")
uploads=st.sidebar.file_uploader("Upload AAPL/AMZN price CSV files",type="csv",accept_multiple_files=True)
if not uploads: st.warning("Upload one or both historical stock CSVs to begin."); st.stop()
frames={}
for u in uploads:
 t=u.name.split("_")[0].upper()
 if t not in {"AAPL","AMZN"}: continue
 with tempfile.NamedTemporaryFile(suffix=".csv") as f:
  f.write(u.getvalue()); f.flush(); frames[t]=add_technical_indicators(load_stock(f.name,t))
if not frames: st.error("No supported AAPL or AMZN file was uploaded."); st.stop()
ticker=st.sidebar.selectbox("Ticker",list(frames)); full=frames[ticker]
start,end=st.sidebar.date_input("Date range",value=(full.Date.min().date(),full.Date.max().date()),min_value=full.Date.min().date(),max_value=full.Date.max().date())
df=full[(full.Date.dt.date>=start)&(full.Date.dt.date<=end)]
if df.empty: st.warning("No data in selected range."); st.stop()
s=financial_summary(df); a,b,c,d=st.columns(4)
a.metric("Observations",f"{s['observations']:,}"); b.metric("Total return",f"{s['total_return_pct']:.2f}%"); c.metric("Annualized volatility",f"{s['annualized_volatility_pct']:.2f}%"); d.metric("Max drawdown",f"{s['max_drawdown_pct']:.2f}%")
p,r,n=st.tabs(["Price & indicators","Returns & risk","News analysis"])
with p:
 st.plotly_chart(px.line(df,x="Date",y=["Adj Close","SMA_20","SMA_50"]),use_container_width=True)
 st.plotly_chart(px.line(df,x="Date",y="RSI_14"),use_container_width=True)
 st.plotly_chart(px.line(df,x="Date",y=["MACD","MACD_Signal"]),use_container_width=True)
with r:
 st.plotly_chart(px.line(df,x="Date",y="Daily_Return_Pct"),use_container_width=True)
 st.plotly_chart(px.line(df,x="Date",y="Drawdown"),use_container_width=True)
 st.dataframe(pd.DataFrame([s]),use_container_width=True)
with n:
 nf=st.file_uploader("Optional FNSPID news CSV",type="csv")
 if nf:
  with tempfile.NamedTemporaryFile(suffix=".csv") as f:
   f.write(nf.getvalue()); f.flush(); news=load_news(f.name)
  news=news[(news.Ticker==ticker)&(news.Date>=pd.Timestamp(start))&(news.Date<=pd.Timestamp(end))]
  st.metric("Headlines",len(news))
  if len(news):
   st.plotly_chart(px.histogram(news,x="Sentiment",nbins=40),use_container_width=True)
   st.dataframe(news_eda(news)["publishers"])
   merged,result=correlate_news_stock(news,df); st.json(result)
   if len(merged): st.plotly_chart(px.scatter(merged,x="Mean_Sentiment",y="Daily_Return",size="Article_Count"),use_container_width=True)
  else: st.info("No matching headlines.")
 else: st.info("Upload the actual news CSV to calculate publisher/time EDA, sentiment, topics and correlations. No news results are fabricated.")
