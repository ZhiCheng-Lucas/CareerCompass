# CareerCompass Project

This README provides instructions on how to set up and run the CareerCompass project as well as some general information about the project.

## General Information and links:

-   Main Git Repo: https://github.com/ZhiCheng-Lucas/CareerCompass
-   API Documentation: https://github.com/ZhiCheng-Lucas/CareerCompass
-   Accessibility Readme: https://github.com/ZhiCheng-Lucas/CareerCompass/blob/main/Accessibility_Report/accessiblity.md
-   Sequence Diagram Information : https://github.com/ZhiCheng-Lucas/CareerCompass/tree/main/sequence_diagram

-   Frontend URL: https://zhicheng-lucas.github.io/CareerCompass/
-   Backend Dashboard URL: https://cloud.digitalocean.com/
-   Backend Production URL: https://orca-app-8ua27.ondigitalocean.app/

## Course Requirements

-   If hosted on cloud: include the URL to the first page of your application.
-   If using public GIT repository: Include the URL to your Git repo.
-   Provide step-by-step instructions on:
    -   How to set up your application based on the submitted file(s).
    -   How to run your application.
-   If there are any username/password details, include them in this file

### If hosted on cloud: include the URL to the first page of your application:

https://zhicheng-lucas.github.io/CareerCompass/

### If using public GIT repository: Include the URL to your Git repo:

https://github.com/ZhiCheng-Lucas/CareerCompass

## Provide step-by-step instructions on:

### How to set up your application based on the submitted file(s):

The submission package contains the following components:

-   Backend source code
-   Frontend source code
-   Accessibility testing scripts and documentation
-   Sequence diagram assets

**Frontend Setup**
The main entry point for the frontend application is located at:

```
frontend/src/App.vue
```

To run the local frontend, you have two available options:

1. Local Frontend using deployed Backend:

```bash
cd frontend
npm install
npm run dev
```

You will see something like:

```
VITE v5.4.9  ready in 2161 ms
➜  Local:   http://localhost:5173/CareerCompass/
➜  Network: use --host to expose
➜  press h + enter to show help
```

Use the link provided.

2. Local Frontend and local backend:
    - Prepare OpenAPI Key:
        - Ensure openai_api_key.txt in the same folder as your docker-compose.yml file
    - Prepare MongoDB Connection String:
        - Ensure mongodb_connection_string.txt in the same folder as your docker-compose.yml file
    - Build and Run:
        - Navigate to the CareerCompass folder where the docker-compose.yml file is located
        - Run: docker-compose up --build
        - Access the backend application at http://localhost:8000
    - Modify frontend API configuration:
        - Go to frontend/src/services/api.ts
        - Uncomment localhost:8000 and comment the orca-app
        ```javascript
        // For devs
        const API_URL = "http://localhost:8000";
        // For prod purposes.
        // const API_URL = 'https://orca-app-8ua27.ondigitalocean.app';
        ```
    - Start frontend:
        ```bash
        cd frontend
        npm install
        npm run dev
        ```
    - Access the frontend at the link provided from npm run dev.

## If there are any username/password details, include them in this file:

-   Please see the uploaded mongodb_connection_string.txt and openai_api_key.txt files that is uploaded on elearn.
-   Sample login Credentials:
    -   ilovevue123@gmail.com
    -   pokemon12345

If there are issues, please do not hesitate to contact our team via telegram.

# General CareerCompass Project Deployment Information

## Overview

CareerCompass is deployed across multiple platforms:

-   Frontend: GitHub Pages (Automated CI/CD)
-   Backend: DigitalOcean

## Frontend Deployment

### Primary Deployment (GitHub Pages)

**Main URL:** https://zhicheng-lucas.github.io/CareerCompass/

#### Automated Deployment Process

-   Deployment is automatically triggered on push to the `main` branch
-   GitHub Actions workflow builds and deploys the frontend
-   No manual intervention required

#### How it works

1. Push changes to the `main` branch
2. GitHub Actions automatically:
    - Builds the Vue.js application
    - Deploys to GitHub Pages
3. Changes are live within minutes

### Access Management

-   GitHub Pages deployment is managed through repository settings

## Backend Deployment

**Dashboard URL:** https://cloud.digitalocean.com/  
**Production URL:** https://orca-app-8ua27.ondigitalocean.app/

### Deployment Process

-   Automated CI/CD pipeline is configured
-   Changes are automatically deployed when code is pushed to the `main` branch
-   No manual deployment steps required

### Infrastructure Management

-   Platform: DigitalOcean
-   Account administrator: Zhi Cheng

## Setup Instructions

0. **Prepare OpenAPI Key:**

    - Create a file named `openai_api_key.txt` in the same folder as your `docker-compose.yml` file.
    - Add the api key to this file.
    - See pinned in our telegram group.
    - **Important:** Do not push this file to GitHub. It should already be listed in the `.gitignore` file.

1. **Prepare MongoDB Connection String:**

    - Create a file named `mongodb_connection_string.txt` in the same folder as your `docker-compose.yml` file.
    - Add your MongoDB connection string to this file.
    - See pinned in our telegram group.
    - **Important:** Do not push this file to GitHub. It should already be listed in the `.gitignore` file.

2. **Build and Run the Project:**

    - Navigate to the CareerCompass folder where the `docker-compose.yml` file is located.
    - Run the following command:
        ```
        docker-compose up --build
        ```

3. **Accessing the Application:**
    - Once the containers are up and running, you can access the application at `http://localhost:8000`

## Sample Endpoints

Try the following endpoints to test the application:

-   `http://localhost:8000/jobs/company/tiktok`
-   `http://localhost:8000/jobs/skills/sql`
-   `http://localhost:8000/jobs/title/learning`
