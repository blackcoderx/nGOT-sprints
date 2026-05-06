# ── Stage 1: builder ─────────────────────────────────────────────────────────
# Install all dependencies into a virtual environment here.
# We use a separate stage so build tools (gcc, poetry) don't end up in the final image.
FROM python:3.11-slim AS builder

# build-essential provides gcc/g++ needed to compile some Python packages (e.g. numpy)
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Install Poetry — the dependency manager that reads pyproject.toml
# POETRY_HOME controls where the Poetry binary is installed
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH so subsequent RUN commands can use it
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Copy only dependency files first — Docker caches this layer so
# a code change doesn't force a full `poetry install` re-run
COPY pyproject.toml poetry.lock* ./

# virtualenvs.in-project=true tells Poetry to create .venv inside /app
# so Stage 2 can copy it cleanly with COPY --from=builder /app/.venv /app/.venv
RUN poetry config virtualenvs.in-project true \
 && poetry install --only=main --no-root   # --no-root skips installing the project itself (not needed at runtime)

# Now copy the actual source code (changes here don't invalidate the dep layer above)
COPY app/ ./app/


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
# Lean final image — no build tools, no Poetry, just Python + .venv + app code
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create a non-root user — running as root inside a container is a security risk
# If the container is compromised, the attacker only gets appuser privileges
RUN groupadd --gid 1001 appuser \
 && useradd --uid 1001 --gid 1001 --no-create-home appuser

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv
# Copy the application source code
COPY --from=builder /app/app  /app/app

# Create the models directory so the API can find its model file
RUN mkdir -p /app/models && chown -R appuser:appuser /app

# Switch to the non-root user for all subsequent commands
USER appuser

# Tell Python to use the .venv we copied from the builder stage
ENV PATH="/app/.venv/bin:$PATH"

# The port the uvicorn server listens on — documented here, matched in docker-compose
EXPOSE 8000

# HEALTHCHECK tells Docker/Kubernetes to poll this URL to decide if the container is healthy
# --interval=30s  check every 30 seconds
# --timeout=10s   fail the check if it takes longer than 10 seconds
# --retries=3     mark unhealthy after 3 consecutive failures
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start the API server
# --host 0.0.0.0 makes it reachable from outside the container (not just localhost)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
