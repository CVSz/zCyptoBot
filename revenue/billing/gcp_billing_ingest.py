def parse_gcp(rows):
    return sum(r["cost"] for r in rows)
