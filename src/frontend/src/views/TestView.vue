<template>
  <div class="p-6 max-w-4xl mx-auto">
    <div class="bg-white shadow rounded-lg p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">API Connection Test</h1>
      
      <div class="space-y-4">
        <div>
          <h2 class="text-lg font-semibold text-gray-800">Backend Health Check</h2>
          <div class="mt-2 p-3 bg-gray-50 rounded">
            <div v-if="healthStatus" class="text-green-600">
              ✅ Backend is healthy: {{ healthStatus }}
            </div>
            <div v-else-if="healthError" class="text-red-600">
              ❌ Backend error: {{ healthError }}
            </div>
            <div v-else class="text-gray-600">
              ⏳ Testing connection...
            </div>
          </div>
        </div>

        <div>
          <h2 class="text-lg font-semibold text-gray-800">Test API Calls</h2>
          <div class="mt-2 space-y-2">
            <button
              @click="testHealth"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Test Health Endpoint
            </button>
            
            <button
              @click="testDomains"
              class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 ml-2"
            >
              Test Domains API
            </button>
          </div>
        </div>

        <div v-if="apiResponse" class="mt-4">
          <h3 class="text-md font-semibold text-gray-800">API Response:</h3>
          <pre class="mt-2 p-3 bg-gray-900 text-green-400 rounded text-sm overflow-auto">{{ JSON.stringify(apiResponse, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const healthStatus = ref<string | null>(null)
const healthError = ref<string | null>(null)
const apiResponse = ref<any>(null)

const testHealth = async () => {
  try {
    healthError.value = null
    const response = await fetch('/api/health')
    const data = await response.json()
    healthStatus.value = data.status
    apiResponse.value = data
  } catch (error) {
    healthError.value = error instanceof Error ? error.message : 'Unknown error'
    apiResponse.value = { error: error instanceof Error ? error.message : 'Unknown error' }
  }
}

const testDomains = async () => {
  try {
    // const domains = await api.getDomains()
    // apiResponse.value = domains
    apiResponse.value = { message: 'TestView temporarily disabled' }
  } catch (error) {
    apiResponse.value = { error: error instanceof Error ? error.message : 'Unknown error' }
  }
}

onMounted(() => {
  testHealth()
})
</script>
