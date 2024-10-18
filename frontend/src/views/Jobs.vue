<template>
  <div class="container mx-auto py-6 space-y-6">
    <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">Job Search</h1>

    <Card class="w-full">
      <CardHeader>
        <CardTitle>Search for Jobs</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="search" class="space-y-4">
          <div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
            <div class="flex-grow">
              <Label for="searchQuery">Search</Label>
              <Input id="searchQuery" v-model="searchQuery" placeholder="Enter job title, company, or skills" />
            </div>
            <div class="w-full md:w-1/4">
              <Label for="searchType">Search By</Label>
              <Select v-model="searchType">
                <SelectTrigger>
                  <SelectValue placeholder="Select search type" />
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

    <div v-else class="space-y-4">
      <Card v-for="job in jobs" :key="job.id" class="w-full">
        <CardHeader>
          <CardTitle>{{ job.job_title }}</CardTitle>
          <CardDescription>{{ job.company }}</CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground">Posted on: {{ formatDate(job.date) }}</p>
          <div class="mt-4">
            <h3 class="font-semibold">Skills:</h3>
            <div class="flex flex-wrap gap-2 mt-2">
              <Badge v-for="skill in job.skills" :key="skill" variant="secondary">
                {{ skill }}
              </Badge>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="outline" @click="openJobLink(job.job_link)">
            View Job Posting
          </Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { getAllJobs, getJobsByTitle, getJobsByCompany, getJobsBySkills } from '@/services/api';
import type { Job } from '@/types/job';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

const jobs = ref<Job[]>([]);
const searchQuery = ref('');
const searchType = ref('title');
const loading = ref(false);
const error = ref<string | null>(null);
const progressValue = ref(0);

const search = async () => {
  loading.value = true;
  error.value = null;
  progressValue.value = 0;

  const updateProgress = () => {
    progressValue.value += 10;
    if (progressValue.value < 90 && loading.value) {
      setTimeout(updateProgress, 200);
    }
  };
  updateProgress();

  try {
    if (!searchQuery.value) {
      jobs.value = await getAllJobs();
    } else {
      switch (searchType.value) {
        case 'title':
          jobs.value = await getJobsByTitle(searchQuery.value);
          break;
        case 'company':
          jobs.value = await getJobsByCompany(searchQuery.value);
          break;
        case 'skills':
          const skills = searchQuery.value.split(',').map(skill => skill.trim());
          jobs.value = await getJobsBySkills(skills);
          break;
      }
    }
  } catch (err) {
    console.error('Error fetching jobs:', err);
    error.value = 'An error occurred while fetching jobs. Please try again.';
    jobs.value = [];
  } finally {
    loading.value = false;
    progressValue.value = 100;
  }
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
};

const openJobLink = (url: string) => {
  window.open(url, '_blank', 'noopener,noreferrer');
};

onMounted(() => {
  search(); // Initial search on component mount
});
</script>