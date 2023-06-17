def detect_user(user):
    if user.role is None and user.is_superadmin:
        return '/admin'
    role_dashboard = {
        'vendor': 'vendor-dashboard',
        'customer': 'customer-dashboard',
    }
    return role_dashboard.get(user.role)
