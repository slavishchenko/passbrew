from pathlib import Path

from passbrew.errors import ExceedsMaximumLength, ValidationError
from passbrew.validators import (
    is_greater_than,
    is_less_than,
    is_positive_integer,
    validate_length,
)


class BasePasswordGenerator:
    """
    A base class for generating passwords.

    This class serves as a foundation for creating customizable password
    generators. It provides basic functionalities to generate passwords
    based on given criteria such as length, character types, and additional
    requirements.

    Attributes
    ----------
    min_length : int
        The minimum length of the generated password.
    max_length : int
        The maximum length of the generated password.

    Methods
    -------
    set_min_length(value: int) -> None
        Sets the minimum length for generated passwords.
    set_max_length(value: int) -> None
        Sets the maximum length for generated passwords.
    validate_input(value: int) -> bool
        Validates whether the provided value is a positive integer
        within the allowed password length range.
    _get() -> str
        Returns the concatenated password from the preparation list.
    """

    DEFAULT_WORD_LIST_PATH = Path(__file__).resolve().parents[2] / "words.txt"

    _min_length = 12
    _max_length = 64
    _password_prep = []

    def __init__(self, word_list_path=DEFAULT_WORD_LIST_PATH) -> None:
        with open(word_list_path, "r", encoding="utf-8") as f:
            self.words = [x.strip() for x in f]

    @property
    def min_length(self):
        """
        Get the minimum password length.

        This property returns the minimum length that has been set
        for the instance.

        :return: The minimum length.
        :rtype: int
        """
        return self._min_length

    @classmethod
    def set_min_length(kls, value: int) -> None:
        """
        Set the minimum length for the password.

        This method sets the minimum length attribute of the class if
        the given value is a positive integer and is less than the
        class's maximum length. It raises a `ValidationError` if the
        provided value is invalid or if it exceeds the maximum length.

        :param value: The minimum length to be set. Default is 12.
        :type value: int
        :raises ValidationError: If the provided value is not a positive
                                 integer or exceeds the maximum length defined by the class.
        """
        try:
            if is_positive_integer(value) and is_less_than(value, kls._max_length):
                kls._min_length = value
        except ValidationError as e:
            raise ValidationError(e)
        except ExceedsMaximumLength as e:
            raise ValidationError(e)

    @property
    def max_length(self):
        """
        Get the maximum password length.

        This property returns the maximum length that has been set
        for the instance.

        :return: The maximum length.
        :rtype: int
        """
        return self._max_length

    @classmethod
    def set_max_length(kls, value: int) -> None:
        """
        Set the maximum length for the password.

        This method sets the maximum length attribute of the class if
        the given value is a positive integer and is greater than the
        class's minimum length. It raises a `ValidationError` if the
        provided value is invalid or if it less than minimum length.

        :param value: The maximum length to be set. Default is 64.
        :type value: int
        :raises ValidationError: If the provided value is not a positive
                                 integer or is less than minimum length defined by the class.
        """
        try:
            if is_positive_integer(value) and is_greater_than(value, kls._min_length):
                kls._max_length = value
        except ValidationError as e:
            raise ValidationError(e)
        except ValueError as e:
            raise ValidationError(e)

    def validate_input(
        self, value, min_length: int = None, max_length: int = None
    ) -> bool:
        """
        Validate the provided input value for password generation.

        This method checks if the given value is a positive integer and
        within the specified length range (min_length to max_length).

        :param value: The value to be validated as a potential password length.
        :type value: int

        :param min_length: Range start.
        :type min_length: int

        :param max_length: Range stop.
        :type max_length: int

        :return: True if the value is a positive integer within the allowed range,
                 otherwise raises a ValidationError.
        :rtype: bool

        :raises ValidationError: If the value is not a positive integer or is not
                                 within the defined minimum and maximum length constraints.
        """
        if not min_length:
            min_length = self.min_length
        if not max_length:
            max_length = self.max_length

        try:
            if is_positive_integer(value) and validate_length(
                value, min_length, max_length
            ):
                return True
        except Exception as e:
            raise ValidationError(e)

    def _get(self) -> str:
        return "".join(self._password_prep)
