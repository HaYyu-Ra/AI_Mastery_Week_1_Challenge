# Data Dictionary

## Historical stock-price files
Expected files: `AAPL_historical_data.csv` and `AMZN_historical_data.csv`.

| Field | Meaning | Use |
|---|---|---|
| Date | Trading date | Time-series index and news alignment |
| Open | Opening price | OHLC analysis |
| High | Highest price | OHLC analysis |
| Low | Lowest price | OHLC analysis |
| Close | Closing price | Price analysis |
| Adj Close | Adjusted closing price | Return and indicator calculations |
| Volume | Traded share volume | Liquidity/volume analysis |
| Dividends | Dividend distribution, if supplied | Corporate-action context |
| Stock Splits | Split ratio, if supplied | Corporate-action context |

The stock loader requires Date, Open, High, Low, Close, Adj Close, and Volume. Additional columns are retained if present. Dates are parsed, invalid required observations removed, and duplicate dates reduced to the last observation.

## Optional financial-news dataset
The news loader accepts common column aliases:

| Canonical field | Accepted aliases | Meaning |
|---|---|---|
| Headline | headline, title | News headline text |
| Date | date, published_at, publication_date | Publication timestamp/date |
| Ticker | stock, ticker, symbol | Associated stock symbol |
| Publisher | publisher, author, source | News publisher/source |

Publisher is recommended for publisher analysis. The headline, date, and ticker fields are required for sentiment and stock alignment. The original FNSPID file was not included in the supplied files, so actual news-derived statistics cannot yet be computed.

## Data handling
- Keep the original source files unchanged.
- Do not commit licensed or restricted raw datasets to a public repository without permission.
- Record timestamp timezone assumptions before aligning news to market sessions.
- The provided historical price data ends on 2024-07-30; it is not live market data.
