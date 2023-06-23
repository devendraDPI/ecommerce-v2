from django.shortcuts import render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from the_shop.utils import get_or_set_current_location


def home(request):
    if get_or_set_current_location(request) is not None:
        point = GEOSGeometry('POINT(%s %s)' % (get_or_set_current_location(request)))
        vendors = Vendor.objects.filter(
            user_profile__location__distance_lte=(point, D(km=6371))
        ).annotate(distance=Distance('user_profile__location', point)).order_by('distance')
        for distance_ in vendors:
            distance_.kms = round(distance_.distance.km, 2)
    else:
        vendors = Vendor.objects.filter(user__is_active=True, is_approved=True, is_featured=False).order_by('modified_at')[:9]
    featured_vendors = Vendor.objects.filter(user__is_active=True, is_approved=True, is_featured=True).order_by('modified_at')
    context = {
        'featured_vendors': featured_vendors,
        'vendors': vendors,
    }
    return render(request, 'home.html', context)
