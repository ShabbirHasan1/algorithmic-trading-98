# Historical Equity Data Fetcher (via KITE API)

A Python script to fetch historical equity data from Zerodha Kite API for multiple stock symbols.

## Overview

This script downloads daily OHLCV (Open, High, Low, Close, Volume) data for Indian stocks using Zerodha's unofficial Kite API. It processes symbols from a CSV file and saves individual files for each stock.

## Features

- **Batch Processing**: Fetches data for up to 2000 symbols
- **Resume Capability**: Skips existing files to continue interrupted downloads
- **Rate Limit Handling**: Automatic retry with 5-second wait for 429 errors
- **Comprehensive Metrics**: Tracks success, failures, and performance statistics
- **Smart Chunking**: Fetches data in 60-day periods to avoid API limits
- **Error Recovery**: Restarts from beginning after rate limits

## Requirements

```python
pandas
requests
```

## Configuration

Update these constants in the script:

```python
ENCTOKEN = "your_kite_session_token"  # Update for each session
START_DATE = datetime(2015, 4, 1)     # Data start date
END_DATE = datetime(2025, 3, 31)      # Data end date
TIMEFRAME = "day"                     # Data timeframe
LIMIT = 2000                          # Max symbols to process
```

## Input File Format

Create `data/storage/tokens.csv` with:
```csv
SYMBOL,KITE_ID
RELIANCE,738561
TCS,2953217
INFY,408065
```

## Output Structure

```
data/storage/raw/equity/zerodha/2015-2025/day/
├── 0001_RELIANCE.csv
├── 0002_TCS.csv
└── 0003_INFY.csv
```

## Usage

### Command Line
```bash
python hd-equity.py
```

### Programmatic
```python
from hd_equity import fetch_equity_data
fetch_equity_data()
```

## Data Format

Each CSV file contains:
- **Date**: Timestamp with timezone
- **Open**: Opening price
- **High**: Highest price
- **Low**: Lowest price
- **Close**: Closing price
- **Volume**: Trading volume

## Error Handling

### Rate Limiting (429)
- Waits 5 seconds and restarts from beginning
- Tracked in metrics

### API Errors
- Logs error code and response
- Skips to next symbol

### Insufficient Data
- Requires >10 rows to save file
- Tracked separately in metrics

## Performance Features

### Rate Limiting Protection
- 1-second delay between symbols
- 3-second delay every 10 successful downloads
- 5-second wait on rate limits

### Metrics Tracking
```
==================================================
PROCESSING SUMMARY
==================================================
Total symbols in CSV: 150
Symbols processed: 45
Successfully fetched: 40
Skipped (existing files): 90
Insufficient data: 3
Rate limited requests: 2
API errors: 0
JSON parsing errors: 0
Processing time: 125.50 seconds
Average time per symbol: 2.79 seconds
==================================================
```

## Getting ENCTOKEN

1. Login to [Kite Web](https://kite.zerodha.com)
2. Open browser developer tools (F12)
3. Go to Network tab
4. Look for any API request
5. Copy the `enctoken` value from request headers
6. Update the `ENCTOKEN` variable

**Note**: Token expires when you logout or session times out.

## Timeframe Options

Available timeframes:
- `minute` - 1-minute candles
- `5minute` - 5-minute candles
- `30minute` - 30-minute candles
- `60minute` - 1-hour candles
- `3hour` - 3-hour candles
- `day` - Daily candles

## Limitations

- **Unofficial API**: Uses web session token, not official API
- **Session Dependent**: Token must be updated regularly
- **Rate Limited**: Zerodha enforces request limits
- **Data Availability**: Historical data varies by symbol

## Troubleshooting

### Common Issues

**"File not found: tokens.csv"**
- Ensure `data/storage/tokens.csv` exists with correct format

**High API errors**
- Check if ENCTOKEN is valid and not expired
- Verify internet connection

**Rate limiting**
- Normal behavior, script handles automatically
- Consider reducing LIMIT if excessive

### Performance Tips

- Run during off-market hours for better API response
- Use smaller LIMIT values for testing
- Monitor metrics for optimization opportunities

## Best Practices

1. **Token Management**: Update ENCTOKEN regularly
2. **Incremental Updates**: Use resume capability for large datasets
3. **Monitoring**: Check metrics for failed downloads
4. **Backup**: Keep backups before running full updates

## File Naming Convention

Files are named as `XXXX_SYMBOL.csv` where:
- `XXXX`: 4-digit zero-padded sequence number (0001, 0002, etc.)
- `SYMBOL`: Stock symbol from input CSV

This ensures consistent ordering and easy identification of files.
