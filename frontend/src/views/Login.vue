<!-- Login.vue -->
<template>
  <div class="flex min-h-screen items-center justify-center">
    <Card class="w-[350px]">
      <CardHeader>
        <CardTitle>Login</CardTitle>
        <CardDescription>Enter your credentials to sign in</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleLogin" class="space-y-4">
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
            <Input id="password" v-model="password" type="password" required />
          </div>
          <Alert v-if="authStore.error" variant="destructive">
            <AlertDescription>
              {{ authStore.error }}
            </AlertDescription>
          </Alert>
          <Button type="submit" class="w-full" :disabled="authStore.loading">
            <Loader2 v-if="authStore.loading" class="mr-2 h-4 w-4 animate-spin" />
            {{ authStore.loading ? 'Signing in...' : 'Sign in' }}
          </Button>
        </form>
      </CardContent>
      <CardFooter class="flex justify-center">
        <p class="text-sm text-muted-foreground">
          Don't have an account?
          <router-link to="/register" class="text-primary hover:underline"> Sign up </router-link>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
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
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    await authStore.login(username.value, password.value)

    // Get redirect path from query params, fallback to '/' if none exists
    const redirectPath = route.query.redirect?.toString() || '/'

    // Ensure we don't redirect back to login or register
    if (redirectPath === '/login' || redirectPath === '/register') {
      router.push('/')
    } else {
      router.push(redirectPath)
    }
  } catch (error) {
    console.error('Login error:', error)
  }
}
</script>
