# SBSB Demo App

This repository represents a customer's small, locally developed web application.

It intentionally starts without a `Dockerfile` or a GitHub Actions workflow. SBSB will analyze the repository, propose those files in a pull request, and verify that the merged workflow publishes a versioned image to GHCR.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000> and check <http://127.0.0.1:8000/health>.

