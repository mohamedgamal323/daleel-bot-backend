from enum import Enum


class Permission(str, Enum):
    # User management permissions
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    RESTORE_USER = "restore_user"
    
    # Domain management permissions
    CREATE_DOMAIN = "create_domain"
    READ_DOMAIN = "read_domain"
    UPDATE_DOMAIN = "update_domain"
    DELETE_DOMAIN = "delete_domain"
    RESTORE_DOMAIN = "restore_domain"
    
    # Category management permissions
    CREATE_CATEGORY = "create_category"
    READ_CATEGORY = "read_category"
    UPDATE_CATEGORY = "update_category"
    DELETE_CATEGORY = "delete_category"
    RESTORE_CATEGORY = "restore_category"
    
    # Asset management permissions
    CREATE_ASSET = "create_asset"
    READ_ASSET = "read_asset"
    UPDATE_ASSET = "update_asset"
    DELETE_ASSET = "delete_asset"
    RESTORE_ASSET = "restore_asset"
    
    # Query permissions
    QUERY_ASSETS = "query_assets"
    
    # Admin permissions
    ADMIN_ACCESS = "admin_access"
    VIEW_DELETED = "view_deleted"
    SYSTEM_CONFIG = "system_config"


# Role-Permission mapping
ROLE_PERMISSIONS = {
    "user": [
        Permission.READ_DOMAIN,
        Permission.READ_CATEGORY,
        Permission.READ_ASSET,
        Permission.QUERY_ASSETS,
    ],
    "domain_admin": [
        # Domain admin can manage everything within their domain
        Permission.READ_DOMAIN,
        Permission.UPDATE_DOMAIN,
        Permission.CREATE_CATEGORY,
        Permission.READ_CATEGORY,
        Permission.UPDATE_CATEGORY,
        Permission.DELETE_CATEGORY,
        Permission.CREATE_ASSET,
        Permission.READ_ASSET,
        Permission.UPDATE_ASSET,
        Permission.DELETE_ASSET,
        Permission.QUERY_ASSETS,
        Permission.VIEW_DELETED,
    ],
    "global_admin": [
        # Global admin has all permissions
        Permission.CREATE_USER,
        Permission.READ_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        Permission.RESTORE_USER,
        Permission.CREATE_DOMAIN,
        Permission.READ_DOMAIN,
        Permission.UPDATE_DOMAIN,
        Permission.DELETE_DOMAIN,
        Permission.RESTORE_DOMAIN,
        Permission.CREATE_CATEGORY,
        Permission.READ_CATEGORY,
        Permission.UPDATE_CATEGORY,
        Permission.DELETE_CATEGORY,
        Permission.RESTORE_CATEGORY,
        Permission.CREATE_ASSET,
        Permission.READ_ASSET,
        Permission.UPDATE_ASSET,
        Permission.DELETE_ASSET,
        Permission.RESTORE_ASSET,
        Permission.QUERY_ASSETS,
        Permission.ADMIN_ACCESS,
        Permission.VIEW_DELETED,
        Permission.SYSTEM_CONFIG,
    ],
}


def get_role_permissions(role: str) -> list[Permission]:
    """Get all permissions for a given role"""
    return ROLE_PERMISSIONS.get(role, [])


def has_permission(role: str, permission: Permission) -> bool:
    """Check if a role has a specific permission"""
    return permission in get_role_permissions(role)
