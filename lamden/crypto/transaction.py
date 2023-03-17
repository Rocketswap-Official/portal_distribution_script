from .canonical import format_dictionary
from ..formatting.primatives import check_format
from ..formatting import rules
from . import wallet
from ..encoder import encode, decode

def build_transaction(wallet, contract: str, function: str, kwargs: dict, 
    nonce: int, processor: str, stamps: int):
    payload = {
        'contract': contract,
        'function': function,
        'kwargs': kwargs,
        'nonce': nonce,
        'processor': processor,
        'sender': wallet.verifying_key,
        'stamps_supplied': stamps,
    }

    payload = format_dictionary(payload) # Sort payload in case kwargs unsorted

    assert check_format(payload, rules.TRANSACTION_PAYLOAD_RULES), 'Invalid payload provided!'

    true_payload = encode(decode(encode(payload)))

    signature = wallet.sign(true_payload)

    metadata = {
        'signature': signature
    }

    tx = {
        'payload': payload,
        'metadata': metadata
    }

    return encode(format_dictionary(tx))