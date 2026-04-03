from pydantic import BaseModel
from typing import List, Literal, Optional


class Observation(BaseModel):
    ticket_id: str
    customer_message: str
    conversation_history: List[str]
    available_actions: List[str]
    kb_snippets: List[str]


class Action(BaseModel):
    action_type: Literal[
        "classify",
        "search",
        "reply",
        "escalate"
    ]
    content: str


class Reward(BaseModel):
    score: float
    reason: str