<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { LineChart } from '@/components/ui/chart-line'

// Types
interface CourseStatistics {
  employment_rate_overall: { [year: string]: number };
  gross_monthly_mean: { [year: string]: number };
}

interface UniversityData {
  [key: string]: {
    [key: string]: {
      [key: string]: CourseStatistics;
    };
  };
}

interface ChartDataPoint {
  year: string;
  [key: string]: string | number;
}

interface SelectOption {
  value: string;
  label: string;
  indent: number;
  type: 'university' | 'faculty' | 'course';
}

// Props
interface Props {
  universityData: UniversityData;
}

const props = defineProps<Props>()

// State
const selectedPath = ref<string>('')
const selectedMetric = ref<'employment_rate_overall' | 'gross_monthly_mean'>('employment_rate_overall')

// Generate hierarchical options for the single dropdown
const courseOptions = computed<SelectOption[]>(() => {
  const options: SelectOption[] = []

  Object.entries(props.universityData).forEach(([university, faculties]) => {
    // Add university
    options.push({
      value: university,
      label: university,
      indent: 0,
      type: 'university'
    })

    Object.entries(faculties).forEach(([faculty, courses]) => {
      // Add faculty
      options.push({
        value: `${university}|${faculty}`,
        label: faculty,
        indent: 1,
        type: 'faculty'
      })

      Object.keys(courses).forEach(course => {
        // Add course
        options.push({
          value: `${university}|${faculty}|${course}`,
          label: course,
          indent: 2,
          type: 'course'
        })
      })
    })
  })

  return options
})

// Format chart data
const chartData = computed(() => {
  const [university, faculty, course] = selectedPath.value.split('|')
  if (!university || !faculty || !course) return []

  const courseData = props.universityData[university]?.[faculty]?.[course]
  if (!courseData) return []

  const metric = selectedMetric.value
  const dataPoints = metric === 'employment_rate_overall' 
    ? courseData.employment_rate_overall 
    : courseData.gross_monthly_mean

  return Object.entries(dataPoints)
    .map(([year, value]) => ({
      year,
      [metric === 'employment_rate_overall' ? 'Employment Rate' : 'Monthly Salary']: value
    }))
    .sort((a, b) => Number(a.year) - Number(b.year))
})

const chartCategories = computed(() => 
  [selectedMetric.value === 'employment_rate_overall' ? 'Employment Rate' : 'Monthly Salary']
)

// Format y-axis values
const yFormatter = (tick: number | Date, i: number, ticks: Array<number | Date>) => {
  if (tick instanceof Date) return ''
  
  if (selectedMetric.value === 'employment_rate_overall') {
    return `${tick.toFixed(1)}%`
  } else {
    return `$${new Intl.NumberFormat('en-US').format(tick)}`
  }
}

// Metric options
const metricOptions = [
  { value: 'employment_rate_overall', label: 'Employment Rate' },
  { value: 'gross_monthly_mean', label: 'Monthly Salary' }
] as const
</script>

<template>
  <Card class="w-full">
    <CardHeader>
      <CardTitle>Graduate Statistics</CardTitle>
      <div class="flex flex-col gap-4 sm:flex-row">
        <Select v-model="selectedPath" class="flex-1">
          <SelectTrigger>
            <SelectValue placeholder="Select Course" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem 
              v-for="option in courseOptions" 
              :key="option.value" 
              :value="option.value"
              :disabled="option.type !== 'course'"
              class="flex items-center"
            >
              <span 
                :class="{
                  'ml-0': option.indent === 0,
                  'ml-4': option.indent === 1,
                  'ml-8': option.indent === 2,
                  'font-bold': option.indent === 0,
                  'font-medium': option.indent === 1,
                }"
              >
                {{ option.label }}
              </span>
            </SelectItem>
          </SelectContent>
        </Select>

        <Select v-model="selectedMetric" class="w-full sm:w-[200px]">
          <SelectTrigger>
            <SelectValue placeholder="Select Metric" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem 
              v-for="option in metricOptions" 
              :key="option.value" 
              :value="option.value"
            >
              {{ option.label }}
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
    </CardHeader>
    <CardContent>
      <div class="h-[400px] w-full">
        <LineChart
          :data="chartData"
          index="year"
          :categories="chartCategories"
          :y-formatter="yFormatter"
        />
      </div>
    </CardContent>
  </Card>
</template>