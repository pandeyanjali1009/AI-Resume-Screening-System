
const form = document.getElementById("screenForm");
const resumeInput = document.getElementById("resumeFiles");
const fileNames = document.getElementById("fileNames");
const message = document.getElementById("message");
const button = document.getElementById("submitButton");
const resultsSection = document.getElementById("resultsSection");
const resultsBody = document.getElementById("resultsBody");

resumeInput.addEventListener("change", () => {
    const files = Array.from(resumeInput.files);

    fileNames.textContent = files.length
        ? files.map(file => file.name).join(", ")
        : "No files selected";
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const description = document.getElementById("jobDescription").value.trim();
    const files = Array.from(resumeInput.files);

    message.textContent = "";
    message.className = "message";
    resultsSection.hidden = true;
    resultsBody.innerHTML = "";

    if (!description) {
        showMessage("Please enter a job description.", true);
        return;
    }

    if (files.length === 0) {
        showMessage("Please upload at least one resume.", true);
        return;
    }

    const allowedExtensions = [".pdf", ".docx", ".txt"];
    const invalidFile = files.find(file =>
        !allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
    );

    if (invalidFile) {
        showMessage("Only PDF, DOCX and TXT files are supported.", true);
        return;
    }

    const formData = new FormData();
    formData.append("job_description", description);

    files.forEach(file => {
        formData.append("files", file);
    });

    button.disabled = true;
    button.textContent = "Screening resumes...";
    showMessage("Please wait while resumes are being processed.", false);

    try {
        const response = await fetch("/screen-resumes", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to process resumes.");
        }

        const results = Array.isArray(data) ? data : data.results;

        if (!Array.isArray(results)) {
            throw new Error("Unexpected response from the screening API.");
        }

        results.forEach(candidate => {
            const row = document.createElement("tr");

            const rank = document.createElement("td");
            rank.textContent = candidate.rank;

            const filename = document.createElement("td");
            filename.textContent = candidate.filename;

            const score = document.createElement("td");
            score.className = "score";
            const numericScore = Number(candidate.similarity_score);
            score.textContent = Number.isFinite(numericScore)
                ? `${numericScore.toFixed(2)}%`
                : candidate.similarity_score;

            row.append(rank, filename, score);
            resultsBody.appendChild(row);
        });

        document.getElementById("candidateCount").textContent =
            `${results.length} candidates processed`;

        resultsSection.hidden = false;
        showMessage("Screening completed successfully.", false, true);

    } catch (error) {
        showMessage(error.message, true);
    } finally {
        button.disabled = false;
        button.textContent = "Screen Resumes";
    }
});

function showMessage(text, isError, isSuccess = false) {
    message.textContent = text;
    message.className = isError
        ? "message error"
        : isSuccess
            ? "message success"
            : "message";
}
