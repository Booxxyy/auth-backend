from rest_framework.permissions import BasePermission
from access_control.models import AccessRoleRule, BusinessElement
from users.models import User

class HasElementPermission(BasePermission):
    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False

        element_name = getattr(view, 'element_name', None)
        permission_type = getattr(view, 'permission_type', None)

        if not element_name or not permission_type:
            return False

        try:
            element = BusinessElement.objects.get(name=element_name)
        except BusinessElement.DoesNotExist:
            return False

        try:
            rule = AccessRoleRule.objects.get(
                role = request.user.role,
                element = element,
            )
        except AccessRoleRule.DoesNotExist:
            return False

        permission_field = f'{permission_type}_permission'

        return getattr(rule, permission_field, False)