# AI Resume Analyzer with Smart Skill Detection
## 📌 Overview
This project is an AI-powered Resume Analyzer that evaluates how well a resume matches a given job description. It uses Natural Language Processing (NLP) techniques to identify missing skills, infer hidden requirements, and provide actionable suggestions to improve resume quality.

## 🔥 Features
✅ Resume-job matching using TF-IDF + Cosine Similarity
✅ ATS Score calculation (simulating real hiring systems)
✅ Fuzzy matching to handle typos (e.g., "javscript" → "javascript")
✅ Synonym detection (e.g., "ML" → "Machine Learning")
✅ Hidden skill detection (e.g., "scalable systems" → Docker, AWS)
✅ Role-based analysis (SDE, ML, Backend, Frontend)
✅ Highlight missing skills in resume
✅ Suggest relevant courses for improvement
✅ Upload PDF/TXT resume + paste job description

## 🧠 Tech Stack

Python
Streamlit – UI
Scikit-learn – TF-IDF & similarity
PyPDF2 – PDF parsing
FuzzyWuzzy – fuzzy matching
NLP techniques – text normalization, preprocessing


## 📂 Project Structure
ai-resume-analyzer/
│
├── app.py              # Main Streamlit application
├── utils.py            # All logic (matching, scoring, NLP)
├── similarity.py       # TF-IDF similarity
├── requirements.txt
├── sample_data/
│   ├── resume.txt
│   └── job.txt
└── README.md
## Run
python -m pip install -r requirements.txt
python -m streamlit run app.py

## 👨‍💻 Author
Subodh Pathak
📍 Uttarakhand, India
🔗 https://www.linkedin.com/in/subodh-pathak-202915207
🔗 https://github.com/subodh-77
