# app/agents/security_review_agent.py

from app.tasks.security_review_task import security_review_task

class SecurityReviewAgent:
    def run(self, architecture_text: str):
        """
        Runs the security review task and returns result
        """
        return security_review_task(architecture_text)
