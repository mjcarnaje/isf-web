def get_active_filter_count(data):
    active_count = sum(value is not None and value not in ["", False] if key != 'query' else False for key, value in data.items())
    return active_count