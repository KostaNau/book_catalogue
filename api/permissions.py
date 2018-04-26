from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserReadOnlyOrIsAdmin(BasePermission):
    """
    The request is authenticated as a admin, or is a user read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS and
            request.user.is_authenticated or
            request.user and
            request.user.is_staff
        )
