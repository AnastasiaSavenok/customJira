from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Allows access only to authorized customers.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.user_type == 'customer'
