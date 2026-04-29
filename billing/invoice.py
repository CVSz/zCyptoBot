from datetime import datetime


def generate_invoice(user, usage, rate):
    total = usage * rate
    return {
        "user": user,
        "total": total,
        "date": str(datetime.utcnow()),
    }
