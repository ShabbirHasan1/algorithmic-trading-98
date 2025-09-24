from config import *
import pandas as pd
import logging

def exitallpositions():

    logging.info("MTM breached Take Profit😎")

    orderbook = api.get_order_book()
    
    # Define the columns to extract from the order book
    orderbook_columns = [
        'norenordno', 'exch', 'tsym', 'rejby', 'qty', 'ordenttm', 'trantype',
        'prctypr', 'prc', 'ret', 'token', 'prcftr', 'ordersource', 'ti', 'avgprc', 's_prdt_ali',
        'prd', 'status', 'fillshares', 'rqty', 'rorgqty', 'rorgprc', 'blprc',
        'trgprc', 'snonum', 'snoordt'
    ]

    order_df = pd.DataFrame(orderbook, columns=orderbook_columns)

    if (order_df['status'].isin(['COMPLETE', 'REJECTED'])).all():
        logging.info("\nAll positions are Squarred-Off, Exited the program.")
        exit()

    else:
        # Iterate through the complete DataFrame
        for _, row in order_df.iterrows():
                try:
                    fillshares = row['fillshares']
                    trantype = row['trantype']
                    
                    if trantype == 'B':
                        lp = 1.001
                    else:
                        lp = 0.999

                    if not pd.isna(row['snonum']) and row['status'] != 'REJECTED' and row['status'] != 'COMPLETE':                      # Trailing Open SL-Orders
                        quote_info = api.get_quotes(exchange=row['exch'], token=row['token'])
                        ltp = round(float(quote_info.get("lp", 0)), 2)
                        exchange = row['exch']
                        rqty = row['rqty']
                        exchange = row['exch']     # Exchange
                        tsym = row['tsym']         # Trading symbol
                        tick_size = round(float(row['ti']), 2) if not pd.isna(row['ti']) else 0.05                                      # Default tick size if missing
                        new_price = round(ltp * lp / tick_size) * tick_size,

                        logging.info(f"Trailed order {row['norenordno']} due to MTM breaching take profit")

                        api.modify_order(
                            exchange=exchange,
                            tradingsymbol=tsym,
                            orderno=row['norenordno'],
                            newquantity=rqty,
                            newprice_type='SL-LMT',
                            newprice = new_price,
                            newtrigger_price = round(ltp / tick_size) * tick_size
                        )
                    
                    elif (fillshares == 0) and pd.isna(row['snonum']) and row['status'] != "REJECTED" and row['status'] == "OPEN":      # Cancel unfilled orders
                        try:
                            api.cancel_order(orderno=row['norenordno'])
                            logging.info(f"Canceled unfilled order {row['norenordno']} due to MTM reaching")
                        except Exception as e:
                            logging.error(f"Failed to cancel order {row['norenordno']}: {e}")
                            continue  # Skip further processing for this order

                except Exception as e:
                            logging.error("Failed to exit all the positions")