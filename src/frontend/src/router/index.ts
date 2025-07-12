import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/domains',
      name: 'domains',
      component: () => import('../views/DomainsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/CategoriesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/assets',
      name: 'assets',
      component: () => import('../views/AssetsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/queries',
      name: 'queries',
      component: () => import('../views/QueriesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/TestView.vue'),
      meta: { requiresAuth: false },
    },
  ],
})

// Navigation guard for authentication
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  console.log('Router guard:', {
    to: to.path,
    from: from.path,
    isAuthenticated: authStore.isAuthenticated,
    requiresAuth: to.meta.requiresAuth
  })
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      console.log('Not authenticated, redirecting to login')
      // Redirect to login page with return url
      next({
        name: 'login',
        query: { redirect: to.fullPath },
      })
      return
    }
  }
  
  // If user is already authenticated and trying to access auth pages, redirect to home
  if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    console.log('Authenticated user accessing auth page, redirecting to home')
    next({ name: 'home' })
    return
  }
  
  console.log('Proceeding to route:', to.path)
  next()
})

export default router
