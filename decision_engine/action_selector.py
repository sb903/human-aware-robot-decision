def select_action(risk):
    if risk < 0.4:
        return "PROCEED"
    elif risk < 0.7:
        return "SLOW_DOWN"
    else:
        return "STOP"
