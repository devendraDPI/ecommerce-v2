import datetime
import simplejson as json


def generate_order_number(pk):
    """Generates order number"""
    today = datetime.date.today().strftime("%w-%j-%W-%Y%m%d")
    return f'{today}-{pk}'


def order_total_by_vendor(order, vendor_id):
    """Returns subtotal, tax_dict, total"""
    all_data = json.loads(order.all_data)
    data = all_data.get(str(vendor_id))
    subtotal = 0
    tax = 0
    tax_dict = {}
    for key, val in data.items():
        subtotal += float(key)
        tax_dict.update(val)
        for i in val:
            for j in val[i]:
                tax += float(val[i][j])
    total = float(subtotal) + float(tax)
    return {
        'subtotal': subtotal,
        'tax_dict': tax_dict,
        'total': total,
    }
