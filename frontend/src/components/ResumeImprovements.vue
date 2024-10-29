<template>
    <div class="space-y-6">
      <Card v-for="(section, index) in improvementSections" :key="index">
        <CardHeader>
          <CardTitle class="text-lg font-semibold">
            {{ section.title }}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul class="space-y-3">
            <!-- Show only first item -->
            <li v-for="(item, itemIndex) in section.items.slice(0, 1)" 
                :key="itemIndex" 
                class="flex gap-2">
              <span class="flex-shrink-0 text-muted-foreground">•</span>
              <span class="text-sm" v-html="formatText(item)"></span>
            </li>
          </ul>
  
          <!-- Collapsible section for remaining items -->
          <Collapsible v-if="section.items.length > 1">
            <ul class="space-y-3 mt-3">
              <CollapsibleContent>
                <li v-for="(item, itemIndex) in section.items.slice(1)" 
                    :key="itemIndex + 1"
                    class="flex gap-2">
                  <span class="flex-shrink-0 text-muted-foreground">•</span>
                  <span class="text-sm" v-html="formatText(item)"></span>
                </li>
              </CollapsibleContent>
            </ul>
  
            <CollapsibleTrigger class="w-full">
              <Button variant="ghost" class="w-full mt-2 hover:bg-muted/50">
                <span class="flex items-center gap-2">
                  <ChevronDown
                    class="h-4 w-4 transition-transform duration-200"
                    :class="{ 'rotate-180': isOpen }"
                  />
                  {{ isOpen ? 'Show less' : `Show ${section.items.length - 1} more` }}
                </span>
              </Button>
            </CollapsibleTrigger>
          </Collapsible>
        </CardContent>
      </Card>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed, ref } from 'vue'
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
  
  interface ImprovementSection {
    title: string
    items: string[]
  }
  
  interface Props {
    improvements: string
  }
  
  const props = defineProps<Props>()
  const isOpen = ref(false)
  
  // Function to format text with emphasis
  const formatText = (text: string): string => {
    return text.replace(
      /\*\*(.*?)\*\*/g, 
      '<span class="font-semibold text-primary">$1</span>'
    )
  }
  
  const improvementSections = computed((): ImprovementSection[] => {
    const sections: ImprovementSection[] = []
    let currentSection: string | null = null
    let currentItems: string[] = []
    
    // Split by newlines and filter empty lines
    const lines = props.improvements.split('\n').filter((line: string): boolean => line.trim().length > 0)
    
    lines.forEach((line: string): void => {
      // Check if line is a section header (ends with ':')
      if (line.includes(':')) {
        // Save previous section if it exists
        if (currentSection !== null) {
          sections.push({
            title: currentSection,
            items: currentItems
          })
        }
        currentSection = line.trim()
        currentItems = []
      } else if (line.trim().startsWith('-')) {
        // Add item to current section
        currentItems.push(line.trim().substring(1).trim())
      }
    })
    
    // Add the last section
    if (currentSection !== null && currentItems.length > 0) {
      sections.push({
        title: currentSection,
        items: currentItems
      })
    }
    
    return sections
  })
  </script>