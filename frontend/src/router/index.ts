// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/Home.vue'
import Jobs from '@/views/Jobs.vue'
import Analytics from '@/views/Analytics.vue'
import Market from '@/views/JobMarket.vue'

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
      component: Jobs,
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: Analytics,
    },
    {
      path: '/market',
      name: 'market',
      component: Market,
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('../views/Resume.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
    }
  ]
})

// Simple navigation guard to save the previous route
router.beforeEach((to, from, next) => {
  // Only add redirect if:
  // 1. Going to login
  // 2. Coming from a non-auth page
  // 3. Don't already have a redirect query
  if (
    to.path === '/login' && 
    !['/login', '/register'].includes(from.path) && 
    !to.query.redirect
  ) {
    next({ 
      path: '/login',
      query: { redirect: from.path }
    })
  } else {
    next()
  }
})

// Remove navigation guard completely for now
export default router