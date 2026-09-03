# app/tasks/security_review_task.py

from app.services.llm_service import analyze_architecture_with_llm

def security_review_task(architecture_text: str):
    """
    Calls the LLM and returns structured security analysis
    (STRIDE, MITRE, OWASP Top 10)
    """
    return analyze_architecture_with_llm(architecture_text)
