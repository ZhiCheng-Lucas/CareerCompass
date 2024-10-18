from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from pymongo import MongoClient
import csv
import json
import re
from collections import Counter

app = FastAPI(title="Job Processing API", description="API for searching and retrieving job listings", version="1.0.0")


def read_secret(secret_name):
    try:
        with open(f"/run/secrets/{secret_name}", "r") as secret_file:
            return secret_file.read().strip()
    except IOError:
        print(f"Could not read secret.")
        return None


# MongoDB connection
connection_string = read_secret("mongodb_connection_string")
if connection_string:
    client = MongoClient(connection_string)
    db = client["WAD2"]
    jobs_collection = db["Jobs"]
    graduate_pay_collection = db["graduate_starting_salary"]

else:
    raise Exception("MongoDB connection string not found in Docker secrets")


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


def load_skills(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return [skill.lower() for skill in data["skills"]]


def parse_skills(description, skills):
    description = description.lower()
    return [skill for skill in skills if skill in description]


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


def insert_jobs_to_mongodb(jobs, collection):
    inserted_count = 0
    for job in jobs:
        job_dict = job.dict()
        result = collection.update_one({"id": job_dict["id"]}, {"$set": job_dict}, upsert=True)
        if result.upserted_id or result.modified_count > 0:
            inserted_count += 1
    return inserted_count


@app.get("/load_data")
async def load_data():
    """
    Load data from CSV file, process it, and insert into MongoDB.
    This operation runs synchronously and may take some time to complete.

    Returns:
        dict: A message indicating the number of jobs inserted or updated in the database.
    """
    csv_file_path = "linkedin_jobs.csv"
    json_file_path = "tech-skills-json.json"

    processed_jobs = process_csv(csv_file_path, json_file_path)
    inserted_count = insert_jobs_to_mongodb(processed_jobs, jobs_collection)

    return {"message": f"Data loading process completed. {inserted_count} jobs inserted or updated in MongoDB."}


@app.get("/")
async def read_root():
    """
    Welcome endpoint for the Job Processing API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Job Processing API"}


@app.get("/jobs/all", response_model=List[Job])
async def get_all_jobs(limit: int = Query(default=100, ge=1, le=1000)):
    """
    Retrieve all jobs from the database, with an optional limit.

    Args:
        limit (int): Maximum number of jobs to return. Default is 100, min 1, max 1000.

    Returns:
        List[Job]: A list of Job objects.
    """
    try:
        jobs = list(jobs_collection.find().limit(limit))
        return [Job(**job) for job in jobs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# If the company field in the db is     "company": "EPS CONSULTANTS PTE LTD",
# Search has to be http://localhost:8000/jobs/company/EPS%20CONSULTANTS%20PTE%20LTD
# You can leave space. The browser should automatically encode it.
@app.get("/jobs/company/{company_name}", response_model=List[Job])
async def get_jobs_by_company(company_name: str):
    jobs = list(jobs_collection.find({"company": {"$regex": f"^{re.escape(company_name)}$", "$options": "i"}}))
    return [Job(**job) for job in jobs]


# http://localhost:8000/jobs/title/learning - will return jobd with learning in its name.
@app.get("/jobs/title/{title_part}", response_model=List[Job])
async def get_jobs_by_title(title_part: str):
    jobs = list(jobs_collection.find({"job_title": {"$regex": re.escape(title_part), "$options": "i"}}))
    return [Job(**job) for job in jobs]


# Can chain multiple skills
# . http://localhost:8000/jobs/skills/blockchain,python
# http://localhost:8000/jobs/skills/sql
# Multiple length skills. You can leave space, the browser should automatically encode it.
#  http://localhost:8000/jobs/skills/big%20data,python
@app.get("/jobs/skills/{skills}", response_model=List[Job])
async def get_jobs_by_skills(skills: str):
    skill_list = [skill.replace("_", " ") for skill in skills.split(",")]
    query = {"$or": [{"skills": {"$regex": f"^{re.escape(skill)}$", "$options": "i"}} for skill in skill_list]}
    jobs = list(jobs_collection.find(query))
    return [Job(**job) for job in jobs]


# For Charts
@app.get("/get_graduate_starting_pay_data")
async def get_graduate_starting_pay_data():
    """
    Retrieve all graduate starting pay data from the database.

    Returns:
        list: A list of all graduate starting pay data entries.
    """
    try:
        data = list(graduate_pay_collection.find({}, {"_id": 0}))  # Exclude the MongoDB _id field
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# For charts
@app.get("/top_skills")
async def get_top_skills(limit: int = Query(default=10, ge=1, le=100)):
    """
    Retrieve the top N most frequent skills from all job listings.

    Args:
        limit (int): Number of top skills to return. Default is 10, min 1, max 100.

    Returns:
        List[Dict]: A list of dictionaries containing skills and their frequencies, sorted by frequency.
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
