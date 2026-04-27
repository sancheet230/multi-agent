# ---------------- IMPORTS ----------------
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph
import os

# ---------------- ENV ----------------
load_dotenv()

# ---------------- LLM SETUP (OpenRouter) ----------------
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ---------------- STATE ----------------
class State(TypedDict):
    job_description: str
    resume: str
    jd_skills: str
    resume_skills: str
    score: str
    suggestions: str
    project_suggestions: str


# ---------------- AGENT 1: JD ANALYZER ----------------
def jd_analyzer(state: State):
    print("\n[JD Analyzer Running...]")

    prompt = f"""
    Extract required skills, tools, and responsibilities from this Job Description:

    {state['job_description']}
    """

    response = llm.invoke(prompt)
    state["jd_skills"] = response.content
    return state


# ---------------- AGENT 2: RESUME ANALYZER ----------------
def resume_analyzer(state: State):
    print("\n[Resume Analyzer Running...]")

    prompt = f"""
    You are an expert ATS (Applicant Tracking System).

    Analyze the following resume and extract:
    - Technical skills
    - Tools/technologies
    - Experience areas

    Resume:
    {state['resume']}
    """

    response = llm.invoke(prompt)
    state["resume_skills"] = response.content
    return state


# ---------------- AGENT 3: SCORING ----------------
def scoring_agent(state: State):
    print("\n[Scoring Agent Running...]")

    prompt = f"""
You are an ATS scoring system.

Return output STRICTLY in this format:

Score: <number>/100

Matching Skills:
- skill1
- skill2

Missing Skills:
- skill1
- skill2

Explanation:
<2-3 lines max>

JD Skills:
{state['jd_skills']}

Resume Skills:
{state['resume_skills']}
"""

    response = llm.invoke(prompt)
    state["score"] = response.content
    return state

# ---------------- AGENT 4: IMPROVEMENT ----------------
def improvement_agent(state: State):
    print("\n[Improvement Agent Running...]")

    prompt = f"""
    Based on the gap between JD and Resume:

    JD Skills:
    {state['jd_skills']}

    Resume Skills:
    {state['resume_skills']}

    Suggest:
    - Skills to add
    - Projects to include
    - Resume improvements
    - Keywords for ATS optimization
    """

    response = llm.invoke(prompt)
    state["suggestions"] = response.content
    return state


# ---------------- AGENT 5: PROJECT SUGGESTION ----------------
def project_suggestion_agent(state: State):
    print("\n[Project Suggestion Agent Running...]")

    prompt = f"""
Suggest 2 strong, resume-ready projects based on missing skills.

Each project MUST include:
- Title
- Tech Stack
- 3 Key Features
- Why it helps for this job

Job Description:
{state['job_description']}

esume Skills:
{state['resume_skills']}
"""

    response = llm.invoke(prompt)
    state["project_suggestions"] = response.content
    return state


# ---------------- LANGGRAPH WORKFLOW ----------------
builder = StateGraph(State)

builder.add_node("jd_analyzer", jd_analyzer)
builder.add_node("resume_analyzer", resume_analyzer)
builder.add_node("scoring", scoring_agent)
builder.add_node("improvement", improvement_agent)
builder.add_node("project_suggestion", project_suggestion_agent)

builder.set_entry_point("jd_analyzer")

builder.add_edge("jd_analyzer", "resume_analyzer")
builder.add_edge("resume_analyzer", "scoring")
builder.add_edge("scoring", "improvement")
builder.add_edge("improvement", "project_suggestion")

graph = builder.compile()


# ---------------- FUNCTION FOR FRONTEND ----------------
def run_resume_analysis(jd, resume_text):
    state = {
        "job_description": jd,
        "resume": resume_text,
        "jd_skills": "",
        "resume_skills": "",
        "score": "",
        "suggestions": "",
        "project_suggestions": ""
    }

    result = graph.invoke(state)
    return result


# ---------------- MAIN FUNCTION (CLI) ----------------
def main():
    print("=== Resume Analyzer ===")

    jd = input("\nEnter Job Description:\n")
    resume = input("\nEnter Resume:\n")

    state = {
        "job_description": jd,
        "resume": resume,
        "jd_skills": "",
        "resume_skills": "",
        "score": "",
        "suggestions": "",
        "project_suggestions": ""
    }

    result = graph.invoke(state)

    print("\n=== FINAL OUTPUT ===")
    print("\nScore:\n", result["score"])
    print("\nSuggestions:\n", result["suggestions"])
    print("\nProject Suggestions:\n", result["project_suggestions"])


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    main()