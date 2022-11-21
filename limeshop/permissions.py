from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class IsAuthAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)):
            return True
        return False


class IsAuthOrCreate(BasePermission):

    def has_permission(self, request, view):
        if (request.method == 'GET' and not request.user.is_authenticated):
            return False
        return True
