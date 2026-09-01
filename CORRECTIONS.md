# Project Corrections Applied

The project was reviewed and the following issues were corrected:

1. Removed the broken root-level `Dockerfile` because it referenced `requirements.txt` and `app/` that do not exist at the repository root.
2. Removed the duplicate broken root-level GitHub Actions workflow, which also expected root-level application files that do not exist.
3. Kept the phase-based architecture consistent: each phase builds from its own directory.
4. Added a `.dockerignore` file to Phase 1.
5. Fixed the Phase 3 CI/CD workflow so pull requests can lint, test, build, and scan without trying to access Docker Hub or AWS secrets. Registry login and image pushes now run only on `push` events.
6. Updated the main README to clarify the corrected repository structure and workflow behavior.

## Important
Run Docker commands from the appropriate phase directory:

```bash
cd phase1-beginner
# or
cd phase2-intermediate
# or
cd phase3-advanced
```
