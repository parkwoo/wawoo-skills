---
name: deployment
description: Plan, execute, and verify a deployment or release (Docker Compose, image tagging, environment, migrations, health checks, rollback). Use when preparing or running a deploy/release, or debugging deployment.
---

# Deployment

## Prerequisites

- Secrets live only in `.env`. **Never commit them.**
- Confirm the target environment, backups, and **rollback procedure** first.

## Steps

1. **Pre-checks**: `git status` (only intended changes), `docker compose config` (environment), backup.
2. **Build**: `docker compose build`. Tag the image with an **immutable tag** (for rollback).
3. **Migrations** (if any): back up → forward → prepare a revert path.
4. **Start**: `docker compose up -d`.
5. **Health**: `curl -s http://127.0.0.1:8080/health`, etc.
6. **Smoke**: key endpoints (auth, non-stream/SSE, etc.).
7. **Load check** (optional): smoke with representative concurrency.
8. **Rollback**: revert to the previous image tag; for the DB, follow the restore procedure.
9. **Evidence**: record the commands run, results, and unverified items.

## Prohibited

- Never leave secrets or keys in logs or documents.
- No production changes or destructive DB operations without approval.
