FROM python:3.10

WORKDIR /app

# Hugging Face configuration
ENV HF_HOME=/app/.cache/huggingface
ENV HF_TOKEN=""

# Copy project from subfolder into the container root
COPY openenv-support-env/ .

# Install dependencies with pip directly into system Python (guaranteed on $PATH)
RUN pip install --no-cache-dir uvicorn fastapi pydantic openai huggingface-hub

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
