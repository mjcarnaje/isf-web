from flask import request, url_for, json
from math import ceil

def safe_load_args(request_args):
    for key, value in request_args.items():
        try:
            request_args[key] = json.loads(value.replace("'", '"'))
        except ValueError:
            pass
    return request_args

def get_range(start, end):
    return list(range(start, end + 1))

def pagination(page_number, total_count, offset, page_size, base_url):
    if total_count == 0:
        return {
            'page_count': [0, 0],
            'current_page': 1,
            'total_count': 0,
            'pages': [],
            'prev_url': '',
            'next_url': ''
        }
    
    page_count = ceil(total_count / page_size)

    delta = 7 if page_count <= 7 else 2 if 4 < page_number < page_count - 3 else 4

    range_start = round(page_number - delta / 2)
    range_end = round(page_number + delta / 2)

    if range_start - 1 == 1 or range_end + 1 == page_count:
        range_start += 1
        range_end += 1

    pages = (
        get_range(
            min(range_start, page_count - delta),
            min(range_end, page_count)
        )
        if page_number > delta
        else get_range(1, min(page_count, delta + 1))
    )

    def with_dots(value, pair):
        return pair if len(pages) + 1 != page_count else [value]

    if pages[0] != 1:
        pages = with_dots(1, [1, "..."]) + pages

    if pages[-1] < page_count:
        pages = pages + with_dots(page_count, ["...", page_count])
    
    pages_with_url = []

    request_args = safe_load_args(request.args.to_dict())
    if 'page' in request_args:
        request_args.pop('page', None)

    for page in pages:
        item = {}
        item['label'] = page
        item['url'] = url_for(base_url, **request_args, page=page) if page != "..." else ""
        item['is_active'] = page == page_number
        pages_with_url.append(item)
    
    prev_url = ''
    next_url = ''

    if offset > 0:
        prev_url = url_for(base_url, **request_args, page=page_number - 1)
    
    if (offset + page_size) < total_count:
        next_url = url_for(base_url, **request_args, page=page_number + 1)
    
    return {
        'page_count': [offset + 1, total_count if offset + page_size > total_count else offset + page_size],
        'current_page': page_number,
        'total_count': total_count,
        'pages': pages_with_url,
        'prev_url': prev_url,
        'next_url': next_url
    }