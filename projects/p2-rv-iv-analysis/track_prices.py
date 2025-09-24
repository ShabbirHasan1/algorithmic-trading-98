import os
import sys
import logging
import pandas as pd
import requests
import zipfile
import asyncio
from datetime import datetime
from time import sleep
from NorenRestApiPy.NorenApi import FeedType

# Add root directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from broker.shoonya.config import *
# import broker.shoonya.basicfunctions as bf
from telegram_bot import send_to_me

# Login to Shoonya API
logging.info("Logging into Shoonya API...")
try:
    limits = api.get_limits()
    logging.info(f"Login successful. Available cash: {limits.get('cash', 0)}")
except Exception as e:
    logging.error(f"Login failed: {e}")
    exit()

# Download and load symbol files
urls = {
    'NSE_symbols.txt': 'https://api.shoonya.com/NSE_symbols.txt.zip',
    'NFO_symbols.txt': 'https://api.shoonya.com/NFO_symbols.txt.zip',
    'BSE_symbols.txt': 'https://api.shoonya.com/BSE_symbols.txt.zip',
    'BFO_symbols.txt': 'https://api.shoonya.com/BFO_symbols.txt.zip'
}

# Download and extract symbol files
for filename, url in urls.items():
    try:
        if os.path.exists(filename):
            os.remove(filename)
        zip_filename = filename + '.zip'
        response = requests.get(url)
        with open(zip_filename, 'wb') as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall('.')
        os.remove(zip_filename)
    except PermissionError:
        logging.info(f"Could not overwrite {filename}, using existing file")

# Load symbol dataframes
try:
    nse_df = pd.read_csv('NSE_symbols.txt')
    nfo_df = pd.read_csv('NFO_symbols.txt')
    bse_df = pd.read_csv('BSE_symbols.txt')
    bfo_df = pd.read_csv('BFO_symbols.txt')
except PermissionError as e:
    logging.error(f"Cannot read symbol files: {e}. Please close any programs using these files.")
    exit()

logging.info(f"Loaded {len(nse_df)} NSE symbols, {len(nfo_df)} NFO symbols, {len(bse_df)} BSE symbols, {len(bfo_df)} BFO symbols")

print(nse_df.head())
print(nfo_df.head())
print(bse_df.head(20))
print(bfo_df.head())

# Filter NSE dataframe for INDEX instruments
index_df = nfo_df[nfo_df['Instrument'] == 'OPTIDX']
print("\nINDEX instruments:")
print(index_df)

# Filter for nearest expiry dates for each symbol
index_df['Expiry'] = pd.to_datetime(index_df['Expiry'], format='%d-%b-%Y')
nearest_expiry_df = index_df.loc[index_df.groupby('Symbol')['Expiry'].idxmin()]
print("\nNearest expiry for each symbol:")
print(nearest_expiry_df[['Symbol', 'TradingSymbol', 'Expiry']].drop_duplicates())

# Get unique symbols with exchange
unique_symbols = index_df[['Symbol', 'Exchange']].drop_duplicates()
print("\nUnique symbols with exchange:")
print(unique_symbols)

# Find token numbers from NSE symbols
index_tokens = nse_df[nse_df['Symbol'].isin(unique_symbols['Symbol'])][['Symbol', 'Token', 'Exchange']]
print("\nIndex tokens from NSE:")
print(index_tokens)

# # Print unique instruments in BSE dataframe
# print("\nUnique instruments in BSE:")
# print(bse_df['Instrument'].unique())
# # print(list(bse_df['Symbol'].unique()))

# print(bfo_df['Instrument'].unique())

# # Filter unique symbols with OPTIDX == Instrument in bfo_df
# bfo_idx = bfo_df[bfo_df['Instrument'] == 'OPTIDX']['Symbol'].unique()
# print("\nUnique OPTIDX symbols in BFO:")
# print(bfo_idx)

# # print(bfo_df['Instrument'].unique())


# Create dict of exchange and token from NSE INDEX instruments (excluding INDIAVIX)
index_nse = nse_df[(nse_df['Instrument'] == 'INDEX') & (nse_df['Symbol'] != 'INDIAVIX')]
index_dict = dict(zip(index_nse['Symbol'], zip(index_nse['Exchange'], index_nse['Token'])))
print("\nIndex dictionary (Symbol: [Exchange, Token]):")
print(index_dict)

# Create mapping between NSE index symbols and NFO option symbols
symbol_mapping = {
    'Nifty 50': 'NIFTY',
    'Nifty Bank': 'BANKNIFTY', 
    'Nifty Fin Services': 'FINNIFTY',
    'NIFTY MID SELECT': 'MIDCPNIFTY',
    'Nifty Next 50': 'NIFTYNXT50'
}
print("\nSymbol mapping:")
print(symbol_mapping)

# Fetch and display LTP for index symbols every 5 seconds
while datetime.datetime.now().strftime('%H:%M') < '17:51':
    print(f"\n{'Symbol':<25} {'Exchange':<10} {'Token':<10} {'LTP':<10} {'Time':<10}")
    print("-" * 60)
    
    for symbol, (exchange, token) in index_dict.items():
        if symbol != 'Nifty 50':
            continue
        try:
            ret = api.get_quotes(exchange=exchange, token=str(token))
            if ret and ret.get('stat') == 'Ok':
                ltp = ret.get('lp', '0.00')
                time_str = datetime.datetime.now().strftime('%H:%M:%S')
                print(f"{symbol:<25} {exchange:<10} {token:<10} {ltp:<10} {time_str:<10}")
                
                # Fetch option chain using current price as strike price
                try:
                    start_time = datetime.datetime.now()
                    # Get the NFO symbol for option chain
                    nfo_symbol = symbol_mapping.get(symbol, symbol)
                    print(f"    NFO Symbol: {nfo_symbol}")
                    print(f"    Symbol: {symbol}, ltp: {ltp}")
                    # Get trading symbol from nearest expiry data
                    trading_symbol_row = nearest_expiry_df[nearest_expiry_df['Symbol'] == nfo_symbol]
                    if not trading_symbol_row.empty:
                        trading_symbol = trading_symbol_row['TradingSymbol'].iloc[0]
                    else:
                        trading_symbol = nfo_symbol
                    rounded_strike = round(float(ltp) / 50) * 50
                    option_chain = api.get_option_chain(exchange='NFO', tradingsymbol=trading_symbol, strikeprice=rounded_strike, count=6)
                    if option_chain and option_chain.get('stat') == 'Ok':
                        print(f"\nOption chain for {symbol}:")
                        print(f"{'CALL':<15} {'Strike':<20} {'PUT':<15}")
                        print("-" * 40)
                        
                        # Group options by strike price
                        strikes = {}
                        for option in option_chain.get('values', []):
                            strike = option.get('strprc', '')
                            if strike not in strikes:
                                strikes[strike] = {'CE': '', 'PE': ''}
                            
                            try:
                                option_token = option.get('token', '')
                                option_exchange = option.get('exch', 'NFO')
                                option_price_ret = api.get_quotes(exchange=option_exchange, token=option_token)
                                option_price = option_price_ret.get('lp', '0.00') if option_price_ret and option_price_ret.get('stat') == 'Ok' else '0.00'
                                strikes[strike][option.get('optt', '')] = option_price
                            except Exception as e:
                                strikes[strike][option.get('optt', '')] = 'N/A'
                        
                        row_number = 0
                        # Display in screener format
                        for strike in sorted(strikes.keys(), key=lambda x: float(x) if x else 0):
                            row_number += 1
                            ce_price = strikes[strike].get('CE', '')
                            pe_price = strikes[strike].get('PE', '')
                            print(f"{row_number} {ce_price:<15} {strike:<20} {pe_price:<15}")

                        
                        # Calculate 0.5% above and below LTP for OTM options
                        ltp_float = float(ltp)
                        otm_ce_target = ltp_float * 1.005  # 0.5% above
                        otm_pe_target = ltp_float * 0.995  # 0.5% below
                        
                        # Find nearest strikes
                        otm_ce_strike = round(otm_ce_target / 50) * 50
                        otm_pe_strike = round(otm_pe_target / 50) * 50
                        
                        print(f"\nOTM Analysis (0.5% from LTP {ltp}):")
                        print(f"CE Target: {otm_ce_target:.2f} -> Strike: {otm_ce_strike}")
                        print(f"PE Target: {otm_pe_target:.2f} -> Strike: {otm_pe_strike}")
                        print(f"Available strikes: {list(strikes.keys())}")
                        print(f"Looking for CE: '{str(otm_ce_strike)}', PE: '{str(otm_pe_strike)}'")
                        
                        # Find costs from the strikes dictionary
                        ce_cost = strikes.get(f"{otm_ce_strike:.2f}", {}).get('CE', 'N/A')
                        pe_cost = strikes.get(f"{otm_pe_strike:.2f}", {}).get('PE', 'N/A')
                        
                        if ce_cost != 'N/A' and pe_cost != 'N/A':
                            try:
                                total_cost = float(ce_cost) + float(pe_cost)
                                message = f"\nLong Straddle Cost:\nCE {otm_ce_strike}: {ce_cost}\nPE {otm_pe_strike}: {pe_cost}\nTotal Cost: {total_cost:.2f}"
                                print(message)
                                asyncio.run(send_to_me(message))
                            except ValueError:
                                message = f"\nLong Straddle Cost:\nCE {otm_ce_strike}: {ce_cost}\nPE {otm_pe_strike}: {pe_cost}"
                                print(message)
                                asyncio.run(send_to_me(message))
                        else:
                            message = f"\nLong Straddle Cost:\nCE {otm_ce_strike}: {ce_cost}\nPE {otm_pe_strike}: {pe_cost}"
                            print(message)
                            asyncio.run(send_to_me(message))
                    else:
                        print(f"  Option chain failed: {option_chain.get('emsg', 'Unknown')}")
                        pass
                    
                    end_time = datetime.datetime.now()
                    time_taken = (end_time - start_time).total_seconds()
                    print(f"    Time taken: {time_taken:.2f} seconds\n")
                except Exception as e:
                    print(f"  Option chain failed for {symbol}: {str(e)[:50]}")
            else:
                error_msg = ret.get('emsg', 'Unknown') if ret else 'No response'
                print(f"{symbol:<25} {exchange:<10} {token:<10} {error_msg[:100]:<10} {'--':<10}")
        except Exception as e:
            print(f"{symbol:<25} {exchange:<10} {token:<10} {str(e)[:100]:<10} {'--':<10}")
    
    break  # Removed to allow continuous monitoring
    sleep(5)

# Create a list of tokens of indexes to keep track of...

# Subscribe to spot prices of those tokens via websocket

# Subscribe the a range of put and call options of the indexes

# Use the df stored to see if the prices are too much underpriced and
# promising profitablbity of atleast 10% with a probability of >95%