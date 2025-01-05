from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CheckCRUD(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == "Врач"


class CheckRole(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == "Пациент"


class CheckFeedback(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_name == request.user


class CheckAppointments(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.patient or request.user == obj.doctor:
            return True
        return False