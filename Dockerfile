FROM python:3.10

WORKDIR /app

ENV HF_HOME=/app/.cache/huggingface
ENV HF_TOKEN=""

COPY . .

# pip installs directly to /usr/local/bin — always on $PATH
RUN pip install --no-cache-dir uvicorn fastapi pydantic openai huggingface-hub

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
