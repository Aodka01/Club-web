from django.utils.deprecation import MiddlewareMixin

class RolePermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user._perm_cache = None
            request.user._user_perm_cache = None
            request.user._group_perm_cache = None
            # Monkey patch get_all_permissions to include role permissions
            original_get_all_permissions = request.user.get_all_permissions
            def get_all_permissions():
                perms = original_get_all_permissions()
                try:
                    profile = request.user.profile
                    for role in profile.roles.all():
                        perms.update([f"{p.content_type.app_label}.{p.codename}" for p in role.permissions.all()])
                except Exception:
                    pass
                return perms
            request.user.get_all_permissions = get_all_permissions
        return self.get_response(request)