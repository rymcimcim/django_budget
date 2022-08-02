from rest_framework import permissions


class IsOwnerOrInSharedReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to users shared with
        for GET, HEAD or OPTIONS requests.
        """
        if request.method in permissions.SAFE_METHODS and \
            (request.user in obj.shared or obj.owner == request.user):
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user or request.user.is_staff
