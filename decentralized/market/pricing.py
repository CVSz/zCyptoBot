def dynamic_price(base: float, demand: float, supply: float, latency: float):
    # demand ↑ → price ↑, supply ↑ → price ↓, latency ↑ → penalty
    return base * (1 + 0.6 * demand - 0.4 * supply + 0.2 * (latency / 200.0))
