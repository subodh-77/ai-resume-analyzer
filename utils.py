from fuzzywuzzy import fuzz
import streamlit as st
from google import genai

import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+# ]', ' ', text)
    return text

# ✅ Synonyms
skill_synonyms = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "js": "javascript",
    "nodejs": "node",
    "db": "database",
    "oop": "object oriented programming",
    "ds": "data structures"
}
VALID_SKILLS = {
    "python", "java", "c++",
    "javascript", "react", "node",
    "html", "css",
    "sql", "mongodb", "mysql",
    "database", "dbms",
    "docker", "kubernetes",
    "aws", "azure", "gcp",
    "git", "github",
    "api", "apis",
    "microservices",
    "ci/cd",
    "system design",
    "caching",
    "load balancing",
    "machine learning",
    "tensorflow",
    "numpy",
    "pandas",
    "data structures",
    "algorithms",
    "os",
    "computer networks",
    "jwt",
    "redis"
}


# ✅ Normalize text
def normalize_text(text):
    text = text.lower()
    for short, full in skill_synonyms.items():
        text = text.replace(short, full)
    return text


# ✅ Improved Fuzzy Matching (phrase-level)
def fuzzy_match(skill, text, threshold=80):
    return fuzz.partial_ratio(skill, text) >= threshold


# ✅ SMART Missing Skills
def smart_missing_skills(resume_text, job_text):

    resume_text = normalize_text(resume_text)
    job_text = job_text.lower()

    missing = []

    for skill in VALID_SKILLS:

        if skill in job_text:

            if skill not in resume_text:
                missing.append(skill)

    return missing


# ✅ Highlight Missing
def highlight_missing_words(resume_text, missing_words):
    words = resume_text.split()
    highlighted = ""

    for word in words:
        clean = word.lower().strip(".,()")

        if clean in missing_words:
            highlighted += f"<span style='color:red; font-weight:bold'>{word}</span> "
        else:
            highlighted += word + " "

    return highlighted


# ✅ Hidden Skills
def expand_hidden_skills(job_text):

    skill_map = {
        "scalable": ["docker", "kubernetes", "microservices"],
        "cloud": ["aws", "azure", "gcp"],
        "backend": ["node", "database", "api"],
        "devops": ["docker", "ci/cd"],
        "system design": ["load balancing", "caching"]
    }

    job_text = job_text.lower()
    extra = []

    for key in skill_map:
        if key in job_text:
            extra.extend(skill_map[key])

    return " ".join(extra)


# ✅ ATS Score
def calculate_ats_score(resume_text, job_text):
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    resume_words = set(resume_text.lower().split())
    
    stop_words = {
        "the", "and", "for", "with", "a", "an", "of",
        "to", "in", "on", "is", "are", "required",
        "preferred", "responsibilities"
    }

    important_skills = {
    "java","python","c++",
    "dsa","algorithms","data","structures",
    "oop","object","oriented",
    "os","operating","systems",
    "dbms","sql","database",
    "computer","networks",
    "git","github",
    "aws","docker",
    "system","design",
    "api","apis",
    "ci/cd",
    "full","stack"
}

    job_words = {
    word for word in job_text.lower().split()
    if word in important_skills
}

    common = resume_words & job_words

    # 60 Marks
    keyword_score = (len(common)/(max(len(job_words),1)))*70

    # 20 Marks
    length_score = 20 if len(resume_words) > 100 else 10

    # 10 Marks
    action_words = [
        "built",
        "developed",
        "designed",
        "implemented",
        "created",
        "optimized",
        "engineered"
    ]

    action_score = min(
        sum(2 for w in action_words if w in resume_words),
        10
    )

    # 10 Marks
    format_score = 10 if len(resume_words) > 30 else 5

    ats_score = keyword_score + length_score + action_score + format_score
    print("Resume words:", len(resume_words))
    print("Job words:", len(job_words))
    print("Common words:", len(common))
    print("Matched:", common)

    return min(round(ats_score, 2), 100)
# ✅ Role-Based
def role_based_missing_skills(resume_text, role):

    resume_text = normalize_text(resume_text)

    role_skills = {

        "SDE": [
            "java",
            "python",
            "c++",
            "data structures",
            "algorithms",
            "object oriented programming",
            "operating systems",
            "dbms",
            "computer networks",
            "system design"
        ],

        "ML": [
            "python",
            "machine learning",
            "pandas",
            "numpy",
            "tensorflow"
        ],

        "Backend": [
            "node",
            "api",
            "database",
            "mongodb",
            "jwt",
            "microservices",
            "docker"
        ],

        "Frontend": [
            "html",
            "css",
            "javascript",
            "react",
            "redux"
        ]
    }

    expected = role_skills.get(role, [])

    missing = []

    for skill in expected:
        if not fuzzy_match(skill, resume_text):
            missing.append(skill)

    return missing
    # ✅ Course Suggestions
def suggest_courses(missing_skills):

    course_map = {
        "docker": "Docker for Beginners - Udemy",
        "aws": "AWS Fundamentals - Coursera",
        "kubernetes": "Kubernetes Basics - Udemy",
        "system": "System Design - Educative",
        "react": "React Complete Guide",
        "node": "Node.js Backend Development",
        "machine": "Machine Learning - Andrew Ng",
        "python": "Python Course - Coursera"
    }

    suggestions = []

    for skill in missing_skills:
        for key in course_map:
            if key in skill.lower():
                suggestions.append(course_map[key])

    return list(set(suggestions))


# ==========================
# GEMINI CONFIGURATION
# ==========================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# ==========================
# LLM ANALYSIS
# ==========================

def analyze_resume_with_llm(resume_text, job_text):

    try:

        prompt = f"""
        Analyze this resume against the job description.

        Return:
        1. Overall feedback
        2. Strengths
        3. Weaknesses
        4. Missing skills
        5. Improvement suggestions

        Resume:
        {resume_text}

        Job Description:
        {job_text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"

# ==========================
# RESUME SUMMARY
# ==========================

def generate_resume_summary(resume_text):

    try:

        prompt = f"""
        Create a professional resume summary
        in 4-5 lines.

        Resume:
        {resume_text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"

# ==========================
# INTERVIEW QUESTIONS
# ==========================

def generate_interview_questions(resume_text):

    try:

        prompt = f"""
        Generate 10 interview questions
        based on this resume.

        Resume:
        {resume_text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


# ==========================
# RESUME IMPROVEMENT
# ==========================

def improve_resume_bullets(resume_text):

    try:

        prompt = f"""
        Rewrite the project descriptions and resume points
        professionally using strong action verbs.

        Resume:
        {resume_text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
   