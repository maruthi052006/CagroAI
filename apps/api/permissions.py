from rest_framework.permissions import BasePermission
from apps.accounts.models import User, FarmerProfile, OfficerProfile

class IsOfficer(BasePermission):
    """
    Grants access only to authenticated users with the Agri-Officer role.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == User.Role.OFFICER


class IsFarmerOwner(BasePermission):
    """
    Grants access if the requesting user is the farmer who owns the field,
    or is an authenticated Agri-Officer assigned to that farmer's zone.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Officer access check
        if request.user.role == User.Role.OFFICER:
            return True

        # Farmer ownership check
        field_owner = getattr(obj, 'owner', None)
        if isinstance(field_owner, FarmerProfile):
            return field_owner.user == request.user
        elif isinstance(obj, FarmerProfile):
            return obj.user == request.user
        return False


class IsAssignedOfficer(BasePermission):
    """
    Grants access if the officer is assigned to the specific farmer or zone.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == User.Role.OFFICER

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role != User.Role.OFFICER:
            return False

        # If obj is a FarmerProfile
        if isinstance(obj, FarmerProfile):
            if obj.assigned_officer and obj.assigned_officer.user == request.user:
                return True
            try:
                officer_profile = request.user.officer_profile
                if obj.zone in officer_profile.zones.all():
                    return True
            except OfficerProfile.DoesNotExist:
                return False

        return True
