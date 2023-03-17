def set_lp_weight(token_reserve: list, total_lp: float) -> float:
    # total_lp is lp_points[token]
    return token_reserve / total_lp


# works for RSWP LP & RSWP LP staked value
def get_lp_values(lp_weight: float, lp_points: list) -> list:
    return list(map(lambda i: i * lp_weight, lp_points))

def set_proportion(lst: list, total: float, amount: float) -> list:
    return list(map(lambda i: (i / total) * amount, lst))