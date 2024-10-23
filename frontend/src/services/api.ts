import axios from 'axios';
import type { Job } from '@/types/job';

const API_URL = 'http://localhost:8000';

// Types for authentication
interface LoginResponse {
  username: string;
  skills: string[];
}

interface AuthResponse {
  message: string;
}

interface RecommendedJob {
  job_title: string;
  company: string;
  job_link: string;
  match_percentage: number;
  matching_skills: string[];
}

interface RecommendedSkill {
  skill: string;
  frequency: number;
  example_jobs: string[];
}

interface ResumeAnalysisResponse {
  message: string;
  extracted_skills: string[];
  ai_improvements: string;
  recommended_jobs: RecommendedJob[];
  recommended_skills_to_learn: RecommendedSkill[];
}

// Authentication endpoints
export const login = async (username: string, password: string): Promise<LoginResponse> => {
  const response = await axios.post<LoginResponse>(`${API_URL}/login`, {
    username,
    password
  });
  return response.data;
};

export const register = async (username: string, password: string): Promise<AuthResponse> => {
  const response = await axios.post<AuthResponse>(`${API_URL}/signup`, {
    username,
    password
  });
  return response.data;
};

// Existing job-related endpoints
export const getAllJobs = async (limit?: number): Promise<Job[]> => {
  const response = await axios.get<Job[]>(`${API_URL}/jobs/all`, {
    params: { limit },
  });
  return response.data;
};

export const getJobsByCompany = async (companyName: string): Promise<Job[]> => {
  const response = await axios.get<Job[]>(`${API_URL}/jobs/company/${encodeURIComponent(companyName)}`);
  return response.data;
};

export const getJobsByTitle = async (titlePart: string): Promise<Job[]> => {
  const response = await axios.get<Job[]>(`${API_URL}/jobs/title/${encodeURIComponent(titlePart)}`);
  return response.data;
};

export const getJobsBySkills = async (skills: string[]): Promise<Job[]> => {
  const skillsString = skills.map(skill => encodeURIComponent(skill)).join(',');
  const response = await axios.get<Job[]>(`${API_URL}/jobs/skills/${skillsString}`);
  return response.data;
};

export const getGraduateStartingPayData = async () => {
  const response = await axios.get(`${API_URL}/get_graduate_starting_pay_data`);
  return response.data;
};

export const getTopSkills = async (limit?: number) => {
  const response = await axios.get(`${API_URL}/top_skills`, {
    params: { limit },
  });
  return response.data;
};

export const uploadResume = async (
  file: File,
  username: string,
  password: string
): Promise<ResumeAnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('username', username);
  formData.append('password', password);

  const response = await axios.post<ResumeAnalysisResponse>(
    `${API_URL}/upload_resume`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
  return response.data;
};

// Function to get recommended jobs based on resume
export const getRecommendedJobs = async (
  username: string,
  password: string
): Promise<RecommendedJob[]> => {
  const response = await axios.get<ResumeAnalysisResponse>(
    `${API_URL}/upload_resume`,
    {
      params: { username, password }
    }
  );
  return response.data.recommended_jobs;
};

// Function to get recommended skills to learn
export const getRecommendedSkills = async (
  username: string,
  password: string
): Promise<RecommendedSkill[]> => {
  const response = await axios.get<ResumeAnalysisResponse>(
    `${API_URL}/upload_resume`,
    {
      params: { username, password }
    }
  );
  return response.data.recommended_skills_to_learn;
};