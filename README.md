# CareerCompass Project

This README provides instructions on how to set up and run the CareerCompass project.

## Setup Instructions

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

## Base URL

```
http://localhost:8000
```

## Endpoints

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

### 7. Get Graduate Starting Pay Data

Retrieves all graduate starting pay data by year.

-   **URL:** `/get_graduate_starting_pay_data`
-   **Method:** GET
-   **Example:**
    ```
    http://localhost:8000/get_graduate_starting_pay_data
    ```
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** A list of graduate starting pay data entries
        ```json
        [
            {
                "year": 2024,
                "degree": "Computer Science",
                "starting_salary": 75000
            },
            {
                "year": 2024,
                "degree": "Data Science",
                "starting_salary": 78000
            },
            ...
        ]
        ```
-   **Error Response:**

    -   **Code:** 500
    -   **Content:** `{ "detail": "An error occurred: [error message]" }`

-   **Notes:**
    https://stats.mom.gov.sg/Pages/Graduate-Starting-Salary-Tables2023.aspx

        -   This endpoint provides valuable information for new graduates to compare starting salaries across different degrees.
        -   The data is typically updated annually.
        -   Salaries are in the local currency (you may want to specify which currency).
        -   If no data is available, an empty list will be returned.

### 8. Get Top Skills

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

### 9. Get Recommended Jobs

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
    -   The function uses fuzzy matching to allow for partial skill matches. For example, "python" in job requirements might match with "python3" in user skills.
    -   The match percentage is calculated as: (number of matching skills / total job skills) \* 100
    -   If multiple jobs have the same match percentage, they are ranked based on their order in the database.
    -   The endpoint returns at most 5 job recommendations, even if more jobs have matching skills.
    -   Match percentages are rounded to two decimal places in the response.
    -   This endpoint is useful for providing personalized job recommendations to users based on their skill set.
    -   Users should ensure their skill list is up to date for the most relevant job recommendations.
    -   The API handles various edge cases, such as users with no skills or non-existent usernames, to provide a robust user experience.

### 10. Get Recommended Skills to Learn

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

### 11. Get Industry Growth Data

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

        - The endpoint returns all records from the industry_growth_collection.
        - Each entry in the response contains forecast data, quarterly growth data, and annual growth data.
        - The 'forecast' field provides the latest growth forecast information, including the forecast date, source, and current/previous forecasts.
        - 'quarterlyGrowth' shows quarter-wise growth data, with quarters represented in the format "QnYY" (e.g., "2Q23" for second quarter of 2023).
        - 'annualGrowth' presents yearly growth data. Future year forecasts are marked with an 'f' suffix and may include a range (min/max) instead of a single value.
        - Growth values are represented as percentages (e.g., 3.8 means 3.8%).
        - This endpoint is useful for analyzing economic trends and making data-driven decisions in job market analysis.

### 12. Get Market Trend Data

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

## General API Notes

-   All endpoints return JSON responses.
-   Date formats used in the API follow the ISO 8601 standard (YYYY-MM-DD).
-   The API uses HTTPS for secure communication (ensure your client supports this).
-   Rate limiting may be applied to prevent abuse (you may want to specify the exact limits).
-   For pagination on endpoints that may return large datasets, use the `limit` parameter where available.
-   Keep your API key (if implemented) secure and do not share it publicly.
-   For any unexpected errors, contact the API support team with the error message and timestamp.

# References

https://stats.mom.gov.sg/Pages/Graduate-Starting-Salary-Tables2023.aspx
https://www.singstat.gov.sg/-/media/files/news/gdp2q2024.ashx
https://data.gov.sg/datasets?query=job+vacancy&page=1&resultId=d_134b26ee29baa1688ec9b051a8a5701f
