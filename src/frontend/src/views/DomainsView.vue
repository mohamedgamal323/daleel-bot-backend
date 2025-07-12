<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Domains</h1>
            <p class="mt-1 text-sm text-gray-600">
              Manage your knowledge domains and their categories.
            </p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="showCreateModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Domain
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Domains List -->
    <div class="bg-white shadow overflow-hidden rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        
        <div v-else-if="domains.length === 0" class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No domains</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new domain.</p>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="domain in domains"
            :key="domain.id"
            class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow"
          >
            <div class="p-6">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-gray-900">{{ domain.name }}</h3>
                <div class="flex space-x-2">
                  <button
                    @click="editDomain(domain)"
                    class="text-gray-400 hover:text-gray-500"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="deleteDomain(domain)"
                    class="text-gray-400 hover:text-red-500"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <p v-if="domain.description" class="mt-2 text-sm text-gray-600">
                {{ domain.description }}
              </p>
              
              <div class="mt-4 flex items-center justify-between">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="domain.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                  {{ domain.is_active ? 'Active' : 'Inactive' }}
                </span>
                
                <div class="text-sm text-gray-500">
                  {{ formatDate(domain.created_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || editingDomain" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingDomain ? 'Edit Domain' : 'Create Domain' }}
          </h3>
          
          <form @submit.prevent="saveDomain">
            <div class="mb-4">
              <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
              <input
                id="name"
                v-model="domainForm.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            
            <div class="mb-4">
              <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                id="description"
                v-model="domainForm.description"
                rows="3"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              ></textarea>
            </div>
            
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {{ saving ? 'Saving...' : (editingDomain ? 'Update' : 'Create') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Domain, DomainCreateRequest, DomainUpdateRequest } from '@shared/types'
import { domainsApi } from '@/services/api'

const domains = ref<Domain[]>([])
const loading = ref(false)
const saving = ref(false)
const showCreateModal = ref(false)
const editingDomain = ref<Domain | null>(null)

const domainForm = ref<DomainCreateRequest>({
  name: '',
  description: '',
})

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

const loadDomains = async () => {
  loading.value = true
  try {
    const response = await domainsApi.getDomains()
    if (response.success && response.data) {
      domains.value = response.data.items
    }
  } catch (error) {
    console.error('Failed to load domains:', error)
  } finally {
    loading.value = false
  }
}

const saveDomain = async () => {
  saving.value = true
  try {
    if (editingDomain.value) {
      // Update existing domain
      const response = await domainsApi.updateDomain(editingDomain.value.id, domainForm.value)
      if (response.success) {
        const index = domains.value.findIndex(d => d.id === editingDomain.value!.id)
        if (index !== -1 && response.data) {
          domains.value[index] = response.data
        }
      }
    } else {
      // Create new domain
      const response = await domainsApi.createDomain(domainForm.value)
      if (response.success && response.data) {
        domains.value.push(response.data)
      }
    }
    closeModal()
  } catch (error) {
    console.error('Failed to save domain:', error)
  } finally {
    saving.value = false
  }
}

const editDomain = (domain: Domain) => {
  editingDomain.value = domain
  domainForm.value = {
    name: domain.name,
    description: domain.description || '',
  }
}

const deleteDomain = async (domain: Domain) => {
  if (confirm(`Are you sure you want to delete "${domain.name}"?`)) {
    try {
      const response = await domainsApi.deleteDomain(domain.id)
      if (response.success) {
        domains.value = domains.value.filter(d => d.id !== domain.id)
      }
    } catch (error) {
      console.error('Failed to delete domain:', error)
    }
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingDomain.value = null
  domainForm.value = {
    name: '',
    description: '',
  }
}

onMounted(() => {
  loadDomains()
})
</script>
