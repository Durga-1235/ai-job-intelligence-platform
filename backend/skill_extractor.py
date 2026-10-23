import psycopg2


skills_list = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Machine Learning",
    "NLP",
    "Django",
    "REST API",
    "TensorFlow",
    "FastAPI",
    "PostgreSQL"
]


def extract_skills(description):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in description.lower():
            found_skills.append(skill)

    return found_skills


connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="job_intelligence",
    user="postgres",
    password=123456
)

cursor = connection.cursor()

cursor.execute("""
    SELECT job_id, job_title, description
    FROM public.jobs
    ORDER BY job_id
""")

jobs = cursor.fetchall()

for job in jobs:
    job_id = job[0]
    job_title = job[1]
    description = job[2]

    extracted_skills = extract_skills(description)

    print("Job ID:", job_id)
    print("Job:", job_title)
    print("Extracted Skills:", extracted_skills)
    print("------------------------")

    skills_text = ", ".join(extracted_skills)

    cursor.execute(
        """
        UPDATE public.jobs
        SET skills = %s
        WHERE job_id = %s
        """,
        (skills_text, job_id)
    )


connection.commit()


cursor.close()
connection.close()