FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project


FROM python:3.13-slim

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy the project into the image
ADD ./app /app/app

# Copy the vectorstore containing MTG rules into the image
ADD ./data/MagicCompRules_2020250207.vectorstore /app/data/MagicCompRules_2020250207.vectorstore

# Run the application
CMD ["/app/.venv/bin/chainlit", "run", "/app/app/entrypoint.py", "-h", "--host", "0.0.0.0", "--port", "80"]
