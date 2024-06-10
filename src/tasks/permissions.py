from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    """
    Allows access only to users with `user_type` == 'employee'.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.user_type == 'employee'
