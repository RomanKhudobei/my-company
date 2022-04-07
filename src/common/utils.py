

def empty_string_to_none(value):
    if isinstance(value, str) and value == '':
        return None

    return value
