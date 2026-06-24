from fuzzywuzzy import fuzz


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
    job_text = normalize_text(job_text)

    job_words = set(job_text.split())

    missing = []

    for skill in job_words:
        if len(skill) > 3:
            if skill not in resume_text and not fuzzy_match(skill, resume_text):
                missing.append(skill)

    return list(set(missing))[:10]


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

    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    common = resume_words & job_words
    keyword_score = (len(common) / (len(job_words) + 1)) * 50

    length = len(resume_words)
    length_score = 20 if length > 100 else 10 if length > 50 else 5

    action_words = ["built", "developed", "designed", "implemented"]
    action_score = sum(3 for w in action_words if w in resume_words)
    action_score = min(action_score, 15)

    format_score = 15 if len(resume_words) > 30 else 5

    return round(keyword_score + length_score + action_score + format_score, 2)


# ✅ Role-Based
def role_based_missing_skills(resume_text, role):

    role_skills = {

        "SDE": [
            "c++", "java", "python",
            "dsa", "data structures", "algorithms",
            "os", "dbms", "system design"
        ],

        "ML": [
            "python", "machine learning",
            "pandas", "numpy", "tensorflow"
        ],

        "Backend": [
            "node", "api", "database",
            "mongodb", "jwt", "microservices"
        ],

        "Frontend": [
            "html", "css", "javascript",
            "react", "ui", "redux"
        ]
    }
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
            if key in skill:
                suggestions.append(course_map[key])

    return list(set(suggestions))

    resume_text = resume_text.lower()
    expected = role_skills.get(role, [])

    missing = [skill for skill in expected if skill not in resume_text]

    return missing