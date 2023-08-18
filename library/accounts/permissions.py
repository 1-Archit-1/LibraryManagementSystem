from rest_framework import permissions
class LibPermission(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        x= True if request.user.user_type == 1 else False
        return x