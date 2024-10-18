import { v4 as uuidv4 } from 'uuid';

export interface Job {
  id: string;
  job_title: string;
  company: string;
  date: string;
  job_link: string;
  skills: string[];
}

export class JobModel implements Job {
  id: string;
  job_title: string;
  company: string;
  date: string;
  job_link: string;
  skills: string[];

  constructor(
    job_title: string,
    company: string,
    date: string,
    job_link: string,
    skills: string[]
  ) {
    this.id = uuidv4(); // Generate a unique ID
    this.job_title = job_title;
    this.company = company;
    this.date = date;
    this.job_link = job_link;
    this.skills = skills;
  }
}