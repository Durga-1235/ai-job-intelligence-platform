# AI-Powered Job Intelligence & Career Recommendation Platform

An AI-powered web application that helps users identify suitable job opportunities based on skills extracted from their resumes. The platform provides resume analysis, skill matching, job search, and job recommendations.

## Key Features

- **Resume Upload:** Upload resumes in PDF or TXT format.
- **Skill Extraction:** Identify technical skills from uploaded resumes.
- **Job Listings:** Retrieve job information from a PostgreSQL database.
- **Job Matching:** Compare resume skills with job requirements.
- **Skill Gap Analysis:** Display matched and missing skills.
- **Job Recommendations:** Recommend relevant job opportunities.
- **Job Search:** Search jobs using keywords and location.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, JavaScript, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Data Processing | Pandas |
| Resume Processing | PyPDF |
| Environment Management | Python Virtual Environment, python-dotenv |

## Project Workflow

1. User uploads a resume.
2. Backend extracts resume text.
3. Relevant skills are identified.
4. Job records are retrieved from PostgreSQL.
5. Resume skills are compared with job requirements.
6. Matched skills and missing skills are calculated.
7. Relevant job recommendations are returned to the frontend.

## Project Structure

```text
ai-job-intelligence-platform/
│
├── backend/
│   ├── main.py
│   ├── job_matcher.py
│   ├── job_fetcher.py
│   ├── load_jobs.py
│   ├── skill_extractor.py
│   ├── resume_processor.py
│   └── data/
│       └── jobs.csv
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
├── resume/
├── .env
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Durga-1235/ai-job-intelligence-platform.git
cd ai-job-intelligence-platform
```

### 2. Backend Setup

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\Activate.ps1
```

Install the required Python packages:

```bash
pip install "fastapi[standard]" pandas psycopg2-binary python-dotenv pypdf
```

### 3. Environment Variables

Create a `.env` file in the project root and configure your local PostgreSQL connection:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_intelligence
DB_USER=postgres
DB_PASSWORD=your_local_database_password
```

**Security:** Never upload your `.env` file or database credentials to GitHub.

### 4. Run the Backend

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

API Documentation: `http://127.0.0.1:8000/docs`

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, usually `http://localhost:5173`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check backend status |
| POST | `/upload-resume` | Upload and analyze a resume |
| GET | `/jobs` | Retrieve available jobs |
| GET | `/search-jobs` | Search jobs by keyword and location |
| GET | `/recommendations` | Retrieve job recommendations |

## Testing

The backend APIs can be tested using the FastAPI Swagger documentation:

`http://127.0.0.1:8000/docs`

Test resume uploads, job listings, job search, and recommendations.

## Future Enhancements

- Advanced NLP-based resume analysis.
- Improved machine learning recommendation models.
- Live job data integration.
- Personalized career development suggestions.
- Cloud deployment.

## Author

**Durga T**

B.Tech – Artificial Intelligence and Data Science

GitHub: https://github.com/Durga-1235
