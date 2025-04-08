import random
from typing import List

from passbrew.errors import ValidationError
from passbrew.utils import capitalize_random_letter, filter_list
from passbrew.validators import (
    is_positive_integer,
    validate_length,
)

from .base_generator import BasePasswordGenerator


class BaseUserFriendlyPasswordGenerator(BasePasswordGenerator):
    """
    A class to generate user-friendly, but secure passwords with a customizable
    set of parameters.

    The UserFriendlyPassword allows users to create passwords of varying lengths
    and complexity. Users can define the inclusion of uppercase letters,
    lowercase letters, digits, and special characters based on their security
    requirements.

    Methods:
        generate() -> str:
            Generates and returns a random password based on the specified attributes.
    """

    _min_length = 12
    _max_length = 64
    _password_prep = []

    def _pick_a_random_word(self, max_length: int) -> str:
        """
        Select a random word from a filtered list of words.

        This method filters the list of available words based on the specified
        maximum length and returns a randomly chosen word from the filtered list.

        :param max_length: The maximum length of words to consider for selection.
        :type max_length: int
        :return: A randomly selected word that meets the length criteria.
        :rtype: str

        :raises: `ValidationError` if `max_length` is less than or
                 equal to zero or not and int.
                 `TypeError` if list is not a list of strings.
                 `IndexError` if the list is empty.
        """

        filtered_words = filter_list(self.words, max_length)
        return random.choice(filtered_words)


class UserFriendlyPasswordGenerator(BaseUserFriendlyPasswordGenerator):
    _special_chars = [
        "!",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        ",",
        ".",
        "-",
        "_",
        "+",
        "=",
        "<",
        ">",
        "?",
    ]
    _char_amount = 1
    _num_amount = 1
    _empty_space_amount = 1

    @property
    def char_amount(self) -> int:
        """
        Get the amount of special characters.

        :return: The number of characters.
        :rtype: int
        """
        return self._char_amount

    @classmethod
    def set_char_amount(kls, value: int) -> None:
        """
        Set the amount of characters to be used in a password.

        :param value: The amount of characters to set. Minimum is 1.
        :type value: int
        :raises ValidationError: If the value is not a positive integer.
        """
        if is_positive_integer(value):
            try:
                kls.get_extra_chars_amnt(kls, char_amount=value)
                kls._char_amount = value
            except ValueError as e:
                raise ValidationError(e)

    @property
    def num_amount(self) -> int:
        """
        Get the amount of numbers.

        :return: Amount of numbers.
        :rtype: int
        """
        return self._num_amount

    @classmethod
    def set_num_amount(kls, value: int) -> None:
        """
        Set the amount of numbers to be used in a password.

        :param value: The amount of numbers to set. Minimum is 1.
        :type value: int
        :raises ValidationError: If the value is not a positive integer.
        """
        if is_positive_integer(value):
            try:
                kls.get_extra_chars_amnt(kls, num_amount=value)
                kls._num_amount = value
            except ValueError as e:
                raise ValidationError(e)

    @property
    def empty_space_amount(self) -> int:
        """
        Get the amount of empty spaces.

        :return: Number of empty spaces.
        :rtype: int
        """
        return self._empty_space_amount

    @classmethod
    def set_empty_space_amount(kls, value: int) -> None:
        """
        Set the amount of empty spaces to be used in a password.

        :param value: The number of empty spaces to set. Minimum is 1.
        :type value: int
        :raises ValidationError: If the value is not a positive integer.
        """
        if is_positive_integer(value):
            try:
                kls.get_extra_chars_amnt(kls, empty_space_amount=value)
                kls._empty_space_amount = value
            except ValueError as e:
                raise ValidationError(e)

    def get_extra_chars_amnt(
        self,
        char_amount: int = None,
        num_amount: int = None,
        empty_space_amount: int = None,
        password_length: int = None,
    ) -> int:
        """
        This method computes the total number of "extra" characters based on
        the sum of character, numeric, and empty space amounts defined in
        the instance. It checks if the total exceeds the maximum allowed password
        length or the specified password length, raising a ValueError if
        it does.

        :param char_amount: The amount of special characters for the password.
        :type char_amount: int

        :param num_amount: The amount of numbers for the password.
        :type num_amount: int

        :param empty_space_amount: The nuber of empty spaces for the password.
        :type empty_space_amount: int

        :param password_length: The desired length of the password.
                                Defaults to maximum password length.
        :type password_length: int

        :return: The total amount of extra characters.
        :rtype: int

        :raises ValueError: If the total of extra characters exceeds the
                            specified maximum length or the provided
                            password length.

        """
        char_amount = char_amount or self._char_amount
        num_amount = num_amount or self._num_amount
        empty_space_amount = empty_space_amount or self._empty_space_amount
        password_length = password_length or self._max_length

        extra_chars_amnt = char_amount + num_amount + empty_space_amount
        if extra_chars_amnt >= self._max_length or extra_chars_amnt >= password_length:
            raise ValueError(
                f"Error calculating extra characters: Total extra characters ({extra_chars_amnt}) "
                f"exceeds the maximum allowed length ({self._max_length}) "
                f"or the specified password length ({password_length})."
            )
        return extra_chars_amnt

    def _get_effective_password_length(self, password_length: int) -> int:
        """
        Calculate the effective password length by subtracting the amount of extra
        characters.

        This method determines the actual usable length for a password by
        subtracting the number of extra characters (including special characters,
        numbers, and spaces) from the specified password length. It uses
        the `get_extra_chars_amnt` method to perform this calculation.

        :param password_length: The total length of the intended password
                                before considering extra characters.
        :type password_length: int

        :return: The effective password length after accounting for extra characters.
        :rtype: int

        :raises ValueError: Propagated from `get_extra_chars_amnt` if the total number of
                            extra characters exceeds the collective password length.

        """
        return password_length - self.get_extra_chars_amnt(
            password_length=password_length
        )

    def _get_random_words(self, password_length: int) -> None:
        """
        Generate and collect random words to form a password.

        This method retrieves random words based on the specified password length
        while ensuring that the total length of words does not exceed the given
        password length. The words are appended to the `_password_prep` list.

        :param password_length: The desired total length of the password.
        :type password_length: int

        :raises ValueError: If `password_length` is outside the allowed range
                            defined by `self.min_length` and `self.max_length`.
        :return: None
        """
        if validate_length(password_length, self._min_length, self._max_length):
            pw_length = self._get_effective_password_length(password_length)
            while pw_length > 0:
                wrd = self._pick_a_random_word(pw_length)
                self._password_prep.append(wrd)
                pw_length -= len(wrd)

    def _get_special_chars(self) -> List:
        """
        Select random special characters for the password.

        This method randomly selects a number of special characters defined by
        `self.char_amount` from a predefined pool of special characters
        (`self._special_chars`).

        :return: A list of randomly selected special characters.
        :rtype: List[str]

        :raises ValidationeError: If `self.char_amount` is less than or equal to zero.
        """
        if self.char_amount <= 0:
            raise ValidationError(
                f"Invalid value for `char_amount`: {self.char_amount}. It must be a positive integer."
            )
        return random.choices(self._special_chars, k=self.char_amount)

    def _get_nums(self) -> List[int]:
        """
        Generate a list of random digits for a password.

        This method generates a list of random integers between 0 and 9,
        inclusive. The total number of integers generated is determined by the
        `num_amount` instance variable. Each generated number represents a digit
        that can be used as part of a password.

        :return: A list of randomly selected integers in the range [0, 9].
        :rtype: List[int]
        """
        nums = []
        for i in range(self.num_amount):
            nums.append(str(random.randint(0, 9)))
        return nums

    def _add_a_capital_letter(self) -> None:
        """
        Adds a capital letter to a randomly selected word from the password preparation
        list.

        This method selects a word from the `_password_prep` attribute, randomly chooses
        a position within that word, and capitalizes the letter at that position.
        The updated word replaces the original word in the `_password_prep` list.

        This function is intended to enhance the complexity of generated passwords by
        ensuring that at least one letter is capitalized.

        :raises IndexError: If the list `_password_prep` is empty or if the selected word
                            does not contain enough characters to capitalize a letter.
        """

        wrd = random.choice(self._password_prep)
        n = random.randint(1, len(wrd) - 1)
        index = self._password_prep[wrd]
        self._password_prep[index] = capitalize_random_letter(wrd, n)

    @property
    def _extra_chars_group(self) -> List:
        """
        Groups special characters and numbers into one list.

        This property fetches a list of special characters and appends a list
        of numbers to it, returning a combined list of extra characters that
        can be used for password generation.

        :return: A list containing both special characters and numbers.
        :rtype: List[str]
        """
        extra_chars = self._get_special_chars()
        extra_chars.extend(self._get_nums())
        return extra_chars

    def _get_collective_password_prep(self) -> None:
        """
        Adds extra characters to the password preparation list.

        :return: None
        """
        self._password_prep.extend(self._extra_chars_group)

    def _add_blank_space(self, lst: List[str]) -> None:
        # TODO Spaces cannot be added consecutively
        """
        Adds blank spaces into the password list.

        Blank spaces must not be at the beginning or the end of the list.

        :param lst: The list to which blank spaces will be added.
        :type lst: List[str]
        :return: None
        """
        for _ in range(self.empty_space_amount):
            index = random.randint(1, len(lst) - 2)
            lst.insert(index, " ")

    def _shuffle(self) -> None:
        """
        Randomizes the order of items in the `_password_prep` list.

        This method uses the `random.shuffle` function to reorder the elements in
        the `_password_prep` list in place. Shuffling the items can help enhance
        the unpredictability of the generated password by ensuring that the order
        of words or characters does not follow a specific pattern.
        """
        random.shuffle(self._password_prep)

    def generate(self, length: int) -> str:
        """
        Generates a password of the specified length.

        This method orchestrates the password generation process by performing the
        following steps:
        1. Validates the input using `validate_input`.
        2. Clears the existing `_password_prep` list to start fresh.
        3. Retrieves a set of random words using `_get_random_words`.
        4. Populates the `_password_prep` list by calling `_get_collective_password_prep`.
        5. Randomizes the order of items in the `_password_prep` list using `_shuffle`.
        6. Adds blank spaces to the password elements by calling `_add_blank_space`.
        7. Constructs and returns the final password using `_get`..

        :param length: The desired length of the generated password. Must be
                       a positive integer.
        :return: A string representing the generated password.

        :raises ValiadtionError: If `length` is not valid.
        """
        self.validate_input(length)
        self._password_prep.clear()
        self._get_random_words(length)
        self._get_collective_password_prep()
        self._shuffle()
        self._add_blank_space(self._password_prep)
        return self._get()
