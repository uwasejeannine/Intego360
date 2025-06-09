from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read permissions are allowed to any authenticated user.
    """

    def has_permission(self, request, view):
        # Read permissions to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions only to admin users
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions only to the owner or admin
        return obj == request.user or (request.user and request.user.role == 'admin')

class IsMayorOrAdmin(permissions.BasePermission):
    """
    Custom permission for mayor-level access or admin.
    """

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'mayor', 'vice_mayor']
        )

class HasDistrictAccess(permissions.BasePermission):
    """
    Custom permission to check if user has access to district data.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin has access to everything
        if request.user.role == 'admin':
            return True
        
        # Check if object has district attribute
        if hasattr(obj, 'district'):
            return request.user.has_district_access(obj.district)
        
        # If object is a district itself
        if hasattr(obj, 'name') and hasattr(obj, 'sectors'):  # Likely a District object
            return request.user.has_district_access(obj)
        
        return False

class HasSectorAccess(permissions.BasePermission):
    """
    Custom permission to check if user has access to sector data.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin has access to everything
        if request.user.role == 'admin':
            return True
        
        # Check if object has sector attribute
        if hasattr(obj, 'sector'):
            return request.user.has_sector_access(obj.sector)
        
        # If object is a sector itself
        if hasattr(obj, 'district') and hasattr(obj, 'name'):  # Likely a Sector object
            return request.user.has_sector_access(obj)
        
        return False

class CanViewSectorData(permissions.BasePermission):
    """
    Custom permission to check if user can view specific sector data.
    """

    def __init__(self, sector_type):
        self.sector_type = sector_type

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.can_view_sector_data(self.sector_type)
        )

class CanManageUsers(permissions.BasePermission):
    """
    Custom permission for user management operations.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin can manage all users
        if request.user.role == 'admin':
            return True
        
        # Mayors can manage users in their district
        if request.user.role in ['mayor', 'vice_mayor'] and request.user.district:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin can manage all users
        if request.user.role == 'admin':
            return True
        
        # Mayors can manage users in their district
        if (request.user.role in ['mayor', 'vice_mayor'] and 
            request.user.district and 
            obj.district == request.user.district):
            return True
        
        # Users can manage their own profile
        if obj == request.user:
            return True
        
        return False

class CanGenerateReports(permissions.BasePermission):
    """
    Custom permission for report generation.
    """

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'mayor', 'vice_mayor', 'data_analyst']
        )

class CanExportData(permissions.BasePermission):
    """
    Custom permission for data export operations.
    """

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'mayor', 'vice_mayor', 'data_analyst']
        )

class CanManageAlerts(permissions.BasePermission):
    """
    Custom permission for alert management.
    """

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'mayor', 'vice_mayor']
        )

class ReadOnlyOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow read-only access to authenticated users,
    but full access only to admins.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user and request.user.is_authenticated and request.user.role == 'admin'