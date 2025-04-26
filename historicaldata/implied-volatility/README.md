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
```

---

## 📂 Folder Structure

```
project/
├── nse_fno_tickers.csv      # Input CSV containing symbol names (already provided)
├── fetch_iv_data.py         # Main script
└── historicaldata/
    └── implied-volatility/
        ├── SYMBOL1.csv      # Output CSV for SYMBOL1
        ├── SYMBOL2.csv      # Output CSV for SYMBOL2
        └── ...
```

---

## 📜 How to Use

1. **Download the repo** (or clone it):
   
   The file `nse_fno_tickers.csv` is **already included** — no need to create it manually.

2. **Run the script**:

```bash
python fetch_iv_data.py
```

3. **Check the output**:  
   Processed CSV files will be saved in the `historicaldata/implied-volatility/` folder.

---

## 🧠 Important Notes

- 📌 The **primary objective** of this script is to fetch **Historical Implied Volatility (IV)**.
- 📌 **OHLC data** (for near-expiry futures) is fetched because it is part of the API response but is **not the main focus**.
- 📌 **IV Rank** and **IV Percentile** are computed using only available historical data at each point (to **avoid lookahead bias**).
- 📌 If any symbol's data cannot be fetched (API error), it will be skipped with an appropriate message.
- 📌 The script automatically creates the output folder if it does not already exist.

---

## 📊 Sample Output CSV Columns

| Date       | Open   | High   | Low    | Close  | IV    | Rank | IV Percentile |
|------------|--------|--------|--------|--------|-------|------|---------------|
| 2024-01-01 | 2520.0 | 2550.0 | 2500.0 | 2530.0 | 23.50 | 1    | 100.0         |
| 2024-01-02 | 2530.0 | 2560.0 | 2510.0 | 2550.0 | 22.80 | 2    | 50.0          |
| ...        | ...    | ...    | ...    | ...    | ...   | ...  | ...           |

---

## 🏗️ Future Enhancements

- Add CLI (Command Line Interface) for passing custom arguments.
- Retry logic for failed API requests.
- Enhanced logging and error tracking.

---

## 🤝 Contributions

PRs, suggestions, and contributions are welcome!  
Feel free to fork this repo, improve it, and create a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

# 🔥 Happy Data Fetching!
