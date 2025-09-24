import os
import sys
import logging
import pandas as pd
import requests
import zipfile
from datetime import datetime
from time import sleep
from NorenRestApiPy.NorenApi import FeedType

# Add root directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from broker.shoonya.config import *
# import broker.shoonya.basicfunctions as bf

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
print(bse_df.head())
print(bfo_df.head())

# Create a list of tokens of indexes to keep track of...

# Subscribe to spot prices of those tokens via websocket

# Subscribe the a range of put and call options of the indexes

# Use the df stored to see if the prices are too much underpriced and
# promising profitablbity of atleast 10% with a probability of >95%