# CareerCompass Project

This README provides instructions on how to set up and run the CareerCompass project.

## Setup Instructions

1. **Prepare MongoDB Connection String:**

   - Create a file named `mongodb_connection_string.txt` in the same folder as your `docker-compose.yml` file.
   - Add your MongoDB connection string to this file.
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

- `http://localhost:8000/jobs/company/tiktok`
- `http://localhost:8000/jobs/skills/sql`
- `http://localhost:8000/jobs/title/learning`
