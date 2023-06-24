from vendor.models import Vendor, UserProfile
from django.conf import settings


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return {'vendor': vendor}


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return {'user_profile': user_profile}


def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
