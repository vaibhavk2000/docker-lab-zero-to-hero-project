# Phase 2 — Intermediate: Optimized Image + Basic CI

## Goal
Shrink the image using a multi-stage build on a slim, purpose-built Python base image, and introduce a basic automated CI pipeline (lint + test + build) that runs on every push and pull request.

---

## What's Inside
```
phase2-intermediate/
├── app/
│   └── main.py
├── requirements.txt          # runtime dependencies only
├── requirements-dev.txt      # flake8, pytest, httpx — for linting and testing
├── test_main.py              # automated tests for the API
├── Dockerfile                # multi-stage build on python:3.12-slim
├── .dockerignore             # tells Docker what NOT to copy into the image
├── .github/workflows/ci.yml  # CI pipeline: lint → test → build
└── README.md
```

---

## How the Multi-Stage Dockerfile Works

A multi-stage build uses multiple `FROM` statements in one Dockerfile. Each stage is a separate environment — you build and install everything you need in an early stage, then copy only the final output into a clean, minimal final image. Build tools never end up in production.

```
Stage 1 (builder): python:3.12-slim
  → install all dependencies including build tools

Stage 2 (final): python:3.12-slim
  → copy only the installed packages and app code from Stage 1
  → result: no pip, no build tools, no cache — just what the app needs to run
```

> The `.dockerignore` file works like `.gitignore` — it tells Docker to exclude files like `venv/`, `__pycache__/`, and `.git` from the build context. This keeps builds fast and prevents local files from leaking into the image.

---

## What the Tests Do (`test_main.py`)

The tests use `pytest` + `httpx` to spin up the FastAPI app in memory and send real HTTP requests to it — no container needed.

- `TestClient` from FastAPI starts the app in-process
- Each test function calls an endpoint (e.g. `GET /`, `GET /health`) and asserts the expected status code and response body
- If an endpoint breaks or returns wrong data, the test fails and the CI pipeline stops — nothing gets built or pushed

This is a safety net: you know the app works correctly before a Docker image is ever built.

---

## Run Locally
```bash
cd phase2-intermediate
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt

# Lint: checks code style and catches common errors
flake8 app test_main.py --max-line-length=100

# Test: runs all test functions in test_main.py
pytest -v

# Run the app
uvicorn app.main:app --reload
```

---

## Build the Optimized Image
```bash
docker build -t docker-mastery:phase2 .
```

## Run the Container
```bash
docker run -d --name phase2-app -p 8000:8000 docker-mastery:phase2
```

---

## Compare Against Phase 1
```bash
docker images | grep docker-mastery
```
Because the final image is based on `python:3.12-slim` and never contains build-time-only tools, it's much smaller than Phase 1 — typically **~150–180MB vs 400–600MB+**.

You can also time the builds:
```bash
time docker build -t docker-mastery:phase1 ../phase1-beginner
time docker build -t docker-mastery:phase2 .
```

---

## How the CI Pipeline Works (`.github/workflows/ci.yml`)

### What triggers it
```yaml
on:
  push:
    branches: ["main"]
    paths: ["phase2-intermediate/**"]
  pull_request:
    branches: ["main"]
    paths: ["phase2-intermediate/**"]
```
The pipeline runs automatically whenever you push a commit (or open a PR) that touches any file inside `phase2-intermediate/`. Changes to other folders don't trigger it — keeping CI fast and focused.

### What the GitHub runner does
When triggered, GitHub spins up a **fresh virtual machine** (ubuntu-latest) — a clean Linux environment with nothing on it. It then runs your jobs in order:

**Job 1: `lint-and-test`**
1. **Checkout** — clones your repo onto the runner VM
2. **Set up Python 3.12** — installs the exact Python version
3. **Install dependencies** — runs `pip install -r requirements-dev.txt`
4. **Lint with flake8** — checks for style errors and obvious bugs; fails the pipeline if any are found
5. **Run tests with pytest** — executes `test_main.py`; fails the pipeline if any test fails

**Job 2: `build-image`** (only runs if Job 1 passes)
1. **Set up Docker Buildx** — enables advanced Docker build features
2. **Build the image** — runs `docker build` using the Dockerfile; confirms the image builds cleanly but does not push it anywhere (that's Phase 3)

> `needs: lint-and-test` in the workflow means Job 2 only starts if Job 1 succeeds. If lint or tests fail, Docker never runs — fast feedback, no wasted time.

> The runner VM is **thrown away** after every run. Nothing persists between runs. This guarantees a clean, reproducible environment every time.

---

## Core Concepts Demonstrated
- **Multi-stage builds**: separate build environment from the runtime image to keep the final image lean
- **`.dockerignore`**: exclude unnecessary files from the build context
- **`requirements-dev.txt`**: keep dev/test tools out of the production image
- **pytest + httpx**: test the API with real HTTP calls without running a real server
- **CI trigger on push/PR**: automated quality gate — broken code can't slip through unnoticed
- **GitHub runner**: ephemeral VM that checks out your code and runs jobs in a clean environment
- **Job dependencies (`needs`)**: enforce order — lint and test must pass before build runs
