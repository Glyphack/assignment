def lists_are_equal(first, second):
    """
    Checks whether to lists are equal or not
    Note: order matters
    """
    equal_length = len(first) == len(second)
    elements_equal = all([a == b for a, b in zip(first, second)])
    return equal_length and elements_equal
