from connections import connect_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES
from private import abort_all_positions
from public import construct_market_prices
from cointegration import store_cointegration_results

if __name__ == '__main__':
    
    # Connect to client
    try:
        print('Connecting to client...')
        client = connect_dydx()
    except Exception as e:
        print('Error connecting to client :', e)
        exit(1)

    # Abote all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print('Closing all positions...')
            close_orders = abort_all_positions(client)
        except Exception as e:
            print('Error closing all positions :', e)
            exit(1)

    # Find Cointegrated Pairs
    if FIND_COINTEGRATED:

        # Construct Market Prices
        try:
            print('Fetching market prices...')
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print('Error fetching market prices :', e)
            exit(1)

        # Store Cointegrated Pairs
        try:
            print('Storing cointegrated pairs...')
            store_result = store_cointegration_results(df_market_prices)
            if store_result != 'saved':
                print('Error saving cointegrated pairs')
                exit(1)
        except Exception as e:
            print('Error saving cointegrated pairs :', e)
            exit(1)




        # Place trades for opening positions
        if PLACE_TRADES:
            try:
                print('Finding trading opportunities...')
                open_positions(client)
            except Exception as e:
                print('Error trading pairs :', e)
                exit(1)
