import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_resumes(job_description: str, resumes: list[dict]) -> list[dict]:
    """Return resumes sorted by textual similarity to the job description."""
    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if not resumes:
        raise ValueError("At least one resume is required.")

    documents = [job_description] + [resume["text"] for resume in resumes]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )

    try:
        matrix = vectorizer.fit_transform(documents)
    except ValueError as error:
        raise ValueError(
            "The job description and resumes do not contain enough usable text."
        ) from error

    scores = cosine_similarity(matrix[0:1], matrix[1:])[0]

    results = pd.DataFrame([
        {
            "filename": resume["filename"],
            "similarity_score": round(float(scores[index]) * 100, 2)
        }
        for index, resume in enumerate(resumes)
    ])

    results = results.sort_values(
        by="similarity_score",
        ascending=False
    ).reset_index(drop=True)

    return [
        {
            "rank": index + 1,
            "filename": row["filename"],
            "similarity_score": row["similarity_score"]
        }
        for index, row in results.iterrows()
    ]
