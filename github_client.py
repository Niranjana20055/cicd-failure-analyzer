from github import Github
from dotenv import load_dotenv
import requests
import zipfile
import io
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
        try:
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            log_text = ""
            for name in zip_file.namelist():
                with zip_file.open(name) as f:
                    content = f.read().decode("utf-8", errors="ignore")
                    log_text += content + "\n"
            return log_text[-8000:] if log_text else "No log content found"
        except Exception:
            return response.text[:8000]

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
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }

    emoji = category_emoji.get(
        diagnosis.get("failure_category", "other"), "🔍"
    )
    sev = severity_color.get(
        diagnosis.get("severity", "medium"), "🟡"
    )

    failure_cat = diagnosis.get("failure_category", "unknown")
    failure_cat_display = failure_cat.replace("_", " ").title()
    severity_display = diagnosis.get("severity", "medium").upper()
    confidence_display = diagnosis.get("confidence", "medium").upper()
    root_cause = diagnosis.get("root_cause", "Unable to determine root cause")
    suggested_fix = diagnosis.get("suggested_fix", "Please review the logs manually")

    comment = (
        f"## {emoji} CI/CD Failure Analysis — AI Analyzer\n\n"
        f"**Workflow:** `{workflow}`\n"
        f"**Severity:** {sev} `{severity_display}`\n"
        f"**Category:** `{failure_cat_display}`\n"
        f"**Confidence:** `{confidence_display}`\n\n"
        f"---\n\n"
        f"### 🔍 Root Cause\n"
        f"{root_cause}\n\n"
        f"---\n\n"
        f"### 🛠️ Suggested Fix\n"
        f"{suggested_fix}\n\n"
        f"---\n\n"
        f"*🤖 Automated diagnosis powered by Llama 3.3 70B via Groq*"
    )

    pr.create_issue_comment(comment)
    return True