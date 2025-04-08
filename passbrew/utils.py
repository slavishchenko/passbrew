from typing import List

from passbrew.validation import is_list_of_strings, is_positive_integer


def filter_list(lst: List[str], max_length: int) -> List[str]:
    """
    Filter elements of a list based on their length.

    This function takes a list of strings and returns a new list
    containing only the strings that have a length less than or equal
    to the specified maximum length.

    :param lst: A list of strings to be filtered.
    :type lst: List[str]
    :param max_length: The maximum length of strings to include in
                        the output list.
    :type max_length: int
    :return: A list of strings that are less than or equal to the
                specified maximum length.
    :rtype: List[str]
    :raises: `TypeError` if `lst` is not a list of strings.
             `ValidationError` if `max_length` is 0, negative number,
             or not an int.

    """
    if is_list_of_strings(lst) and is_positive_integer(max_length):
        return [x for x in lst if len(x) <= max_length]
    else:
        raise TypeError(f"Input should be a list of string. Recieved: {type(lst)}")


def capitalize_random_letter(wrd: str, index: int) -> str:
    """
    Capitalize a letter in a string at a specified index.

    This function takes a string and an index, then returns a new string with
    the letter at the specified index capitalized. The function ensures that
    all characters before the index are in lowercase, while the character
    at the index is capitalized, and all characters after the index remain unchanged.

    :param wrd: The input string from which a letter will be capitalized.
    :type wrd: str
    :param n: The index of the letter in the string that should be capitalized.
    :type n: int

    :return: A new string with the specified letter capitalized and all
             preceding letters converted to lowercase.
    :rtype: str

    :raises IndexError: If the index `n` is out of bounds for the input string.
    """
    return wrd[:index].lower() + wrd[index:].capitalize()
