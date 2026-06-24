import streamlit as st
from similarity import calculate_similarity
from utils import (
    smart_missing_skills,   
    highlight_missing_words,
    suggest_courses,
    expand_hidden_skills,
    calculate_ats_score,
    role_based_missing_skills
)
import PyPDF2

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("🚀 AI Resume Analyzer")
st.write("Upload Resume & Job Description with Smart Analysis")

# ✅ ROLE SELECTION (UPDATED + Frontend added)
role = st.selectbox("🎯 Select Job Role", ["SDE", "ML", "Backend", "Frontend"])

# ✅ FUNCTIONS TO READ FILES
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "
    return text

def read_txt(file):
    return file.read().decode("utf-8")

# ✅ RESUME UPLOAD
resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "txt"])

# ✅ JOB DESCRIPTION INPUT
st.subheader("💼 Job Description Input")

job_option = st.radio("Choose input method:", ["Upload File", "Paste Text"])

job_text = ""

if job_option == "Upload File":
    job_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"])
    
    if job_file:
        if job_file.type == "application/pdf":
            job_text = read_pdf(job_file)
        else:
            job_text = read_txt(job_file)

else:
    job_text = st.text_area(
        "Paste Job Description Here",
        height=200,
        placeholder="Paste Amazon/Google job description here..."
    )

# ✅ ANALYZE BUTTON
if st.button("Analyze Resume"):

    if resume_file and job_text:

        # ✅ READ RESUME
        resume_text = read_pdf(resume_file) if resume_file.type == "application/pdf" else read_txt(resume_file)

        # ✅ HIDDEN SKILLS
        hidden_skills = expand_hidden_skills(job_text)

        # ✅ MERGE TEXT
        enhanced_job_text = job_text + " " + hidden_skills

        # ✅ SCORES
        score = calculate_similarity(resume_text, enhanced_job_text)

        # ✅ 🔥 SMART MATCHING (Fuzzy + Synonym)
        missing = smart_missing_skills(resume_text, enhanced_job_text)

        ats_score = calculate_ats_score(resume_text, enhanced_job_text)

        # ✅ ROLE-BASED
        role_missing = role_based_missing_skills(resume_text, role)

        # ✅ EXTRA FEATURES
        highlighted_resume = highlight_missing_words(resume_text, missing)
        courses = suggest_courses(missing)

        # ✅ OUTPUT
        st.subheader("✅ Match Results")

        col1, col2 = st.columns(2)
        col1.metric("Match Score", f"{score}%")
        col2.metric("ATS Score", f"{ats_score}/100")

        # ✅ FIXED CONDITION (IMPORTANT)
        if score > 75:
            st.success("Strong match!")
        elif score > 50:
            st.warning("Moderate match")
        else:
            st.error("Low match!")

        # ✅ HIDDEN SKILLS
        st.subheader("🧠 Hidden (Inferred) Skills")
        hidden_list = list(set(hidden_skills.split()))
        if hidden_list:
            for skill in hidden_list:
                st.write("•", skill)
        else:
            st.write("No hidden skills detected")

        # ✅ ROLE-BASED
        st.subheader(f"🎯 Missing Skills for {role} Role")
        if role_missing:
            for skill in role_missing:
                st.write("•", skill)
        else:
            st.write("No major skills missing ✅")

        # ✅ HIGHLIGHTED RESUME
        st.subheader("📝 Resume with Missing Skills Highlighted")
        st.markdown(highlighted_resume, unsafe_allow_html=True)

        # ✅ SMART MISSING
        st.subheader("❌ Missing Skills (Smart Matching)")
        for skill in missing:
            st.write("•", skill)

        # ✅ COURSE SUGGESTIONS
        st.subheader("🎓 Recommended Courses")
        if courses:
            for course in courses:
                st.write("•", course)
        else:
            st.write("No suggestions needed ✅")

    else:
        st.warning("⚠️ Upload resume and provide job description!")