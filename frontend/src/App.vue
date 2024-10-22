<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- Navigation -->
    <nav class="bg-background border-b border-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <ThemeAwareLogo />
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="nav-link"
                :class="{ 'active': $route.path === '/' }"
              >
                Home
              </router-link>
              <!-- Only show these links when authenticated -->
              <template v-if="authStore.isAuthenticated">
                <router-link
                  to="/jobs"
                  class="nav-link"
                  :class="{ 'active': $route.path === '/jobs' }"
                >
                  Jobs
                </router-link>
                <router-link
                  to="/resume"
                  class="nav-link"
                  :class="{ 'active': $route.path === '/resume' }"
                >
                  Resume
                </router-link>
                <router-link
                  to="/analytics"
                  class="nav-link"
                  :class="{ 'active': $route.path === '/analytics' }"
                >
                  Analytics
                </router-link>
              </template>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Auth buttons -->
            <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
              <span class="text-sm text-muted-foreground">
                {{ authStore.currentUser?.username }}
              </span>
              <Button 
                variant="outline" 
                size="sm"
                @click="handleLogout"
              >
                Log out
              </Button>
            </div>
            <div v-else class="flex items-center space-x-2">
              <Button 
                variant="ghost" 
                size="sm"
                @click="router.push('/login')"
              >
                Sign in
              </Button>
              <Button 
                variant="default" 
                size="sm"
                @click="router.push('/register')"
              >
                Register
              </Button>
            </div>
            <ThemeToggle />
            <AccessibilityOptions />
          </div>
        </div>
      </div>
    </nav>
    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view></router-view>
    </main>
    <!-- Footer -->
    <footer class="bg-background border-t border-border">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-muted-foreground">
          © 2024 CareerCompass. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AccessibilityOptions from '@/components/AccessibilityOptions.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import ThemeAwareLogo from '@/components/ThemeAwareLogo.vue'
import { Button } from '@/components/ui/button'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
@import '@/assets/index.css';

/* Add these styles for the navigation links */
.nav-link {
  @apply inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium;
  @apply text-muted-foreground border-transparent;
  @apply hover:border-border hover:text-foreground;
}
.nav-link.active {
  @apply border-primary text-foreground;
}
</style>