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