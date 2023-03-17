from decimal import Decimal
import json

def json_to_dict(obj: str) -> dict:
    return json.loads(obj, strict=False)


def is_fixed_or_hash_self(hash_value):
    # {"__fixed__":"9999999999779"}
    # {"__hash_self__":{"__fixed__":"4.9483948227450823637842E-8"}}
    if isinstance(hash_value, dict):
        try:
            v = hash_value["__fixed__"]
            return Decimal(v)
        except KeyError:
            try:
                v = hash_value["__hash_self__"]
                if isinstance(v, int):
                    return v
                else:
                    # __hash_self__ could hold a __fixed__ object
                    return Decimal(v["__fixed__"])
            except Exception as e:
                return 0
    return hash_value