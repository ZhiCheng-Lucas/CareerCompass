<template>
  <div class="space-y-8 p-6">
    <header class="text-center">
      <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-4">
        Welcome to CareerCompass
      </h1>
      <p class="text-xl text-muted-foreground max-w-2xl mx-auto">
        Navigate your career journey with precision using our AI-powered job search and analysis
        tools.
      </p>
    </header>
    <TransitionGroup name="card-animation" tag="div" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card v-for="(feature, index) in features" :key="feature.title"
        class="flex flex-col transform transition-all duration-300 hover:scale-105 hover:shadow-lg bg-opacity-20 backdrop-blur-lg">
        <CardHeader>
          <div class="text-3xl mb-4">{{ feature.icon }}</div>
          <!-- Changed from CardTitle to h2 as suggested by GovTech OObee's Accessibility checker 
               to ensure feature titles are properly marked up as headings under the main h1 -->
          <h2 class="font-semibold text-lg">{{ feature.title }}</h2>
        </CardHeader>
        <CardContent class="flex-grow">
          <p>{{ feature.description }}</p>
        </CardContent>
      </Card>
    </TransitionGroup>
    <div class="text-center">
      <Button @click="startJobSearch" variant="default" size="lg"
        class="relative overflow-hidden border-2 border-transparent hover:border-transparent transition-all duration-300 ease-in-out transform hover:scale-105 animated-border">
        Start your job search
      </Button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

const router = useRouter()

const features = [
  {
    icon: '🔍',
    title: 'Smart Job Search',
    description:
      'Find the perfect job using our AI-powered search engine tailored to your skills and preferences.'
  },
  {
    icon: '📊',
    title: 'Market Insights',
    description:
      'Stay informed with real-time analytics on job market trends, salary distributions, and in-demand skills.'
  },
  {
    icon: '📝',
    title: 'Resume Optimizer',
    description:
      'Enhance your resume with our AI-driven suggestions to increase your chances of landing interviews.'
  },
  {
    icon: '🎯',
    title: 'Personalized Recommendations',
    description: 'Receive job suggestions that match your profile and career aspirations.'
  },
  {
    icon: '📈',
    title: 'Career Growth Tools',
    description: 'Access resources and tools to plan your career progression and skill development.'
  },
  {
    icon: '🌐',
    title: 'Industry Insights',
    description:
      'Explore detailed information about various industries and their growth projections.'
  }
]

const startJobSearch = () => {
  router.push('/jobs')
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

.card {
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  transition: all 0.3s ease;
}

.card:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-5px);
}

.button {
  position: relative;
  overflow: hidden;
}

.button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: all 0.6s;
}

.button:hover::before {
  left: 100%;
}
</style>
