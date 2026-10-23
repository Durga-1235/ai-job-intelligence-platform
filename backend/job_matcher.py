import psycopg2
from sentence_transformers import SentenceTransformer, util
from backend.resume_processor import resume_skills


# AI model load
model = SentenceTransformer("all-MiniLM-L6-v2")


# Resume skills → one text
resume_text = ", ".join(resume_skills)


# PostgreSQL connection
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="job_intelligence",
    user="postgres",
    password="Durga@12345"
)

cursor = connection.cursor()


# Get jobs from database
cursor.execute("""
    SELECT job_id, job_title, description, skills
    FROM public.jobs
    ORDER BY job_id
""")

jobs = cursor.fetchall()


# Convert resume into AI embedding
resume_embedding = model.encode(
    resume_text,
    convert_to_tensor=True
)


recommendations = []


for job in jobs:

    job_id = job[0]
    job_title = job[1]
    description = job[2]
    skills = job[3]

    # Job description → AI embedding
    job_embedding = model.encode(
        description,
        convert_to_tensor=True
    )

    # Calculate AI similarity
    similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    ).item()

    score = similarity * 100

    job_skills = [
        skill.strip()
        for skill in skills.split(",")
    ]

    resume_skill_lower = [
        skill.lower()
        for skill in resume_skills
    ]

    matched_skills = []
    missing_skills = []

    for skill in job_skills:

        if skill.lower() in resume_skill_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    recommendations.append({
        "job_id": job_id,
        "job_title": job_title,
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    })


# Highest AI score first
recommendations.sort(
    key=lambda x: x["score"],
    reverse=True
)


# Top 3 jobs
top_jobs = recommendations[:3]


print("\nAI Recommended Jobs")
print("-------------------")

for job in top_jobs:

    print("\nJob:", job["job_title"])
    print("AI Match Score:", round(job["score"], 2), "%")
    print("Matched Skills:", job["matched_skills"])
    print("Missing Skills:", job["missing_skills"])


cursor.close()
connection.close()