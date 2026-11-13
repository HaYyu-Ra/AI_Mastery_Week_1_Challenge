# Analysis Methodology

## Stock data preparation
The pipeline checks required columns, parses dates, converts numeric fields, removes invalid adjusted-close records, sorts chronologically, and removes duplicate dates. Adjusted Close is used for return and technical-indicator calculations.

## Quantitative indicators
- Simple daily return: (P_t/P_{t-1}-1).
- Log return: (ln(P_t/P_{t-1})).
- SMA: rolling arithmetic mean over 20 and 50 trading observations.
- EMA: exponentially weighted moving averages with spans 12 and 26.
- MACD: EMA(12) minus EMA(26); signal is EMA(9) of MACD.
- RSI(14): exponentially smoothed gains and losses over 14 observations.
- Bollinger Bands: SMA(20) plus/minus two rolling standard deviations.
- Annualized volatility: standard deviation of daily returns multiplied by (sqrt{252}).
- Drawdown: adjusted close divided by its running maximum, minus one.
- CAGR: annualized compound growth over the observed sample interval.

## News processing
Headline polarity is calculated using TextBlob as a transparent baseline sentiment model. Labels use polarity thresholds of +0.05 and -0.05. Publisher counts, daily/hourly article counts, headline length, sentiment distributions, frequent terms, and topic modelling can be generated once the actual news corpus is uploaded.

## Correlation
Sentiment is averaged per ticker and calendar date and joined to daily stock returns. Pearson measures linear association; Spearman measures rank association. Both p-values are reported when there are at least three matched observations and both series vary. Same-day association is descriptive, not causal, and may be affected by publication timing and look-ahead bias. For stronger analysis, test next-session and lagged sentiment and account for market/sector returns.

## Interpretation and limitations
The AAPL and AMZN price samples have different start dates, and the observed period ends 2024-07-30. Historical volatility and drawdown comparisons are descriptive and do not establish future performance. TextBlob is not a finance-specific language model. This project is for educational research and is not investment advice.
