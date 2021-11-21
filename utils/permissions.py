from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsCriticoUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and (
            request.user.is_superuser or request.user.is_staff
        ):
            return True

        return request.user.is_staff and not request.user.is_superuser
