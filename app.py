from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_resume():

    # Check if file uploaded
    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    # Check filename
    if file.filename == '':
        return "No selected file"

    # Save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    file.save(filepath)

    # Read PDF
    reader = PdfReader(filepath)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    # Get Job Description
    job_description = request.form.get('job_description', '')

    # Skills List
    skills = [
        "Python",
        "Java",
        "Flask",
        "Django",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "SQL",
        "Machine Learning",
        "Git",
        "GitHub",
        "API",
        "Bootstrap"
    ]

    # Extract Skills
    extracted_skills = []

    skill_scores = {
    "Python": 90,
    "Java": 80,
    "Flask": 75,
    "Django": 70,
    "HTML": 95,
    "CSS": 90,
    "JavaScript": 88,
    "React": 85,
    "Git": 80,
    "GitHub": 82,
    "API": 78,
    "Bootstrap": 75
}

    for skill in skills:
        if skill.lower() in resume_text.lower():
            extracted_skills.append(skill)

    # ATS Score
    total_skills = len(skills)

    found_skills = len(extracted_skills)

    ats_score = int((found_skills / total_skills) * 100)

    # Missing Skills
    missing_skills = []

    for skill in skills:
        if skill not in extracted_skills:
            missing_skills.append(skill)

    # Job Description Matching
    job_keywords = []

    job_words = job_description.lower().split()

    for word in job_words:

        clean_word = word.strip(",.!?()[]{}")

        if len(clean_word) > 3:

            if clean_word not in job_keywords:
                job_keywords.append(clean_word)

    matched_keywords = []

    for keyword in job_keywords:

        if keyword in resume_text.lower():
            matched_keywords.append(keyword)

    # Match Score
    if len(job_keywords) > 0:

        match_score = int(
            (len(matched_keywords) / len(job_keywords)) * 100
        )

    else:
        match_score = 0

    # Recommended Jobs
    recommended_jobs = []

    if "React" in extracted_skills or "JavaScript" in extracted_skills:
        recommended_jobs.append("Frontend Developer")

    if "Python" in extracted_skills or "Flask" in extracted_skills:
        recommended_jobs.append("Python Developer")

    if "Flask" in extracted_skills and "React" in extracted_skills:
        recommended_jobs.append("Full Stack Developer")

    if "Django" in extracted_skills:
        recommended_jobs.append("Backend Developer")

    if "Machine Learning" in extracted_skills:
        recommended_jobs.append("ML Engineer")

    # AI Suggestions
    suggestions = []

    if "SQL" not in extracted_skills:
        suggestions.append("Learn SQL for database-related roles.")

    if "Machine Learning" not in extracted_skills:
        suggestions.append("Add Machine Learning projects.")

    if "GitHub" not in extracted_skills:
        suggestions.append("Include GitHub projects.")

    if ats_score < 70:
        suggestions.append("Improve your resume with more technical skills.")

    if "React" in extracted_skills and "Flask" in extracted_skills:
        suggestions.append("You are suitable for Full Stack Development roles.")

    return render_template(
        'result.html',
        ats_score=ats_score,
        extracted_skills=extracted_skills,
        missing_skills=missing_skills,
        recommended_jobs=recommended_jobs,
        suggestions=suggestions,
        resume_text=resume_text,
        match_score=match_score,
        matched_keywords=matched_keywords,
        skill_scores=skill_scores
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)