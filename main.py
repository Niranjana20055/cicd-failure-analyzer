from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import hmac
import hashlib
import json
import os
from analyzer import analyze_failure
from github_client import post_pr_comment, get_workflow_log
from logger import log_failure
from datetime import datetime

load_dotenv()

app = FastAPI(
    title="CI/CD Failure Analyzer",
    description="AI-powered GitHub Actions failure diagnosis agent",
    version="1.0.0"
)

def verify_signature(payload: bytes, signature: str) -> bool:
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    expected = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.get("/")
def health_check():
    return {
        "status": "operational",
        "service": "CI/CD Failure Analyzer",
        "powered_by": "Llama 3.3 70B via Groq"
    }

@app.post("/webhook/github")
async def github_webhook(request: Request):
    payload_bytes = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    if not verify_signature(payload_bytes, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    event_type = request.headers.get("X-GitHub-Event", "")
    payload = json.loads(payload_bytes)

    if event_type != "workflow_run":
        return {"status": "ignored", "reason": f"Event {event_type} not handled"}

    workflow_run = payload.get("workflow_run", {})
    if workflow_run.get("conclusion") != "failure":
        return {"status": "ignored", "reason": "Workflow did not fail"}

    repo_name = payload.get("repository", {}).get("full_name", "")
    workflow_name = workflow_run.get("name", "unknown")
    branch = workflow_run.get("head_branch", "unknown")
    commit_sha = workflow_run.get("head_sha", "")[:7]
    run_id = workflow_run.get("id")

    pr_number = None
    pull_requests = workflow_run.get("pull_requests", [])
    if pull_requests:
        pr_number = pull_requests[0].get("number")

    log_text = get_workflow_log(repo_name, run_id)
    diagnosis = analyze_failure(log_text, workflow_name, repo_name)

    comment_posted = "No"
    if pr_number:
        try:
            post_pr_comment(repo_name, pr_number, diagnosis, workflow_name)
            comment_posted = "Yes"
        except Exception as e:
            comment_posted = f"Failed: {str(e)}"

    log_failure({
        "repo": repo_name,
        "workflow": workflow_name,
        "branch": branch,
        "commit_sha": commit_sha,
        "failure_category": diagnosis.get("failure_category", "other"),
        "root_cause": diagnosis.get("root_cause", ""),
        "suggested_fix": diagnosis.get("suggested_fix", ""),
        "confidence": diagnosis.get("confidence", "low"),
        "pr_comment_posted": comment_posted,
        "timestamp": datetime.now()
    })

    return {
        "status": "analyzed",
        "repo": repo_name,
        "workflow": workflow_name,
        "failure_category": diagnosis.get("failure_category"),
        "pr_comment_posted": comment_posted
    }