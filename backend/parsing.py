import csv
import json
import re
from job_class import Job
from pymongo import MongoClient
from bson import ObjectId


def load_skills(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return [skill.lower() for skill in data["skills"]]


def parse_skills(description, skills):
    description = description.lower()
    found_skills = []
    for skill in skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", description):
            found_skills.append(skill)
    return found_skills


def parse_description(description, skills):
    return parse_skills(description, skills)


def process_csv(csv_file_path, json_file_path):
    skills = load_skills(json_file_path)
    jobs = []

    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Check if any of the required fields are empty
            if all(row[field].strip() for field in ["Title", "Company", "Date", "Job Link", "Description"]):
                parsed_skills = parse_description(row["Description"], skills)

                # Only create and append the job if parsed_skills is not empty
                if parsed_skills:
                    job = Job(
                        job_title=row["Title"],
                        company=row["Company"],
                        date=row["Date"],
                        job_link=row["Job Link"],
                        skills=parsed_skills,
                    )
                    jobs.append(job)
            else:
                print(f"Skipping row due to empty field(s): {row['Title']}")

    return jobs


def connect_to_mongodb(connection_string):
    client = MongoClient(connection_string)
    return client


def insert_jobs_to_mongodb(jobs, db_client, db_name, collection_name):
    db = db_client[db_name]
    collection = db[collection_name]

    for job in jobs:
        job_dict = {
            "job_title": job.job_title,
            "company": job.company,
            "date": job.date,
            "job_link": job.job_link,
            "skills": job.skills,
            "id": str(job.id),  # Convert UUID to string
        }
        collection.insert_one(job_dict)


def read_connection_string(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()


if __name__ == "__main__":
    csv_file_path = "linkedin_jobs.csv"
    json_file_path = "tech-skills-json.json"
    secrets_file_path = "secret.txt"
    db_name = "WAD2"
    collection_name = "Jobs"

    # Process CSV and create Job objects
    processed_jobs = process_csv(csv_file_path, json_file_path)

    # Print out the processed jobs
    for job in processed_jobs:
        print(job)
        print("---")

    # Read MongoDB connection string from secrets file
    mongodb_connection_string = read_connection_string(secrets_file_path)

    # Connect to MongoDB Atlas
    mongo_client = connect_to_mongodb(mongodb_connection_string)

    # Insert jobs into MongoDB
    insert_jobs_to_mongodb(processed_jobs, mongo_client, db_name, collection_name)

    print(f"Inserted {len(processed_jobs)} jobs into MongoDB Atlas.")

    # Close the MongoDB connection
    mongo_client.close()
