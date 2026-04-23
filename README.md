# SATU Dental — Senior Data Engineer Coding Challenge

**Candidate:** Abel Gideon Silaen
**Position:** Senior Data Engineer
**Time:** ~90 minutes total (SQL 15m + Python 20m + AI challenge 30m + buffer)

Welcome! This repo contains the take-home portion of your interview. It has three problems — SATU Dental's Engineering Manager will tell you whether to do **Problem 1 + Problem 2** OR **Problem 1 + the AI-Assisted Challenge** during the live session. You do not need to do all three on your own time.

## Context: SATU Dental

SATU Dental is a dental clinic SaaS. Backend in Go (chi, GORM), frontend in Next.js. We're currently bootstrapping a data warehouse project. Our domain includes:
- Patient appointments and treatments
- Clinic operations and chair utilization
- Payments and invoicing
- EDC/ECR bank integrations (BCA, BRI, Mandiri) for card settlement
- Insurance claims

## Structure

```
.
├── README.md                  <- you are here
├── problem-1-sql/             <- Problem 1: SQL patient retention analysis
├── problem-2-python/          <- Problem 2: Appointment data cleanup + daily summary (pandas)
└── ai-challenge/              <- Alternative: AI-assisted reconciliation pipeline
```

## How to Work

1. **Read the problem README.**
2. **Inspect the skeleton and seed data.**
3. **Write your solution in the provided placeholder files.**
4. **Run the tests** (commands provided in each problem README).
5. **Commit as you go** — we want to see your thinking.

## What We're Looking For

- Correctness first, then clarity, then performance.
- Clean, idiomatic code. No code golf.
- Tests passing.
- Clear commit history / comments where you made non-obvious tradeoffs.
- For the AI-assisted challenge: honesty about what the AI wrote vs. what you wrote.

Good luck!
