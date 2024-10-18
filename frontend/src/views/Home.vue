<template>
  <div class="space-y-8 p-6">
    <header class="text-center">
      <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-4">
        Welcome to CareerCompass
      </h1>
      <p class="text-xl text-muted-foreground max-w-2xl mx-auto">
        Navigate your career journey with precision using our AI-powered job search and analysis tools.
      </p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card v-for="feature in features" :key="feature.title" class="flex flex-col">
        <CardHeader>
          <div class="text-3xl mb-4">{{ feature.icon }}</div>
          <CardTitle>{{ feature.title }}</CardTitle>
        </CardHeader>
        <CardContent class="flex-grow">
          <p>{{ feature.description }}</p>
        </CardContent>
      </Card>
    </div>

    <div class="text-center">
      <Button @click="startJobSearch" variant="default" size="lg">
        Start Your Job Search
      </Button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const router = useRouter();

const features = [
  {
    icon: '🔍',
    title: 'Smart Job Search',
    description: 'Find the perfect job using our AI-powered search engine tailored to your skills and preferences.'
  },
  {
    icon: '📊',
    title: 'Market Insights',
    description: 'Stay informed with real-time analytics on job market trends, salary distributions, and in-demand skills.'
  },
  {
    icon: '📝',
    title: 'Resume Optimizer',
    description: 'Enhance your resume with our AI-driven suggestions to increase your chances of landing interviews.'
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
    description: 'Explore detailed information about various industries and their growth projections.'
  }
];

const startJobSearch = () => {
  router.push('/jobs');
};
</script>