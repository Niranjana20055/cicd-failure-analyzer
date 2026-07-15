# 🛠️ CI/CD Failure Analyzer

**An autonomous AI agent that diagnoses GitHub Actions failures, identifies root causes, and posts fixes as PR comments — so developers don't have to dig through CI logs manually.**

![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![LLM](https://img.shields.io/badge/LLM-Llama%203.3%2070B-purple)

## 🚀 Overview

When a CI/CD pipeline fails, the usual next step is a developer manually scrolling through hundreds of lines of build logs to figure out what broke. **CI/CD Failure Analyzer** automates that entirely: it listens for failed GitHub Actions runs, reads the full log, uses an LLM to reason about the root cause, and posts a clear diagnosis with a suggested fix directly as a comment on the pull request.

## ✨ What It Does

- **Receives GitHub Actions failures via webhook** — the agent is triggered automatically the moment a workflow run fails, no manual polling
- **Reads the full log automatically** — pulls and parses the complete failure log through the GitHub API
- **Diagnoses the root cause using an LLM** — Llama 3.3 70B reasons over the log content to identify *why* the pipeline failed (dependency conflict, test failure, misconfiguration, etc.), not just where
- **Posts the diagnosis as a PR comment** — the fix and explanation land directly where the developer is already working, no context-switching
- **Dashboard of failures and patterns** — a Streamlit interface surfaces past failures and recurring root-cause patterns across runs, so teams can spot systemic issues, not just one-off bugs

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| LLM / Reasoning | Llama 3.3 70B |
| Backend / API | FastAPI |
| Dashboard | Streamlit |
| CI Source | GitHub Actions API + Webhooks |

## 🔍 How It Works

1. A GitHub Actions workflow fails → a webhook event fires to the FastAPI backend
2. The backend fetches the failed job's full log via the GitHub API
3. The log is parsed and passed to Llama 3.3 70B with a diagnostic prompt
4. The model identifies the root cause and generates a fix recommendation
5. The agent posts the diagnosis as a comment on the associated PR
6. The Streamlit dashboard shows the full history of failures, diagnoses, and recurring patterns across the repo

## 🏗️ Setup

```bash
git clone https://github.com/Niranjana20055/cicd-failure-analyzer.git
cd cicd-failure-analyzer
pip install -r requirements.txt

# backend
uvicorn main:app --reload

# dashboard
streamlit run app.py
```

**Deployment:** Backend and dashboard are configured for deployment on Railway.
