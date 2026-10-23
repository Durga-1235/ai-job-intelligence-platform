import requests
import psycopg2
import re
import html


SKILL_KEYWORDS = [
    "Python", "SQL", "Excel", "Power BI", "Tableau",
    "Machine Learning", "Deep Learning", "NLP",
    "TensorFlow", "PyTorch", "Pandas", "NumPy",
    "React", "JavaScript", "HTML", "CSS",
    "Django", "FastAPI", "REST API", "PostgreSQL",
    "MySQL", "Java", "C++", "Git", "AWS", "Azure",
    "Docker", "Kubernetes", "Flask", "Node.js"
]


def clean_description(description):
    description = re.sub(r"<[^>]+>", " ", description or "")
    description = html.unescape(description)
    return re.sub(r"\s+", " ", description).strip()


def extract_skills(text):
    text_lower = (text or "").lower()

    found_skills = [
        skill for skill in SKILL_KEYWORDS
        if re.search(
            r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)",
            text_lower
        )
    ]

    return ", ".join(found_skills)


def fetch_jobs():
    url = "https://remotive.com/api/remote-jobs"

    response = requests.get(
        url,
        params={"limit": 10},
        timeout=(10, 90)
    )
    response.raise_for_status()

    jobs = response.json().get("jobs", [])
    print("Fetched jobs:", len(jobs))

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="job_intelligence",
        user="postgres",
        password="Durga@12345"
    )

    cursor = connection.cursor()
    saved = 0
    updated = 0

    try:
        for job in jobs:
            title = job.get("title") or "Unknown"
            company = job.get("company_name") or "Unknown"
            location = job.get("candidate_required_location") or "Remote"

            description = clean_description(job.get("description"))

            # Extract skills from job title and description
            skills = extract_skills(title + " " + description)

            # Do not guess missing salary information
            salary = None

            cursor.execute(
                """
                SELECT job_id
                FROM public.jobs
                WHERE job_title = %s AND company = %s
                LIMIT 1
                """,
                (title, company)
            )

            existing_job = cursor.fetchone()

            if existing_job:
                cursor.execute(
                    """
                    UPDATE public.jobs
                    SET location = %s,
                        skills = %s,
                        description = %s
                    WHERE job_id = %s
                    """,
                    (
                        location,
                        skills,
                        description,
                        existing_job[0]
                    )
                )
                updated += 1

            else:
                cursor.execute(
                    """
                    INSERT INTO public.jobs
                        (job_title, company, location,
                         skills, salary, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        title,
                        company,
                        location,
                        skills,
                        salary,
                        description
                    )
                )
                saved += 1

        connection.commit()

        print("New jobs saved:", saved)
        print("Existing jobs updated:", updated)

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    fetch_jobs()
