from .models import User
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.role == User.ROLE.ADMIN
        )
