import os
import json
import random


def load_task(level: str):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "data", "tickets.json")
    with open(file_path) as f:
        tickets = json.load(f)

    if level == "easy":
        return random.choice(tickets["easy"])
    elif level == "medium":
        return random.choice(tickets["medium"])
    else:
        return random.choice(tickets["hard"])