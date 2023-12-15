from typing import List

def get_active_filter_count(data: dict, skip_values: List[str] = None):
    active_count = 0

    if skip_values is None:
        skip_values = []

    _skip_values = ['query'] + skip_values

    for key, value in data.items():
        if key not in _skip_values and value:
            active_count += 1

    return active_count
