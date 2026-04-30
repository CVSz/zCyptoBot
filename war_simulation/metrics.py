def kpis(arr, margin, retention, win_rate):
    if not (0 <= retention <= 2):
        raise ValueError("invalid retention")
    return {
        "ARR": arr,
        "GrossMargin": margin,
        "NetRetention": retention,
        "WinRate": win_rate,
    }
