from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from models.model import ResumeMatchAnalysis
import uuid


def match_analyzer(job, resume):
 
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                '''You are a professional resume analyzer. Compare the provided resume to job requirements and generate a detailed analysis in valid JSON format. Extract skills from resume and compare with job requirements.
                Extract the following fields from the given text:
                1. Compare resume to job requirements and return overall match percentage.
                2. Extract all skills from resume and return relevant skills compared to job description.
                3. Extract all skills from resume and return relevant missing skills compared to job description.
                4. Extract overall experience from resume and return detailed analysis compared to job description.
                5. Extract overall education from resume and return detailed analysis compared to job description.
                6. Provide a detailed analysis recommending improvements and providing skill gaps.
                7. Provide relevant percentage for experience match, education match and project match.

                Use the following format and replace the examples:
                {{
                    "full_name": "string"
                    "overall_match_percentage": "int",
                    "matching_skills":["string"],
                    "missing_skills": ["string"],
                    "experience_match_analysis": "string",
                    "experience_match_percentage": "int",
                    "education_match_analysis": "string",
                    "education_match_percentage":"int",
                    "project_relevance_percentage": "int",
                    "recommendations_for_improvement": [
                        {{
                            "section": "string",
                            "recommendation": "string",
                            "guidance": "string"
                        }}
                    ],
                    "skills_gap_analysis": {{
                        "technical_skills": "string",
                        "soft_skills": "string"
                    }}
                }}
                '''
            ),
            (
                "human",
               '''Job requirements: 
                {job}
                Resume details:
                {resume}
                myid: {myid}
                '''

            )
        ]
    ) 
    llm = ChatOllama(model="llama3.2:1b", temperature=0)
    # llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    # llm = init_chat_model("google_genai:gemini-2.5-flash-lite")
    structure_model = llm.with_structured_output(
            schema=ResumeMatchAnalysis,
            method="json_schema",
            include_raw=False
        )
    prompt = prompt_template.invoke({"job": job, "resume": resume, "myid": uuid.uuid4()})
    result = structure_model.invoke(prompt)
    return result


# r = match_analyzer(job, resume)
# print(r.__dict__)

