<template>
  <div class="space-y-6">
    <!-- Iterate through main categories -->
    <div v-for="(category, categoryKey) in parsedImprovements" :key="categoryKey" class="space-y-4">
      <!-- Main category title -->
      <h2 class="text-xl font-semibold">{{ formatTitle(categoryKey) }}</h2>
      
      <!-- Iterate through subcategories -->
      <Card v-for="(subcategory, subcategoryKey) in category" :key="subcategoryKey">
        <CardHeader>
          <CardTitle class="text-lg font-semibold">
            {{ formatTitle(subcategoryKey) }}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <!-- Display first improvement item -->
          <ul class="space-y-3">
            <li v-if="subcategory.length > 0" class="flex gap-2">
              <span class="flex-shrink-0 text-muted-foreground">•</span>
              <span class="text-sm" v-html="formatText(subcategory[0])"></span>
            </li>
          </ul>

          <!-- Collapsible section for remaining improvements -->
          <Collapsible v-if="subcategory.length > 1" @toggle="(open) => handleCollapsibleChange(categoryKey, subcategoryKey, open)">
            <CollapsibleContent>
              <ul class="space-y-3 mt-3">
                <li v-for="(improvement, index) in subcategory.slice(1)" 
                    :key="index"
                    class="flex gap-2">
                  <span class="flex-shrink-0 text-muted-foreground">•</span>
                  <span class="text-sm" v-html="formatText(improvement)"></span>
                </li>
              </ul>
            </CollapsibleContent>

            <CollapsibleTrigger class="w-full">
              <Button variant="ghost" class="w-full mt-2 hover:bg-muted/50">
                <span class="flex items-center gap-2">
                  <ChevronDown
                    class="h-4 w-4 transition-transform duration-200"
                    :class="{ 'rotate-180': isOpenMap[`${categoryKey}-${subcategoryKey}`] }"
                  />
                  {{ isOpenMap[`${categoryKey}-${subcategoryKey}`] 
                     ? 'Show less' 
                     : `Show ${subcategory.length - 1} more` }}
                </span>
              </Button>
            </CollapsibleTrigger>
          </Collapsible>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger
} from '@/components/ui/collapsible'
import { ChevronDown } from 'lucide-vue-next'

interface ImprovementData {
  language_and_clarity: {
    grammar_spelling: string[];
    sentence_structure: string[];
  };
  experience_and_achievements: {
    job_descriptions: string[];
    metrics_and_results: string[];
    suggested_additions: string[];
  };
  skills_and_qualifications: {
    skill_improvements: string[];
    qualification_enhancements: string[];
  };
}

interface Props {
  improvements: string;
}

const props = defineProps<Props>()

// Track collapse state for each subcategory
const isOpenMap = ref<Record<string, boolean>>({})

// Parse the JSON string into our data structure
const parsedImprovements = computed<ImprovementData>(() => {
  try {
    // Clean the JSON string by removing markdown code block syntax
    const cleanJson = props.improvements
      .replace(/^```json\n/, '') // Remove starting ```json
      .replace(/\n```$/, '')     // Remove ending ```
    
    return JSON.parse(cleanJson)
  } catch (error) {
    console.error('Error parsing improvements JSON:', error)
    // Return empty structure if parsing fails
    return {
      language_and_clarity: {
        grammar_spelling: [],
        sentence_structure: []
      },
      experience_and_achievements: {
        job_descriptions: [],
        metrics_and_results: [],
        suggested_additions: []
      },
      skills_and_qualifications: {
        skill_improvements: [],
        qualification_enhancements: []
      }
    }
  }
})

// Watch for changes in parsed improvements to reset collapse states
watch(parsedImprovements, () => {
  isOpenMap.value = {}
}, { deep: true })

// Format category and subcategory titles for display
const formatTitle = (key: string): string => {
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// Format text content with emphasis
const formatText = (text: string): string => {
  return text.replace(
    /\*\*(.*?)\*\*/g, 
    '<span class="font-semibold text-primary">$1</span>'
  )
}

// Handle Collapsible state changes
const handleCollapsibleChange = (categoryKey: string, subcategoryKey: string, isOpen: boolean) => {
  isOpenMap.value[`${categoryKey}-${subcategoryKey}`] = isOpen
}
</script>

<style scoped>
.space-y-6 > :not([hidden]) ~ :not([hidden]) {
  margin-top: 1.5rem;
}

.space-y-4 > :not([hidden]) ~ :not([hidden]) {
  margin-top: 1rem;
}

.space-y-3 > :not([hidden]) ~ :not([hidden]) {
  margin-top: 0.75rem;
}
</style>