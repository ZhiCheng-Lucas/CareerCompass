import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * Test suite for conducting automated accessibility scans across a website
 * Uses Playwright for browser automation and Axe-core for accessibility testing
 */
test.describe('website accessibility scan', () => {
  /**
   * Main test case that crawls the website and checks for accessibility violations
   * Implements a breadth-first search approach to navigate through pages
   */
  test('should not have any automatically detectable accessibility issues', async ({ page }) => {
    // Track URLs that have been processed to avoid duplicate checks
    const visitedUrls = new Set<string>();
    
    // Queue of URLs to be processed, starting with the homepage
    const urlsToVisit: string[] = ['http://localhost:5173/'];
    
    // Base URL used to ensure we only test pages within our website
    const baseUrl = 'http://localhost:5173';
    
    // Configuration object for customizing the crawler's behavior
    const config = {
      waitTime: 2000,     // Delay in ms to allow for dynamic content loading and authentication
      maxPages: 50,       // Maximum number of pages to test to prevent infinite crawls
      excludePaths: [     // URL paths to skip during crawling (e.g., sensitive or irrelevant sections)
        // eg.
        // '/admin', 
        // '/private'
      ], 
    };

    // Counter for the number of pages processed
    let pagesChecked = 0;
    
    // Map to store accessibility violations found, keyed by URL
    // Value is an array of violation objects from axe-core
    const violations = new Map<string, any[]>();

    // Main crawling loop - continues until no more URLs to visit or max pages reached
    while (urlsToVisit.length > 0 && pagesChecked < config.maxPages) {
      const currentUrl = urlsToVisit.pop();
      
      // Skip if URL is invalid or already visited
      if (!currentUrl) continue;
      if (visitedUrls.has(currentUrl)) continue;
      
      // Check if current URL matches any excluded paths
      if (config.excludePaths.some(path => currentUrl.includes(path))) {
        console.log(`Skipping excluded path: ${currentUrl}`);
        continue;
      }

      console.log(`Testing accessibility for: ${currentUrl}`);
      
      try {
        // Navigate to page and wait for network activity to settle
        await page.goto(currentUrl, { waitUntil: 'networkidle' });
        
        // Additional wait time for dynamic content and authentication
        await page.waitForTimeout(config.waitTime);
        
        // Run accessibility scan using axe-core
        const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
        
        // If violations found, store them and log details
        if (accessibilityScanResults.violations.length > 0) {
          violations.set(currentUrl, accessibilityScanResults.violations);
          console.log(`Found ${accessibilityScanResults.violations.length} violations on ${currentUrl}`);
          console.log(accessibilityScanResults.violations)
        }

        // Extract all links from the current page using client-side JavaScript
        // This helps discover new URLs to test
        const links = await page.evaluate(() => {
          return Array.from(document.querySelectorAll('a'))
            .map(a => a.href)
            .filter(href => href && href.startsWith('http'));
        });

        // Add new internal links to the processing queue
        for (const link of links) {
          if (link.startsWith(baseUrl) && !visitedUrls.has(link)) {
            urlsToVisit.push(link);
          }
        }

      } catch (error) {
        // Error handling with type checking for better error messages
        if (error instanceof Error) {
          console.error(`Error testing ${currentUrl}:`, error.message);
        } else {
          console.error(`Error testing ${currentUrl}:`, error);
        }
      }

      // Mark current URL as visited and increment counter
      visitedUrls.add(currentUrl);
      pagesChecked++;
    }

    // Generate and display summary report of findings
    console.log('\n--- Accessibility Test Summary ---');
    console.log(`Pages checked: ${pagesChecked}`);
    console.log(`Pages with violations: ${violations.size}`);
    
    // If violations found, provide detailed report
    if (violations.size > 0) {
      console.log('\nDetailed Violations:');
      violations.forEach((pageViolations, url) => {
        console.log(`\n${url}:`);
        pageViolations.forEach(violation => {
          console.log(`- ${violation.id}: ${violation.help}`);
        });
      });
    }

    // Final assertion - fail test if any violations found
    expect(violations.size, `Found accessibility violations on ${violations.size} pages`).toBe(0);
  });
});