from typing import Optional, List
from pydantic import BaseModel, Field

class JobData(BaseModel):
    '''Job details'''
    job_title: Optional[str] = Field(description="Title of job")
    experience_text: Optional[str] = Field(description="Experience that applicant must have")
    salary: Optional[str] = Field(description="Salary offered for this role")
    location: Optional[str] = Field(description="Location of the company")
    job_description: Optional[str]
    other_details: Optional[str]
    education: Optional[str] = Field(description="Minimum education")
    skills: Optional[List[str]] = Field(description="Individual Programming languages, frameworks and libraries", default_factory=list)

class Candidate(BaseModel):
    '''Candidate personal details'''
    myid: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]

class ResumeData(Candidate):
    '''Parsed Resume Data'''
    skills: Optional[List[str]] = Field(description="Individual Programming languages, frameworks and libraries", default_factory=list)
    soft_skills: Optional[List[str]]
    years_of_experience: Optional[str] = Field(description="Total experience of candidate in years or months")
    education_details: Optional[str]
    key_achievements: Optional[List[str]]
    core_competencies: Optional[str]  
    industry_experience: Optional[str]
    leadership_experience: Optional[str]
    projects_completed: Optional[List[str]]
    

class Recommendation(BaseModel):
    section: str
    recommendation: str
    guidance: str


class SkillsGapAnalysis(BaseModel):
    technical_skills: str
    soft_skills: str


class ResumeMatchAnalysis(Candidate):
    overall_match_percentage: Optional[int] = Field(
        description="Overall match percentage between resume and job"
    )
    matching_skills: List[str] = Field(
        # default_factory=list,
        description="Skills present in both resume and job"
    )
    missing_skills: List[str] = Field(
        # default_factory=list,
        description="Skills required by job but missing in resume"
    )
    experience_match_analysis: Optional[str]
    experience_match_percentage: Optional[int]
    education_match_analysis: Optional[str]
    education_match_percentage: Optional[int]
    project_relevance_percentage: Optional[int] = Field(description="based on keywords in job and resume")
    recommendations_for_improvement: List[Recommendation] 
    skills_gap_analysis: List[SkillsGapAnalysis]