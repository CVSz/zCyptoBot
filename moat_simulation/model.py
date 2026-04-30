def moat(data, standards, distribution, switching):
    """
    All inputs normalized 0..1
    """
    for v in (data, standards, distribution, switching):
        if not (0 <= v <= 1):
            raise ValueError("inputs 0..1")
    return 0.3 * data + 0.3 * standards + 0.2 * distribution + 0.2 * switching
