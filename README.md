# Nova Financial Insights — 10 Academy AI Mastery Week 1

Author: Hayyu Ragea Chewaka  
GitHub: https://github.com/HaYyu-Ra/AI_Mastery_Week_1_Challenge

A reproducible Streamlit analytics dashboard and Python pipeline for AAPL and AMZN historical prices, technical indicators, financial risk metrics, financial-news EDA, sentiment and statistical association testing.

## Run locally
```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

Upload historical stock CSVs through the dashboard sidebar. Required columns: Date, Open, High, Low, Close, Adj Close and Volume. The optional news CSV must include headline, date and stock/ticker columns; publisher is recommended.

## Four challenge tasks
1. Data engineering: validation, cleaning, date/publisher/time EDA, headline NLP, sentiment and optional LDA topic modeling.
2. Quantitative finance: returns, SMA/EMA, RSI, MACD, Bollinger Bands, rolling volatility and drawdown.
3. Correlation: daily sentiment aggregation, date alignment, Pearson/Spearman coefficients and p-values.
4. Dashboard/reporting: interactive Streamlit charts and reproducible analysis functions.

## Data limitation
The supplied stock files end 2024-07-30. The FNSPID news dataset was not included in the provided materials. News analysis is enabled but produces no empirical results until the actual CSV is uploaded. No synthetic news results are used.

## Deployment
Configured for Render using `render.yaml`. Deploy the `deployment` branch as a Python web service.

## Disclaimer
Educational analysis only, not investment advice. Same-day correlation is descriptive and does not establish causation or predictive power.
