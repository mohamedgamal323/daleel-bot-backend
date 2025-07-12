// Authentication Types
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface TokenRefreshRequest {
  refresh_token: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    username: string;
    email: string;
    role: string;
    is_active: boolean;
  };
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

export interface ResetPasswordRequest {
  new_password: string;
}

export interface UserRegistrationRequest {
  username: string;
  email: string;
  password: string;
  role: UserRole;
}

// User Types
export interface User {
  id: string;
  username: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
  last_login?: string;
}

export type UserRole = 'user' | 'domain_admin' | 'global_admin';

// Domain Types
export interface Domain {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
  created_by?: string;
}

export interface DomainCreateRequest {
  name: string;
  description?: string;
}

export interface DomainUpdateRequest {
  name?: string;
  description?: string;
  is_active?: boolean;
}

// Category Types
export interface Category {
  id: string;
  name: string;
  description?: string;
  domain_id: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
  created_by?: string;
}

export interface CategoryCreateRequest {
  name: string;
  description?: string;
  domain_id: string;
}

export interface CategoryUpdateRequest {
  name?: string;
  description?: string;
  is_active?: boolean;
}

// Asset Types
export interface Asset {
  id: string;
  title: string;
  content?: string;
  asset_type: AssetType;
  category_id: string;
  file_path?: string;
  metadata?: Record<string, any>;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
  created_by?: string;
}

export type AssetType = 'document' | 'image' | 'video' | 'audio' | 'other';

export interface AssetCreateRequest {
  title: string;
  content?: string;
  asset_type: AssetType;
  category_id: string;
  file_path?: string;
  metadata?: Record<string, any>;
}

export interface AssetUpdateRequest {
  title?: string;
  content?: string;
  asset_type?: AssetType;
  category_id?: string;
  file_path?: string;
  metadata?: Record<string, any>;
  is_active?: boolean;
}

// Query Types
export interface QueryRequest {
  query: string;
  domain_id?: string;
  category_id?: string;
  limit?: number;
}

export interface QueryResponse {
  query: string;
  results: QueryResult[];
  total_results: number;
  query_time: number;
}

export interface QueryResult {
  asset_id: string;
  title: string;
  content_snippet: string;
  relevance_score: number;
  asset_type: AssetType;
  category_name: string;
  domain_name: string;
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T = any> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Permission Types
export type Permission = 
  | 'CREATE_USER' | 'READ_USER' | 'UPDATE_USER' | 'DELETE_USER' | 'RESTORE_USER'
  | 'CREATE_DOMAIN' | 'READ_DOMAIN' | 'UPDATE_DOMAIN' | 'DELETE_DOMAIN' | 'RESTORE_DOMAIN'
  | 'CREATE_CATEGORY' | 'READ_CATEGORY' | 'UPDATE_CATEGORY' | 'DELETE_CATEGORY' | 'RESTORE_CATEGORY'
  | 'CREATE_ASSET' | 'READ_ASSET' | 'UPDATE_ASSET' | 'DELETE_ASSET' | 'RESTORE_ASSET'
  | 'QUERY_ASSETS' | 'ADMIN_ACCESS' | 'VIEW_DELETED' | 'SYSTEM_CONFIG';

// Error Types
export interface ApiError {
  code: string;
  message: string;
  details?: any;
}

// Navigation Types (for frontend)
export interface NavItem {
  name: string;
  path: string;
  icon?: string;
  permission?: Permission;
  children?: NavItem[];
}

// Form Types (for frontend)
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'select' | 'textarea' | 'checkbox' | 'file';
  required?: boolean;
  placeholder?: string;
  options?: { value: string; label: string }[];
  validation?: {
    minLength?: number;
    maxLength?: number;
    pattern?: string;
    message?: string;
  };
}
