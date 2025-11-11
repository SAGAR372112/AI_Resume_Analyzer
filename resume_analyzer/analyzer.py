import pdfplumber
from groq import Groq
import json
from decouple import config

API_KEY = config('API_KEY')

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_resume_with_llm(resume_text:str, job_description:str) -> dict:

    prompt = f"""
    You are an AI Assistant that analyzes a resume for a software engineering job application.
    Given the resume and the job description, extract the following details:

    1. Identify all skills mentioned in resume.
    2. Calculate the total years of experience.
    3. Categories the projects based on domain (e.g, AI, webdevelopment, Cloud, etc.)
    4. Rank the resume relevance to the job descriptions on a scale of scale of 0 to 100.


    Resume:
    {resume_text}

    Job_Description:
    {job_description}

    Provide the output in valid JSON format with this structure:
    {{
        "rank": "<percentage>",
        "skills": ["skill1", "skill2", .....],
        "total_experience": "<number of year>",
        "project _category": ["category1", "category2", ...]
    }}
    """

    try:
        client = Groq(api_key = API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{'role': 'user', 'content': prompt}], 
            temperature = 0.7,
            response_format = {"type" : "json_object"}
        )
        result = response.choices[0].message.content
        return json.loads(result)

    except Exception as e:
        print(e)
        
def process_resume(pdf_path, job_description):
    try:
        resume_text = extract_text_from_pdf(pdf_path)
        data = analyze_resume_with_llm(resume_text, job_description)
        return data
    except Exception as e:
        print(e)
        return None