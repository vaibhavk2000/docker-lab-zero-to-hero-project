# Phase 1 — Beginner: Basic Dockerized FastAPI App

## Goal
Understand the fundamentals of Docker: images, containers, Dockerfile instructions, and the basic CLI workflow — using a plain Ubuntu base image with everything installed manually.

---

## What's Inside
```
phase1-beginner/
├── app/
│   └── main.py        # FastAPI app with 3 routes: /, /health, /info
├── requirements.txt   # FastAPI + uvicorn dependencies
├── Dockerfile         # single-stage build on ubuntu:22.04
└── README.md
```

---

## How the Dockerfile Works

The Dockerfile starts from `ubuntu:22.04` — a full general-purpose Linux OS — and manually installs Python, pip, and the app dependencies on top of it.

Key instructions and what they do:
- `FROM ubuntu:22.04` — sets the base layer; every subsequent instruction builds on top of this
- `ENV DEBIAN_FRONTEND=noninteractive` — prevents apt from prompting for input during the build
- `RUN apt-get install python3 python3-pip ...` — installs Python into the image (adds a new layer)
- `WORKDIR /app` — sets the working directory inside the container for all following commands
- `COPY requirements.txt .` then `RUN pip3 install` — copies dependency file first so Docker can cache this layer separately from your app code
- `COPY app/ app/` — copies your application code into the image
- `EXPOSE 8000` — documents that the container listens on port 8000 (doesn't actually publish it)
- `CMD [...]` — the default command that runs when the container starts (starts uvicorn)

> Each `RUN`, `COPY`, `WORKDIR` instruction creates a new **layer**. Docker caches layers — if nothing changed in a layer, Docker reuses the cached version on the next build. This is why dependency installation is split from code copying.

---

## Run Locally Without Docker (optional sanity check)
```bash
cd phase1-beginner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Visit http://localhost:8000/docs

---

## Build the Docker Image
```bash
docker build -t docker-mastery:phase1 .
```
- `docker build` reads the Dockerfile and executes each instruction in order
- `-t docker-mastery:phase1` gives the resulting image a name and tag
- `.` tells Docker to use the current directory as the **build context** (the files it can access)

---

## Run the Container
```bash
docker run -d --name phase1-app -p 8000:8000 docker-mastery:phase1
```
- `docker run` creates and starts a container from the image
- `-d` runs it in detached mode (background)
- `--name phase1-app` gives the container a name so you can refer to it by name
- `-p 8000:8000` maps port 8000 on your machine to port 8000 inside the container — without this, the container is unreachable from your browser

Visit http://localhost:8000 and http://localhost:8000/docs

---

## Everyday Docker CLI Commands
```bash
docker ps                         # list running containers
docker ps -a                      # list all containers (including stopped ones)
docker logs phase1-app            # view container output/logs
docker logs -f phase1-app         # follow logs live (like tail -f)
docker exec -it phase1-app bash   # open a shell inside the running container
docker stop phase1-app            # gracefully stop the container
docker rm phase1-app              # delete the stopped container
docker rmi docker-mastery:phase1  # delete the image from your machine
```

> `docker exec -it` is useful for debugging — you can inspect files, check environment variables, and run commands as if you were inside the container.

---

## Inspect Image Size (the problem this phase sets up)
```bash
docker images docker-mastery:phase1
```
Because it's built on a full `ubuntu:22.04` OS plus manually-installed Python, expect the image to be **400–600MB+**. This is the problem Phase 2 solves.

---

## Core Concepts Demonstrated
- **Image vs container**: an image is a blueprint (read-only), a container is a running instance of it
- **Dockerfile instructions**: `FROM`, `ENV`, `RUN`, `WORKDIR`, `COPY`, `EXPOSE`, `CMD`
- **Layers and caching**: each instruction adds a layer; unchanged layers are reused on rebuild
- **Port mapping** (`-p host:container`): bridges your machine's network to the container's network
- **Why a generic OS base is heavy**: you pay the cost of the full OS even though you only need Python

---

## What's Next
Phase 2 replaces the Ubuntu base with a slim, purpose-built Python image, switches to a multi-stage build to keep the final image lean, and adds an automated CI pipeline.
