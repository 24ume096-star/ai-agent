from app.models import Reward, Action


def compute_reward(state, action: Action):
    correct_label = state["label"]

    score = 0.0
    done = False
    reason = ""

    if action.action_type == "classify":
        if correct_label in action.content:
            score += 0.3
            reason = "Correct classification"
        else:
            score -= 0.2
            reason = "Wrong classification"

    elif action.action_type == "search":
        score += 0.2
        reason = "Used knowledge base"

    elif action.action_type == "reply":
        if correct_label in action.content:
            score += 0.5
            done = True
            reason = "Good reply"
        else:
            score -= 0.3
            reason = "Bad reply"

    elif action.action_type == "escalate":
        score += 0.1
        done = True
        reason = "Escalated"

    return Reward(score=score, reason=reason), done