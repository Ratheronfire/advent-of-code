def clamp(num: int | float, min_num: int | float, max_num: int | float) -> int | float:
    return max(min_num, min(num, max_num))