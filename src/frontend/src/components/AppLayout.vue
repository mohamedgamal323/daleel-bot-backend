<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
              <router-link to="/" class="flex items-center">
                <img 
                  class="h-8 w-8" 
                  :src="logoUrl" 
                  alt="DaleelBot"
                />
                <span class="ml-2 text-xl font-bold text-gray-900">DaleelBot</span>
              </router-link>
            </div>
            
            <!-- Navigation Links -->
            <div class="hidden md:ml-10 md:flex md:items-center md:space-x-8">
              <router-link 
                v-for="item in navigation" 
                :key="item.id"
                :to="item.href"
                :class="[
                  item.current 
                    ? 'border-primary-500 text-gray-900' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                {{ item.name }}
              </router-link>
            </div>
          </div>
          
          <!-- User Menu -->
          <div class="hidden md:ml-4 md:flex md:items-center md:space-x-4">
            <!-- Search -->
            <div class="relative">
              <input 
                type="text" 
                placeholder="Search..." 
                class="w-64 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                v-model="searchQuery"
                @keyup.enter="performSearch"
              />
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
            
            <!-- Profile Dropdown -->
            <div class="relative" v-if="user">
              <button 
                @click="showUserMenu = !showUserMenu"
                class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <img 
                  class="h-8 w-8 rounded-full" 
                  :src="'/default-avatar.png'" 
                  :alt="user.username"
                />
              </button>
              
              <!-- Dropdown -->
              <div 
                v-if="showUserMenu"
                @click.away="showUserMenu = false"
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50"
              >
                <div class="py-1">
                  <div class="px-4 py-2 text-sm text-gray-700 border-b">
                    <div class="font-medium">{{ user.username }}</div>
                    <div class="text-gray-500">{{ user.email }}</div>
                  </div>
                  <router-link 
                    to="/profile" 
                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Profile
                  </router-link>
                  <router-link 
                    to="/settings" 
                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Settings
                  </router-link>
                  <button 
                    @click="handleLogout"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Sign out
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Login Button -->
            <router-link 
              v-else
              to="/login"
              class="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Sign in
            </router-link>
          </div>
          
          <!-- Mobile menu button -->
          <div class="md:hidden flex items-center">
            <button 
              @click="showMobileMenu = !showMobileMenu"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            >
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mobile menu -->
      <div v-if="showMobileMenu" class="md:hidden">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <router-link 
            v-for="item in navigation" 
            :key="item.id"
            :to="item.href"
            :class="[
              item.current 
                ? 'bg-primary-50 border-primary-500 text-primary-700' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium'
            ]"
            @click="showMobileMenu = false"
          >
            {{ item.name }}
          </router-link>
        </div>
      </div>
    </nav>
    
    <!-- Page Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { NavigationItem } from '@/types'
import logoUrl from '@/assets/daleelbot-logo.png'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const searchQuery = ref('')

const user = computed(() => authStore.user)

const navigation = computed<NavigationItem[]>(() => [
  {
    id: 'dashboard',
    name: 'Dashboard',
    href: '/',
    current: route.path === '/',
  },
  {
    id: 'domains',
    name: 'Domains',
    href: '/domains',
    current: route.path.startsWith('/domains'),
  },
  {
    id: 'categories',
    name: 'Categories',
    href: '/categories',
    current: route.path.startsWith('/categories'),
  },
  {
    id: 'assets',
    name: 'Assets',
    href: '/assets',
    current: route.path.startsWith('/assets'),
  },
  {
    id: 'queries',
    name: 'Queries',
    href: '/queries',
    current: route.path.startsWith('/queries'),
  },
])

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/search?q=${encodeURIComponent(searchQuery.value)}`)
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!((e.target as Element)?.closest('.relative'))) {
      showUserMenu.value = false
    }
  })
})
</script>
