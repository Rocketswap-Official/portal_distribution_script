from api.blockservice import *
from api.node import gather_transaction_info, get_nonce_and_processor, send_transaction
from typing import Callable
from calculations.collecting import *
from calculations.extraction import *
from calculations.filtering import *
from calculations.formatting import *
from calculations.valuation import set_lp_weight
from calculations.batching import create_batches
from calculations.stamps_estimation import estimate_stamps_for_batch
from base_logger import logger
import time


DEX = "con_rocketswap_official_v1_1"
RSWP = "con_rswp_lst001"
FARM = "con_staking_rswp_rswp_interop_v2"
YIELD = "con_liq_mining_rswp_rswp"
WALLET_DEV = "fcefe7743fa70c97ae2d5290fd673070da4b0293da095f0ae8aceccf5e62b6a1"
DISTR = "con_distribute_v2"
P_TOKEN = "con_yeti_contract_7"


async def rswp(obj: dict, contract: str) -> tuple:
    balances_states = await get_hash_states(
        all_states=obj, contract=contract, variable="balances"
    )
    eligible_wallets = collect_eligible_wallets(states=balances_states)
    wallets_without_dev = remove_item(item=WALLET_DEV, lst=eligible_wallets)
    user_eligible_wallets = pass_only_user_wallets(lst=wallets_without_dev)
    user_balances, balance_sum = collect_balances(
        states=balances_states, wallets=user_eligible_wallets
    )
    return user_eligible_wallets, user_balances, balance_sum


async def rswp_lp(
    obj: dict, contract: str, variable: str, total_lp: float, token_reserve: float
) -> tuple:
    lp_points_states = await get_hash_states(
        all_states=obj, contract=contract, variable=variable
    )
    lp_weight = set_lp_weight(token_reserve=token_reserve, total_lp=total_lp)
    eligible_wallets = collect_eligible_wallets_lp(
        states=lp_points_states, lp_weight=lp_weight
    )
    wallets_without_dev = remove_item(item=WALLET_DEV, lst=eligible_wallets)
    user_eligible_wallets = pass_only_user_wallets(lst=wallets_without_dev)
    user_balances, balance_sum = collect_balances_lp(
        states=lp_points_states, wallets=user_eligible_wallets, lp_weight=lp_weight
    )
    return user_eligible_wallets, user_balances, balance_sum


def get_tx_info(
    contract: str,
    kwargs: dict,
    method: str,
    stamps: int,
    nonce_and_processor: tuple,
) -> dict:
    return gather_transaction_info(
        contract=contract,
        method=method,
        kwargs=kwargs,
        stamps=stamps,
        nonce_and_processor=nonce_and_processor,
    )


def send_distr_transaction(contract: str, method: str, kwargs: dict, stamps: int):
    nonce_and_processor = get_nonce_and_processor()
    tx_info = get_tx_info(
        contract=contract,
        kwargs=kwargs,
        method=method,
        stamps=stamps,
        nonce_and_processor=nonce_and_processor,
    )

    return send_transaction(tx_info=tx_info)


def pay_rewards(wallet_list: list, amount_list: list):
    method = "distr_token_var"
    kwargs = {
        "token": P_TOKEN,
        "addresses": wallet_list,
        "amounts": amount_list,
    }
    stamps = estimate_stamps_for_batch(batch=wallet_list)

    result = send_distr_transaction(
        contract=DISTR, method=method, kwargs=kwargs, stamps=stamps
    )
    return result


def distribute_portal(wallet_list: list, amount_list: list):
    if not wallet_list or not amount_list:
        logger.info("nothingness!")
        return
    for i in range(len(wallet_list)):
        wallets = wallet_list[i]
        amounts = amount_list[i]
        if len(wallets) == len(amounts):
            result = pay_rewards(wallet_list=wallets, amount_list=amounts)
            logger.info(result)
            # print("Works!")
            time.sleep(1)
        else:
            logger.info("There is a length inconsistence!")

    logger.warning("##########Distribution loop ended!##########")


def distribute_to_all(all_wallets: list, all_amounts: list):
    for w, amt in zip(all_wallets, all_amounts):
        distribute_portal(wallet_list=w, amount_list=amt)
        time.sleep(2)


async def create_list_of_lists(lst: list):
    l = []
    for i in lst:
        b = create_batches(data=i, batch_size=100)
        l.append(b)
    return l
