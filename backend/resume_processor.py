import re

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
    "PostgreSQL",
    "React"
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


with open("backend/resume/resume.txt", "r", encoding="utf-8") as file:
    resume_text = file.read()


clean_resume = clean_text(resume_text)

resume_skills = extract_skills(clean_resume)

print("Resume Skills:")
print(resume_skills)