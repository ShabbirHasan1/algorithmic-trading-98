# Fundamentals Data Fetcher (screener.in)

A Python script to scrape fundamental financial data from Screener.in for multiple stock symbols.

## Overview

This script fetches comprehensive fundamental data including quarterly results, profit & loss statements, balance sheets, cash flows, ratios, and shareholding patterns for Indian stocks from Screener.in.

## Features

- **Dual Operation Modes**: Fetch new data (skip existing) or update all data
- **Rate Limiting Handling**: Automatic retry with 30-second wait for 429 errors
- **Smart Throttling**: 5-second wait after every 10 successful fetches
- **Comprehensive Statistics**: Tracks fetched, skipped, rate-limited, and failed requests
- **Structured Data Storage**: Saves data in vertical format with clear table identification
- **Error Resilience**: Handles network errors, missing files, and malformed data

## Requirements

```python
pandas
requests
beautifulsoup4
```

## File Structure

```
data/
├── storage/
│   ├── tokens.csv          # Input file with SYMBOL column
│   └── raw/
│       └── fundamentals/   # Output directory
│           ├── 0001_RELIANCE.csv
│           ├── 0002_TCS.csv
│           └── ...
```

## Data Tables Extracted

The script extracts 7 main financial tables:

1. **Quarterly Results** - Recent quarterly performance
2. **Profit & Loss** - Annual P&L statements
3. **Balance Sheet** - Annual balance sheet data
4. **Cash Flows** - Cash flow statements
5. **Ratios** - Financial ratios and metrics
6. **Shareholding Pattern - Quarterly** - Recent shareholding changes
7. **Shareholding Pattern - Yearly** - Annual shareholding data

## Usage

### Command Line Execution

```bash
python hd_fundamentals.py
```

### Interactive Menu

```
Choose an option:
1. Fetch new data (skip existing files)
2. Update all data (fetch everything)
Enter your choice (1 or 2): 1
```

### Function Usage

```python
from hd_fundamentals import fetch_new_data, update_all_data

# Fetch only new data (recommended for regular updates)
fetch_new_data()

# Update all data (full refresh)
update_all_data()
```

## Output Format

Each CSV file contains vertically stacked tables:

```csv
Quarterly Results,,,
Mar 2024,Dec 2023,Sep 2023,Jun 2023
Sales,50000,48000,45000,42000
Net Profit,8000,7500,7200,6800
,,,
Profit & Loss,,,
Mar 2024,Mar 2023,Mar 2022,Mar 2021
Total Income,200000,180000,160000,140000
Total Expenses,180000,162000,144000,126000
,,,
```

## Configuration

### Input File Format

`data/storage/tokens.csv` must contain:
```csv
SYMBOL
RELIANCE
TCS
INFY
HDFCBANK
```

### Output Naming Convention

Files are saved as: `XXXX_SYMBOL.csv`
- `XXXX`: 4-digit zero-padded number (0001, 0002, etc.)
- `SYMBOL`: Stock symbol from input file

## Error Handling

### Rate Limiting (429 Errors)
- Automatic 30-second wait
- Single retry attempt
- Tracked in statistics

### Network Errors
- Immediate failure for non-429 HTTP errors
- Logged and counted in statistics

### File System Errors
- Creates output directories automatically
- Handles missing input files gracefully

## Performance Features

### Smart Waiting
- Only waits after successful fetches, not skipped files
- 5-second pause every 10 successful downloads
- Prevents overwhelming the server

### Statistics Tracking
```
=== SUMMARY ===
Total symbols processed: 150
Files fetched: 45
Files skipped: 90
Rate limited: 3
Failed to fetch: 12
```

## Functions Reference

### `fetch_fundamentals_data(symbol, file_number, skip_existing=True, stats=None)`
Core function to fetch data for a single symbol.

**Parameters:**
- `symbol`: Stock symbol to fetch
- `file_number`: Sequential number for filename
- `skip_existing`: Skip if file already exists
- `stats`: Dictionary to track statistics

**Returns:** `True` if successful, `False` otherwise

### `fetch_new_data()`
Fetches data for all symbols, skipping existing files.

### `update_all_data()`
Fetches data for all symbols, including existing files.

### `main()`
Interactive menu for user selection.

## Best Practices

1. **Regular Updates**: Use option 1 (fetch missing stocks data) to continue fetching the data in multiple go's
2. **Full Refresh**: Use option 2 (update all data) when new quarter results are announced
3. **Monitor Statistics**: Check summary for failed fetches and investigate
4. **Backup Data**: Keep backups before running full updates

## Troubleshooting

### Common Issues

**"File not found: tokens.csv"**
- Ensure `data/storage/tokens.csv` exists with SYMBOL column

**"Column 'SYMBOL' not found"**
- Check CSV file has correct header: `SYMBOL`

**High failure rate**
- Check internet connection
- Verify Screener.in is accessible
- Consider increasing retry attempts

**Rate limiting**
- Normal behavior, script handles automatically
- High rate limiting may indicate server load

## Data Quality Notes

- Data reflects Screener.in's consolidated financial statements
- Historical data availability varies by company
- Some companies may have missing tables
- Data is scraped as-is without validation

## Maintenance

### Regular Tasks
- Monitor failed fetches in summary statistics
- Update symbol list in tokens.csv as needed
- Clean up old data files periodically
- Check for Screener.in website structure changes

### Updates Required If
- Screener.in changes table structure
- New financial tables are added
- CSS class names change (`data-table`)
- URL structure modifications
