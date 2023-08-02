from typing import Sequence


def filter_dict(d: dict, keys: Sequence[str]) -> dict:
    new_d = {}
    for key in keys:
        new_d[key] = d.get(key)
    return new_d
