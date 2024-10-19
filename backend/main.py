# Import necessary libraries and modules
from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from fuzzywuzzy import fuzz
from typing import List, Dict
from bson import ObjectId
from pymongo import MongoClient
import csv
import json
import re
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

# Initialize FastAPI app
app = FastAPI(title="Job Processing API", description="API for searching and retrieving job listings", version="1.0.0")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Set up password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to read Docker secrets
def read_secret(secret_name):
    try:
        with open(f"/run/secrets/{secret_name}", "r") as secret_file:
            return secret_file.read().strip()
    except IOError:
        print(f"Could not read secret.")
        return None


# Set up MongoDB connection
connection_string = read_secret("mongodb_connection_string")
if connection_string:
    client = MongoClient(connection_string)
    db = client["WAD2"]
    jobs_collection = db["Jobs"]
    graduate_pay_collection = db["graduate_starting_salary"]
    auth_collection = db["auth"]
else:
    raise Exception("MongoDB connection string not found in Docker secrets")

# Create a unique index on the username field to ensure email uniqueness
auth_collection.create_index("username", unique=True)


# Define Pydantic models for data validation and serialization
class Job(BaseModel):
    id: str
    job_title: str
    company: str
    date: str
    job_link: str
    skills: List[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    skills: List[str]


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=10)


# Password verification function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Password hashing function
def get_password_hash(password):
    return pwd_context.hash(password)


# Function to load skills from a JSON file
def load_skills(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return [skill.lower() for skill in data["skills"]]


# Function to parse skills from job description
def parse_skills(description, skills):
    description = description.lower()
    return [skill for skill in skills if skill in description]


# Function to process CSV file and extract job data
def process_csv(csv_file_path, json_file_path):
    skills = load_skills(json_file_path)
    jobs = []

    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if all(row[field].strip() for field in ["Title", "Company", "Date", "Job Link", "Description"]):
                parsed_skills = parse_skills(row["Description"], skills)
                if parsed_skills:
                    job = Job(
                        id=str(ObjectId()),
                        job_title=row["Title"],
                        company=row["Company"],
                        date=row["Date"],
                        job_link=row["Job Link"],
                        skills=parsed_skills,
                    )
                    jobs.append(job)
    return jobs


# Function to insert or update jobs in MongoDB
def insert_jobs_to_mongodb(jobs, collection):
    inserted_count = 0
    for job in jobs:
        job_dict = job.dict()
        result = collection.update_one({"id": job_dict["id"]}, {"$set": job_dict}, upsert=True)
        if result.upserted_id or result.modified_count > 0:
            inserted_count += 1
    return inserted_count


# Signup endpoint
@app.post("/signup", status_code=201)
async def signup(user: UserCreate):
    """
    Create a new user account with empty initial skills.

    Request body:
    {
        "username": "user@example.com",
        "password": "securepassword123"
    }

    Response:
    {
        "message": "User registered successfully with empty skills list"
    }

    Possible errors:
    - 400 Bad Request: If the username already exists
    - 500 Internal Server Error: If there's an issue with the database operation
    """
    try:
        # Hash the password
        hashed_password = get_password_hash(user.password)

        # Prepare user document with empty skills list
        user_doc = {
            "username": user.username,
            "hashed_password": hashed_password,
            "skills": [],  # Initialize with an empty list
        }

        # Insert the new user
        result = auth_collection.insert_one(user_doc)

        if result.inserted_id:
            return {"message": "User registered successfully with empty skills list"}
        else:
            raise HTTPException(status_code=500, detail="Failed to register user")

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Login endpoint
@app.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    """
    Authenticate a user and return their username and skills if successful.

    Request body:
    {
        "username": "user@example.com",
        "password": "securepassword123"
    }

    Response:
    {
        "username": "user@example.com",
        "skills": []
    }

    Possible errors:
    - 401 Unauthorized: If the username doesn't exist or the password is incorrect
    """
    db_user = auth_collection.find_one({"username": user.username})

    if db_user is None:
        raise HTTPException(status_code=401, detail="Username does not exist")

    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return UserResponse(username=db_user["username"], skills=db_user["skills"])


# Data loading endpoint
@app.get("/load_data")
async def load_data():
    """
    Load data from CSV file, process it, and insert into MongoDB.
    This operation runs synchronously and may take some time to complete.

    Response:
    {
        "message": "Data loading process completed. X jobs inserted or updated in MongoDB."
    }

    Note: This endpoint is typically used for initial data population or updates.
    """
    csv_file_path = "linkedin_jobs.csv"
    json_file_path = "tech-skills-json.json"

    processed_jobs = process_csv(csv_file_path, json_file_path)
    inserted_count = insert_jobs_to_mongodb(processed_jobs, jobs_collection)

    return {"message": f"Data loading process completed. {inserted_count} jobs inserted or updated in MongoDB."}


# Root endpoint
@app.get("/")
async def read_root():
    """
    Welcome endpoint for the Job Processing API.

    Response:
    {
        "message": "Welcome to the Job Processing API"
    }
    """
    return {"message": "Welcome to the Job Processing API"}


# Get all jobs endpoint
@app.get("/jobs/all", response_model=List[Job])
async def get_all_jobs(limit: int = Query(default=100, ge=1, le=10000)):
    """
    Retrieve all jobs from the database, with an optional limit.

    Query Parameters:
    - limit (optional): Maximum number of jobs to return. Default is 100, min 1, max 10000.

    Examples:
    - GET /jobs/all
    - GET /jobs/all?limit=500

    Response: A list of Job objects
    [
        {
            "id": "...",
            "job_title": "Software Engineer",
            "company": "Tech Corp",
            "date": "2023-05-01",
            "job_link": "https://example.com/job1",
            "skills": ["python", "javascript", "docker"]
        },
        ...
    ]

    Possible errors:
    - 500 Internal Server Error: If there's an issue with the database operation
    """
    try:
        jobs = list(jobs_collection.find().limit(limit))
        return [Job(**job) for job in jobs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Get jobs by company endpoint
@app.get("/jobs/company/{company_name}", response_model=List[Job])
async def get_jobs_by_company(company_name: str):
    """
    Retrieve jobs from a specific company (case-insensitive).

    URL Parameters:
    - company_name: The exact name of the company (case-insensitive)

    Example:
    GET /jobs/company/EPS%20CONSULTANTS%20PTE%20LTD

    Note: Spaces in the company name are automatically encoded by the browser.

    Response: A list of Job objects from the specified company
    [
        {
            "id": "...",
            "job_title": "Data Analyst",
            "company": "EPS CONSULTANTS PTE LTD",
            "date": "2023-05-15",
            "job_link": "https://example.com/job2",
            "skills": ["sql", "python", "data visualization"]
        },
        ...
    ]
    """
    jobs = list(jobs_collection.find({"company": {"$regex": f"^{re.escape(company_name)}$", "$options": "i"}}))
    return [Job(**job) for job in jobs]


# Get jobs by title endpoint
@app.get("/jobs/title/{title_part}", response_model=List[Job])
async def get_jobs_by_title(title_part: str):
    """
    Retrieve jobs that contain a specific title part (case-insensitive).

    URL Parameters:
    - title_part: A part of the job title to search for

    Example:
    GET /jobs/title/learning

    Response: A list of Job objects with titles containing the specified part
    [
        {
            "id": "...",
            "job_title": "Machine Learning Engineer",
            "company": "AI Solutions Inc.",
            "date": "2023-05-20",
            "job_link": "https://example.com/job3",
            "skills": ["python", "machine learning", "tensorflow"]
        },
        ...
    ]
    """
    jobs = list(jobs_collection.find({"job_title": {"$regex": re.escape(title_part), "$options": "i"}}))
    return [Job(**job) for job in jobs]


# Get jobs by skills endpoint
@app.get("/jobs/skills/{skills}", response_model=List[Job])
async def get_jobs_by_skills(skills: str):
    """
    Retrieve jobs that require specific skills (case-insensitive).

    URL Parameters:
    - skills: Comma-separated list of skills

    Examples:
    - GET /jobs/skills/blockchain,python
    - GET /jobs/skills/sql
    - GET /jobs/skills/big%20data,python

    Note:
    - Multiple skills can be chained using commas.
    - Spaces in skill names are automatically encoded by the browser.

    Response: A list of Job objects requiring the specified skills
    [
        {
            "id": "...",
            "job_title": "Blockchain Developer",
            "company": "Crypto Innovations",
            "date": "2023-05-25",
            "job_link": "https://example.com/job4",
            "skills": ["blockchain", "python", "smart contracts"]
        },
        ...
    ]
    """
    skill_list = [skill.replace("_", " ") for skill in skills.split(",")]
    query = {"$or": [{"skills": {"$regex": f"^{re.escape(skill)}$", "$options": "i"}} for skill in skill_list]}
    jobs = list(jobs_collection.find(query))
    return [Job(**job) for job in jobs]


# Get graduate starting pay data endpoint
@app.get("/get_graduate_starting_pay_data")
async def get_graduate_starting_pay_data():
    """
    Retrieve all graduate starting pay data from the database.

    Example:
    GET /get_graduate_starting_pay_data

    Response: A list of graduate starting pay data entries
    [
        {
            "year": 2023,
            "degree": "Computer Science",
            "starting_salary": 65000
        },
        ...
    ]

    Possible errors:
    - 500 Internal Server Error: If there's an issue with the database operation
    """
    try:
        data = list(graduate_pay_collection.find({}, {"_id": 0}))  # Exclude the MongoDB _id field
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Get top skills endpoint
@app.get("/top_skills")
async def get_top_skills(limit: int = Query(default=10, ge=1, le=100)):
    """
    Retrieve the top N most frequent skills from all job listings.

    Query Parameters:
    - limit (optional): Number of top skills to return. Default is 10, min 1, max 100.

    Examples:
    - GET /top_skills
    - GET /top_skills?limit=20

    Response: A list of dictionaries containing skills and their frequencies, sorted by frequency
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

    Possible errors:
    - 500 Internal Server Error: If there's an issue with the database operation
    """
    try:
        # Get all jobs from the database
        jobs = jobs_collection.find({}, {"skills": 1, "_id": 0})

        # Count skills
        skill_counter = Counter()
        for job in jobs:
            skill_counter.update(job.get("skills", []))

        # Get top N skills
        top_skills = skill_counter.most_common(limit)

        # Format the result
        result = [{"skill": skill, "count": count} for skill, count in top_skills]

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def calculate_skill_match(user_skills: List[str], job_skills: List[str]) -> tuple[float, List[str]]:
    """
    Calculate the percentage of matching skills and return matching skills.
    Uses fuzzy matching to allow for partial matches.
    """
    matching_skills = []
    for user_skill in user_skills:
        for job_skill in job_skills:
            if fuzz.partial_ratio(user_skill.lower(), job_skill.lower()) >= 80:
                matching_skills.append(job_skill)
                break

    match_percentage = (len(matching_skills) / len(job_skills)) * 100 if job_skills else 0
    return match_percentage, matching_skills


@app.get("/get_recommended_jobs/{username}")
async def get_recommended_jobs(username: str):
    """
    Get top 5 recommended jobs for a user based on their skills.

    This function performs the following steps:
    1. Validates the username exists in the database.
    2. Retrieves the user's skills.
    3. Fetches all jobs from the database.
    4. Calculates a match percentage for each job based on the user's skills.
    5. Returns the top 5 jobs with the highest match percentage.

    Args:
        username (str): The username (email) of the user to get recommendations for.

    Returns:
        List[Dict]: A list of dictionaries containing the top 5 recommended jobs.
                    Each dictionary includes:
                    - job_title (str): The title of the job.
                    - company (str): The company offering the job.
                    - job_link (str): URL link to the job posting.
                    - match_percentage (float): Percentage of user's skills matching the job requirements.
                    - matching_skills (List[str]): List of skills that matched between the user and the job.

    Raises:
        HTTPException:
            - 404 status code if the username is not found in the database.

    Examples:
        1. Successful request with recommendations:
           GET /get_recommended_jobs/user@example.com
           Response:
           [
               {
                   "job_title": "Senior Python Developer",
                   "company": "Tech Solutions Inc.",
                   "job_link": "https://example.com/job/12345",
                   "match_percentage": 85.71,
                   "matching_skills": ["python", "django", "postgresql"]
               },
               {
                   "job_title": "Full Stack Engineer",
                   "company": "WebDev Co.",
                   "job_link": "https://example.com/job/67890",
                   "match_percentage": 71.42,
                   "matching_skills": ["python", "javascript", "react"]
               },
               ...
           ]

        2. User with no skills:
           GET /get_recommended_jobs/newuser@example.com
           Response:
           {
               "message": "User has no skills listed. No job recommendations available."
           }

        3. Invalid username:
           GET /get_recommended_jobs/nonexistent@example.com
           Response:
           {
               "detail": "Invalid username"
           }

    Notes:
        - The function uses fuzzy matching to allow for partial skill matches.
          For example, "python" in job requirements might match with "python3" in user skills.
        - The match percentage is calculated as: (number of matching skills / total job skills) * 100
        - If multiple jobs have the same match percentage, they are ranked based on their order in the database.
        - The function returns at most 5 job recommendations, even if more jobs have matching skills.
        - Job links are truncated in the example for brevity, but in actual responses, they will be full URLs.
        - Match percentages are rounded to two decimal places in the response.
    """
    user = auth_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username")

    user_skills = user.get("skills", [])
    if not user_skills:
        return {"message": "User has no skills listed. No job recommendations available."}

    all_jobs = list(jobs_collection.find())
    job_matches = []

    for job in all_jobs:
        match_percentage, matching_skills = calculate_skill_match(user_skills, job.get("skills", []))
        job_matches.append(
            {
                "job_title": job["job_title"],
                "company": job["company"],
                "job_link": job["job_link"],
                "match_percentage": round(match_percentage, 2),
                "matching_skills": matching_skills,
            }
        )

    # Sort by match percentage (descending) and take top 5
    recommended_jobs = sorted(job_matches, key=lambda x: x["match_percentage"], reverse=True)[:5]

    return recommended_jobs


@app.get("/get_recommended_skill_to_learn/{username}")
async def get_recommended_skill_to_learn(username: str):
    """
    Get top 5 recommended skills for a user to learn based on their current skills and job market demand.

    This function performs the following steps:
    1. Validates the username exists in the database.
    2. Retrieves the user's current skills.
    3. Finds jobs where the user matches at least one skill.
    4. Identifies new skills from these jobs that the user doesn't have.
    5. Ranks these new skills by frequency.
    6. Returns the top 5 skills with their frequency and example jobs.

    Args:
        username (str): The username (email) of the user to get skill recommendations for.

    Returns:
        List[Dict]: A list of dictionaries containing the top (up to 5) recommended skills.
                    Each dictionary includes:
                    - skill (str): The name of the recommended skill.
                    - frequency (int): Number of matching jobs that require this skill.
                    - example_jobs (List[str]): Titles of up to 3 jobs requiring this skill.

    Raises:
        HTTPException:
            - 404 status code if the username is not found in the database.

    Examples:
        1. Successful request with recommendations:
           GET /get_recommended_skill_to_learn/user@example.com
           Response:
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

        2. User with no skills:
           GET /get_recommended_skill_to_learn/newuser@example.com
           Response:
           {
               "message": "User has no skills listed. No skill recommendations available."
           }

        3. Invalid username:
           GET /get_recommended_skill_to_learn/nonexistent@example.com
           Response:
           {
               "detail": "Invalid username"
           }

    Notes:
        - The function recommends skills from jobs where the user matches at least one skill.
        - Recommended skills are ranked by their frequency in matching jobs.
        - If there are fewer than 5 new skills to recommend, only the available skills are returned.
        - In case of ties in skill frequency, skills are ranked based on the order they appear in the data.
        - The function provides up to 3 example job titles for each recommended skill.
    """
    # Validate user and retrieve their skills
    user = auth_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username")

    user_skills = set(user.get("skills", []))
    if not user_skills:
        return {"message": "User has no skills listed. No skill recommendations available."}

    # Find jobs where the user matches at least one skill
    matching_jobs = list(jobs_collection.find({"skills": {"$in": list(user_skills)}}))

    if not matching_jobs:
        return {"message": "No matching jobs found for user's skills. No skill recommendations available."}

    # Identify new skills from matching jobs
    new_skills = set()
    skill_to_jobs = {}
    for job in matching_jobs:
        job_skills = set(job.get("skills", []))
        new_job_skills = job_skills - user_skills
        new_skills.update(new_job_skills)
        for skill in new_job_skills:
            if skill not in skill_to_jobs:
                skill_to_jobs[skill] = []
            skill_to_jobs[skill].append(job["job_title"])

    # Count frequency of new skills
    skill_frequency = Counter()
    for job in matching_jobs:
        job_skills = set(job.get("skills", []))
        new_job_skills = job_skills - user_skills
        skill_frequency.update(new_job_skills)

    # Prepare recommendations
    recommendations = []
    for skill, freq in skill_frequency.most_common(5):  # Get top 5 skills
        recommendations.append(
            {"skill": skill, "frequency": freq, "example_jobs": skill_to_jobs[skill][:3]}  # Limit to 3 example jobs
        )

    return recommendations


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
