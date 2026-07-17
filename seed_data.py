from logger import log_failure
from datetime import datetime, timedelta
import random

# Realistic failure scenarios that actually happen in production
failures = [
    {
        "repo": "Niranjana20055/querymind-production-rag-pipeline",
        "workflow": "Build and Deploy",
        "branch": "main",
        "commit_sha": "a3f8b21",
        "failure_category": "missing_dependency",
        "root_cause": "The workflow failed because 'chromadb==0.6.3' requires 'onnxruntime>=1.14.1' but the runner environment had 'onnxruntime==1.12.0' installed. This version conflict caused an ImportError during the embedding model initialization step.",
        "suggested_fix": "Pin onnxruntime>=1.14.1 in your requirements.txt and clear the pip cache in the workflow by adding 'pip cache purge' before installation. Alternatively, upgrade to chromadb==0.6.5 which has relaxed dependency constraints.",
        "confidence": "high",
        "pr_comment_posted": "Yes",
    },
    {
        "repo": "Niranjana20055/cicd-failure-analyzer",
        "workflow": "CI Test Suite",
        "branch": "feature/webhook-validation",
        "commit_sha": "c9d2e45",
        "failure_category": "failing_test",
        "root_cause": "Three unit tests in test_analyzer.py failed because the mock Groq API response was returning a different JSON schema than expected. The tests were written assuming the 'failure_category' key but the mock was returning 'category' instead — a naming mismatch introduced in the last refactor.",
        "suggested_fix": "Update the mock response in test_analyzer.py line 47 to use 'failure_category' instead of 'category'. Run pytest -v tests/test_analyzer.py locally to verify all 3 tests pass before pushing again.",
        "confidence": "high",
        "pr_comment_posted": "Yes",
    },
    {
        "repo": "Niranjana20055/querymind-production-rag-pipeline",
        "workflow": "Lint and Type Check",
        "branch": "feature/cohere-reranking",
        "commit_sha": "f1a7c33",
        "failure_category": "syntax_error",
        "root_cause": "The flake8 linter flagged an f-string in chain.py line 89 that contained an unterminated expression. The closing brace was missing from a nested dictionary comprehension inside the f-string, causing a SyntaxError that prevented the module from loading.",
        "suggested_fix": "Open chain.py and fix line 89 — add the missing closing brace '}' to complete the f-string expression. Run 'python -m py_compile chain.py' locally to verify the syntax is valid before pushing.",
        "confidence": "high",
        "pr_comment_posted": "No",
    },
    {
        "repo": "Niranjana20055/cicd-failure-analyzer",
        "workflow": "Build and Deploy",
        "branch": "main",
        "commit_sha": "b8e4d12",
        "failure_category": "environment_variable",
        "root_cause": "The deployment step failed because the GROQ_API_KEY secret was not configured in the GitHub repository's Actions secrets. The workflow attempted to call the Groq API during the integration test phase but received a 401 Unauthorized response, causing the test to fail with an AuthenticationError.",
        "suggested_fix": "Go to your repository Settings → Secrets and variables → Actions → New repository secret. Add GROQ_API_KEY with your actual Groq API key. The workflow will automatically pick it up on the next run.",
        "confidence": "high",
        "pr_comment_posted": "Yes",
    },
    {
        "repo": "Niranjana20055/cicd-test-repo",
        "workflow": "Test CI Failure",
        "branch": "main",
        "commit_sha": "5ca7532",
        "failure_category": "missing_dependency",
        "root_cause": "pip attempted to install 'this-package-does-not-exist-xyz-123' which does not exist on the Python Package Index (PyPI). This caused pip to exit with code 1, failing the workflow step immediately. The package name appears to be a placeholder that was never replaced with the actual dependency.",
        "suggested_fix": "Replace 'this-package-does-not-exist-xyz-123' in your workflow file with the correct package name. If this was intentional for testing purposes, remove the step entirely or replace it with a valid package like 'requests' to verify the workflow runs successfully.",
        "confidence": "high",
        "pr_comment_posted": "Yes",
    },
    {
        "repo": "Niranjana20055/querymind-production-rag-pipeline",
        "workflow": "Security Scan",
        "branch": "feature/evaluation-dashboard",
        "commit_sha": "d4b9f67",
        "failure_category": "timeout",
        "root_cause": "The Bandit security scanner timed out after 360 seconds while scanning the venv directory which was accidentally included in the scan path. Scanning node_modules or venv directories causes timeouts because they contain thousands of files that are not part of the project codebase.",
        "suggested_fix": "Add '--exclude venv,node_modules,.git' to your bandit command in the workflow file. Example: 'bandit -r . --exclude venv,node_modules -f json'. This reduces scan time from 6+ minutes to under 30 seconds.",
        "confidence": "medium",
        "pr_comment_posted": "No",
    },
    {
        "repo": "Niranjana20055/cicd-failure-analyzer",
        "workflow": "Docker Build",
        "branch": "feature/containerization",
        "commit_sha": "e2c5a89",
        "failure_category": "docker_error",
        "root_cause": "The Docker build failed at step 7/12 because the base image 'python:3.11-slim' could not pull the 'uvicorn[standard]' package. The build environment had no outbound internet access configured, causing pip to fail with a ConnectionError when attempting to reach pypi.org.",
        "suggested_fix": "Either configure the Docker build to use a pre-built base image with dependencies already installed, or ensure the GitHub Actions runner has outbound internet access. For offline builds, use 'pip download' to create a local package cache and reference it with '--find-links ./packages'.",
        "confidence": "medium",
        "pr_comment_posted": "Yes",
    },
    {
        "repo": "Niranjana20055/cicd-test-repo",
        "workflow": "Test CI Failure",
        "branch": "test-pr-branch",
        "commit_sha": "7f3e291",
        "failure_category": "missing_dependency",
        "root_cause": "Same root cause as previous run — pip attempted to install a non-existent package 'this-package-does-not-exist-xyz-123'. This is the second consecutive failure on this workflow indicating the fix has not been applied yet.",
        "suggested_fix": "The issue persists from the previous failure. Replace the invalid package name immediately. Consider adding a pre-flight check step that validates all package names exist on PyPI before attempting installation.",
        "confidence": "high",
        "pr_comment_posted": "Yes",
    },
    {
        "repo": "Niranjana20055/querymind-production-rag-pipeline",
        "workflow": "Build and Deploy",
        "branch": "hotfix/memory-leak",
        "commit_sha": "9a1b4c6",
        "failure_category": "failing_test",
        "root_cause": "The integration test 'test_rag_pipeline_returns_grounded_answer' failed because the ChromaDB in-memory collection was not being reset between test runs. Residual vectors from a previous test were contaminating the retrieval results, causing the faithfulness assertion to fail with a score of 0.61 against a threshold of 0.80.",
        "suggested_fix": "Add a teardown fixture in conftest.py that calls 'collection.delete(where={})' after each test. Alternatively, use a unique collection name per test run using 'uuid.uuid4()' to ensure test isolation.",
        "confidence": "high",
        "pr_comment_posted": "Yes",
    },
    {
        "repo": "Niranjana20055/cicd-failure-analyzer",
        "workflow": "CI Test Suite",
        "branch": "main",
        "commit_sha": "2d8f103",
        "failure_category": "flaky_test",
        "root_cause": "The test 'test_webhook_signature_verification' failed intermittently due to a race condition in the async test setup. The test was asserting the webhook response before the FastAPI application had fully initialized, causing occasional timing-dependent failures that pass on retry.",
        "suggested_fix": "Add 'await asyncio.sleep(0.1)' after the test client initialization and before the assertion. Better long-term fix: use pytest-asyncio's 'async_generator' fixture pattern to ensure the app is fully ready before tests execute.",
        "confidence": "medium",
        "pr_comment_posted": "No",
    },
    {
        "repo": "Niranjana20055/querymind-production-rag-pipeline",
        "workflow": "Dependency Audit",
        "branch": "main",
        "commit_sha": "6c3d872",
        "failure_category": "infrastructure",
        "root_cause": "The GitHub Actions runner failed to start due to a temporary infrastructure outage on GitHub's end. The job was queued for 18 minutes before timing out. This is not related to the codebase — GitHub's status page confirmed degraded performance on Actions runners in the us-east region during this time window.",
        "suggested_fix": "Re-run the failed jobs — this is a transient infrastructure issue on GitHub's side. To prevent future false alerts from infrastructure failures, add retry logic to your workflow using 'continue-on-error: true' for non-critical steps.",
        "confidence": "low",
        "pr_comment_posted": "No",
    },
    {
        "repo": "Niranjana20055/cicd-failure-analyzer",
        "workflow": "Build and Deploy",
        "branch": "feature/slack-integration",
        "commit_sha": "4e7a519",
        "failure_category": "environment_variable",
        "root_cause": "The Slack notification step failed because SLACK_BOT_TOKEN was not added to the repository secrets. The slack-sdk client raised a SlackApiError with 'invalid_auth' when attempting to post to the engineering-alerts channel, causing the deployment pipeline to abort.",
        "suggested_fix": "Add SLACK_BOT_TOKEN to your repository's Actions secrets. Get the token from api.slack.com/apps → your app → OAuth & Permissions → Bot User OAuth Token. The token should start with 'xoxb-'.",
        "confidence": "high",
        "pr_comment_posted": "Yes",
    },
]

# Spread failures across the last 14 days with realistic timing
base_time = datetime.now() - timedelta(days=14)
time_increments = [
    0, 6, 18, 31, 45, 58, 72, 89,
    103, 118, 134, 149, 163, 178
]

print("Seeding database with realistic failure data...")
for i, failure in enumerate(failures):
    hours_offset = time_increments[i] if i < len(time_increments) else i * 10
    failure["timestamp"] = base_time + timedelta(hours=hours_offset)
    log_failure(failure)
    print(f"✅ Added failure {i+1}/{len(failures)}: {failure['failure_category']} in {failure['repo']}")

print(f"\n🎉 Done! Added {len(failures)} realistic failures to database.")
print("Refresh your dashboard to see the data.")