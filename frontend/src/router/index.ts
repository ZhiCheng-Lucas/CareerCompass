import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/Home.vue'
import JobsView from '@/views/Jobs.vue'
import MarketInsightsView from '@/views/Analytics.vue' // We should also rename this file
import IndustryInsightsView from '@/views/JobMarket.vue' // We should also rename this file
import ResumeView from '@/views/Resume.vue'
import LoginView from '@/views/Login.vue'
import RegisterView from '@/views/Register.vue'

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
      component: JobsView
    },
    {
      path: '/market-insights',
      name: 'market-insights',
      component: MarketInsightsView
    },
    {
      path: '/industry-insights',
      name: 'industry-insights',
      component: IndustryInsightsView
    },
    {
      path: '/resume',
      name: 'resume',
      component: ResumeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    }
  ]
})

// Simple navigation guard to save the previous route
router.beforeEach((to, from, next) => {
  // Only add redirect if:
  // 1. Going to login
  // 2. Coming from a non-auth page
  // 3. Don't already have a redirect query
  if (to.path === '/login' && !['/login', '/register'].includes(from.path) && !to.query.redirect) {
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
