from connections import connect_dydx
from constants import ABORT_ALL_POSITIONS
from private import abort_all_positions

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
        close_orders = abort_all_positions(client)

        try:
            print('Closing all positions...')
            # close_orders = abort_all_positions(client)
        except Exception as e:
            print('Error closing all positions :', e)
            exit(1)