## Accessibility Testing with Playwright

Our project uses Playwright and GovTech Oobee (formerly known as Purple A11y) for automated accessibility testing across all pages. The tests automatically crawl through the website and check for WCAG compliance using axe-core.

### Progress Report

You can find all accessibility testing reports in the `./Accessibility_Report` folder. This includes:

-   GovTech Oobee (Purple A11y) reports
-   Playwright automated test results

The reports are organized by date, allowing you to:

-   Track accessibility improvements over time
-   Compare results between different testing tools

#### Oct 22, 2023 - Initial Report and Scan

**Playwright Detailed Violations:**

1. Home Page (http://localhost:5173/):

    - heading-order: Heading levels should only increase by one

2. Analytics Page:

    - link-in-text-block: Links must be distinguishable without relying on color
    - page-has-heading-one: Page should contain a level-one heading

3. Register Page:

    - link-in-text-block: Links must be distinguishable without relying on color
    - page-has-heading-one: Page should contain a level-one heading

4. Login Page:

    - link-in-text-block: Links must be distinguishable without relying on color
    - page-has-heading-one: Page should contain a level-one heading

5. Resume Page:

    - page-has-heading-one: Page should contain a level-one heading

6. Jobs Page:
    - link-in-text-block: Links must be distinguishable without relying on color
    - page-has-heading-one: Page should contain a level-one heading

**GovTech Findings:**

-   Heading levels should only increase by one
-   Elements must meet minimum color contrast ratio thresholds
-   Buttons must have discernible text

#### Nov 1, 2023 - Progress Update

**Fixed Issues:**

commit

-   282cc65c5312c8714043318f99ce86f47b403ea1
-   88bb7a524240e6d5ee77f5097bec8f0757ce4052

-   ✅ link-in-text-block: Links must be distinguishable without relying on color
-   ✅ page-has-heading-one: Page should contain a level-one heading
-   ✅ Heading levels should only increase by one
-   ✅ Buttons must have discernible text

**Current Violations:**

**GovTech Findings:**

-   Elements must meet minimum color contrast ratio thresholds

**Playwright Detailed Violations:**

All pages are experiencing the same violation:

-   color-contrast: Elements must meet minimum color contrast ratio thresholds

Affected pages:

-   http://localhost:5173/
-   http://localhost:5173/CareerCompass/market
-   http://localhost:5173/CareerCompass/analytics
-   http://localhost:5173/CareerCompass/resume
-   http://localhost:5173/CareerCompass/jobs

### Prerequisites

Before running the tests, ensure you have the following:

-   Project dependencies installed (`npm install`)
-   Development server running (`npm run dev`)

### Running the Tests

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Run the Playwright tests:

```bash
npx playwright test
```

3. After the tests complete, you'll see a message like:

```
Serving HTML report at http://localhost:9323. Press Ctrl+C to quit.
```

4. (optional) Record Keeping
   Find the report file in frontend/playwright-report and transfer it to CareerCompass/Testing_Report for record keeping. Rename to the file to the current date.

### Viewing Test Results

1. Open the provided URL in your browser (e.g., http://localhost:9323)
2. Click on the test to view details
3. Navigate to the bottom of the test details
4. Look for the "Attachments" section
5. Expand "stdout" to see detailed accessibility violations

### Understanding Test Output

The test results will show:

-   Total number of pages checked
-   Number of pages with violations
-   Detailed breakdown of violations per page
-   Specific WCAG rules that were violated

Example violation output:

```
Testing accessibility for: http://localhost:5173/
Found 1 violations on http://localhost:5173/
[
  {
    id: 'heading-order',
    impact: 'moderate',
    tags: [ 'cat.semantics', 'best-practice' ],
    description: 'Ensure the order of headings is semantically correct',
    help: 'Heading levels should only increase by one',
    helpUrl: 'https://dequeuniversity.com/rules/axe/4.10/heading-order?application=playwright',
    nodes: [ [Object] ]
  }
]
```
