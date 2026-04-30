def parse_azure(rows):
    return sum(r["pretaxCost"] for r in rows)
