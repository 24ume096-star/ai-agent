---
title: OpenEnv Support Environment
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# OpenEnv AI Customer Support Environment

A production-ready, OpenEnv-compliant AI customer support simulation environment built for hackathon evaluation.

## Overview

This environment simulates a realistic customer support scenario where AI agents must resolve support tickets across three difficulty levels:

| Level | Description |
|-------|-------------|
| 🟢 **Easy** | Simple FAQs, single-turn resolution |
| 🟡 **Medium** | Multi-turn conversations, policy lookups |
| 🔴 **Hard** | Complex edge cases, escalation handling |

## Environment Details

- **Framework**: [OpenEnv](https://github.com/openenv/openenv)
- **Entrypoint**: `app.env:SupportEnv`
- **Max Steps**: 5
- **Scoring**: 0.0 – 1.0 (programmatic grading)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/reset` | Reset the environment with a task level |
| `POST` | `/step` | Submit an agent action |
| `GET`  | `/state` | Get current environment state |

## Running the Inference Script

```bash
# Install dependencies
pip install -r requirements.txt

# Run baseline agent
python inference.py --task easy
```

## Configuration Reference

See the [Hugging Face Spaces config reference](https://huggingface.co/docs/hub/spaces-config-reference) for more details.
