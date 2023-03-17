from lamden.crypto.transaction import build_transaction
from lamden.crypto.wallet import Wallet
from typing import Any
from base_logger import logger
from settings import env
import requests

MY_WALLET = Wallet(env["priv_key"])
NODE_URL = env["node_urls"][2]

def get_nonce_and_processor() -> tuple:
    try:
        response = requests.get(f"{NODE_URL}/nonce/{MY_WALLET.verifying_key}")
        logger.info("Getting nonce and processor")
        return response.json()["nonce"], response.json()["processor"]
    except requests.exceptions.RequestException as e:
        logger.warning(e)
        return None, None
    except Exception as e:
        logger.warning(e)
        return None, None
    
def gather_transaction_info(contract: str, method: str, kwargs: dict, 
    stamps: float, nonce_and_processor: tuple) -> dict:
    nonce, processor = nonce_and_processor
    
    if nonce and processor:
        tx = build_transaction(
            wallet=MY_WALLET,
            processor=processor,
            stamps=stamps,
            nonce=nonce,
            contract=contract,
            function=method,
            kwargs=kwargs,
        )
        return tx
    else:
        return {}
    
def post_transaction(tx_info: dict) -> dict:
    try:
        response = requests.post(f"{NODE_URL}", data=tx_info)
        logger.info("Posting transaction. . .")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.warning(e)
        return {}
    except Exception as e:
        logger.warning(e)
        return {}

def send_transaction(tx_info: dict) -> dict:
    if tx_info:
        response = post_transaction(tx_info=tx_info)
        return response
    else:
        logger.warning("tx_info object returned {}")
        return {}
    
def get_tx_results(tx_hash: str) -> Any:
    try:
        res = requests.get(f"{NODE_URL}/tx", params={"hash": tx_hash})
        return res.json()
    except requests.exceptions.RequestException as e:
        logger.warning(e)
        return {}
    except Exception as e:
        logger.warning(e)
        return {}