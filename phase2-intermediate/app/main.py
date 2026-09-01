from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="Docker Mastery Demo API",
    description="A tiny FastAPI service used to demonstrate Docker across three maturity phases.",
    version="1.1.0",
)


@app.get("/")
def root():
    """Root endpoint - simple welcome message."""
    return {
        "message": "Welcome to the Docker Mastery Demo API",
        "phase": "2 - intermediate",
        "status": "running",
    }


@app.get("/health")
def health():
    """Health check endpoint - used by CI smoke tests and container healthchecks."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/info")
def info():
    """Basic metadata about the running service."""
    return {
        "app": "docker-mastery-demo",
        "version": app.version,
        "phase": "2 - intermediate",
    }
