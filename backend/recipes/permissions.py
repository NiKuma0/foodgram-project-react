from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class CreaterCanChange(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user == obj.author:
            return True
        return False
