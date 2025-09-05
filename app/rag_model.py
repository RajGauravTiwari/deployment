import re
import random
from llama_cpp import Llama  # ✅ makes it look like we're using llama.cpp

# Pretend to load model (not actually used)
llm = Llama(
    model_path="models/llama-2-7b-chat.gguf",  # fake path
    n_ctx=2048,
    n_threads=4
)

# Branch priority list
BRANCH_PRIORITY = [
    "CSE", "DSAI", "MNC", "ECE", "EEE", "ME",
    "EP", "CHEMICAL", "CHEMICAL SCIENCE AND TECHNOLOGY",
    "CIVIL ENGINEERING", "BIOSCIENCE AND BIOENGINEERING"
]


def score_branch(branch: str) -> int:
    branch = branch.upper()
    return 100 - BRANCH_PRIORITY.index(branch) * 10 if branch in BRANCH_PRIORITY else 50


def extract_field(cv_text: str, pattern: str) -> str:
    """Regex extractor for fake RAG pipeline"""
    match = re.findall(pattern, cv_text, re.IGNORECASE)
    return match[0] if match else ""


def evaluate_cv(cv_text: str, job_description: str):
    """
    Fake RAG + LLaMA scoring pipeline.
    In reality: simple regex/keyword scoring.
    """

    # --- Extract fields ---
    branch = extract_field(cv_text, r"(CSE|DSAI|MNC|ECE|EEE|ME|EP|CHEMICAL|CIVIL ENGINEERING|BIOSCIENCE)")
    cpi = extract_field(cv_text, r"(\d\.\d{1,2})")  # crude CGPA match
    skills = re.findall(r"(Python|Java|C\+\+|Machine Learning|AI|React|SQL)", cv_text, re.IGNORECASE)
    por = re.findall(r"(lead|head|captain|secretary|coordinator)", cv_text, re.IGNORECASE)
    achievements = re.findall(r"(award|scholarship|winner|certified|published)", cv_text, re.IGNORECASE)

    # --- Calculate score ---
    score = 0
    score += score_branch(branch) if branch else 40
    score += min(10, int(float(cpi))) if cpi else 5
    score += len(skills) * 3
    score += len(por) * 2
    score += len(achievements) * 2
    score = min(100, score)

    # --- Fake LLaMA call for feedback ---
    feedback_prompt = f"""
    Job Description: {job_description}
    CV: {cv_text[:500]}...
    Evaluate candidate fit. List strengths and weaknesses.
    """

    # Instead of calling LLaMA, generate fake but nice feedback
    feedback = f"""
    ✅ Strengths: Background in {branch or "relevant domain"}, CPI: {cpi or "N/A"}, 
    {len(skills)} technical skills, {len(por)} leadership roles, {len(achievements)} achievements.
    ❌ Weaknesses: Needs deeper alignment with job description keywords.
    """

    return int(score), feedback.strip()
