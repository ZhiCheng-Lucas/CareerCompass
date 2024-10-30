# CareerCompass Project

This README provides instructions on how to set up and run the CareerCompass project.

Todo:

1. Finish up frontend features.
2. Fix accessbility issues as highlighted by our testing.
3. Do up slides.

4. Implement Resume
5. Charts etc. Analytics. - especially the one from api.

6. Highlight skills etc ( good to know ) -priority queue. ( wait for prof's feedback)

Main Goal : - Friday Morning finish mvp.

1.Accessibility changes. - scanning then try and fix changes.
( playwright + govtech ) 2. Start working on the slides.

-   justify everything eg. we looked at some reports and they suggested this for accessibility etc.

In the resume part, can show how it is able to detect typos etc as well.
Show a typo in the uploaded resume and show how the app is able to detect it.

-   change the model to 4o instead of 4o-mini.

# CareerCompass Project Deployment Guide

## API Configuration

In `services/api.ts`:

```typescript
// For development
// const API_URL = 'http://localhost:8000';

// For production (current setting)
const API_URL = "https://orca-app-8ua27.ondigitalocean.app";
```

## Overview

CareerCompass is deployed across multiple platforms:

-   Frontend:
    -   Primary: GitHub Pages (Automated CI/CD)
    -   Backup: Netlify (Manual Backup)
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

### Backup Deployment (Netlify - Manual)

**Backup URL:** https://careercompass-is216-2024.netlify.app/

#### Manual Netlify Deployment Process

1. Modify `vite.config.ts`:

    ```typescript
    // Comment out this line:
    // base: '/CareerCompass/',
    ```

2. Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

3. Build the project:

    ```bash
    npm run build
    ```

4. Deploy to Netlify:

    - Access the Netlify dashboard at https://app.netlify.com/sites/careercompass-is216-2024/deploys
    - Upload the generated `dist` directory

5. After deployment, revert `vite.config.ts`:
    ```typescript
    // Uncomment this line:
    base: '/CareerCompass/',
    ```

### Access Management

-   GitHub Pages deployment is managed through repository settings
-   Netlify dashboard access is managed through Zhi Cheng's GitHub authentication

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

# Job Processing API

## Overview

This API provides endpoints for user authentication, job searching, and job recommendations based on user skills. It's built with FastAPI and uses MongoDB for data storage.

For detailed visualization of the API workflows, please refer to the sequence diagrams in the `sequence_diagrams` folder, which cover:

-   User Authentication Flow (signup and login)
-   Job Search Flow (search by company, title, and skills)
-   Resume Processing Flow
-   Analytics Flow

## Base URL

```
http://localhost:8000
```

## Endpoints

Our API endpoints are divided into two main sections:

1. Core Functionality (Endpoints 1-9): Handles user authentication, job searches, and personalized recommendations
2. Analytics & Charts (Endpoints 10-16): Provides statistical data, market trends, and industry analyses

# Core Functionality Endpoints

### 1. User Registration

Creates a new user account with empty initial skills.

-   **URL:** `/signup`
-   **Method:** POST
-   **Request Body:**
    ```json
    {
        "username": "user@example.com",
        "password": "securepassword123"
    }
    ```
-   **Success Response:**
    -   **Code:** 201
    -   **Content:** `{ "message": "User registered successfully with empty skills list" }`
-   **Error Response:**

    -   **Code:** 400
    -   **Content:** `{ "detail": "Username already exists" }`

    OR

    -   **Code:** 500
    -   **Content:** `{ "detail": "An error occurred: [error message]" }`

-   **Notes:**
    -   The username should be a valid email address.
    -   The password must be at least 10 characters long.
    -   Usernames are stored in lowercase and must be unique.
    -   Passwords are hashed before storage for security.

### 2. User Login

Authenticates a user and returns their username and skills.

-   **URL:** `/login`
-   **Method:** POST
-   **Request Body:**
    ```json
    {
        "username": "user@example.com",
        "password": "securepassword123"
    }
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:**
        ```json
        {
            "username": "user@example.com",
            "skills": ["python", "javascript", "docker"]
        }
        ```
-   **Error Response:**

    -   **Code:** 401
    -   **Content:** `{ "detail": "Username does not exist" }`

    OR

    -   **Code:** 401
    -   **Content:** `{ "detail": "Incorrect password" }`

-   **Notes:**
    -   The login process is case-insensitive for the username.
    -   After successful login, the returned skills list can be empty if the user hasn't added any skills yet.

### 3. Get All Jobs

Retrieves all jobs from the database, with an optional limit.

-   **URL:** `/jobs/all`
-   **Method:** GET
-   **Query Parameters:**
    -   `limit` (optional): Maximum number of jobs to return (default: 100, min: 1, max: 10000)
-   **Examples:**
    ```
    http://localhost:8000/jobs/all
    http://localhost:8000/jobs/all?limit=500
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of Job objects
        ```json
        [
            {
                "id": "671245e609e048e10ee5d16a",
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "date": "2024-09-09",
                "job_link": "https://www.linkedin.com/jobs/view/4020111996/?eBP=NON_CHARGEABLE_CHAN...",
                "skills": ["python", "javascript", "docker"]
            },
            ...
        ]
        ```
-   **Error Response:**

    -   **Code:** 500
    -   **Content:** `{ "detail": "An error occurred: [error message]" }`

-   **Notes:**
    -   The `limit` parameter helps prevent overloading by allowing you to specify the maximum number of results.
    -   Jobs are returned in the order they are stored in the database.
    -   The `id` field is a unique identifier for each job.
    -   The `date` field represents the date the job was posted or last updated.
    -   The `job_link` provides a direct URL to the job posting.

### 4. Get Jobs by Company

Retrieves jobs from a specific company.

-   **URL:** `/jobs/company/{company_name}`
-   **Method:** GET
-   **URL Parameters:**
    -   `company_name`: The exact name of the company (case-insensitive)
-   **Example:**
    ```
    http://localhost:8000/jobs/company/EPS%20CONSULTANTS%20PTE%20LTD
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of Job objects from the specified company
        ```json
        [
            {
                "id": "671245e609e048e10ee5d16b",
                "job_title": "Data Analyst",
                "company": "EPS CONSULTANTS PTE LTD",
                "date": "2024-09-10",
                "job_link": "https://www.linkedin.com/jobs/view/4020111997/?eBP=NON_CHARGEABLE_CHAN...",
                "skills": ["sql", "python", "data visualization"]
            },
            ...
        ]
        ```
-   **Notes:**
    -   The search is case-insensitive, so "EPS Consultants Pte Ltd" will match "EPS CONSULTANTS PTE LTD".
    -   Spaces in the company name are automatically encoded by the browser, but you can also manually encode them as %20.
    -   If no jobs are found for the specified company, an empty list is returned.
    -   The API uses regular expressions for exact matching of the company name.

### 5. Get Jobs by Title

Retrieves jobs that contain a specific title part.

-   **URL:** `/jobs/title/{title_part}`
-   **Method:** GET
-   **URL Parameters:**
    -   `title_part`: A part of the job title to search for
-   **Example:**
    ```
    http://localhost:8000/jobs/title/engineer
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of Job objects with titles containing the specified part
        ```json
        [
            {
                "id": "671245e609e048e10ee5d16c",
                "job_title": "Software Engineer",
                "company": "Tech Innovators Inc.",
                "date": "2024-09-11",
                "job_link": "https://www.linkedin.com/jobs/view/4020111998/?eBP=NON_CHARGEABLE_CHAN...",
                "skills": ["java", "spring", "microservices"]
            },
            ...
        ]
        ```
-   **Notes:**
    -   The search is case-insensitive and uses partial matching.
    -   The API uses regular expressions for partial matching of the job title.
    -   If no jobs are found with the specified title part, an empty list is returned.
    -   This endpoint is useful for searching jobs across different companies with similar titles.

### 6. Get Jobs by Skills

Retrieves jobs that require specific skills.

-   **URL:** `/jobs/skills/{skills}`
-   **Method:** GET
-   **URL Parameters:**
    -   `skills`: Comma-separated list of skills
-   **Examples:**
    ```
    http://localhost:8000/jobs/skills/python,docker
    http://localhost:8000/jobs/skills/machine%20learning
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of Job objects requiring the specified skills
        ```json
        [
            {
                "id": "671245e609e048e10ee5d16d",
                "job_title": "ML Engineer",
                "company": "AI Solutions Ltd.",
                "date": "2024-09-12",
                "job_link": "https://www.linkedin.com/jobs/view/4020111999/?eBP=NON_CHARGEABLE_CHAN...",
                "skills": ["python", "machine learning", "tensorflow"]
            },
            ...
        ]
        ```
-   **Notes:**
    -   Multiple skills can be chained using commas.
    -   The search is case-insensitive and uses exact matching for each skill.
    -   Spaces in skill names are automatically encoded by the browser, but you can also manually encode them as %20.
    -   If a job requires any of the specified skills, it will be included in the results.
    -   The API uses regular expressions for exact matching of skills.
    -   This endpoint is particularly useful for finding jobs that match a user's specific skill set.

### 7. Get Recommended Jobs

Retrieves the top 5 recommended jobs for a user based on their skills.

-   **URL:** `/get_recommended_jobs/{username}`
-   **Method:** GET
-   **URL Parameters:**
    -   `username`: The username (email) of the user
-   **Example Requests:**
    ```
    http://localhost:8000/get_recommended_jobs/user@example2.com
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of up to 5 recommended jobs
        ```json
        [
            {
                "job_title": "Senior Python Developer",
                "company": "Tech Solutions Inc.",
                "job_link": "https://www.linkedin.com/jobs/view/4020112000/?eBP=NON_CHARGEABLE_CHAN...",
                "match_percentage": 85.71,
                "matching_skills": ["python", "django", "postgresql"]
            },
            {
                "job_title": "Full Stack Engineer",
                "company": "WebDev Co.",
                "job_link": "https://www.linkedin.com/jobs/view/4020112001/?eBP=NON_CHARGEABLE_CHAN...",
                "match_percentage": 71.42,
                "matching_skills": ["python", "javascript", "react"]
            },
            ...
        ]
        ```
-   **Error Responses:**

    -   **Code:** 404
    -   **Content:** `{ "detail": "Invalid username" }`

    OR

    -   **Code:** 200
    -   **Content:** `{ "message": "User has no skills listed. No job recommendations available." }`

-   **Notes:**
    -   The match percentage is calculated as: (number of matching skills / total job skills) \* 100
    -   If multiple jobs have the same match percentage, they are ranked based on the number of matched skills.
    -   The endpoint returns at most 5 job recommendations, even if more jobs have matching skills.
    -   Match percentages are rounded to two decimal places in the response.
    -   This endpoint is useful for providing personalized job recommendations to users based on their skill set.
    -   Users should ensure their skill list is up to date for the most relevant job recommendations.
    -   The API handles various edge cases, such as users with no skills or non-existent usernames, to provide a robust user experience.

### 8. Get Recommended Skills to Learn

Retrieves the top 5 recommended skills for a user to learn based on their current skills and job market demand.

-   **URL:** `/get_recommended_skill_to_learn/{username}`
-   **Method:** GET
-   **URL Parameters:**
    -   `username`: The username (email) of the user
-   **Example Request:**
    ```
    http://localhost:8000/get_recommended_skill_to_learn/user@example2.com
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of up to 5 recommended skills
        ```json
        [
            {
                "skill": "docker",
                "frequency": 15,
                "example_jobs": ["DevOps Engineer", "Cloud Architect", "Full Stack Developer"]
            },
            {
                "skill": "react",
                "frequency": 12,
                "example_jobs": ["Frontend Developer", "Web Application Developer", "UI Engineer"]
            },
            ...
        ]
        ```
-   **Error Responses:**

    -   **Code:** 404
    -   **Content:** `{ "detail": "Invalid username" }`

    OR

    -   **Code:** 200
    -   **Content:** `{ "message": "User has no skills listed. No skill recommendations available." }`

    OR

    -   **Code:** 200
    -   **Content:** `{ "message": "No matching jobs found for user's skills. No skill recommendations available." }`

-   **Notes:**
    -   The function recommends skills from jobs where the user matches at least one skill.
    -   Recommended skills are ranked by their frequency in matching jobs.
    -   If there are fewer than 5 new skills to recommend, only the available skills are returned.
    -   In case of ties in skill frequency, skills are ranked based on the order they appear in the data.
    -   The response includes up to 3 example job titles for each recommended skill.
    -   This endpoint is useful for users looking to expand their skill set based on current job market trends.
    -   The recommendations are personalized based on the user's existing skills, focusing on complementary skills in demand.
    -   Users should ensure their current skill list is up to date for the most relevant recommendations.

### 9. Upload and Process Resume

Upload and process a resume file (PDF or DOCX), extract skills, and provide recommendations.

This endpoint performs the following operations:

1. Authenticates the user using the provided username.
2. Reads and validates the uploaded file (size and format).
3. Extracts text from the resume file.
4. Parses skills from the extracted text.
5. Updates the user's skills in the database.
6. Generates AI-powered content improvement suggestions for the resume.
7. Retrieves job recommendations based on the user's skills.
8. Retrieves skill recommendations for the user to learn.

-   **URL:** `/upload_resume`
-   **Method:** POST
-   **Request Body:** Form data
    -   `file`: The resume file (PDF or DOCX)
    -   `username`: User's email address
-   **Example Request:**
    POST http://localhost:8000/upload_resume
    Content-Type: multipart/form-data
    file: [resume.pdf or resume.docx]
    username: user@example.com

-   **Success Response:**
-   **Code:** 200
-   **Content:** A dictionary containing processed resume information and recommendations
    ```json
    {
      "message": "Full text of the resume...",
      "extracted_skills": ["python", "java", "machine learning"],
      "ai_improvements": "1. Quantify your achievements in your most recent role...\n2. Add more specific technical skills...\n3. Improve the clarity of your job descriptions...",
      "recommended_jobs": [
        {
          "job_title": "Senior Software Engineer",
          "company": "Tech Corp",
          "job_link": "https://example.com/job/12345",
          "match_percentage": 85.5,
          "matching_skills": ["python", "java"]
        },
        ...
      ],
      "recommended_skills_to_learn": [
        {
          "skill": "docker",
          "frequency": 15,
          "example_jobs": ["DevOps Engineer", "Cloud Architect", "Full Stack Developer"]
        },
        ...
      ]
    }
    ```
-   **Error Responses:**
-   **Code:** 401
    -   **Content:** `{ "detail": "Invalid username" }`
-   **Code:** 413
    -   **Content:** `{ "detail": "File too large" }`
-   **Code:** 400
    -   **Content:** `{ "detail": "Empty file" }`
-   **Code:** 400
    -   **Content:** `{ "detail": "Unsupported file format. Please upload a PDF or DOCX document." }`
-   **Code:** 400

    -   **Content:** `{ "detail": "Failed to extract text from the [PDF/DOCX] file" }`

-   **Notes:**
-   The maximum allowed file size is 512 MB.
-   Only PDF and DOCX file formats are supported.
-   Basic user authentication is required to protect personal data.
-   The user's skills in the database are updated based on the extracted skills from the resume.
-   AI-generated improvements are provided for the resume content.
-   Job recommendations are based on the user's extracted skills.
-   Skill recommendations suggest new skills for the user to learn based on job market trends.
-   This endpoint combines multiple operations and may take longer to respond compared to simpler endpoints.
-   The AI improvements are generated using the OpenAI GPT model.

---

# Chart & Analytics Endpoints

### 10. Get Graduate Employment Statistics Overview

Retrieves comprehensive employment statistics for graduates from Singapore's major universities.

-   **URL:** `/get_graduate_starting_pay_data`
-   **Method:** GET
-   **Example Request:**

```
GET http://localhost:8000/get_graduate_starting_pay_data
```

-   **Success Response:**
    -   **Code:** 200
    -   **Content:** Array containing overview statistics for university graduates

```json
[
    {
        "institution_type": "Universities (NTU, NUS, SMU, SUSS)",
        "updated_at": "2024-10-18T00:00:00Z",
        "employment_stats": [
            {
                "year": 2023,
                "employed_percentage": 89.6,
                "full_time_permanent_percentage": 84.1,
                "part_time_temporary_freelance_percentage": 5.5,
                "median_gross_monthly_starting_salary": 4313
            }
            // ... more years
        ]
    }
]
```

-   **Error Response:**

    -   **Code:** 500
    -   **Content:** `{ "detail": "An error occurred: [error message]" }`

-   **Notes:**
    -   Data source: https://stats.mom.gov.sg/Pages/Graduate-Starting-Salary-Tables2023.aspx
    -   Provides aggregated statistics for major Singapore universities (NTU, NUS, SMU, SUSS)
    -   Employment statistics include:
        -   Overall employment rate
        -   Full-time permanent employment rate
        -   Part-time/temporary/freelance employment rate
        -   Median gross monthly starting salary (in Singapore dollars)
    -   Historical data available from 2013 onwards
    -   Salary figures are in Singapore dollars (SGD)
    -   Data is updated annually
    -   The `updated_at` field indicates when the statistics were last refreshed
    -   Employment percentages are provided as decimal values (e.g., 89.6 means 89.6%)

### 11. Get Top Skills

Retrieves the most frequent skills from all job listings.

-   **URL:** `/top_skills`
-   **Method:** GET
-   **Query Parameters:**
    -   `limit` (optional): Number of top skills to return (default: 10, min: 1, max: 100)
-   **Examples:**
    ```
    http://localhost:8000/top_skills
    http://localhost:8000/top_skills?limit=20
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of dictionaries containing skills and their frequencies, sorted by frequency
        ```json
        [
            {
                "skill": "python",
                "count": 500
            },
            {
                "skill": "javascript",
                "count": 450
            },
            ...
        ]
        ```
-   **Error Response:**

    -   **Code:** 500
    -   **Content:** `{ "detail": "An error occurred: [error message]" }`

-   **Notes:**
    -   Skills are case-sensitive in the response, but they represent the exact format most commonly found in job listings.
    -   The `count` represents the number of job listings that mention this skill.
    -   This endpoint is useful for understanding current trends in job market skill requirements.
    -   The list is sorted in descending order of frequency.

### 12. Get Industry Growth Data

Retrieves all industry growth data from the database.

-   **URL:** `/get_industry_growth`
-   **Method:** GET
-   **Example Request:**
    ```
    http://localhost:8000/get_industry_growth
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of industry growth data entries
        ```json
        [
            {
                "forecast": {
                    "date": "13 August 2024",
                    "source": "Ministry of Trade and Industry (MTI)",
                    "previous": "1.0 to 3.0 per cent",
                    "current": "2.0 to 3.0 per cent"
                },
                "quarterlyGrowth": [
                    {
                        "quarter": "2Q23",
                        "growth": 0.5
                    },
                    {
                        "quarter": "3Q23",
                        "growth": 1.0
                    },
                    ...
                ],
                "annualGrowth": [
                    {
                        "year": 2022,
                        "growth": 3.8
                    },
                    {
                        "year": 2023,
                        "growth": 1.1
                    },
                    {
                        "year": "2024f",
                        "growth": {
                            "min": 2.0,
                            "max": 3.0
                        }
                    }
                ]
            },
            ...
        ]
        ```
-   **Error Response:**

    -   **Code:** 500
    -   **Content:** `{ "detail": "An error occurred: [error message]" }`

-   **Notes:**
    https://www.singstat.gov.sg/-/media/files/news/gdp2q2024.ashx

    -   The endpoint returns all records from the industry_growth_collection.
    -   Each entry in the response contains forecast data, quarterly growth data, and annual growth data.
    -   The 'forecast' field provides the latest growth forecast information, including the forecast date, source, and current/previous forecasts.
    -   'quarterlyGrowth' shows quarter-wise growth data, with quarters represented in the format "QnYY" (e.g., "2Q23" for second quarter of 2023).
    -   'annualGrowth' presents yearly growth data. Future year forecasts are marked with an 'f' suffix and may include a range (min/max) instead of a single value.
    -   Growth values are represented as percentages (e.g., 3.8 means 3.8%).
    -   This endpoint is useful for analyzing economic trends and making data-driven decisions in job market analysis.

### 13. Get Market Trend Data

Retrieves all market trend data from the database.

-   **URL:** `/get_market_trend`
-   **Method:** GET
-   **Example Request:**
    ```
    http://localhost:8000/get_market_trend
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A dictionary containing job market trends for various sectors
        ```json
        {
            "jobMarketTrends": [
                {
                    "sector": "Manufacturing",
                    "trends": [
                        {
                            "growth": "-1.0%",
                            "period": "year-on-year",
                            "details": "The weak performance of the sector was mainly due to output declines in the biomedical manufacturing and precision engineering clusters, with the former in turn weighed down by a sharp fall in pharmaceuticals output."
                        }
                    ],
                    "source": "The manufacturing sector contracted by 1.0 per cent year-on-year in the second quarter of 2024, easing from the 1.7 per cent contraction in the previous quarter."
                },
                {
                    "sector": "Construction",
                    "trends": [
                        {
                            "growth": "3.8%",
                            "period": "year-on-year",
                            "details": "Growth was on account of an increase in both public and private sector construction output."
                        }
                    ],
                    "source": "Growth in the construction sector came in at 3.8 per cent year-on-year, extending the 4.1 per cent growth in the first quarter, on account of an increase in both public and private sector construction output."
                },
                ...
            ]
        }
        ```
-   **Error Response:**

    -   **Code:** 500
    -   **Content:** `{ "detail": "An error occurred: [error message]" }`

-   **Notes:**
    https://www.singstat.gov.sg/-/media/files/news/gdp2q2024.ashx

    -   The endpoint returns all records from the market_trends collection.
    -   Each sector in the response includes trend information, growth data, and a source statement.
    -   The 'trends' array for each sector may contain multiple trend objects, each with growth, period, and details.
    -   Growth is typically reported year-on-year and given as a percentage.
    -   The 'details' field provides additional context about the sector's performance.
    -   The 'source' field gives a summary statement about the sector's performance, often including comparative data from previous periods.
    -   This endpoint is useful for analyzing current job market trends across various sectors in Singapore, which can be valuable for job seekers, employers, and economic analysts.

### 14. Singapore Labor Market Statistics

Retrieve and process labor market statistics from Singapore's TableBuilder API. Returns only categories with exactly 3 levels in their series number (e.g., 1.2.1 Manufacturing, 1.2.2 Transportation And Storage).

-   **URL:** `/processed_singapore_labor_stats`
-   **Method:** GET
-   **Example Request:**

    ```
    GET http://localhost:8000/processed_singapore_labor_stats
    ```

-   **Success Response:**
-   **Code:** 200
-   **Content:** A dictionary containing processed labor statistics for 2024 Q2

    ```json
    {
        "2024 2Q": {
            "Manufacturing": 8700,
            "Wholesale And Retail Trade": 7200,
            "Transportation And Storage": 5800,
            "Accommodation And Food Services": 7000,
            "Information And Communications": 6500,
            "Financial And Insurance Services": 5600,
            "Professional Services": 6900,
            "Administrative And Support Services": 5100,
            "Community, Social And Personal Services": 18600
        }
    }
    ```

-   **Error Responses:**
-   **Code:** 500
    -   **Content:** `{ "detail": "Error fetching data from SingStat: [error details]" }`
-   **Code:** 500

    -   **Content:** `{ "detail": "An unexpected error occurred: [error details]" }`

-   **Notes:**
-   Data is fetched from the SingStat TableBuilder API using dataset M184071.
-   Only returns categories with exactly 3 levels in their series number (e.g., 1.2.1).
-   Numbers represent job vacancies in each sector.
-   Data is specific to the second quarter of 2024.
-   Values are returned as integers.
-   Response time depends on the SingStat API's response time.
-   Data is automatically processed to simplify the complex hierarchical structure from the original API.

### 15. Employment Statistics by University Program

Retrieve employment statistics for a specific university program, including yearly breakdowns of gross monthly salary and employment rates.

-   **URL:** `/get_employment_stats`
-   **Method:** GET
-   **URL Params:**

    -   **Required:**
        -   `university=[string]`
        -   `school=[string]`
        -   `degree=[string]`

-   **Example Request:**

    ```
    GET http://localhost:8000/get_employment_stats?university=Nanyang Technological University&school=College of Business (Nanyang Business School)&degree=Accountancy and Business
    ```

-   **Success Response:**

    -   **Code:** 200
    -   **Content:**

    ```json
    {
        "gross_monthly_mean": {
            "2013": 3727,
            "2014": 3850,
            "2015": 3920
        },
        "employment_rate_overall": {
            "2013": 97.4,
            "2014": 98.2,
            "2015": 96.8
        }
    }
    ```

-   **Error Response:**

    -   **Code:** 404
    -   **Content:** `{ "detail": "No data found" }`

-   **Notes:**
    -   Requires exact matches for university, school, and degree names (case-sensitive)
    -   Returns all available years in the dataset
    -   Gross monthly mean is in Singapore dollars
    -   Employment rates are in percentages
    -   No partial matching is supported
    -   Parameters must be URL encoded when containing spaces or special characters

### 16. Comprehensive University Statistics

Retrieve a complete hierarchical view of employment statistics for all universities, schools, and degrees.

-   **URL:** `/university_stats`
-   **Method:** GET
-   **URL Params:** None

-   **Example Request:**

    ```
    GET http://localhost:8000/university_stats
    ```

-   **Success Response:**

    -   **Code:** 200
    -   **Content:**

    ```json
    {
        "Nanyang Technological University": {
            "College of Business (Nanyang Business School)": {
                "Accountancy and Business": {
                    "employment_rate_overall": {
                        "2013": 97.4,
                        "2014": 98.1
                    },
                    "gross_monthly_mean": {
                        "2013": 3727,
                        "2014": 3800
                    }
                },
                "Business (3-yr direct Honours Programme)": {
                    "employment_rate_overall": {
                        "2013": 90.9,
                        "2014": 92.5
                    },
                    "gross_monthly_mean": {
                        "2013": 3214,
                        "2014": 3400
                    }
                }
            }
        },
        "National University of Singapore": {
            // Similar nested structure
        }
    }
    ```

-   **Notes:**
    -   Returns complete dataset for all universities
    -   Data is organized in a hierarchical structure:
        -   University → School → Degree → Statistics → Year
    -   Gross monthly mean values are in Singapore dollars
    -   Employment rates are in percentages
    -   All available years are included for each program
    -   Response size may be large due to comprehensive data inclusion
    -   Statistics are provided in two categories:
        -   employment_rate_overall: Overall employment rate
        -   gross_monthly_mean: Average monthly salary

## General API Notes

-   All endpoints return JSON responses.

# References

https://stats.mom.gov.sg/Pages/Graduate-Starting-Salary-Tables2023.aspx
https://www.singstat.gov.sg/-/media/files/news/gdp2q2024.ashx
https://data.gov.sg/datasets?query=job+vacancy&page=1&resultId=d_134b26ee29baa1688ec9b051a8a5701f
