import random
import string

def sanitize_comma_separated(input_string):
    """
    Sanitize a comma-separated string by removing leading and trailing whitespaces
    from each element.

    Parameters:
    - input_string (str): The comma-separated input string.

    Returns:
    - list: A list of sanitized values.
    """
    # Split the input string by commas
    values = input_string.split(',')

    # Remove leading and trailing whitespaces from each element
    sanitized_values = [value.strip() for value in values]
    joined_string = ', '.join(str(value) for value in sanitized_values)
    return joined_string


def starts_with(input_string, prefix):
    """
    Check if the input string starts with the specified prefix.

    Parameters:
    - input_string (str): The input string to check.
    - prefix (str): The prefix to check for at the beginning of the input string.

    Returns:
    - bool: True if the input string starts with the prefix, False otherwise.
    """
    return input_string.startswith(prefix)


def generate_simple_id():
    # Generate a random 5-character ID using uppercase letters and digits
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))