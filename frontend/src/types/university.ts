// Course-level statistics
export interface CourseStatistics {
    employment_rate_overall: {
      [year: string]: number;
    };
    gross_monthly_mean: {
      [year: string]: number;
    };
  }
  
  // Course mapping
  export interface CourseMap {
    [courseName: string]: CourseStatistics;
  }
  
  // Faculty mapping
  export interface FacultyMap {
    [facultyName: string]: CourseMap;
  }
  
  // University mapping
  export interface UniversityMap {
    [universityName: string]: FacultyMap;
  }
  
  // Chart data point
  export interface ChartDataPoint {
    year: string;
    value: number;
  }
  
  // Metric type
  export type MetricType = 'employment_rate_overall' | 'gross_monthly_mean';