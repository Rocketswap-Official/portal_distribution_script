from actions import *
from calculations.verification import is_payable_amounts_right
from calculations.batching import create_batches
# snapshots for testing
# from data import DEX_DATA, RSWP_DATA, FARM_DATA, YIELD_DATA
import asyncio 
import httpx
import time

# total to be distributed
AMOUNT = Decimal("1666431.61011361")


async def main():
    
    # rswp_balances_obj = json_to_dict(obj=RSWP_DATA)
    # farm_balances_obj = json_to_dict(obj=FARM_DATA)
    # dex_all_states_obj = json_to_dict(obj=DEX_DATA)
    # yield_balances_obj = json_to_dict(obj=YIELD_DATA)

    async with httpx.AsyncClient() as client:
        tasks = []
        for c in [RSWP, FARM, YIELD]:
            tasks.append(asyncio.create_task(get_all_states_of_hash(
                httpx_client=client, contract=c, hash="balances")))
        tasks.append(get_all_states_of_contract(httpx_client=client, contract=DEX))

        results = await asyncio.gather(*tasks)

    rswp_balances_obj, farm_balances_obj, yield_balances_obj, dex_all_states_obj = results

    reserves_states = await get_hash_states(
        all_states=dex_all_states_obj, contract=DEX, variable="reserves"
    )
    lp_points_dex = await get_hash_states(
        all_states=dex_all_states_obj, contract=DEX, variable="lp_points"
    )
    total_lp = is_fixed_or_hash_self(lp_points_dex[RSWP]["__hash_self__"])
    token_reserve = is_fixed_or_hash_self(reserves_states[RSWP][1])

    # obtain eligible wallets with RSWP value > 1000, their balances,
    # and the sum of all those balances
    wallets_1, balances_1, total_balance_1 = await rswp(obj=rswp_balances_obj, contract=RSWP)
    wallets_2, balances_2, total_balance_2 = await rswp_lp(
        obj=dex_all_states_obj,
        contract=DEX,
        variable="lp_points",
        total_lp=total_lp,
        token_reserve=token_reserve,
    )
    wallets_3, balances_3, total_balance_3 = await rswp(obj=farm_balances_obj, contract=FARM)
    wallets_4, balances_4, total_balance_4 = await rswp_lp(
        obj=yield_balances_obj,
        contract=YIELD,
        variable="balances",
        total_lp=total_lp,
        token_reserve=token_reserve,
    )
    # needed to calculate each wallet share: (i/overall_total_balance) * AMOUNT
    overall_total_balance = (
        total_balance_1 + total_balance_2 + total_balance_3 + total_balance_4
    )

    balances = [balances_1, balances_2, balances_3, balances_4]
    
    # calculate how much each wallet is supposed to receive for each case
    # RSWP staked LP, RSWP staked, RSWP LP, RSWP
    payable_list = compile_payable_amounts(
        balances=balances,
        overall_total_balance=overall_total_balance,
        amount_to_share=AMOUNT,
    )

    # check if all payable amounts add up to the total to be distributed
    if is_payable_amounts_right(balances=payable_list, amount_to_share=AMOUNT):
        ws = [wallets_1, wallets_2, wallets_3, wallets_4]
    
        all_amounts = await create_list_of_lists(lst=payable_list)
        all_wallets = await create_list_of_lists(lst=ws)
        # distribute to all:
        # RSWP staked LP, RSWP staked, RSWP LP, RSWP
        # distribute_to_all(all_wallets=all_wallets , all_amounts=all_amounts)

    else:
        print("Payable amounts not right!")


if __name__ == "__main__":
    st = time.perf_counter()
    asyncio.run(main())
    print(f"{time.perf_counter() - st} sec")
    # main()
