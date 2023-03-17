import copy

def is_hex(s: str) -> bool:
    s_copy = copy.copy(s)
    s_copy = s_copy.lower()
    for ch in s:
        if ch < "0" or ch > "9" and ch < "a" or ch > "f":
            return False
    return True