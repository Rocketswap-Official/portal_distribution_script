from base_logger import logger
from settings import env
import random
from typing import Any


def pick_blockservice_randomly():
    urls = env["blockservice_urls"]
    random.shuffle(urls)
    return urls[-1]


async def get_all_states_of_contract(httpx_client: Any, contract: str) -> dict:
    try:
        blockservice_url = pick_blockservice_randomly()
        response = await httpx_client.get(
            f"{blockservice_url}/current/all/{contract}"
        )
        logger.info(
            f"Fetching all states of {contract} from blockservice"
        )
        return response.json()
    except httpx.RequestError as e:
        logger.warning(e)
        return {}


async def get_all_states_of_hash(httpx_client: Any, contract: str, hash: str) -> dict:
    try:
        blockservice_url = pick_blockservice_randomly()
        response = await httpx_client.get(
            f"{blockservice_url}/current/all/{contract}/{hash}"
        )
        logger.info(
            f"Fetching states of {hash} of {contract} from blockservice"
        )
        return response.json()
    except httpx.RequestError as e:
        logger.warning(e)
        return {}
