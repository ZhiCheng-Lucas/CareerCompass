<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTopSkills, getGraduateStartingPayData, getUniversityStats } from '@/services/api'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import SkillsDemand from '@/components/SkillsDemand.vue'
import GraduatePay from '@/components/GraduatePay.vue'
import EmploymentStats from '@/components/EmploymentStats.vue'
import GraduateStats from '@/components/GraduateStats.vue'
import type { UniversityMap } from '@/types/university'

interface Skill {
  skill: string
  count: number
}

interface EmploymentStat {
  year: number
  employed_percentage: number
  full_time_permanent_percentage: number
  median_gross_monthly_starting_salary: number
}

interface GraduatePayData {
  institution_type: string
  updated_at: string
  employment_stats: EmploymentStat[]
}

const topSkills = ref<Skill[]>([])
const graduatePayData = ref<GraduatePayData[]>([])
const universityStats = ref<UniversityMap>({})

onMounted(async () => {
  try {
    const [skills, payData, stats] = await Promise.all([
      getTopSkills(),
      getGraduateStartingPayData(),
      getUniversityStats()
    ])

    topSkills.value = skills
    graduatePayData.value = payData
    universityStats.value = stats
  } catch (error) {
    console.error('Error fetching analytics data:', error)
  }
})
</script>

<template>
  <div class="container mx-auto py-6 space-y-8">
    <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
      Graduate Statistics
    </h1>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <Card class="w-full">
        <CardHeader>
          <!-- Changed from CardTitle to h2 as suggested by GovTech OObee's Accessibility checker 
               to maintain proper heading hierarchy under the main h1 -->
          <h2 class="text-2xl font-semibold tracking-tight">Top 10 In-Demand Skills</h2>
        </CardHeader>
        <CardContent>
          <SkillsDemand :skills-data="topSkills" />
        </CardContent>
      </Card>
      <Card class="w-full">
        <CardHeader>
          <!-- Changed from CardTitle to h2 as suggested by GovTech OObee's Accessibility checker 
               to maintain proper heading hierarchy under the main h1 -->
          <h2 class="text-2xl font-semibold tracking-tight">Graduate Pay Statistics</h2>
        </CardHeader>
        <CardContent>
          <GraduatePay :employment-data="graduatePayData[0]?.employment_stats || []" />
        </CardContent>
      </Card>
      <Card class="w-full lg:col-span-2">
        <CardHeader>
          <!-- Changed from CardTitle to h2 as suggested by GovTech OObee's Accessibility checker 
               to maintain proper heading hierarchy under the main h1 -->
          <h2 class="text-2xl font-semibold tracking-tight">Graduate Employment Statistics</h2>
        </CardHeader>
        <CardContent>
          <EmploymentStats :employment-data="graduatePayData[0]?.employment_stats || []" />
        </CardContent>
      </Card>
      <div class="w-full lg:col-span-2">
        <GraduateStats :university-data="universityStats" />
      </div>
    </div>
  </div>
</template>
