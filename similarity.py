important_skills = {
    "java", "python", "c++",
    "dsa", "algorithms",
    "data", "structures",
    "oop", "dbms", "os",
    "sql", "database",
    "computer", "networks",
    "git", "github",
    "aws", "docker",
    "system", "design",
    "api", "mongodb",
    "react", "javascript",
    "html", "css",
    "node", "microservices"
}
def calculate_similarity(resume_text, job_text):

    resume_words = set(resume_text.lower().split())

    job_words = {
        word for word in job_text.lower().split()
        if word in important_skills
    }

    common = resume_words & job_words

    score = (len(common) / max(len(job_words), 1)) * 100

    return round(score, 2)