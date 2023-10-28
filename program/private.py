from datetime import datetime, timedelta
import time
from utils import format_number

# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    # Get Position Id
    account_response = client.private.get_account()
    position_id = account_response.data['account']['positionId']

    # Get Expiration Time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data['iso'].replace('Z', '')) + timedelta(seconds=70 + (7 * 60 * 60))

    # Place an order
    place_order = client.private.create_order(
        position_id=position_id,
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,                                        # Should be true for limit order
        size=size,
        price=price,
        limit_fee="0.015",
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",                                    # Fill or Kill
        reduce_only=reduce_only,                                       # cancel an existing order
    )

    return place_order.data


# Abort all open positions
def abort_all_positions(client):
    
    # Cancel or order
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)

    # Get markets for reference of tick size
    markets = client.public.get_markets().data

    # Protect API
    time.sleep(0.5)

    # Get all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data['positions']

    # Handle open positions
    close_orders = []
    if len(all_positions) > 0:

        # Loop through each position
        for position in all_positions:

            # Determine market
            market = position['market']

            # Determine side
            side = "BUY"
            if position['side'] == "LONG":
                side = "SELL"

            # Get price
            # CAN MODIFY HERE
            price = float(position['entryPrice'])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)

            # Place order to close
            order = place_market_order(
                client=client,
                market=market,
                side=side,
                size=position['sumOpen'],
                price=accept_price,
                reduce_only=True
            )

            # Append result
            close_orders.append(order)

            # Protect API
            time.sleep(0.2)

        return close_orders