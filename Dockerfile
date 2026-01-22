# 1. Specify the base image (lightweight version of Python 3.12)
FROM python:3.12-slim

# 2. Install uv (copy binary from the official image in GHCR (GitHub Container Registry))
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. Set the working directory
WORKDIR /app

# 4. Copy dependency files
COPY pyproject.toml uv.lock ./

# 5. Install dependencies
# --frozen: Strictly adhere to the lock file
# --no-dev: Do not install development dependencies (for production)
RUN uv sync --frozen --no-dev

# 6. Copy the source code to the image
COPY src ./src

# 7. Set environment variables (add .venv to PATH for easier command access)
ENV PATH="/app/.venv/bin:$PATH"

# 8. Execution command (listening on host 0.0.0.0, all interfaces, is a Docker best practice)
CMD ["uv", "run", "uvicorn", "src.todo_app:app", "--host", "0.0.0.0", "--port", "8000"]