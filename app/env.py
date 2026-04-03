import random
from typing import Dict, Any
from app.models import Observation, Action, Reward
from app.tasks import load_task
from app.reward import compute_reward

class SupportEnv:
    def __init__(self):
        self.state_data = None
        self.done = False
        self.step_count = 0

    def reset(self, task_name: str = "easy"):
        self.state_data = load_task(task_name)
        self.state_data["current_kb"] = []
        self.done = False
        self.step_count = 0
        return self._get_observation()

    def step(self, action: Action):
        self.step_count += 1
        reward, done = compute_reward(self.state_data, action)

        if action.action_type == "search":
            self.state_data["current_kb"] = self.state_data.get("kb", [])

        self.state_data["history"].append(
            f"agent ({action.action_type}): {action.content}"
        )
        self.done = done
        return {
            "observation": self._get_observation(),
            "reward": reward.score,
            "done": done,
            "info": {"reason": reward.reason}
        }
        
    def add_customer_message(self, message: str):
        self.state_data["history"].append(f"customer: {message}")
        self.state_data["message"] = message

    def state(self):
        return self.state_data

    def _get_observation(self):
        return Observation(
            ticket_id=self.state_data["ticket_id"],
            customer_message=self.state_data["message"],
            conversation_history=self.state_data["history"],
            available_actions=["classify", "search", "reply", "escalate"],
            kb_snippets=self.state_data.get("current_kb", [])
        )