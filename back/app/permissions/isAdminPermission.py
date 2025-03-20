from rest_framework.permissions import BasePermission
from app.constantes import UserRoles


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles == UserRoles.ADMIN

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
