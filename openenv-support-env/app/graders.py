def grade_task(state):
    actions = state["history"]

    score = 0.0

    if any("classify" in a for a in actions):
        score += 0.3

    if any("search" in a for a in actions):
        score += 0.2

    if any("reply" in a for a in actions):
        score += 0.5

    return min(score, 1.0)