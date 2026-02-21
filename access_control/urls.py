from django.urls import path
from access_control.views import (
    RoleListView,
    RoleCreateView,
    RoleDetailView,
    RoleUpdateView,
    RoleDeleteView,
    AccessRoleRuleListView,
    AccessRoleRuleCreateView,
    AccessRoleRuleUpdateView,
    AccessRoleRuleDeleteView,
)

urlpatterns = [
    path('roles/', RoleListView.as_view()),
    path('roles/create/', RoleCreateView.as_view()),
    path('roles/<int:pk>/', RoleDetailView.as_view()),
    path('roles/<int:pk>/update/', RoleUpdateView.as_view()),
    path('roles/<int:pk>/delete/', RoleDeleteView.as_view()),
    path('rules/', AccessRoleRuleListView.as_view()),
    path('rules/create/', AccessRoleRuleCreateView.as_view()),
    path('rules/<int:pk>/update/', AccessRoleRuleUpdateView.as_view()),
    path('rules/<int:pk>/delete/', AccessRoleRuleDeleteView.as_view()),
]