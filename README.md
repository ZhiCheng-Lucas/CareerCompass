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

# Job Processing API Documentation

This API provides endpoints for searching and retrieving job listings, graduate pay data, and skill trends.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Get Jobs by Company

Retrieves jobs from a specific company.

-   **URL:** `/jobs/company/{company_name}`
-   **Method:** GET
-   **URL Parameters:**
    -   `company_name`: The exact name of the company (case-insensitive)
-   **Example:**
    ```
    http://localhost:8000/jobs/company/EPS%20CONSULTANTS%20PTE%20LTD
    ```
-   **Note:** Spaces in the company name are automatically encoded by the browser.

### 2. Get Jobs by Title

Retrieves jobs that contain a specific title part.

-   **URL:** `/jobs/title/{title_part}`
-   **Method:** GET
-   **URL Parameters:**
    -   `title_part`: A part of the job title to search for
-   **Example:**
    ```
    http://localhost:8000/jobs/title/learning
    ```

### 3. Get Jobs by Skills

Retrieves jobs that require specific skills.

-   **URL:** `/jobs/skills/{skills}`
-   **Method:** GET
-   **URL Parameters:**
    -   `skills`: Comma-separated list of skills
-   **Examples:**
    ```
    http://localhost:8000/jobs/skills/blockchain,python
    http://localhost:8000/jobs/skills/sql
    http://localhost:8000/jobs/skills/big%20data,python
    ```
-   **Note:** Multiple skills can be chained using commas. Spaces in skill names are automatically encoded by the browser.

## For Chart Data

### 4. Get Graduate Starting Pay Data

Retrieves all graduate starting pay data.

-   **URL:** `/get_graduate_starting_pay_data`
-   **Method:** GET
-   **Example:**
    ```
    http://localhost:8000/get_graduate_starting_pay_data
    ```

### 5. Get Top Skills

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

## Response Formats

-   Jobs endpoints return a list of Job objects with the following structure:

    ```json
    {
        "id": "string",
        "job_title": "string",
        "company": "string",
        "date": "string",
        "job_link": "string",
        "skills": ["string"]
    }
    ```

-   The graduate pay data endpoint returns a list of objects with the structure defined in your database.

-   The top skills endpoint returns a list of objects with the following structure:
    ```json
    [
      {
        "skill": "string",
        "count": integer
      }
    ]
    ```

## Error Handling

-   If an error occurs, the API will return a JSON object with an "detail" field describing the error.
-   HTTP status codes are used to indicate the success or failure of an API request.

## Notes

-   All endpoints are case-insensitive for search parameters.
-   The API uses regular expressions for partial matching in title and skill searches.
-   Ensure to URL-encode parameters when making requests, especially for company names or skills with spaces.
