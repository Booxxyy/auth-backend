from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from access_control.models import Role, AccessRoleRule
from access_control.serializers import RoleSerializer, AccessRoleRuleSerializer
from access_control.permissions import HasElementPermission

# Create your views here.
class RoleListView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'roles'
    permission_type = 'read_all'

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class RoleCreateView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'roles'
    permission_type = 'create'

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleDetailView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'roles'
    permission_type = 'read_all'

    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

class RoleUpdateView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'roles'
    permission_type = 'update'

    def patch(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleDeleteView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'roles'
    permission_type = 'delete'

    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccessRoleRuleListView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'access_roles'
    permission_type = 'read_all'

    def get(self, request):
        rules = AccessRoleRule.objects.all()
        serializer = AccessRoleRuleSerializer(rules, many=True)
        return Response(serializer.data)

class AccessRoleRuleCreateView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'access_roles'
    permission_type = 'create'

    def post(self, request):
        serializer = AccessRoleRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccessRoleRuleUpdateView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'access_roles'
    permission_type = 'update'

    def patch(self, request, pk):
        try:
            rule = AccessRoleRule.objects.get(pk=pk)
        except AccessRoleRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AccessRoleRuleSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccessRoleRuleDeleteView(APIView):
    permission_classes = [HasElementPermission]
    element_name = 'access_roles'
    permission_type = 'delete'

    def delete(self, request, pk):
        try:
            rule = AccessRoleRule.objects.get(pk=pk)
        except AccessRoleRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)