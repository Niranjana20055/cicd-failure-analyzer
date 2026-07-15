from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

load_dotenv()

def analyze_failure(log_text: str, workflow_name: str, repo: str) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""You are a senior DevOps engineer and CI/CD expert.
Analyze this GitHub Actions workflow failure log and provide a diagnosis.

Repository: {repo}
Workflow: {workflow_name}

FAILURE LOG:
{log_text[-8000:]}

Respond ONLY with a valid JSON object in this exact format:
{{
  "failure_category": "one of: missing_dependency | failing_test | syntax_error | environment_variable | flaky_test | docker_error | permission_error | timeout | infrastructure | other",
  "root_cause": "2-3 sentence precise technical explanation of what caused the failure",
  "suggested_fix": "specific actionable fix the developer should apply",
  "confidence": "high | medium | low",
  "severity": "critical | high | medium | low"
}}

Return ONLY the JSON. No explanation. No markdown. No backticks."""

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content.strip())
        return result
    except json.JSONDecodeError:
        return {
            "failure_category": "other",
            "root_cause": response.content,
            "suggested_fix": "Please review the logs manually",
            "confidence": "low",
            "severity": "medium"
        }