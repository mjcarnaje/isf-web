from babel.numbers import format_currency as _format_currency

def format_currency(number, currency_code='PHP', locale='en_PH'):
    formatted_amount = _format_currency(number, currency_code, locale=locale)
    return formatted_amount