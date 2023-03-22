from decouple import config

BLOCKSERVICE_1 = config("ARKO_BS_1")
BLOCKSERVICE_2 = config("ARKO_BS_2")
BLOCKSERVICE_3 = config("ARKO_BS_3")
NODE_1 = config("ARKO_TEST_1")
NODE_2 = config("ARKO_TEST_2")
NODE_3 = config("ARKO_TEST_3")
PRIV_K = config("PRIV_K")

env = {
    "blockservice_urls": [BLOCKSERVICE_1, BLOCKSERVICE_2, BLOCKSERVICE_3],
    "node_urls": [NODE_1, NODE_2, NODE_3],
    "priv_key": PRIV_K,
}
