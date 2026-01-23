# API QA / SDET Playground (Python, pytest, uv)

This repository is a learning + portfolio project to practice backend/API test automation with **pytest**.

## Targets
- Public APIs (httpbin, DummyJSON) for fundamentals
- Local FastAPI service (Simple Todo App)

## Requirements
- Windows (or macOS/Linux)
- Docker (Recommended)

### For Local Development
- Python 3.12
- [uv](https://github.com/astral-sh/uv) installed

## Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:uemurm/Backend-Pytest.git
   cd Backend-Pytest
   ```

2. **Install dependencies (Local Dev Only)**
   This project uses `uv` for dependency management.
   ```bash
   uv sync
   ```
   This command will create a virtual environment (`.venv/`) and install all required packages defined in `pyproject.toml`.

## Workflow

You can run the application and tests either using **Docker Compose** (recommended) or **Locally**.

### Option 1: Using Docker Compose (Recommended)

This runs the API server and tests in isolated containers.

**1. Run the API Server**
```bash
docker compose up --build
```
To stop the service, press `Ctrl+C` or run:
```bash
docker compose down
```

---

The API will be available at `http://127.0.0.1:8000`.
Interactive docs: `http://127.0.0.1:8000/docs`

**2. Run Tests**
To run tests in a containerised environment and stop the app automatically after tests finish:
```bash
docker compose up --build --abort-on-container-exit
```

### Option 2: Local Execution

**1. Start the API Server**
```bash
uv run uvicorn src.todo_app:app --reload
```

**2. Run Tests**
```bash
uv run pytest --verbose
```

## Project Structure
- `src/`: Source code (API clients, utilities, local server)
- `tests/`: Test files
- `pyproject.toml`: Project configuration and dependencies
- `Dockerfile`: Container definition for the application
- `compose.yaml`: Docker Compose configuration
