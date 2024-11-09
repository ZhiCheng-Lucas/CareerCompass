<template>
  <div class="container mx-auto p-4 sm:p-6">
    <!-- Error Alert -->
    <Alert v-if="error" variant="destructive" class="mb-4">
      <AlertCircle class="h-4 w-4" />
      <h3 class="mb-1 font-medium leading-none tracking-tight">Upload Failed</h3>
      <AlertDescription>
        {{ error }}
      </AlertDescription>
    </Alert>

    <!-- Header section -->
    <div class="mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold tracking-tight">Resume Optimiser</h1>
      <p class="text-muted-foreground mt-2">
        Upload your resume for AI optimization, personalized job matches, and targeted skill recommendations.
      </p>
    </div>

    <!-- Upload Card -->
    <Card class="mb-6">
      <CardHeader>
        <h2 class="text-lg font-semibold">Upload Resume</h2>
        <CardDescription> Upload your resume in PDF format. Max file size: 5MB </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <Alert v-if="!authStore.isAuthenticated" variant="default" class="mb-4">
            <AlertCircle class="h-4 w-4" />
            <h3 class="mb-1 font-medium leading-none tracking-tight">Authentication Required</h3>
            <AlertDescription>
              Please sign in to upload and manage your resume.
              <Button variant="link" class="px-0 text-primary" @click="router.push('/login')">
                Sign in here
              </Button>
            </AlertDescription>
          </Alert>
          <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <Button :disabled="!authStore.isAuthenticated || isUploading" @click="handleUploadClick"
              class="w-full sm:w-auto">
              <Upload v-if="!isUploading" class="mr-2 h-4 w-4" />
              <Loader2 v-else class="mr-2 h-4 w-4 animate-spin" />
              {{ isUploading ? 'Uploading...' : 'Upload Resume' }}
            </Button>
            <p v-if="!authStore.isAuthenticated" class="text-sm text-muted-foreground">
              Sign in to enable resume upload
            </p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Analysis Results Section -->
    <div v-if="analysisResults" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Improvements Section -->
      <Card>
        <CardHeader>
          <h2 class="text-lg font-semibold flex items-center">
            <ClipboardCheck class="mr-2 h-5 w-5" />
            Suggested Improvements
          </h2>
        </CardHeader>
        <CardContent>
          <ResumeImprovements :improvements="analysisResults.ai_improvements" />
        </CardContent>
      </Card>

      <!-- Recommended Jobs Section -->
      <Card>
        <CardHeader>
          <h2 class="text-lg font-semibold flex items-center">
            <Briefcase class="mr-2 h-5 w-5" />
            Recommended Jobs
          </h2>
        </CardHeader>
        <CardContent class="max-h-[600px] overflow-y-auto">
          <div class="space-y-4">
            <div v-for="job in analysisResults.recommended_jobs" :key="job.job_link"
              class="p-4 rounded-lg border hover:border-primary transition-colors">
              <h3 class="font-medium">{{ job.job_title }}</h3>
              <p class="text-sm text-muted-foreground">{{ job.company }}</p>
              <div class="flex flex-wrap items-center gap-2 mt-2">
                <Badge variant="secondary">{{ job.match_percentage }}% Match</Badge>
                <a :href="job.job_link" target="_blank" class="text-sm text-primary hover:underline ml-auto">
                  View Job
                </a>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Recommended Skills Section -->
      <Card>
        <CardHeader>
          <h2 class="text-lg font-semibold flex items-center">
            <GraduationCap class="mr-2 h-5 w-5" />
            Skills to Learn
          </h2>
        </CardHeader>
        <CardContent class="max-h-[600px] overflow-y-auto">
          <div class="space-y-4">
            <div v-for="skill in analysisResults.recommended_skills_to_learn" :key="skill.skill"
              class="p-4 rounded-lg border hover:border-primary transition-colors">
              <div class="flex items-center justify-between flex-wrap gap-2">
                <h3 class="font-medium">{{ skill.skill }}</h3>
                <Badge>{{ skill.frequency }} jobs</Badge>
              </div>
              <div class="mt-2">
                <p class="text-sm text-muted-foreground">Relevant roles:</p>
                <div class="flex flex-wrap gap-1 mt-1">
                  <Badge v-for="job in skill.example_jobs" :key="job" variant="outline" class="text-xs">
                    {{ job }}
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Hidden file input -->
    <input type="file" ref="fileInput" class="hidden" accept=".pdf" @change="handleFileChange" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { uploadResume } from '@/services/api'
import type { APIError } from '@/services/api' // Add this import
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import ResumeImprovements from '../components/ResumeImprovements.vue'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'
import {
  Upload,
  AlertCircle,
  Loader2,
  ClipboardCheck,
  Briefcase,
  GraduationCap
} from 'lucide-vue-next'

interface RecommendedJob {
  job_title: string
  company: string
  job_link: string
  match_percentage: number
  matching_skills: string[]
}

interface RecommendedSkill {
  skill: string
  frequency: number
  example_jobs: string[]
}

interface ResumeAnalysisResponse {
  message: string
  extracted_skills: string[]
  ai_improvements: string
  recommended_jobs: RecommendedJob[]
  recommended_skills_to_learn: RecommendedSkill[]
}

const router = useRouter()
const authStore = useAuthStore()
const fileInput = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)
const analysisResults = ref<ResumeAnalysisResponse | null>(null)
const error = ref<string | null>(null)

const handleUploadClick = () => {
  if (!authStore.isAuthenticated) return
  error.value = null // Clear any previous errors
  fileInput.value?.click()
}

const handleFileChange = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length || !authStore.currentUser?.username) return

  const file = input.files[0]
  if (!file) return

  try {
    error.value = null // Clear any previous errors
    isUploading.value = true
    const response = await uploadResume(file, authStore.currentUser.username)
    analysisResults.value = response

    if (response.extracted_skills && response.extracted_skills.length > 0) {
      authStore.updateUserSkills(response.extracted_skills)
    }
  } catch (err) {
    console.error('Error uploading resume:', err)
    const apiError = err as APIError
    error.value = apiError.message
    analysisResults.value = null // Clear any previous results
  } finally {
    isUploading.value = false
    input.value = '' // Clear the input
  }
}
</script>

<style scoped>
.card-animation-enter-active,
.card-animation-leave-active {
  transition: all 0.5s ease;
}

.card-animation-enter-from,
.card-animation-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.card-animation-enter-to,
.card-animation-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
