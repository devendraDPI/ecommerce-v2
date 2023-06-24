import datetime

def generate_order_number(pk):
    """Generates order number"""
    today = datetime.date.today().strftime("%w-%j-%W-%Y%m%d")
    return f'{today}-{pk}'
