"""
Common functions
"""


def add0(num):
    """
    add 0 to number less than 10
    """
    if num < 10:
        return '0'+str(num)
    return str(num)
