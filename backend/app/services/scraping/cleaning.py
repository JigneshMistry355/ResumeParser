from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from models.model import JobData

load_dotenv()


def setup_gemini_api():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set")
    os.environ.setdefault("GOOGLE_API_KEY", gemini_api_key)


def get_llm():
    return init_chat_model("google_genai:gemini-2.5-flash-lite")


def job_analyzer(text):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                '''You are an expert in extracting structured data from job posting. 
                Extract the following fields from the given text:

                1. job_title
                2. experience_text
                3  salary
                4. location
                5. job_description
                6. other_details
                7. education
                8. skills 

               
                Return ONLY structured JSON.'''
            ),
            (
                "human",
                "{text}"
            )
        ]
    ) 
    llm = ChatOllama(model="llama3.2:1b", temperature=0)
    # llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    # llm = get_llm()
    structure_model = llm.with_structured_output(
            schema=JobData,
            method="json_schema",
            include_raw=False
        )
    prompt = prompt_template.invoke({"text": text})
    result = structure_model.invoke(prompt)
    return result.__dict__


# r = job_analyzer(text)
# print(r.__dict__)