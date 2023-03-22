from base_logger import logger


async def get_hash_states(all_states: dict, contract: str, variable: str) -> dict:
    try:
        return all_states[contract][variable]
    except Exception as e:
        logger.warning(e)
        return {}