from github import Github
from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_workflow_log(repo_name: str, run_id: int) -> str:
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo_name}/actions/runs/{run_id}/logs"
    response = requests.get(url, headers=headers, allow_redirects=True)
    if response.status_code == 200:
        return response.text[:10000]
    return f"Could not fetch logs. Status: {response.status_code}"

def post_pr_comment(repo_name: str, pr_number: int, diagnosis: dict, workflow: str):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    category_emoji = {
        "missing_dependency": "📦",
        "failing_test": "🧪",
        "syntax_error": "🔴",
        "environment_variable": "🔑",
        "flaky_test": "⚠️",
        "docker_error": "🐳",
        "permission_error": "🔒",
        "timeout": "⏱️",
        "infrastructure": "🏗️",
        "other": "🔍"
    }
    severity_color = {
        "critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"
    }

    emoji = category_emoji.get(diagnosis.get("failure_category", "other"), "🔍")
    sev = severity_color.get(diagnosis.get("severity", "medium"), "🟡")

    comment = f"""## {emoji} CI/CD Failure Analysis — AI Analyzer

**Workflow:** `{workflow}`
**Severity:** {sev} `{diagnosis.get('severity', 'medium').upper()}`
**Category:** `{diagnosis.get('failure_category', 'unknown').replace('_', ' ').title()}`
**Confidence:** `{diagnosis.get('confidence', 'medium').upper()}`

---

### 🔍 Root Cause
{diagnosis.get('root_cause', 'Unable to determine root cause')}

---

### 🛠️ Suggested Fix
{diagnosis.get('suggested_fix', 'Please review the logs manually')}

---

*🤖 Automated diagnosis powered by Llama 3.3 70B via Groq*"""

    pr.create_issue_comment(comment)
    return True