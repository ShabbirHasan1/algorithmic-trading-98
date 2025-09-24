# Scalping Trading Bot

## Overview
This is an automated scalping bot that identifies short-term trading opportunities by analyzing real-time market depth data. The bot focuses on capturing small price movements with quick entry and exit strategies.

## Core Strategy Logic

### 1. Market Data Collection
- **Real-time Feed**: Connects to live market data via WebSocket
- **Market Depth**: Monitors 5 levels of buy/sell order book data
- **Key Metrics Tracked**:
  - Last Traded Price (LTP)
  - Total Buy Quantity (TBQ) 
  - Total Sell Quantity (TSQ)
  - Buy/Sell quantities at 5 price levels

### 2. Signal Generation Algorithm

#### Buy Signal Conditions
- **Buy Pressure**: 70-95% of total volume is on buy side
- **Order Book Dominance**: Top 5 buy levels have 1.5x more quantity than sell levels
- **Logic**: Strong buying interest with deep support levels

#### Sell Signal Conditions  
- **Sell Pressure**: 70-95% of total volume is on sell side
- **Order Book Dominance**: Top 5 sell levels have 1.5x more quantity than buy levels
- **Logic**: Strong selling pressure with heavy resistance

#### Signal Strength Ranking
- Stocks are ranked by dominance percentage (highest first)
- Only the strongest signal is selected for trading
- If no clear signals exist, the analysis repeats

### 3. Risk Management

#### Position Sizing
- Fixed quantity of 1 share (for testing)
- Can be configured to use percentage of capital

#### Stop Loss Strategy
- **Stop Loss**: 0.25% of entry price
- **Take Profit**: 1% of entry price  
- **Risk-Reward Ratio**: 1:4 (risking 0.25% to make 1%)

#### Trade Limits
- Maximum trades per day to prevent overtrading
- Automatic position monitoring and management

### 4. Execution Flow

#### Pre-Market Setup
1. Load filtered stock universe from CSV
2. Establish WebSocket connection
3. Subscribe to market depth data for all stocks
4. Wait for market open (9:15 AM)

#### Trading Loop
1. **Analyze**: Calculate buy/sell pressure for all stocks
2. **Rank**: Sort stocks by signal strength
3. **Select**: Choose the strongest signal
4. **Execute**: Place market order with stop-loss
5. **Monitor**: Track position until exit

#### Order Management
- **Entry**: Market orders for immediate execution
- **Exit**: Automatic stop-loss orders
- **Cleanup**: Unsubscribe from feeds after trade placement

### 5. Key Features

#### Market Depth Analysis
- Analyzes order flow imbalances
- Identifies institutional buying/selling pressure
- Uses multi-level order book data for confirmation

#### Real-time Processing
- Processes live market data continuously
- Instant signal generation and execution
- Sub-second response times

#### Automated Risk Control
- Pre-defined stop losses on every trade
- Daily trade limits
- Position size management

## Trading Philosophy

### Scalping Principles
- **Speed**: Capitalize on momentary price inefficiencies
- **Volume**: Focus on high-volume, liquid stocks
- **Momentum**: Trade in direction of dominant market pressure
- **Quick Exits**: Hold positions for minimal time

### Market Microstructure Edge
- **Order Flow**: Reads institutional buying/selling intentions
- **Depth Analysis**: Identifies support/resistance levels
- **Imbalance Detection**: Spots temporary supply/demand mismatches

## Risk Considerations

### Market Risks
- High-frequency trading requires stable internet connection
- Market volatility can cause rapid losses
- Slippage on market orders during volatile periods

### Technical Risks
- WebSocket connection failures
- API rate limits or downtime
- Data feed delays or errors

### Operational Limits
- Designed for liquid, high-volume stocks only
- Requires continuous market monitoring
- Performance depends on execution speed

## Success Metrics
- **Win Rate**: Percentage of profitable trades
- **Risk-Reward**: Maintaining 1:4 ratio
- **Drawdown**: Maximum consecutive losses
- **Daily P&L**: Net profit/loss per trading session

## Configuration Notes
- Adjust `MAX_TRADES_PER_DAY` based on risk tolerance
- Modify stop-loss/take-profit percentages as needed
- Update stock universe based on liquidity requirements
- Fine-tune signal thresholds based on market conditions