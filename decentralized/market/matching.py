from .orderbook import OrderBook


def match(ob: OrderBook):
    trades = []
    while ob.bids and ob.asks and ob.bids[0].price >= ob.asks[0].price:
        b = ob.bids[0]
        a = ob.asks[0]
        qty = min(b.qty, a.qty)
        price = (b.price + a.price) / 2.0

        trades.append({"price": price, "qty": qty, "buyer": b.order_id, "seller": a.node_id})

        b.qty -= qty
        a.qty -= qty

        if b.qty == 0:
            ob.bids.pop(0)
        if a.qty == 0:
            ob.asks.pop(0)

    return trades
