
import { useState, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [resumeResult, setResumeResult] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [jobsError, setJobsError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/jobs`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load jobs.");
        }
        return response.json();
      })
      .then((data) => {
        setJobs(data.jobs || []);
      })
      .catch(() => {
        setJobsError(
          "Could not load jobs. Please check whether the backend is running."
        );
      });
  }, []);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    setFile(null);
    setResumeResult(null);
    setError("");

    if (!selectedFile) return;

    const validFile = /\.(pdf|txt)$/i.test(selectedFile.name);

    if (!validFile) {
      setError("Please select a PDF or TXT resume.");
      event.target.value = "";
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("File size must be less than 5 MB.");
      event.target.value = "";
      return;
    }

    setFile(selectedFile);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please choose your resume first.");
      return;
    }

    setLoading(true);
    setError("");
    setResumeResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/upload-resume`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || "Resume analysis failed.");
      }

      setResumeResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong. Please check the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatSkills = (skills) => {
    if (!skills || skills.length === 0) return "None";
    return skills.join(", ");
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-badge">CAREER DISCOVERY PLATFORM</div>

        <h1>AI Job Intelligence Platform</h1>

        <p>
          Discover opportunities that match your skills.
          Upload your resume and explore relevant jobs.
        </p>

        <button
          className="explore-button"
          onClick={() =>
            document
              .getElementById("available-jobs")
              ?.scrollIntoView({ behavior: "smooth" })
          }
        >
          Explore Jobs ↓
        </button>
      </header>

      <main className="container">
        <section className="section-card">
          <div className="section-heading">
            <span className="section-number">01</span>
            <div>
              <h2>Resume Analysis</h2>
              <p>
                Upload your resume to find matching opportunities.
              </p>
            </div>
          </div>

          <div className="upload-box">
            <div className="upload-icon">↑</div>
            <h3>Upload your resume</h3>
            <p>Choose a PDF or TXT resume file.</p>

            <input
              type="file"
              accept=".pdf,.txt,application/pdf,text/plain"
              onChange={handleFileChange}
              aria-label="Choose resume file"
            />

            {file && (
              <p className="selected-file">
                Selected: {file.name}
              </p>
            )}

            <button
              className="primary-button"
              onClick={handleAnalyze}
              disabled={!file || loading}
            >
              {loading ? "Analysing..." : "Analyse Resume"}
            </button>

            {error && (
              <p className="error-message" role="alert">
                {error}
              </p>
            )}
          </div>
        </section>

        {resumeResult && (
          <>
            <section className="section-card">
              <div className="section-heading">
                <span className="section-number">02</span>
                <div>
                  <h2>Extracted Skills</h2>
                  <p>
                    Skills identified from {resumeResult.filename}.
                  </p>
                </div>
              </div>

              {resumeResult.extracted_skills?.length > 0 ? (
                <div className="skill-list">
                  {resumeResult.extracted_skills.map((skill) => (
                    <span className="skill-tag" key={skill}>
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p>
                  No supported skills found. Check whether the PDF
                  contains selectable text and supported skill names.
                </p>
              )}
            </section>

            <section className="recommendations-section">
              <div className="section-heading">
                <span className="section-number">03</span>
                <div>
                  <h2>Recommended for You</h2>
                  <p>
                    Jobs ranked using the current resume-matching logic.
                  </p>
                </div>
              </div>

              {resumeResult.recommendations?.length > 0 ? (
                <div className="job-grid">
                  {resumeResult.recommendations.map((job) => (
                    <article className="job-card" key={job.job_id}>
                      <div className="job-card-top">
                        <span className="job-avatar">
                          {job.job_title?.charAt(0) || "J"}
                        </span>
                        <span className="match-badge">
                          {Number(job.score).toFixed(2)}% Match
                        </span>
                      </div>

                      <h3>{job.job_title}</h3>

                      <hr />

                      <h4>Matched skills</h4>
                      <p>{formatSkills(job.matched_skills)}</p>

                      <h4>Skills to learn</h4>
                      <p>{formatSkills(job.missing_skills)}</p>
                    </article>
                  ))}
                </div>
              ) : (
                <p>No matching jobs were found in the database.</p>
              )}
            </section>
          </>
        )}

        <section id="available-jobs" className="section-card">
          <div className="section-heading">
            <span className="section-number">04</span>
            <div>
              <h2>Available Jobs</h2>
              <p>Explore jobs currently stored in your database.</p>
            </div>
          </div>

          {jobsError && (
            <p className="error-message">{jobsError}</p>
          )}

          {!jobsError && jobs.length === 0 && (
            <p>No jobs available in the database yet.</p>
          )}

          <div className="job-grid">
            {jobs.map((job) => (
              <article className="job-card" key={job.job_id}>
                <div className="job-card-top">
                  <span className="job-avatar">
                    {job.job_title?.charAt(0) || "J"}
                  </span>
                </div>

                <h3>{job.job_title}</h3>

                <p className="job-location">
                  {job.location || "Location not specified"}
                </p>

                <h4>Required skills</h4>
                <p>{job.skills || "Not specified"}</p>

                {job.salary && (
                  <p>
                    <strong>Salary:</strong> {job.salary}
                  </p>
                )}

                {job.description && (
                  <details>
                    <summary>View job description</summary>
                    <p className="description-text">
                      {job.description}
                    </p>
                  </details>
                )}
              </article>
            ))}
          </div>
        </section>
      </main>

      <footer className="footer">
        AI Job Intelligence Platform · Resume-based job matching
      </footer>
    </div>
  );
}

export default App;
