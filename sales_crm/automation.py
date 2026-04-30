def next_action(deal):
    if deal.stage == "lead":
        return "send_intro_email"
    if deal.stage == "demo":
        return "send_roi_dashboard"
    if deal.stage == "pilot":
        return "push_contract"
    return "follow_up"
