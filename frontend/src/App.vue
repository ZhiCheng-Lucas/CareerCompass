<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- Desktop Navigation (lg and above) -->
    <nav v-if="!isMobile" class="bg-background border-b border-border">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 justify-between">
          <div class="flex">
            <div class="flex flex-shrink-0 items-center">
              <ThemeAwareLogo />
            </div>
            <div class="ml-6 flex space-x-8">
              <router-link
                to="/"
                class="nav-link"
                :class="{ 'active': $route.path === '/' }"
              >
                Home
              </router-link>
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
            <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
              <span class="text-sm text-muted-foreground">
                {{ authStore.currentUser?.username }}
              </span>
              <Button variant="outline" size="sm" @click="handleLogout">
                Log out
              </Button>
            </div>
            <div v-else class="flex items-center space-x-2">
              <Button variant="ghost" size="sm" @click="router.push('/login')">
                Sign in
              </Button>
              <Button variant="default" size="sm" @click="router.push('/register')">
                Register
              </Button>
            </div>
            <ThemeToggle />
            <AccessibilityOptions />
          </div>
        </div>
      </div>
    </nav>

    <!-- Mobile Layout (below lg) -->
    <div v-else>
      <!-- Mobile Header -->
      <div class="fixed top-0 left-0 right-0 z-40 border-b border-border bg-background">
        <div class="flex h-16 items-center justify-between px-4">
          <Button variant="ghost" size="sm" class="p-2" @click="isOpen = true">
            <Menu class="h-5 w-5" />
          </Button>
          <ThemeAwareLogo />
          <div class="w-10" />
        </div>
      </div>

      <!-- Mobile Drawer -->
      <Drawer
        v-model:open="isOpen"
        direction="left"
        :fixed="true"
        :modal="true"
        :dismissible="true"
      >
        <DrawerContent class="h-[100dvh] w-[300px] bg-background border-r border-border">
          <div class="flex h-full flex-col">
            <!-- Drawer Header -->
            <div class="border-b border-border p-4">
              <div class="flex items-center justify-between">
                <ThemeAwareLogo />
                <Button variant="ghost" size="sm" @click="isOpen = false">
                  <X class="h-5 w-5" />
                </Button>
              </div>
            </div>

            <!-- Navigation Links -->
            <div class="flex-1 overflow-y-auto">
              <div class="p-4 space-y-2">
                <router-link
                  v-for="link in navigationLinks"
                  :key="link.path"
                  :to="link.path"
                  v-show="!link.requiresAuth || authStore.isAuthenticated"
                  class="flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors"
                  :class="[
                    $route.path === link.path 
                      ? 'bg-primary/10 text-primary' 
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                  ]"
                  @click="isOpen = false"
                >
                  <component :is="link.icon" class="mr-3 h-5 w-5" />
                  {{ link.name }}
                </router-link>
              </div>

              <!-- Settings Section -->
              <div class="p-4 border-t border-border">
                <p class="px-3 py-2 text-sm font-medium text-muted-foreground">Settings</p>
                <div class="space-y-2 mt-2">
                  <div class="flex items-center justify-between rounded-md px-3 py-2 hover:bg-accent">
                    <span class="text-sm font-medium">Theme</span>
                    <ThemeToggle />
                  </div>
                  <div class="flex items-center justify-between rounded-md px-3 py-2 hover:bg-accent">
                    <span class="text-sm font-medium">Accessibility</span>
                    <AccessibilityOptions />
                  </div>
                </div>
              </div>
            </div>

            <!-- Auth Section -->
            <div class="border-t border-border p-4">
              <div v-if="authStore.isAuthenticated" class="space-y-4">
                <p class="text-sm text-muted-foreground">
                  Signed in as {{ authStore.currentUser?.username }}
                </p>
                <Button variant="outline" class="w-full" @click="handleLogoutAndClose">
                  Log out
                </Button>
              </div>
              <div v-else class="space-y-2">
                <Button variant="outline" class="w-full" @click="handleNavigate('/login')">
                  Sign in
                </Button>
                <Button variant="default" class="w-full" @click="handleNavigate('/register')">
                  Register
                </Button>
              </div>
            </div>
          </div>
        </DrawerContent>
      </Drawer>
    </div>

    <!-- Main content -->
    <main class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8" :class="{ 'mt-16': isMobile }">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="border-t border-border bg-background">
      <div class="mx-auto max-w-7xl py-4 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-muted-foreground">
          © 2024 CareerCompass. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'
import AccessibilityOptions from '@/components/AccessibilityOptions.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import ThemeAwareLogo from '@/components/ThemeAwareLogo.vue'
import { Button } from '@/components/ui/button'
import { Drawer, DrawerContent } from '@/components/ui/drawer'
import { Menu, X, Home, Briefcase, FileText, ChartBar } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const isOpen = ref(false)
const windowWidth = ref(window.innerWidth)

// Responsive handling
const isMobile = computed(() => windowWidth.value < 1024) // lg breakpoint

const handleResize = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const navigationLinks = [
  { name: 'Home', path: '/', icon: Home, requiresAuth: false },
  { name: 'Jobs', path: '/jobs', icon: Briefcase, requiresAuth: true },
  { name: 'Resume', path: '/resume', icon: FileText, requiresAuth: true },
  { name: 'Analytics', path: '/analytics', icon: ChartBar, requiresAuth: true }
]

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

// // For Govtech Purple A11y Testing.
// onMounted(async () => {
//   await authStore.login('pokemongo@gmail.com', '9YtupB9E4B3TpPG!DcAK')
// })
// 
const handleLogoutAndClose = () => {
  handleLogout()
  isOpen.value = false
}

const handleNavigate = (path: string) => {
  router.push(path)
  isOpen.value = false
}
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
@import '@/assets/index.css';

.nav-link {
  @apply inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium;
  @apply border-transparent text-muted-foreground;
  @apply hover:border-border hover:text-foreground;
}

.nav-link.active {
  @apply border-primary text-foreground;
}
</style>