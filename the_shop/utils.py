def get_or_set_current_location(request):
    """Returns the current location (longitude, latitude)"""
    if 'lat' in request.session:
        latitude = request.session['lat']
        longitude = request.session['lng']
        return longitude, latitude
    elif 'lat' in request.GET:
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lng')
        request.session['lat'] = latitude
        request.session['lng'] = longitude
        return longitude, latitude
    else:
        return None
