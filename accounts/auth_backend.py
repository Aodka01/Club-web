from django.contrib.auth.backends import ModelBackend
from .models import Profile

class RolePermissionBackend(ModelBackend):
    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active:
            return set()
        
        # Obtener permisos del usuario y grupos
        perms = super().get_all_permissions(user_obj, obj)
        if perms is None:
            perms = set()
        else:
            perms = set(perms)
        
        # Agregar permisos de roles
        try:
            profile = user_obj.profile
        except Profile.DoesNotExist:
            return perms
        
        for role in profile.roles.all():
            for perm in role.permissions.all():
                perms.add(f"{perm.content_type.app_label}.{perm.codename}")
        
        return perms

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj, obj)

