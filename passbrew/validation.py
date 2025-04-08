from typing import List

from passbrew.exceptions import ExceedsMaximumLength, IntError, ValidationError


def is_integer(value: int) -> bool:
    """
    Determine if the given value is an integer.

    This function checks if the input value is of integer type and returns
    True if it is, and False otherwise.

    :param value: The value to be checked.
    :param type: int
    :return: True if the value is an integer, False otherwise
    :rtype: bool
    :raises: exception.IntError
    """
    if isinstance(value, int):
        return True
    else:
        raise IntError(
            f"Invalid input type. Expected 'int', got '{type(value).__name__}' instead."
        )


def is_positive(number: int):
    """
    Check if a number is positive.

    :param num: The number to be checked.
    :param type: int
    :return: True if the number is positive, False otherwise
    :rtype: bool
    :raises: ValueError
    """
    if number > 0:
        return True
    else:
        raise ValueError(
            "The input must be a positive number. Please provide a valid positive number."
        )


def is_positive_integer(value) -> bool:
    """
    Check if the given value is a positive integer.

    This function verifies whether the input value is both an integer and
    a positive number. It uses helper functions `is_integer()` and
    `is_positive()` to perform these checks. If the checks are successful,
    the function returns True. If the input is not valid, an appropriate
    `ValidationError` is raised.

    :param value: The value to be checked. Can be of any type.
    :type value: Any

    :return: True if the value is a positive integer, False otherwise.
    :rtype: bool

    :raises: ValidationError
    """
    try:
        is_integer(value) and is_positive(value)
        return True
    except IntError as e:
        raise ValidationError(e)
    except ValueError as e:
        raise ValidationError(e)


def validate_length(length: int, min: int, max: int) -> bool:
    """
    Validates if a given length falls within specified minimum and maximum bounds.

    :param length: The length to validate.
    :param min: The minimum acceptable length (inclusive).
    :param max: The maximum acceptable length (inclusive).

    :raises ValueError: If `length` is not within the specified range.
                        Provides details about the invalid value and the valid range.
    """
    if length in range(min, max + 1):
        return True
    else:
        raise ValueError(
            f"Invalid length: {length}. "
            f"Length must be between {min} (inclusive) and {max} (inclusive)."
        )


def is_less_than(a: int, b: int) -> bool:
    """
    This function compares two integers and raises an exception if the first integer
    is greater than or equal to the second.

    :param a: The integer to be compared.
    :type a: int
    :param b: The integer to compare against.
    :type b: int
    :returns: True if `a` is less than `b`.
    :rtype: bool
    :raises ExceedsMaximumLength: If `a` is greater than or equal to `b`.
    """
    if a >= b:
        raise ExceedsMaximumLength(
            f"Value {a} exceeds the maximum permitted value {b}."
        )
    return True


def is_greater_than(a: int, b: int) -> bool:
    """
    This function compares two integers and raises an exception if the first integer
    is less than or equal to the second.

    :param a: The integer to be compared.
    :type a: int
    :param b: The integer to compare against.
    :type b: int
    :returns: True if `a` is greater than `b`.
    :rtype: bool
    :raises ValueError: If `a` is less than or equal to `b`.
    """
    if a <= b:
        raise ValueError(f"Value {a} is less than or equal to the permitted value {b}.")
    return True


def is_list_of_strings(lst: List):
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False
