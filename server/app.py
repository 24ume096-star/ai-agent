import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.env import SupportEnv
from app.models import Action

app = FastAPI(
    title="OpenEnv AI Customer Support",
    description="AI customer support simulation environment with 3 difficulty levels (easy, medium, hard).",
    version="0.1.0"
)

# Single global environment instance
_env = SupportEnv()

# ── Request / Response models ──────────────────────────────────────────────────

class ResetRequest(BaseModel):
    task: str = "easy"  # easy | medium | hard

class StepRequest(BaseModel):
    action_type: str   # classify | search | reply | escalate
    content: str

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def read_root():
    return {"status": "ok", "message": "Support Env Server Live"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

from typing import Optional

@app.post("/reset", tags=["Environment"])
def reset(req: Optional[ResetRequest] = None):
    """Reset the environment and start a new task (easy / medium / hard)."""
    task_name = req.task if req and req.task else "easy"
    valid = ["easy", "medium", "hard"]
    if task_name not in valid:
        raise HTTPException(status_code=400, detail=f"task must be one of {valid}")
    obs = _env.reset(task_name)
    return {
        "task": task_name,
        "observation": obs.model_dump()
    }

@app.post("/step", tags=["Environment"])
def step(req: StepRequest):
    """Submit an agent action and receive the next observation + reward."""
    valid_actions = ["classify", "search", "reply", "escalate"]
    if req.action_type not in valid_actions:
        raise HTTPException(status_code=400, detail=f"action_type must be one of {valid_actions}")
    if _env.state_data is None:
        raise HTTPException(status_code=400, detail="Environment not initialised — call /reset first")

    result = _env.step(Action(action_type=req.action_type, content=req.content))
    return {
        "observation": result["observation"].model_dump(),
        "reward": result["reward"],
        "done": result["done"],
        "info": result["info"]
    }

@app.get("/state", tags=["Environment"])
def state():
    """Return the current raw environment state."""
    if _env.state_data is None:
        raise HTTPException(status_code=400, detail="Environment not initialised — call /reset first")
    return _env.state()

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=True)

if __name__ == "__main__":
    main()
