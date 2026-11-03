
import os
import psycopg2
from dotenv import load_dotenv
from backend.resume_processor import resume_skills

load_dotenv()

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = connection.cursor()

cursor.execute("""
    SELECT job_id, job_title, description, skills
    FROM public.jobs
    ORDER BY job_id
""")

jobs = cursor.fetchall()

recommendations = []

resume_skill_lower = [
    skill.lower() for skill in resume_skills
]

for job in jobs:
    job_id, job_title, description, skills = job

    job_skills = [
        skill.strip()
        for skill in (skills or "").split(",")
        if skill.strip()
    ]

    matched_skills = [
        skill for skill in job_skills
        if skill.lower() in resume_skill_lower
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill.lower() not in resume_skill_lower
    ]

    score = (
        len(matched_skills) / len(job_skills) * 100
        if job_skills else 0
    )

    recommendations.append({
        "job_id": job_id,
        "job_title": job_title,
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    })

recommendations.sort(
    key=lambda x: x["score"],
    reverse=True
)

recommendations = recommendations[:3]

cursor.close()
connection.close()
