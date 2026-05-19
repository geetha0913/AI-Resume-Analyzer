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

    # Check file uploaded
    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    # Check filename
    if file.filename == '':
        return "No selected file"

    # Save uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    file.save(filepath)

    # Read PDF
    reader = PdfReader(filepath)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

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

    # Extracted Skills
    extracted_skills = []

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
        suggestions.append("Add Machine Learning projects to strengthen your AI profile.")

    if "GitHub" not in extracted_skills:
        suggestions.append("Include GitHub projects in your resume.")

    if ats_score < 70:
        suggestions.append("Improve your resume by adding more technical skills.")

    if "React" in extracted_skills and "Flask" in extracted_skills:
        suggestions.append("You are suitable for Full Stack Development roles.")

    return render_template(
        'result.html',
        ats_score=ats_score,
        extracted_skills=extracted_skills,
        missing_skills=missing_skills,
        recommended_jobs=recommended_jobs,
        suggestions=suggestions,
        resume_text=resume_text
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)