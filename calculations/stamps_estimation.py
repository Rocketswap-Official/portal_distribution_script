from base_logger import logger

# stamps
BUY, SELL, TRANSFER = 164 * 2, 158 * 2, 50 * 2
STAMPS_PER_TAU = 169


def estimate_tau_cost_for_distr(wallet_list: list) -> int:
    num_of_addresses = len(wallet_list)
    total_stamps = BUY + SELL
    total_stamps += num_of_addresses * TRANSFER
    cost_in_tau = total_stamps / STAMPS_PER_TAU
    logger.info(f"Distribution cost: {cost_in_tau} TAU")
    return cost_in_tau


def estimate_stamps_for_batch(batch: list) -> int:
    num_of_addresses = len(batch)
    stamps = num_of_addresses * TRANSFER
    cost_in_tau = stamps / STAMPS_PER_TAU
    logger.info(f"Estimated batch stamps: {stamps}")
    logger.info(f"Batch stamps in TAU: {cost_in_tau}")
    return stamps


def estimate_stamps_for_sell_buy():
    stamps = BUY + SELL
    cost_in_tau = stamps / STAMPS_PER_TAU
    logger.info(f"Estimated sell/buy stamps: {stamps}")
    logger.info(f"Sell/buy stamps in TAU: {cost_in_tau}")
    return stamps
