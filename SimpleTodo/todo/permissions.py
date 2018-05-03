from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create','retrieve']:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
