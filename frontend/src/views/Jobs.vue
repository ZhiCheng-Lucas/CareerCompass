<template>
  <div class="container mx-auto py-6 space-y-6">
    <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">Job Search</h1>

    <Card class="w-full">
      <CardHeader>
        <h2 class="font-semibold text-lg leading-none tracking-tight">Search for Jobs</h2>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="search" class="space-y-4">
          <div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
            <div class="flex-grow">
              <Label for="searchQuery">Search</Label>
              <Input id="searchQuery" v-model="searchQuery" :placeholder="getPlaceholderText" />
              <p v-if="searchType === 'skills'" class="text-sm text-muted-foreground mt-1">
                Separate multiple skills with commas (e.g., "JavaScript, React, TypeScript")
              </p>
            </div>
            <div class="w-full md:w-1/4">
              <Label for="searchType">Search By</Label>
              <Select v-model="searchType">
                <SelectTrigger aria-label="Select search type">
                  <SelectValue :placeholder="searchType || 'Select search type'" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="title">Title</SelectItem>
                  <SelectItem value="company">Company</SelectItem>
                  <SelectItem value="skills">Skills</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <Button type="submit" class="w-full md:w-auto">Search</Button>
        </form>
      </CardContent>
    </Card>

    <div v-if="loading" class="text-center space-y-2">
      <Progress :value="progressValue" class="w-[60%] mx-auto" />
      <p class="text-lg text-muted-foreground">Loading jobs...</p>
    </div>

    <div v-else-if="error" class="text-center">
      <p class="text-lg text-destructive">{{ error }}</p>
    </div>

    <div v-else-if="jobs.length === 0" class="text-center">
      <p class="text-lg text-muted-foreground">No jobs found. Try adjusting your search.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <Card v-for="job in jobs" :key="job.id" class="w-full">
        <CardHeader>
          <div class="flex justify-between items-start gap-2">
            <h3 class="font-semibold">{{ job.job_title }}</h3>
            <Badge v-if="authStore.isAuthenticated" :variant="getMatchBadgeVariant(job.skills)"
              class="whitespace-nowrap"
              :title="`You match ${getSkillMatchCount(job.skills)} out of ${job.skills.length} required skills`">
              {{ getMatchPercentage(job.skills) }}% match
            </Badge>
          </div>
          <CardDescription>{{ job.company }}</CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground">Posted on: {{ formatDate(job.date) }}</p>
          <div class="mt-4">
            <h4 class="font-semibold">Skills:</h4>
            <div class="flex flex-wrap gap-2 mt-2">
              <Badge v-for="skill in job.skills" :key="skill" :variant="isSkillMatch(skill) ? 'default' : 'secondary'"
                class="cursor-pointer" @click="searchBySkill(skill)">
                {{ skill }}
                <span v-if="isSkillMatch(skill)" class="ml-1 text-xs" title="You have this skill">✓</span>
              </Badge>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="outline" @click="openJobLink(job.job_link)"
            :aria-label="`View job posting for ${job.job_title} at ${job.company}`">
            View Job Posting
          </Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getAllJobs, getJobsByTitle, getJobsByCompany, getJobsBySkills } from '@/services/api'
import type { Job } from '@/types/job'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Card,
  CardHeader,
  CardDescription,
  CardContent,
  CardFooter
} from '@/components/ui/card'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'

const authStore = useAuthStore()
const jobs = ref<Job[]>([])
const searchQuery = ref('')
const searchType = ref('title')
const loading = ref(false)
const error = ref<string | null>(null)
const progressValue = ref(0)

const getPlaceholderText = computed(() => {
  switch (searchType.value) {
    case 'skills':
      return 'Enter skills separated by commas (e.g., JavaScript, React)'
    case 'title':
      return 'Enter job title'
    case 'company':
      return 'Enter company name'
    default:
      return 'Enter search terms'
  }
})

const isAuthenticated = computed(() => authStore.isAuthenticated)
const userSkills = computed(() => authStore.user?.skills || [])

// Function to check if a skill matches user's skills (case-insensitive)
const isSkillMatch = (skill: string) => {
  if (!isAuthenticated.value) return false
  return userSkills.value.some(
    userSkill => userSkill.toLowerCase() === skill.toLowerCase()
  )
}

const getSkillMatchCount = (jobSkills: string[]) => {
  if (!isAuthenticated.value) return 0
  return jobSkills.filter(skill => isSkillMatch(skill)).length
}

const getMatchPercentage = (jobSkills: string[]) => {
  if (!isAuthenticated.value || jobSkills.length === 0) return 0
  const matchCount = getSkillMatchCount(jobSkills)
  return Math.round((matchCount / jobSkills.length) * 100)
}

const getMatchBadgeVariant = (jobSkills: string[]) => {
  const matchPercentage = getMatchPercentage(jobSkills)

  if (matchPercentage >= 75) return 'default'
  if (matchPercentage >= 50) return 'secondary'
  return 'outline'
}

const parseSkills = (skillsString: string): string[] => {
  return skillsString
    .split(',')
    .map(skill => skill.trim())
    .filter(skill => skill.length > 0)
}

const search = async () => {
  loading.value = true
  error.value = null
  progressValue.value = 0

  const updateProgress = () => {
    progressValue.value += 10
    if (progressValue.value < 90 && loading.value) {
      setTimeout(updateProgress, 200)
    }
  }
  updateProgress()

  try {
    if (!searchQuery.value) {
      jobs.value = await getAllJobs()
    } else {
      switch (searchType.value) {
        case 'title':
          jobs.value = await getJobsByTitle(searchQuery.value)
          break
        case 'company':
          jobs.value = await getJobsByCompany(searchQuery.value)
          break
        case 'skills':
          const skills = parseSkills(searchQuery.value)
          if (skills.length === 0) {
            error.value = 'Please enter at least one skill'
            jobs.value = []
            return
          }
          jobs.value = await getJobsBySkills(skills)
          break
      }
    }
  } catch (err) {
    console.error('Error fetching jobs:', err)
    error.value = 'An error occurred while fetching jobs. Please try again.'
    jobs.value = []
  } finally {
    loading.value = false
    progressValue.value = 100
  }
}

const searchBySkill = (skill: string) => {
  searchType.value = 'skills'
  searchQuery.value = skill
  search()
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const openJobLink = (url: string) => {
  window.open(url, '_blank', 'noopener,noreferrer')
}

// Initial search on component mount
onMounted(() => {
  search()
})
</script>