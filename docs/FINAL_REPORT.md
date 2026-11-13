# Final Report — Nova Financial Insights

## Scope and data
The supplied AAPL price data has 10,998 observations from 1980-12-12 to 2024-07-30; AMZN has 6,846 from 1997-05-15 to 2024-07-30. The FNSPID news corpus was not included, so no empirical news findings are asserted.

## Task 1 — Data engineering and EDA
The stock loader validates required fields, parses dates, converts numeric columns, removes invalid/duplicate rows and sorts chronologically. The news loader accepts headline/date/ticker/publisher aliases and calculates sentiment, headline length, publisher counts, daily/hourly frequency and frequent terms. News statistics await the actual FNSPID file.

## Task 2 — Financial quantitative analysis
Calculations include simple/log returns, SMA(20/50), EMA(12/26), MACD(12,26,9), RSI(14), Bollinger Bands(20,2), rolling annualized volatility, drawdown, CAGR and return/risk summaries. pandas/numpy implementations avoid mandatory compiled TA-Lib. Historical annualized volatility: AAPL 44.28%, AMZN 56.24%. Maximum drawdown: AAPL -81.80%, AMZN -94.40%.

## Task 3 — News and stock correlation
With FNSPID, daily sentiment is aggregated by ticker/date and joined to same-date returns. Pearson/Spearman coefficients and p-values are computed when sample size and variation permit. No correlation results are claimed until real headlines are supplied. Same-day association is not causal and can introduce look-ahead bias; next-session and lagged tests are recommended.

## Task 4 — Dashboard and reporting
Streamlit app includes ticker/date selection, price and moving-average charts, RSI, MACD, returns, drawdown, risk metrics and optional news tab. Render config and CI tests are included.

## Limitations and recommendations
Price data ends 2024-07-30 and is not live. FNSPID is absent; sentiment/topic/correlation conclusions remain pending. Validate timezone and publication timing, test next-session returns, control for market/sector moves, use chronological out-of-sample tests and include transaction costs. Educational analysis only, not investment advice.
