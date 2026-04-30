def add_supply(book, provider, price, capacity):
    book.append({
        "provider": provider,
        "price": price,
        "capacity": capacity,
    })
    return book
