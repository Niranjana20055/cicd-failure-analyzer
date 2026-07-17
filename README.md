<div align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/GitHub-Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white"/>

# ⚡ CI/CD Failure Analyzer — AI-Powered DevOps Intelligence

### Autonomous GitHub Actions failure diagnosis · LLM-powered root cause analysis · Automated PR comments · Real-time observability dashboard

**[📽️ Demo Video](your-video-link-here)** · **[🔍 QueryMind — My Other AI Project](https://niranjana-querymind.streamlit.app/)**

</div>

---

## 🧠 What Is This?

Every SDE has wasted hours staring at a failed CI/CD pipeline trying to find the one line that caused the error.

**CI/CD Failure Analyzer solves this automatically.**

The moment a GitHub Actions workflow fails, this system:
- Receives the failure via webhook in real time
- Fetches and parses the full error log automatically
- Sends it to Llama 3.3 70B for root cause diagnosis
- Posts the diagnosis as a structured comment on the Pull Request
- Logs everything to a live observability dashboard

**Zero manual intervention. Diagnosis in under 10 seconds.**

---

## ✨ Features

- ⚡ **Real-time webhook integration** — receives GitHub Actions failures instantly
- 🧠 **LLM-powered diagnosis** — Llama 3.3 70B analyzes logs and identifies root cause
- 📋 **Automated PR comments** — posts structured diagnosis before the developer even opens their laptop
- 🔍 **6 failure categories** — missing dependency, failing test, syntax error, environment variable, flaky test, timeout, and more
- 📊 **Live observability dashboard** — tracks all failures, confidence scores, and patterns over time
- 🔐 **Webhook signature verification** — HMAC-SHA256 validation ensures only GitHub can trigger the system
- 🗂️ **Persistent failure log** — SQLite database stores every diagnosis with full metadata

---

## 🏗️ Architecture

```
GitHub Actions workflow fails
           │
           ▼
GitHub sends webhook → FastAPI server (HMAC verified)
           │
           ▼
GitHub API fetches full failure log (zip extracted)
           │
           ▼
Llama 3.3 70B via Groq analyzes log
           │
           ▼
Structured diagnosis: category + root cause + fix + confidence
           │
           ├──→ Posts comment on Pull Request automatically
           │
           ├──→ Logs to SQLite database
           │
           └──→ Updates Streamlit observability dashboard
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Llama 3.3 70B via Groq | Root cause diagnosis |
| **Backend** | FastAPI + Uvicorn | Webhook server |
| **GitHub Integration** | PyGithub + Webhooks | Log fetching + PR comments |
| **Database** | SQLite + SQLAlchemy | Failure log persistence |
| **Frontend** | Streamlit + Plotly | Observability dashboard |
| **Security** | HMAC-SHA256 | Webhook signature verification |
| **Orchestration** | LangChain | LLM integration |

---

## 📊 Failure Categories Detected

| Category | Description |
|---|---|
| `missing_dependency` | Package not found on PyPI or npm |
| `failing_test` | Unit or integration test assertion failures |
| `syntax_error` | Code syntax or compilation errors |
| `environment_variable` | Missing or misconfigured secrets/env vars |
| `flaky_test` | Non-deterministic test failures |
| `timeout` | Step exceeded time limit |
| `docker_error` | Container build or runtime failures |
| `permission_error` | Access denied to resources or secrets |
| `infrastructure` | Runner or cloud infrastructure issues |

---

## 📁 Project Structure

```
cicd-analyzer/
├── main.py              # FastAPI webhook server + signature verification
├── analyzer.py          # LLM diagnosis engine (Llama 3.3 70B via Groq)
├── github_client.py     # GitHub log fetcher + PR comment poster
├── logger.py            # SQLite failure log (SQLAlchemy)
├── dashboard.py         # Streamlit observability dashboard
├── requirements.txt     # All dependencies
├── .env.example         # Environment variable template
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Niranjana20055/cicd-failure-analyzer.git
cd cicd-failure-analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Add your API keys to .env
```

### 5. Start the FastAPI server
```bash
uvicorn main:app --reload --port 8000
```

### 6. Start the dashboard (new terminal)
```bash
streamlit run dashboard.py
```

### 7. Expose locally with ngrok (new terminal)
```bash
ngrok http 8000
```

### 8. Add webhook to your GitHub repo
- Go to repo → Settings → Webhooks → Add webhook
- Payload URL: `https://your-ngrok-url.ngrok-free.app/webhook/github`
- Content type: `application/json`
- Secret: your webhook secret
- Events: Workflow runs

---

## 🔑 Environment Variables

```env
GROQ_API_KEY=your_groq_key          # console.groq.com — free
GITHUB_TOKEN=ghp_your_token         # GitHub → Settings → Developer settings
GITHUB_WEBHOOK_SECRET=your_secret   # Any random string — must match webhook config
```

---

## 🔍 Why This Project Stands Out

> Every company with a CI/CD pipeline faces the same problem — engineers waste 20-30 minutes reading failure logs when they could be writing code.

This system addresses three real production engineering problems:

**1. Mean Time To Resolution (MTTR)** — by diagnosing failures in under 10 seconds instead of minutes.

**2. Developer context switching** — engineers don't need to leave their PR to understand what broke.

**3. Failure pattern detection** — the dashboard identifies recurring failure types across branches and workflows, enabling proactive fixes.

This is the kind of internal tooling that platform engineering teams at Google, Microsoft, and Atlassian build and maintain — now as an open-source project.

---

## 📊 Sample PR Comment Output

```
## 📦 CI/CD Failure Analysis — AI Analyzer

Workflow: Build & Test
Severity: 🟠 HIGH
Category: Missing Dependency
Confidence: HIGH

🔍 Root Cause
The workflow failed because pip attempted to install
'pytorch-lightning==1.9.0' which has been deprecated
and removed from PyPI. The package was renamed to
'lightning' in version 2.0.

🛠️ Suggested Fix
Replace 'pytorch-lightning==1.9.0' with 'lightning>=2.0'
in your requirements.txt and update any imports from
'pytorch_lightning' to 'lightning'.

🤖 Automated diagnosis powered by Llama 3.3 70B via Groq
```

---

## 👩‍💻 Author

**Niranjana Vijayaraghavan**
Final Year B.Tech CSE · VIT Vellore

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/niranjana-vijayaraghavan/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/Niranjana20055)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-purple?style=flat)](https://niranjana-vijayaraghavan-portfolio.lovable.app)

---

<div align="center">
Built with FastAPI · LangChain · Groq · PyGithub · Streamlit · SQLite
</div>