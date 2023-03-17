from base_logger import logger
import requests
import random


def pick_blockservice_randomly():
    urls = env["blockservice_urls"]
    random.shuffle(urls)
    return urls[-1]


# # DISTR_CONTRACT
# def get_tau_amt_to_spend()->float | int:
#     try:
#         blockservice_url = pick_blockservice_randomly()
#         response = requests.get(
#             f"{blockservice_url}/current/one/{DISTR_CONTRACT}/tau_to_distribute"
#         )
#         d = is_fixed_or_hash_self(response.json()["value"])
#         logger.info(f"TAU to distribute: {d}")
#         return d
#     except requests.exceptions.RequestException as e:
#         logger.warning(e)
#         return 0

# def get_reward_token_amount(contract: str)->float | int:
#     try:
#         blockservice_url = pick_blockservice_randomly()
#         response = requests.get(
#             f"{blockservice_url}/current/one/{contract}/balances/{DISTR_CONTRACT}"
#         )
#         r = is_fixed_or_hash_self(response.json()["value"])
#         logger.info(f"Reward amount: {r}")
#         return r
#     except requests.exceptions.RequestException as e:
#         logger.warning(e)
#         return 0


# # YETI
# def get_all_states_of_yeti() -> dict:
#     try:
#         blockservice_url = pick_blockservice_randomly()
#         response = requests.get(f"{blockservice_url}/current/all/{YETI_CONTRACT}")
#         logger.info(f"Fetching all states of {YETI_CONTRACT} from blockservice")
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         logger.warning(e)
#         return {}


# def get_yeti_balance_of_contract(contract: str, all_states: dict) -> float | int:
#     try:
#         balances = all_states[YETI_CONTRACT]["balances"]
#         x = balances[contract]
#         return is_fixed_or_hash_self(x)
#     except Exception as e:
#         logger.warning(e)
#         return 0


# def get_yeti_holders_and_balances(all_states: dict) -> dict:
#     try:
#         balances = all_states[YETI_CONTRACT]["balances"]
#         return balances
#     except Exception as e:
#         logger.warning(e)
#         return {}


# def get_yeti_metadata(metadata_key: str, all_states: dict) -> str:
#     try:
#         metadata = all_states[YETI_CONTRACT]["metadata"]
#         return metadata[metadata_key]
#     except Exception as e:
#         logger.warning(e)
#         return ""


def get_all_states_of_contract(contract: str) -> dict:
    try:
        blockservice_url = pick_blockservice_randomly()
        response = requests.get(
            f"{blockservice_url}/current/all/{contract}"
        )
        logger.info(
            f"Fetching all states of {contract} from blockservice"
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.warning(e)
        return {}

def get_all_states_of_hash(contract: str, hash: str) -> dict:
    try:
        blockservice_url = pick_blockservice_randomly()
        response = requests.get(
            f"{blockservice_url}/current/all/{contract}/{hash}"
        )
        logger.info(
            f"Fetching states of {hash} of {contract} from blockservice"
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.warning(e)
        return {}




# def get_dex_fee_percentage(state_name: str, all_states: dict) -> float | int:
#     try:
#         state = all_states["con_rocketswap_official_v1_1"]["state"]
#         x = state[state_name]
#         return is_fixed_or_hash_self(x)
#     except Exception as e:
#         logger.warning(e)
#         return 0


# def get_token_reserves(token: str, all_states: dict) -> tuple:
#     try:
#         reserves = all_states["con_rocketswap_official_v1_1"]["reserves"]
#         x, y = reserves[token]
#         currency_reserve, token_reserve = is_fixed_or_hash_self(
#             x
#         ), is_fixed_or_hash_self(y)
#         return currency_reserve, token_reserve
#     except Exception as e:
#         logger.warning(e)
#         return None, None

# # for test
# def get_all_states_of_marmite() -> dict:
#     try:
#         blockservice_url = "https://arko-bs-2.lamden.io"
#         response = requests.get(f"{blockservice_url}/current/all/con_marmite100_contract")
#         logger.info(f"Fetching all states of MARMITE from blockservice")
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         logger.warning(e)
#         return {}

# def get_marmite_holders_and_balances(all_states: dict) -> dict:
#     try:
#         balances = all_states["con_marmite100_contract"]["balances"]
#         return balances
#     except Exception as e:
#         logger.warning(e)
#         return {}