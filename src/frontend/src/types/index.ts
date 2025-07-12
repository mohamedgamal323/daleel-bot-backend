// Type definitions for commonly used types
export type { 
  LoginCredentials, 
  LoginResponse, 
  UserRegistrationRequest, 
  User, 
  Domain, 
  Category, 
  Asset, 
  QueryRequest, 
  ApiResponse 
} from '@shared/types'

// Frontend-specific types
export interface RouteMetadata {
  title: string
  requiresAuth: boolean
  roles?: string[]
}

export interface NavigationItem {
  id: string
  name: string
  href: string
  icon?: string
  current?: boolean
  children?: NavigationItem[]
}

export interface FormField {
  id: string
  name: string
  type: string
  label: string
  placeholder?: string
  required?: boolean
  validation?: {
    min?: number
    max?: number
    pattern?: string
    message?: string
  }
}

export interface TableColumn {
  key: string
  label: string
  sortable?: boolean
  width?: string
  align?: 'left' | 'center' | 'right'
}

export interface PaginationInfo {
  currentPage: number
  totalPages: number
  totalItems: number
  itemsPerPage: number
}

export interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

export interface Modal {
  id: string
  title: string
  content: string
  actions: {
    label: string
    action: () => void
    variant: 'primary' | 'secondary' | 'danger'
  }[]
}

export interface FileUpload {
  file: File
  name: string
  size: number
  type: string
  progress: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  error?: string
}
