import PyPDF2
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from models.model import ResumeData
from langchain_ollama import ChatOllama

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# def read_docx(file):
#     doc = docx.Document(file)
#     text = ""
#     for paragraph in doc.paragraphs:
#         text += paragraph.text + "\n"
#     return text

def load_resume(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return read_pdf(uploaded_file)
    # elif uploaded_file.name.endswith('.docx'):
    #     return read_docx(uploaded_file)
    else:
        st.error("Unsupported file")
        return None
    


def resume_analyzer(resume):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                '''Analyze this resume and provide a detailed JSON with:
                1. skills - extract each individual skills in list
                2. Soft skills
                3. Years of experience
                4. Education details
                5. Key achievements
                6. Core competencies  
                7. Industry experience
                8. Leadership experience
                9. Technologies used
                10. Projects completed
                Format the response as a JSON object with these categories.
                '''
            ),
            (
                "human",
                "{resume}"
            )
        ]
    ) 
    llm = ChatOllama(model="llama3.2:1b", temperature=0)
    # llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    # llm = init_chat_model("google_genai:gemini-2.5-flash-lite")
    structure_model = llm.with_structured_output(
            schema=ResumeData,
            method="json_schema",
            include_raw=False
        )
    prompt = prompt_template.invoke({"resume": resume})
    result = structure_model.invoke(prompt)
    return result