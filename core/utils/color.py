def get_color(score: float) -> str | None:
    if score == 0.0:
        return "FFFFFF"
    elif 0.1 <= score < 4.0:
        return "39B549"
    elif 4.0 <= score < 7.0:
        return "FCEE21"
    elif 7.0 <= score < 9.0:
        return "F7941F"
    elif 9.0 <= score <= 10.0:
        return "C0282E"
    else:
        return None
