import pandas as pd
import psycopg2
import re
df = pd.read_csv("backend/data/jobs.csv")
df["location"] = df["location"].str.strip().str.title()
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
df["clean_description"] = df["description"].apply(clean_text)
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

    return ", ".join(found_skills)

df["skills"] = df["clean_description"].apply(extract_skills)
print(df)
print(df.isnull().sum())
print(df.duplicated().sum())
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="job_intelligence",
    user="postgres",
    password="Durga@12345"
)

print("PostgreSQL connected successfully!")
cursor = connection.cursor()
for index, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO jobs
        (job_title, company, location, description, skills, salary)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            row["job_title"],
            row["company"],
            row["location"],
            row["description"],
            row["skills"],
            int(row["salary"])
        )
    )

connection.commit()

print("All jobs inserted successfully!")

cursor.close()
connection.close()