# Realized Volatility Analysis

## Overview
A comprehensive volatility analysis tool that calculates realized volatility patterns by analyzing historical price movements over specific time periods. The system identifies weekly volatility patterns and provides statistical insights for options trading strategies.

## Core Analysis Logic

### 1. Weekly Volatility Calculation
- **Period Definition**: Configurable start and end days (default: Friday to Thursday)
- **Absolute Change Measurement**: Calculates percentage price movement between period endpoints
- **Peak Movement Analysis**: Identifies maximum intraday volatility during each period
- **Historical Pattern Recognition**: Analyzes multi-year volatility trends

### 2. Statistical Metrics

#### Primary Measurements
- **Absolute Change Percentage**: Close-to-close movement over the defined period
- **Maximum Peak Change**: Highest intraday movement (high/low vs period start)
- **Minimum Peak Change**: Lowest volatility period (important for option selling)

#### Advanced Analytics
- **Percentile Analysis**: 20-bucket distribution of volatility outcomes
- **Yearly Breakdown**: Annual volatility pattern comparison
- **Monthly Seasonality**: Month-by-month volatility characteristics

### 3. Data Processing Pipeline

#### Input Requirements
```
- Historical OHLCV data in CSV format
- Date column in standard format
- Numeric price columns (Open, High, Low, Close)
- Volume data (optional)
```

#### Processing Steps
```
1. LOAD → Read historical price data from CSV files
2. CLEAN → Validate dates and numeric price data
3. CALCULATE → Compute weekly volatility metrics
4. ANALYZE → Generate percentile and seasonal statistics
5. EXPORT → Save comprehensive analysis to text file
```

### 4. Output Analysis

#### Volatility Statistics
- **Average Absolute Change**: Mean weekly price movement
- **Average Max Peak Change**: Mean maximum intraday volatility
- **Minimum Max Peak**: Lowest volatility period (risk assessment)

#### Percentile Distribution
- **Top 5%**: Extreme volatility events
- **75-95%**: High volatility periods
- **25-75%**: Normal volatility range
- **Bottom 25%**: Low volatility periods

#### Temporal Analysis
- **Yearly Trends**: Long-term volatility evolution
- **Monthly Seasonality**: Seasonal volatility patterns
- **Period Consistency**: Reliability of volatility estimates

## Trading Applications

### Options Strategy Development
- **Volatility Selling**: Identify low-volatility periods for premium collection
- **Volatility Buying**: Spot high-volatility opportunities for long options
- **Risk Management**: Use minimum peak changes for position sizing
- **Seasonal Strategies**: Exploit monthly volatility patterns

### Risk Assessment
- **Historical Context**: Compare current volatility to historical ranges
- **Worst-Case Scenarios**: Plan for extreme volatility events
- **Expected Ranges**: Set realistic profit/loss expectations
- **Position Sizing**: Scale trades based on volatility forecasts

## Configuration Parameters

### Time Period Settings
```python
START_DAY = "Friday"     # Period start day
END_DAY = "Thursday"     # Period end day
FILE_LIMIT = 2          # Number of files to process
```

### Data Source Configuration
```python
FOLDER_PATH = "data/storage/processed/equity/zerodha/2015/day"
OUTPUT_FOLDER = "backtestresults/volatility"
```

## Key Insights Generated

### Volatility Characteristics
- **Consistency Metrics**: How reliable are volatility estimates
- **Extreme Event Frequency**: Probability of large moves
- **Seasonal Patterns**: Monthly and yearly volatility cycles
- **Risk-Reward Profiles**: Expected vs maximum movements

### Statistical Validation
- **Sample Size Analysis**: Number of periods analyzed
- **Distribution Analysis**: Volatility outcome patterns
- **Trend Analysis**: Long-term volatility evolution
- **Outlier Identification**: Extreme volatility events

## Practical Applications

### Option Pricing Validation
- Compare realized volatility to implied volatility
- Identify mispriced options based on historical patterns
- Validate volatility forecasts against actual outcomes

### Portfolio Risk Management
- Set position limits based on historical volatility
- Plan for worst-case volatility scenarios
- Optimize entry/exit timing based on volatility cycles

### Strategy Development
- Design volatility-based trading strategies
- Backtest strategies using historical volatility data
- Optimize parameters based on volatility characteristics

---

*Quantifying market volatility for informed trading decisions*