# Authentication and Authorization System

This document describes the complete authentication and authorization system implemented in the Daleel Bot Backend.

## Overview

The system provides JWT-based authentication with role-based access control (RBAC) and permission-based authorization. It's designed to support a Vue.js frontend with secure API access based on user roles and permissions.

## Architecture

### Core Components

1. **Authentication Service** (`src/application/services/auth_service.py`)
   - User login/logout
   - Password management 
   - Token refresh
   - User validation

2. **JWT Manager** (`src/application/security/jwt_manager.py`)
   - JWT token creation and validation
   - Password hashing and verification
   - Token expiration handling

3. **Auth Dependencies** (`src/application/auth/dependencies.py`)
   - FastAPI dependency injection for authentication
   - Role and permission checking
   - Current user extraction

4. **Auth Controller** (`src/api/v1/auth_controller.py`)
   - REST API endpoints for authentication
   - User registration, login, logout
   - Password management endpoints

## Roles and Permissions

### Roles

- **`user`**: Basic user with read-only access to domains, categories, and assets
- **`domain_admin`**: Can manage categories and assets within their domain
- **`global_admin`**: Full system access including user management

### Permissions

The system uses fine-grained permissions:

**User Management:**
- `CREATE_USER`, `READ_USER`, `UPDATE_USER`, `DELETE_USER`, `RESTORE_USER`

**Domain Management:**
- `CREATE_DOMAIN`, `READ_DOMAIN`, `UPDATE_DOMAIN`, `DELETE_DOMAIN`, `RESTORE_DOMAIN`

**Category Management:**
- `CREATE_CATEGORY`, `READ_CATEGORY`, `UPDATE_CATEGORY`, `DELETE_CATEGORY`, `RESTORE_CATEGORY`

**Asset Management:**
- `CREATE_ASSET`, `READ_ASSET`, `UPDATE_ASSET`, `DELETE_ASSET`, `RESTORE_ASSET`

**Other:**
- `QUERY_ASSETS`, `ADMIN_ACCESS`, `VIEW_DELETED`, `SYSTEM_CONFIG`

### Role-Permission Mapping

```python
ROLE_PERMISSIONS = {
    "user": [
        Permission.READ_DOMAIN,
        Permission.READ_CATEGORY, 
        Permission.READ_ASSET,
        Permission.QUERY_ASSETS,
    ],
    "domain_admin": [
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
        # All permissions
    ],
}
```

## API Endpoints

### Authentication Endpoints

All authentication endpoints are under `/api/v1/auth/`:

#### User Registration
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "new_user",
  "email": "user@example.com",
  "password": "secure_password123",
  "role": "user"
}
```

Response:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid",
    "username": "new_user",
    "email": "user@example.com",
    "role": "user",
    "is_active": true
  }
}
```

#### User Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "existing_user",
  "password": "user_password"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "username": "existing_user",
    "email": "user@example.com",
    "role": "user",
    "is_active": true
  }
}
```

#### Token Refresh
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### Change Password
```http
POST /api/v1/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

#### Admin Password Reset
```http
POST /api/v1/auth/admin/reset-password/{user_id}
Authorization: Bearer <admin_access_token>
Content-Type: application/json

{
  "new_password": "new_password"
}
```

#### Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

## Frontend Integration (Vue.js)

### 1. Store JWT Tokens

Store tokens securely in the frontend:

```javascript
// In Vuex store or Pinia
const authStore = {
  state: {
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    user: JSON.parse(localStorage.getItem('user') || 'null')
  },
  
  mutations: {
    setAuth(state, { access_token, refresh_token, user }) {
      state.accessToken = access_token
      state.refreshToken = refresh_token
      state.user = user
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify(user))
    },
    
    clearAuth(state) {
      state.accessToken = null
      state.refreshToken = null
      state.user = null
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  }
}
```

### 2. HTTP Interceptors

Set up Axios interceptors for automatic token handling:

```javascript
import axios from 'axios'

// Request interceptor to add token
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor for token refresh
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post('/api/v1/auth/refresh', {
            refresh_token: refreshToken
          })
          
          // Update tokens
          authStore.commit('setAuth', response.data)
          
          // Retry original request
          const originalRequest = error.config
          originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`
          return axios(originalRequest)
        } catch (refreshError) {
          // Refresh failed, logout user
          authStore.commit('clearAuth')
          router.push('/login')
        }
      }
    }
    return Promise.reject(error)
  }
)
```

### 3. Route Protection

Protect routes based on user roles:

```javascript
// In Vue Router
const router = createRouter({
  routes: [
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, role: 'global_admin' }
    },
    {
      path: '/dashboard', 
      component: Dashboard,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user') || 'null')
  
  if (to.meta.requiresAuth) {
    if (!user) {
      next('/login')
      return
    }
    
    if (to.meta.role && user.role !== to.meta.role) {
      next('/unauthorized')
      return
    }
  }
  
  next()
})
```

### 4. Permission-Based UI Components

Show/hide UI elements based on permissions:

```vue
<template>
  <div>
    <button v-if="canCreateUser" @click="createUser">
      Create User
    </button>
    
    <button v-if="canDeleteUser" @click="deleteUser">
      Delete User
    </button>
  </div>
</template>

<script>
export default {
  computed: {
    user() {
      return this.$store.state.auth.user
    },
    
    userPermissions() {
      // This would come from your permission mapping
      return getUserPermissions(this.user?.role)
    },
    
    canCreateUser() {
      return this.userPermissions.includes('CREATE_USER')
    },
    
    canDeleteUser() {
      return this.userPermissions.includes('DELETE_USER')
    }
  }
}
</script>
```

## Security Configuration

### JWT Settings

Current JWT configuration (should be moved to environment variables in production):

```python
class SecurityConfig:
    SECRET_KEY = "your-secret-key-change-in-production"  # Use env var
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days
```

### Password Security

- Passwords are hashed using bcrypt
- Minimum security standards should be enforced on the frontend
- Password changes require current password verification

## Testing

The system includes comprehensive tests:

- Unit tests for JWT token creation/validation
- Unit tests for password hashing/verification
- Integration tests for authentication flow
- API endpoint tests with authentication

Run tests:
```bash
python -m pytest src/tests/test_auth.py -v
python -m pytest src/tests/test_auth_integration.py -v
```

## Production Considerations

1. **Environment Variables**: Move all secrets to environment variables
2. **HTTPS**: Ensure all communication uses HTTPS
3. **Token Blacklisting**: Consider implementing token blacklisting for logout
4. **Rate Limiting**: Add rate limiting to authentication endpoints
5. **Audit Logging**: Log authentication events for security monitoring
6. **Password Policies**: Implement strong password requirements
7. **Account Lockout**: Add account lockout after failed login attempts
8. **Session Management**: Consider session timeout and concurrent session limits

## Usage Examples

### Creating a Protected Endpoint

```python
from fastapi import APIRouter, Depends
from src.application.auth.dependencies import require_user_write

router = APIRouter()

@router.post("/protected-resource")
async def create_resource(
    current_user: User = Depends(require_user_write),
    # other dependencies
):
    # Only users with CREATE_USER permission can access this
    return {"message": "Resource created"}
```

### Multiple Permission Requirements

```python
from src.application.auth.dependencies import require_permissions
from src.domain.enums.permission import Permission

@router.post("/complex-operation")
async def complex_operation(
    current_user: User = Depends(
        require_permissions({Permission.CREATE_ASSET, Permission.UPDATE_DOMAIN})
    ),
):
    # Requires both CREATE_ASSET and UPDATE_DOMAIN permissions
    return {"message": "Complex operation completed"}
```

This authentication system provides a robust foundation for securing the Daleel Bot Backend APIs and integrates seamlessly with modern frontend frameworks like Vue.js.
