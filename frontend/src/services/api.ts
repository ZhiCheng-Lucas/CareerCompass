import axios, { AxiosError } from 'axios';
import type { Job } from '@/types/job';



// For devs
// const API_URL = 'http://localhost:8000';

// For prod purposes.
const API_URL = 'https://orca-app-8ua27.ondigitalocean.app';

// Types for authentication
interface LoginResponse {
  username: string;
  skills: string[];
}

interface AuthResponse {
  message: string;
}

export interface APIError {
  message: string;
  status: number;
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

export interface MarketTrend {
  growth: string;
  period: string;
  details: string;
}

export interface SectorTrend {
  sector: string;
  trends: MarketTrend[];
  source: string;
}

export interface MarketTrendResponse {
  jobMarketTrends: SectorTrend[];
}

export interface IndustryGrowth {
  forecast: {
    date: string;
    source: string;
    previous: string;
    current: string;
  };
  quarterlyGrowth: Array<{
    quarter: string;
    growth: number;
  }>;
  annualGrowth: Array<{
    year: number;
    growth: number;
  }>;
}

export interface LaborStats {
  [period: string]: {
    [sector: string]: number;
  };
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
): Promise<ResumeAnalysisResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('username', username);

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
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Handle 500 error specifically
      if (error.response?.status === 500) {
        throw {
          message: 'Server error: File processing failed. Please try again later or contact support.',
          status: 500
        } as APIError;
      }
      // Handle other status codes
      if (error.response?.status === 413) {
        throw {
          message: 'File size too large. Please upload a smaller file.',
          status: 413
        } as APIError;
      }
      if (error.response?.status === 415) {
        throw {
          message: 'Invalid file type. Please upload a PDF file.',
          status: 415
        } as APIError;
      }
      // Generic error with response
      throw {
        message: error.response?.data?.message || 'Error uploading resume. Please try again.',
        status: error.response?.status || 500
      } as APIError;
    }
    // Network or other errors
    throw {
      message: 'Network error: Unable to connect to server. Please check your connection.',
      status: 0
    } as APIError;
  }
};

export const getUniversityStats = async () => {
  const response = await axios.get(`${API_URL}/university_stats`);
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

export const getMarketTrends = async () => {
  const response = await axios.get<[{ jobMarketTrends: SectorTrend[] }]>(`${API_URL}/get_market_trend`);
  return response.data;
};

export const getIndustryGrowth = async (): Promise<IndustryGrowth[]> => {
  const response = await axios.get<IndustryGrowth[]>(`${API_URL}/get_industry_growth`);
  return response.data;
};

export const getSingaporeLaborStats = async (): Promise<LaborStats> => {
  const response = await axios.get<LaborStats>(`${API_URL}/processed_singapore_labor_stats`);
  return response.data;
};