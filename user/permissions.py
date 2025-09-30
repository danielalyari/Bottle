from rest_framework import permissions
from user.models import UserProfile

class NotBannedPermission(permissions.BasePermission):
    """
    اجازه دسترسی به view فقط برای کاربران غیر بن شده
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return False
        return not profile.is_banned
