import math

def almost_equal(a: float, b: float) -> bool:
    return math.isclose(a, b)

def is_payable_amounts_right(balances: list, amount_to_share: float) -> bool:
    l = []
    for i in balances:
        l.append(sum(i))
    s = sum(l)
    return almost_equal(a=s, b=amount_to_share)