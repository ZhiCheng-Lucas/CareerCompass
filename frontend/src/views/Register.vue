<template>
    <div class="flex min-h-screen items-center justify-center">
      <Card class="w-[350px]">
        <CardHeader>
          <CardTitle>Create Account</CardTitle>
          <CardDescription>Enter your details to sign up</CardDescription>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="handleRegister" class="space-y-4">
            <div class="space-y-2">
              <Label for="email">Email</Label>
              <Input
                id="email"
                v-model="username"
                type="email"
                placeholder="user@example.com"
                required
              />
            </div>
            <div class="space-y-2">
              <Label for="password">Password</Label>
              <Input
                id="password"
                v-model="password"
                type="password"
                required
                @input="isPasswordValid = password.length >= 10"
              />
              <p class="text-sm text-muted-foreground" :class="{ 'text-red-500': password.length > 0 && !isPasswordValid }">
                Password must be at least 10 characters long
              </p>
            </div>
            <Alert v-if="authStore.error" variant="destructive">
              <AlertDescription>
                {{ authStore.error }}
              </AlertDescription>
            </Alert>
            <Button
              type="submit"
              class="w-full"
              :disabled="!isPasswordValid || authStore.loading"
            >
              <Loader2 v-if="authStore.loading" class="mr-2 h-4 w-4 animate-spin" />
              {{ authStore.loading ? 'Creating account...' : 'Create account' }}
            </Button>
          </form>
        </CardContent>
        <CardFooter class="flex justify-center">
          <p class="text-sm text-muted-foreground">
            Already have an account?
            <router-link
              to="/login"
              class="text-primary hover:underline"
            >
              Sign in
            </router-link>
          </p>
        </CardFooter>
      </Card>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { Loader2 } from 'lucide-vue-next'
  import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    CardFooter
  } from '@/components/ui/card'
  import { Input } from '@/components/ui/input'
  import { Label } from '@/components/ui/label'
  import { Button } from '@/components/ui/button'
  import { Alert, AlertDescription } from '@/components/ui/alert'
  
  const router = useRouter()
  const authStore = useAuthStore()
  
  const username = ref('')
  const password = ref('')
  const isPasswordValid = ref(false)
  
  const handleRegister = async () => {
    if (!isPasswordValid.value) return
    
    try {
      await authStore.register(username.value, password.value)
      router.push('/jobs')
    } catch (error) {
      // Error is handled in the store
    }
  }
  </script>
