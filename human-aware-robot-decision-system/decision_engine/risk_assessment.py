def calculate_risk(distance, motion, env):
    risk = 0.2

    if distance < 1:
        risk += 0.4
    elif distance < 2:
        risk += 0.2

    if motion == "running":
        risk += 0.3
    elif motion == "walking":
        risk += 0.1

    if env == "corridor":
        risk += 0.1

    return min(risk, 1.0)
