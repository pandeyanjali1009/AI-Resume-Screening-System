
# AI Resume Screening System

An NLP-based Resume Screening System that compares candidate resumes with a given Job Description (JD) and ranks candidates based on their text similarity scores.

The project uses TF-IDF and Cosine Similarity to identify how closely a resume's content matches the requirements mentioned in a job description.

It provides a simple web interface where users can enter a job description, upload one or multiple resumes, and view the similarity scores and candidate rankings.

---

## Project Overview

Recruiters may receive multiple resumes for a single job opening. Manually reviewing every resume can take time.

This project demonstrates a basic automated resume screening approach by comparing resume content against job requirements and ranking resumes based on textual similarity.

The system supports both individual resume screening and bulk resume screening.

---

## Features

- Enter a job title and job description.
- Upload one or multiple candidate resumes.
- Supports PDF, DOCX and TXT file formats.
- Extract text from uploaded resumes.
- Compare resumes with the given job description.
- Calculate similarity scores using TF-IDF and Cosine Similarity.
- Rank multiple candidates based on similarity scores.
- Display screening results through a simple web interface.
- Provide a FastAPI endpoint for resume screening.
- Includes automated testing with 50 synthetic resumes.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend API development |
| HTML | Webpage structure |
| CSS | Webpage styling |
| JavaScript | Frontend interaction and API requests |
| Scikit-learn | TF-IDF vectorization and cosine similarity |
| Pandas | Organizing and ranking candidate results |
| PyPDF2 | Extracting text from PDF resumes |
| python-docx | Extracting text from DOCX resumes |
| Uvicorn | Running the FastAPI application |

---

## How the System Works

1. The user enters a job title and job description through the web interface.
2. One or multiple resumes are uploaded.
3. The system extracts text from the uploaded resume files.
4. TF-IDF converts the job description and resume text into numerical vectors.
5. Cosine Similarity calculates the textual similarity between each resume and the job description.
6. The system sorts candidates by their similarity scores in descending order.
7. The results are displayed with candidate rankings and similarity percentages.

---

## Project Structure

```text
AI_Resume_Screening_System/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── resume_parser.py
│   ├── ranker.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       └── script.js
│
├── scripts/
│   └── test_api_50_resumes.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Resume-Screening-System.git
```

### 2. Open the Project Folder

```bash
cd AI-Resume-Screening-System
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Running the Web Application

Start the FastAPI server using:

```bash
uvicorn app.main:app --reload
```

Once the server starts, open the following address in your browser:

**Web Application:**

http://127.0.0.1:8000/

The user can then:

1. Enter a job title.
2. Paste the job description.
3. Upload one or multiple resumes.
4. Click the Screen Resumes button.
5. View candidate rankings and similarity scores.

---

## API Documentation

The project also provides an API endpoint for resume screening.

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs

The API can be used to submit a job description and multiple resume files for processing.

---

## Testing with 50 Synthetic Resumes

The project includes an automated test script:

```bash
python scripts/test_api_50_resumes.py
```

This script generates 50 synthetic candidate resumes and sends them to the FastAPI screening endpoint.

The test validates:

- Successful processing of all 50 resumes.
- Similarity score calculation.
- Candidate ranking in descending order.
- Sequential ranking of the processed candidates.

**Testing Note:** The 50 resumes are synthetic test profiles created for validating the system's functionality. They are not real candidate resumes and the test does not represent a real-world accuracy evaluation.

---

## Limitations

- The system evaluates textual similarity, not a candidate's complete suitability for a job.
- Similarity scores do not represent the probability of selection.
- Scanned PDF resumes without extractable text are not supported.
- Resume quality, context and actual candidate experience require human evaluation.
- The system is intended as a basic screening and comparison tool, not a replacement for recruiter decisions.

---

## Future Improvements

- Add more advanced NLP-based matching techniques.
- Improve resume information extraction.
- Add skill-based comparison and filtering.
- Improve the candidate results interface.
- Support additional resume formats.

---

## Author

Developed as a practical project to explore Natural Language Processing, resume screening, text similarity and API development using Python.

---
