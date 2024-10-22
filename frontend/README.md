# vue-project

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

CD in frontend :

```sh
cd frontend/
```

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

## Accessibility Testing with Playwright

Our project uses Playwright for automated accessibility testing across all pages. The tests automatically crawl through the website and check for WCAG compliance using axe-core.

### Prerequisites

Before running the tests, ensure you have the following:

- Project dependencies installed (`npm install`)
- Development server running (`npm run dev`)

### Running the Tests

0. Uncomment the onMount autologin.

Navigate to App.vue and uncomment

```
onMounted(async () => {
  await authStore.login('pokemongo@gmail.com', '9YtupB9E4B3TpPG!DcAK')
})
```

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

4. Comment the onMount autologin.

Navigate to App.vue and comment

```
onMounted(async () => {
  await authStore.login('pokemongo@gmail.com', '9YtupB9E4B3TpPG!DcAK')
})
```

5. (optional) Record Keeping
   Find the report file in frontend/playwright-report and transfer it to CareerCompass/Automated_Testing_Documentation for record keeping. Rename to the file to the current date.

### Viewing Test Results

1. Open the provided URL in your browser (e.g., http://localhost:9323)
2. Click on the test to view details
3. Navigate to the bottom of the test details
4. Look for the "Attachments" section
5. Expand "stdout" to see detailed accessibility violations

### Understanding Test Output

The test results will show:

- Total number of pages checked
- Number of pages with violations
- Detailed breakdown of violations per page
- Specific WCAG rules that were violated

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

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
