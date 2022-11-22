def str_to_int(s: str):
    try:
        return int(s)
    except ValueError:
        return None
