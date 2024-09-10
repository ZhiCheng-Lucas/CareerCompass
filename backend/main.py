"""
Job Processing API

This FastAPI application provides endpoints to search and retrieve job listings
from a MongoDB database. It allows searching by company, job title, and skills.

Endpoints:
- GET /: Welcome message
- GET /jobs/company/{company_name}: Get jobs by company name
- GET /jobs/title/{title_part}: Get jobs by partial job title
- GET /jobs/skills/{skills}: Get jobs by skills (comma-separated)

Usage:
Run this script to start the FastAPI server. Access the API documentation
at http://localhost:8000/docs when the server is running.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from pymongo import MongoClient
from parsing import read_connection_string

app = FastAPI(title="Job Processing API", description="API for searching and retrieving job listings", version="1.0.0")

# MongoDB connection
connection_string = read_connection_string("secret.txt")
client = MongoClient(connection_string)
db = client["WAD2"]
jobs_collection = db["jobs"]


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


@app.get("/")
async def read_root():
    """
    Welcome endpoint for the Job Processing API.

    Returns:
        dict: A welcome message.

    Example:
        GET /
        Response: {"message": "Welcome to the Job Processing API"}
    """
    return {"message": "Welcome to the Job Processing API"}


@app.get("/jobs/company/{company_name}", response_model=List[Job])
async def get_jobs_by_company(company_name: str):
    """
    Retrieve all jobs for a specific company.

    Args:
        company_name (str): The exact name of the company to search for.

    Returns:
        List[Job]: A list of Job objects matching the company name.

    Example:
        GET /jobs/company/NSCC
        Response: [
            {
                "id": "60f1a7b9e4b0b1f3c3d9e8f7",
                "job_title": "HPC Storage Engineer (System)",
                "company": "NSCC",
                "date": "2023-07-15",
                "job_link": "https://example.com/job/123",
                "skills": ["HPC", "Storage", "Linux"]
            },
            ...
        ]
    """
    jobs = list(jobs_collection.find({"company": company_name}))
    return [Job(**job) for job in jobs]


@app.get("/jobs/title/{title_part}", response_model=List[Job])
async def get_jobs_by_title(title_part: str):
    """
    Retrieve all jobs where the job title contains a specific term.

    Args:
        title_part (str): A part of the job title to search for (case-insensitive).

    Returns:
        List[Job]: A list of Job objects where the job title contains the search term.

    Example:
        GET /jobs/title/engineer
        Response: [
            {
                "id": "60f1a7b9e4b0b1f3c3d9e8f7",
                "job_title": "HPC Storage Engineer (System)",
                "company": "NSCC",
                "date": "2023-07-15",
                "job_link": "https://example.com/job/123",
                "skills": ["HPC", "Storage", "Linux"]
            },
            ...
        ]
    """
    jobs = list(jobs_collection.find({"job_title": {"$regex": title_part, "$options": "i"}}))
    return [Job(**job) for job in jobs]


@app.get("/jobs/skills/{skills}", response_model=List[Job])
async def get_jobs_by_skills(skills: str):
    """
    Retrieve all jobs that require at least one of the specified skills.
    for skills with spaces.
    can either
    http://localhost:8000/jobs/skills/big%20data,nlp
    or
    http://localhost:8000/jobs/skills/big_data,nlp


    Args:
        skills (str): Comma-separated list of skills to search for.
                      Use underscore for spaces in skill names (e.g., machine_learning).

    Returns:
        List[Job]: A list of Job objects that match at least one of the specified skills.

    Examples:
        1. Search for multiple skills:
           GET /jobs/skills/python,php,css
        2. Search for a skill with spaces:
           GET /jobs/skills/machine_learning
        3. Search for a single skill:
           GET /jobs/skills/bash
    """
    skill_list = [skill.replace("_", " ") for skill in skills.split(",")]
    query = {"$or": [{"skills": {"$regex": f".*{skill}.*", "$options": "i"}} for skill in skill_list]}
    jobs = list(jobs_collection.find(query))
    return [Job(**job) for job in jobs]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
