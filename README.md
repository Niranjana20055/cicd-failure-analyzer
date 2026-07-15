# 🛠️ CI/CD Failure Analyzer

**An autonomous AI agent that diagnoses GitHub Actions failures, identifies root causes, and posts suggested fixes directly as PR comments.**

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![LLM](https://img.shields.io/badge/LLM-Llama%203.3%2070B-purple)

## 🚀 Overview

CI/CD pipelines fail all the time — flaky tests, dependency mismatches, misconfigured YAML, environment drift — and debugging them usually means a developer manually digging through logs. **CI/CD Failure Analyzer** automates that first pass: it watches for failed GitHub Actions runs, pulls the logs, uses an LLM to reason about the root cause, and posts a clear, actionable explanation (with a suggested fix) as a comment on the relevant pull request.

The goal is to cut the time between "pipeline turned red" and "I know what broke" from minutes of log-spelunking to a single automated comment.

## ✨ Key Features

- **Automatic failure detection** — listens for failed GitHub Actions workflow runs
- **Log ingestion & parsing** — pulls raw CI logs via the GitHub API and extracts the relevant error context
- **LLM-powered root cause analysis** — uses Llama 3.3 70B to reason over stack traces/log output and identify *why* the pipeline failed, not just *that* it failed
- **Automated PR comments** — posts a human-readable diagnosis and suggested fix directly on the pull request
- **FastAPI backend** — handles GitHub webhooks, log retrieval, and orchestrates the analysis pipeline
- **Streamlit dashboard** — lets you inspect past failures, view agent reasoning, and test the analyzer manually

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| LLM / Reasoning | Llama 3.3 70B |
| Backend / API | FastAPI |
| UI / Dashboard | Streamlit |
| CI Source | GitHub Actions API + Webhooks |
| Deployment (planned) | Railway |

## 🔍 How It Works

1. A GitHub Actions workflow fails → a webhook event fires
2. FastAPI backend receives the event and fetches the failed job's logs
3. Logs are cleaned/chunked and passed to Llama 3.3 70B with a diagnostic prompt
4. The model identifies the likely root cause and proposes a fix
5. The agent posts the diagnosis as a comment on the associated PR
6. Everything is also viewable in the Streamlit dashboard for manual review

## 🚧 Project Status

This project is **actively in development**. Core log-parsing and LLM diagnosis logic is functional; GitHub webhook integration and Railway deployment are in progress. Next milestones:

- [ ] Finish webhook → FastAPI event pipeline
- [ ] Deploy backend + dashboard to Railway
- [ ] Add support for multi-job workflow failures
- [ ] Expand root-cause taxonomy (test flakiness vs. dependency vs. infra errors)

## 🏗️ Local Setup

```bash
git clone https://github.com/Niranjana20055/cicd-failure-analyzer.git
cd cicd-failure-analyzer
pip install -r requirements.txt

# backend
uvicorn main:app --reload

# dashboard
streamlit run app.py
```
