from calculations.formatting import is_fixed_or_hash_self
from calculations.valuation import set_proportion

def collect_eligible_wallets(states: dict):
    l = []
    for k, v in states.items():
        b = is_fixed_or_hash_self(v)
        if b >= 1000:
            l.append(k)
    return l


def collect_eligible_wallets_lp(states: dict, lp_weight: float):
    l = []
    for k, v in states.items():
        b = is_fixed_or_hash_self(v) * lp_weight
        if b >= 1000:
            l.append(k)
    return l


def collect_balances(states: dict, wallets: list) -> tuple:
    n = 0
    i = []
    for k, v in states.items():
        if k in wallets:
            b = is_fixed_or_hash_self(v)
            n += b
            i.append(b)
    return i, n


def collect_balances_lp(states: dict, wallets: list, lp_weight: float) -> tuple:
    n = 0
    i = []
    for k, v in states.items():
        if k in wallets:
            b = is_fixed_or_hash_self(v)
            n += b * lp_weight
            i.append(b * lp_weight)
    return i, n


def compile_payable_amounts(
    balances: list, overall_total_balance: float, amount_to_share: float
) -> list:
    payable_list = []
    for b in balances:
        amounts_payable = set_proportion(
            lst=b, total=overall_total_balance, amount=amount_to_share
        )
        payable_list.append(amounts_payable)
    return payable_list
