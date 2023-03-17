from calculations.formatting import is_fixed_or_hash_self
from base_logger import logger
from decimal import Decimal
import math


def create_single_batch(data: list) -> list:
    logger.info("1 batch created")
    return [data]
    

def create_multiple_batches(data: list, batch_number: int, batch_size: int) -> list:
    i = 0
    l = []
    for c in range(batch_number):
        if c == batch_number - 1:
            l.append(data[i:])
            logger.info(f"{batch_number} batches created")
            return l
        l.append(data[i : i + batch_size])
        i = i + batch_size


def create_batches(data: list, batch_size: int) -> list:
    len_of_list = len(data)
    batch_number = math.ceil(len_of_list / batch_size)

    if batch_number == 1:
        return create_single_batch(data=data)
    else:
        return create_multiple_batches(
            data=data, batch_number=batch_number, batch_size=batch_size
        )


def create_list_of_amount_for_batch(
    batch: list, balance_states: dict, contract_balance: float, total: float
) -> list:
    a = []
    for k, v in balance_states.items():
        if k in batch:
            user_balance = is_fixed_or_hash_self(v)
            user_balance -= Decimal("0.00000001")
            a.append(contract_balance * (user_balance / total))
    return a
   