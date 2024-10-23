import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/Home.vue'
import Jobs from '@/views/Jobs.vue'
import Analytics from '@/views/Analytics.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: Jobs
      // Removed requiresAuth meta
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: Analytics
      // Removed requiresAuth meta
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('../views/Resume.vue')
      // Resume page will handle auth state internally
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
      meta: { requiresGuest: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Handle routes that require guest access (login/register)
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }
  next()
})

export default router