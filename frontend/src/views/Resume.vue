<template>
    <div class="container mx-auto p-6">
      <div class="mb-8">
        <h1 class="text-3xl font-bold tracking-tight">Resume Manager</h1>
        <p class="text-muted-foreground mt-2">Upload and manage your professional resume</p>
      </div>
  
      <!-- Resume Upload Card -->
      <Card class="mb-6">
        <CardHeader>
          <CardTitle>Upload Resume</CardTitle>
          <CardDescription>
            Upload your resume in PDF format. Max file size: 5MB
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <Alert v-if="!authStore.isAuthenticated" variant="default" class="mb-4">
              <AlertCircle class="h-4 w-4" />
              <AlertTitle>Authentication Required</AlertTitle>
              <AlertDescription>
                Please sign in to upload and manage your resume.
                <Button 
                  variant="link" 
                  class="px-0 text-primary"
                  @click="router.push('/login')"
                >
                  Sign in here
                </Button>
              </AlertDescription>
            </Alert>
  
            <!-- Upload Section -->
            <div class="flex items-center gap-4">
              <Button
                :disabled="!authStore.isAuthenticated"
                @click="handleUploadClick"
                class="relative"
              >
                <Upload class="mr-2 h-4 w-4" />
                Upload Resume
              </Button>
              <p v-if="!authStore.isAuthenticated" class="text-sm text-muted-foreground">
                Sign in to enable resume upload
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
  
      <!-- Current Resume Section (Only visible when authenticated) -->
      <Card v-if="authStore.isAuthenticated">
        <CardHeader>
          <CardTitle>Current Resume</CardTitle>
          <CardDescription>
            View and manage your uploaded resume
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div v-if="currentResume" class="space-y-4">
            <!-- Resume display/management UI here -->
            <p>Resume details would go here</p>
          </div>
          <div v-else class="text-center py-8">
            <FileX class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <p class="text-muted-foreground">No resume uploaded yet</p>
          </div>
        </CardContent>
      </Card>
  
      <!-- Hidden file input -->
      <input
        type="file"
        ref="fileInput"
        class="hidden"
        accept=".pdf"
        @change="handleFileChange"
      />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { Button } from '@/components/ui/button'
  import { 
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent
  } from '@/components/ui/card'
  import {
    Alert,
    AlertTitle,
    AlertDescription
  } from '@/components/ui/alert'
  import { Upload, FileX, AlertCircle } from 'lucide-vue-next'
  
  const router = useRouter()
  const authStore = useAuthStore()
  const fileInput = ref<HTMLInputElement | null>(null)
  const currentResume = ref(null)
  
  const handleUploadClick = () => {
    if (!authStore.isAuthenticated) return
    fileInput.value?.click()
  }
  
  const handleFileChange = (event: Event) => {
    const input = event.target as HTMLInputElement
    if (!input.files?.length) return
  
    const file = input.files[0]
    // Here you would typically:
    // 1. Validate file type and size
    // 2. Upload to your backend
    // 3. Update the currentResume ref
    console.log('File selected:', file)
    
    // Reset input
    input.value = ''
  }
  </script>