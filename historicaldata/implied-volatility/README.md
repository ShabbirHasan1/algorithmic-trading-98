# 📈 NSE F&O Symbols - Historical Implied Volatility (IV) Fetcher

This Python script fetches:
- **Historical Implied Volatility (IV) data**  
for a list of NSE F&O symbols using the **Sensibull API**.

Additionally, it also retrieves (as supplementary data):
- **Near-expiry futures OHLC (Open, High, Low, Close) data**  
(because the API provides it together with IV).

The script processes the data and saves a clean CSV file for each symbol, including calculated:
- **IV Rank**  
- **IV Percentile**

---

## 🚀 Key Features

- Fetch **historical Implied Volatility** for NSE F&O symbols.
- Dynamically calculate **IV Rank** using historical data.
- Dynamically calculate **IV Percentile** based on past IV values.
- Saves **organized** CSV files for each symbol separately.
- Also includes **Near-Expiry Futures OHLC** data (optional, supplementary).
- Designed to **avoid lookahead bias** using expanding windows.

---

## 🛠️ Requirements

- Python 3.7+
- Libraries:
  - `requests`
  - `pandas`
  - `os`
  - `json`

Install the required libraries using:

```bash
pip install pandas requests
