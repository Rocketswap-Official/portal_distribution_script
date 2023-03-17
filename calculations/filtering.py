import copy
from calculations.type_checking import is_hex

def remove_item(item: str, lst: list) -> list:
    try:
        lst_copy = copy.copy(lst)
        lst_copy.remove(item)
        return lst_copy
    except ValueError:
        return lst_copy


def pass_only_user_wallets(lst: list):
    return list(filter(lambda i: is_hex(i) and len(i) == 64, lst))