FROM python:3.10

WORKDIR /app

# OpenEnv frameworks require UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Hugging Face configuration
ENV HF_HOME=/app/.cache/huggingface
ENV HF_TOKEN=""

# Copy project from subfolder into the container root
COPY openenv-support-env/ .

RUN uv sync

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
