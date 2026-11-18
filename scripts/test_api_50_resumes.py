from io import BytesIO

import requests

API_URL = "http://127.0.0.1:8000/screen-resumes"

JOB_DESCRIPTION = """
We are looking for a Data Analyst with knowledge of Python, SQL, Excel,
Power BI, data analysis, data visualization, Pandas, NumPy, statistics,
reporting and data cleaning. The candidate should analyze datasets,
prepare reports, create dashboards and identify business insights.
"""

SKILL_SETS = [
    "Python SQL Excel Power BI Pandas NumPy statistics data analysis",
    "Python SQL Tableau Excel data visualization reporting",
    "Java HTML CSS JavaScript web development",
    "Python machine learning scikit-learn data cleaning SQL",
    "Excel Power BI business intelligence dashboard reporting",
    "Python Pandas NumPy matplotlib seaborn data analysis",
    "SQL database management Excel reporting",
    "Python SQL Power BI data visualization statistics",
    "C++ Java software development algorithms",
    "Python Excel data cleaning data reporting SQL",
]


def generate_resume(candidate_number: int) -> str:
    skills = SKILL_SETS[(candidate_number - 1) % len(SKILL_SETS)]
    return f"""
    RESUME: Candidate {candidate_number}

    PROFESSIONAL SUMMARY:
    Candidate with knowledge of technology, problem solving and projects.

    TECHNICAL SKILLS:
    {skills}

    PROJECT EXPERIENCE:
    Worked on practical projects involving data processing, analysis,
    reporting and technical problem solving.

    EDUCATION:
    Bachelor's Degree in Technology.
    """


def main():
    # Create 50 synthetic text resumes in memory; no personal data is used.
    files = []
    file_objects = []

    for number in range(1, 51):
        file_object = BytesIO(generate_resume(number).encode("utf-8"))
        file_objects.append(file_object)
        files.append(
            ("files", (f"candidate_{number:02d}.txt", file_object, "text/plain"))
        )

    try:
        print("Sending 50 synthetic resumes to the API...")
        response = requests.post(
            API_URL,
            data={"job_description": JOB_DESCRIPTION},
            files=files,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()

        ranked = result["results"]
        scores = [candidate["similarity_score"] for candidate in ranked]
        ranks = [candidate["rank"] for candidate in ranked]

        assert len(ranked) == 50, "Expected 50 ranked resumes."
        assert scores == sorted(scores, reverse=True), "Scores are not descending."
        assert ranks == list(range(1, 51)), "Ranks are not sequential."

        print("\nTOP 10 CANDIDATES")
        print("-" * 65)
        for candidate in ranked[:10]:
            print(
                f"Rank: {candidate['rank']:>2} | "
                f"{candidate['filename']:<20} | "
                f"Similarity: {candidate['similarity_score']:.2f}%"
            )

        print("\nSUCCESS: All 50 resumes were processed and ranking order was validated.")
        print("Note: These are synthetic test resumes, not a real-world accuracy study.")

    except requests.exceptions.ConnectionError:
        print("Could not connect to the API. Start the server first:")
        print("uvicorn app.main:app --reload")
    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
    except (AssertionError, KeyError) as error:
        print(f"Test validation failed: {error}")
    finally:
        for file_object in file_objects:
            file_object.close()


if __name__ == "__main__":
    main()
