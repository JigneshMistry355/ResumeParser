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


class ResumeData(BaseModel):
    '''Parsed Resume Data'''
    skills: Optional[List[str]] = Field(description="Individual Programming languages, frameworks and libraries", default_factory=list)
    soft_skills: Optional[List[str]]
    years_of_experience: Optional[str]
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


class ResumeMatchAnalysis(BaseModel):
    overall_match_percentage: Optional[str] = Field(
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
    education_match_analysis: Optional[str]
    recommendations_for_improvement: List[Recommendation] 
    skills_gap_analysis: List[SkillsGapAnalysis]