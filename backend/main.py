from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from backend.job_matcher import recommendations
from pypdf import PdfReader
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="job_intelligence",
    user="postgres",
    password="Durga@12345"
)

@app.get("/")
def home():
    return {"message": "Job Intelligence Platform"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    filename = (file.filename or "").lower()

    if not filename.endswith((".txt", ".pdf")):
        return {
            "error": "Please upload a PDF or TXT resume file"
        }

    contents = await file.read()

    # Extract text from PDF or TXT
    if filename.endswith(".pdf"):
        try:
            pdf = PdfReader(BytesIO(contents))
            resume_text = "\n".join(
                page.extract_text() or ""
                for page in pdf.pages
            )
        except Exception:
            return {
                "error": "Unable to read this PDF. Please upload a valid PDF."
            }

        if not resume_text.strip():
            return {
                "error": "No readable text found. This may be a scanned PDF."
            }
    else:
        resume_text = contents.decode("utf-8", errors="ignore")

    # Extract skills from resume
    skills_list = [
        "Python", "SQL", "Excel", "Power BI",
        "Machine Learning", "NLP", "Django",
        "REST API", "TensorFlow", "FastAPI",
        "PostgreSQL", "React"
    ]

    extracted_skills = [
        skill for skill in skills_list
        if skill.lower() in resume_text.lower()
    ]

    # Get jobs from PostgreSQL
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT job_id, job_title, skills
            FROM public.jobs
            ORDER BY job_id
        """)
        jobs = cursor.fetchall()
    finally:
        cursor.close()

    # Match resume skills with job skills
    new_recommendations = []
    resume_skill_set = {
        skill.lower() for skill in extracted_skills
    }

    for job in jobs:
        job_id, job_title, job_skills = job

        required_skills = [
            skill.strip()
            for skill in (job_skills or "").split(",")
            if skill.strip()
        ]

        matched_skills = [
            skill for skill in required_skills
            if skill.lower() in resume_skill_set
        ]

        missing_skills = [
            skill for skill in required_skills
            if skill.lower() not in resume_skill_set
        ]

        score = (
            len(matched_skills) / len(required_skills) * 100
            if required_skills else 0
        )

        new_recommendations.append({
            "job_id": job_id,
            "job_title": job_title,
            "score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    new_recommendations.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return {
        "filename": file.filename,
        "extracted_skills": extracted_skills,
        "recommendations": new_recommendations[:3]
    }


@app.get("/jobs")
def get_jobs():
    cursor = connection.cursor()

    cursor.execute("""
       SELECT job_id, job_title, location, skills, salary, description
       FROM public.jobs
       ORDER BY job_id
    """)

    jobs = cursor.fetchall()
    cursor.close()

    job_list = []

    for job in jobs:
        job_list.append({
            "job_id": job[0],
            "job_title": job[1],
            "location": job[2],
            "skills": job[3],
            "salary": job[4],
            "description": job[5]
        })

    return {"jobs": job_list}
    
@app.get("/search-jobs")
def search_jobs(
    keyword: str = "",
    location: str = ""
):
    cursor = connection.cursor()

    try:
        query = """
            SELECT job_id, job_title, location, skills,
                   salary, description
            FROM public.jobs
            WHERE job_title ILIKE %s
              AND location ILIKE %s
            ORDER BY job_id
        """

        cursor.execute(
            query,
            (f"%{keyword}%", f"%{location}%")
        )

        jobs = cursor.fetchall()

        return {
            "count": len(jobs),
            "jobs": [
                {
                    "job_id": job[0],
                    "job_title": job[1],
                    "location": job[2],
                    "skills": job[3],
                    "salary": job[4],
                    "description": job[5]
                }
                for job in jobs
            ]
        }

    finally:
        cursor.close()

        


@app.get("/recommendations")
def get_recommendations():
    return {
        "recommendations": recommendations
    }