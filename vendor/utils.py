from vendor.models import Vendor


def get_vendor(request):
    """Returns vendor"""
    vendor = Vendor.objects.get(user=request.user)
    return vendor
