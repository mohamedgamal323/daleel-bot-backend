import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'
import type { 
  ApiResponse, 
  PaginatedResponse,
  LoginCredentials,
  LoginResponse,
  UserRegistrationRequest,
  User,
  Domain,
  Category,
  Asset,
  QueryRequest,
  QueryResponse,
  DomainCreateRequest,
  DomainUpdateRequest,
  CategoryCreateRequest,
  CategoryUpdateRequest,
  AssetCreateRequest,
  AssetUpdateRequest
} from '@shared/types'

// Create axios instance with base configuration
const api: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Authentication API
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<ApiResponse<LoginResponse>> => {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  register: async (userData: UserRegistrationRequest): Promise<ApiResponse<LoginResponse>> => {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  logout: async (): Promise<ApiResponse> => {
    const response = await api.post('/auth/logout')
    return response.data
  },

  getProfile: async (): Promise<ApiResponse<User>> => {
    const response = await api.get('/auth/profile')
    return response.data
  },

  updateProfile: async (profileData: Partial<User>): Promise<ApiResponse<User>> => {
    const response = await api.put('/auth/profile', profileData)
    return response.data
  },

  refreshToken: async (): Promise<ApiResponse<LoginResponse>> => {
    const response = await api.post('/auth/refresh')
    return response.data
  },
}

// Users API
export const usersApi = {
  getUsers: async (page = 1, limit = 10): Promise<ApiResponse<PaginatedResponse<User>>> => {
    const response = await api.get('/users', { params: { page, limit } })
    return response.data
  },

  getUser: async (id: string): Promise<ApiResponse<User>> => {
    const response = await api.get(`/users/${id}`)
    return response.data
  },

  createUser: async (userData: UserRegistrationRequest): Promise<ApiResponse<User>> => {
    const response = await api.post('/users', userData)
    return response.data
  },

  updateUser: async (id: string, userData: Partial<User>): Promise<ApiResponse<User>> => {
    const response = await api.put(`/users/${id}`, userData)
    return response.data
  },

  deleteUser: async (id: string): Promise<ApiResponse> => {
    const response = await api.delete(`/users/${id}`)
    return response.data
  },
}

// Domains API
export const domainsApi = {
  getDomains: async (page = 1, limit = 10): Promise<ApiResponse<PaginatedResponse<Domain>>> => {
    const response = await api.get('/domains', { params: { page, limit } })
    return response.data
  },

  getDomain: async (id: string): Promise<ApiResponse<Domain>> => {
    const response = await api.get(`/domains/${id}`)
    return response.data
  },

  createDomain: async (domainData: DomainCreateRequest): Promise<ApiResponse<Domain>> => {
    const response = await api.post('/domains', domainData)
    return response.data
  },

  updateDomain: async (id: string, domainData: DomainUpdateRequest): Promise<ApiResponse<Domain>> => {
    const response = await api.put(`/domains/${id}`, domainData)
    return response.data
  },

  deleteDomain: async (id: string): Promise<ApiResponse> => {
    const response = await api.delete(`/domains/${id}`)
    return response.data
  },
}

// Categories API
export const categoriesApi = {
  getCategories: async (domainId?: string, page = 1, limit = 10): Promise<ApiResponse<PaginatedResponse<Category>>> => {
    const params: any = { page, limit }
    if (domainId) params.domain_id = domainId
    const response = await api.get('/categories', { params })
    return response.data
  },

  getCategory: async (id: string): Promise<ApiResponse<Category>> => {
    const response = await api.get(`/categories/${id}`)
    return response.data
  },

  createCategory: async (categoryData: CategoryCreateRequest): Promise<ApiResponse<Category>> => {
    const response = await api.post('/categories', categoryData)
    return response.data
  },

  updateCategory: async (id: string, categoryData: CategoryUpdateRequest): Promise<ApiResponse<Category>> => {
    const response = await api.put(`/categories/${id}`, categoryData)
    return response.data
  },

  deleteCategory: async (id: string): Promise<ApiResponse> => {
    const response = await api.delete(`/categories/${id}`)
    return response.data
  },
}

// Assets API
export const assetsApi = {
  getAssets: async (categoryId?: string, page = 1, limit = 10): Promise<ApiResponse<PaginatedResponse<Asset>>> => {
    const params: any = { page, limit }
    if (categoryId) params.category_id = categoryId
    const response = await api.get('/assets', { params })
    return response.data
  },

  getAsset: async (id: string): Promise<ApiResponse<Asset>> => {
    const response = await api.get(`/assets/${id}`)
    return response.data
  },

  createAsset: async (assetData: AssetCreateRequest): Promise<ApiResponse<Asset>> => {
    const response = await api.post('/assets', assetData)
    return response.data
  },

  updateAsset: async (id: string, assetData: AssetUpdateRequest): Promise<ApiResponse<Asset>> => {
    const response = await api.put(`/assets/${id}`, assetData)
    return response.data
  },

  deleteAsset: async (id: string): Promise<ApiResponse> => {
    const response = await api.delete(`/assets/${id}`)
    return response.data
  },

  uploadAsset: async (file: File, categoryId: string, title: string): Promise<ApiResponse<Asset>> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('category_id', categoryId)
    formData.append('title', title)
    
    const response = await api.post('/assets/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}

// Query API
export const queryApi = {
  query: async (queryData: QueryRequest): Promise<ApiResponse<QueryResponse>> => {
    const response = await api.post('/query', queryData)
    return response.data
  },

  getQueries: async (page = 1, limit = 10): Promise<ApiResponse<PaginatedResponse<any>>> => {
    const response = await api.get('/queries', { params: { page, limit } })
    return response.data
  },
}

// Health check API
export const healthApi = {
  check: async (): Promise<ApiResponse> => {
    const response = await api.get('/health')
    return response.data
  },
}

export default api
