# API QA / SDET Playground (Python, pytest, uv)

This repository is a learning + portfolio project to practice backend/API test automation with **pytest**.

## Targets
- Public APIs (httpbin, DummyJSON) for fundamentals
- Local FastAPI service (Simple Todo App)

## Requirements
- Windows (or macOS/Linux)
- [uv](https://github.com/astral-sh/uv) installed
- Python 3.12
- Docker (optional, for containerised execution)

## Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:uemurm/Backend-Pytest.git
   cd Backend-Pytest
   ```

2. **Install dependencies**
   This project uses `uv` for dependency management.
   ```bash
   uv sync
   ```
   This command will create a virtual environment (`.venv`) and install all required packages defined in `pyproject.toml`.

## Running the Application

You can run the FastAPI server either locally or using Docker.

### Option A: Local Execution

Start the server using `uv`:
```bash
uv run uvicorn src.todo_app:app --reload
```

### Option B: Docker Execution

1. **Build the image**:
   ```bash
   docker build --tag todo-app .
   ```

2. **Run the container**:
   ```bash
   docker run --publish 8000:8000 todo-app
   ```

---

The API will be available at `http://127.0.0.1:8000`.
Interactive docs: `http://127.0.0.1:8000/docs`

## Running Tests

Run all tests with pytest:
```bash
uv run pytest
```
Or activate the virtual environment first:
```bash
# Windows (PowerShell)
.venv\Scripts\activate

# Run tests
pytest
```

## Project Structure
- `src/`: Source code (API clients, utilities, local server)
- `tests/`: Test files
- `pyproject.toml`: Project configuration and dependencies
- `Dockerfile`: Container definition for the application
