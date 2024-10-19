<template>
  <div class="container mx-auto py-6 space-y-8">
    <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">Graduate Statistics</h1>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <Card class="w-full">
        <CardHeader>
          <CardTitle>Top 10 In-Demand Skills</CardTitle>
        </CardHeader>
        <CardContent>
          <SkillsDemand :skills-data="topSkills" />
        </CardContent>
      </Card>

      <Card class="w-full">
        <CardHeader>
          <CardTitle>Graduate Pay Statistics</CardTitle>
        </CardHeader>
        <CardContent>
          <GraduatePay :employment-data="graduatePayData[0]?.employment_stats || []" />
        </CardContent>
      </Card>

      <Card class="w-full lg:col-span-2">
        <CardHeader>
          <CardTitle>Graduate Employment Statistics</CardTitle>
        </CardHeader>
        <CardContent>
          <EmploymentStats :employment-data="graduatePayData[0]?.employment_stats || []" />
        </CardContent>
      </Card>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { getTopSkills, getGraduateStartingPayData } from '@/services/api';
  import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
  import SkillsDemand from '@/components/SkillsDemand.vue';
  import GraduatePay from '@/components/GraduatePay.vue';
  import EmploymentStats from '@/components/EmploymentStats.vue';
  
  const topSkills = ref<Array<{ skill: string; count: number }>>([]);
  const graduatePayData = ref<Array<{
    institution_type: string;
    updated_at: string;
    employment_stats: Array<{
      year: number;
      employed_percentage: number;
      full_time_permanent_percentage: number;
      median_gross_monthly_starting_salary: number;
    }>;
  }>>([]);
  
  onMounted(async () => {
    try {
      topSkills.value = await getTopSkills();
      graduatePayData.value = await getGraduateStartingPayData();
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    }
  });
  </script>