import uuid
from typing import List


class Job:
    def __init__(self, job_title: str, company: str, date: str, job_link: str, skills: List[str]):
        self.id = uuid.uuid4()  # Generate a unique ID
        self.job_title = job_title
        self.company = company
        self.date = date
        self.job_link = job_link
        self.skills = skills

    def __str__(self):
        return f"Job(id={self.id}, title='{self.job_title}', company='{self.company}', date='{self.date}', skills={self.skills})"

    def add_skill(self, skill: str):
        if skill not in self.skills:
            self.skills.append(skill)

    def remove_skill(self, skill: str):
        if skill in self.skills:
            self.skills.remove(skill)
