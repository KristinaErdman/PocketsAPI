from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.pk)

    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user or request.user.is_staff)
