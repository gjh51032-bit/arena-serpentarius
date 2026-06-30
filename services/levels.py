def calculate_level(points: int) -> int:
    level = 1
    threshold = 20

    while points >= threshold:
        level += 1
        threshold += level * 20

    return level
