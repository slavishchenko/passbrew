import random

from passbrew.exceptions import ValidationError
from passbrew.generators.user_friendly import BaseUserFriendlyPasswordGenerator
from passbrew.validation import is_greater_than, is_less_than, is_positive_integer


class PassphraseGenerator(BaseUserFriendlyPasswordGenerator):
    """
    A class for generating user-friendly passphrases.

    The Passphrase class extends the UserFriendlyPassword class and provides
    functionality to create secure and memorable passphrases comprised of
    random words. The generated passphrase maintains a specified length while
    ensuring that it does not end with an empty space.

    Methods
    -------
    generate(pw_length: int) -> str
        Generates and returns a user-friendly passphrase of the specified length.
    """

    # Using 4 to 8 words for a passphrase offers strong security while
    # remaining memorable, balancing complexity and usability.
    _min_word_count = 4
    _max_word_count = 12

    @property
    def min_word_count(self) -> int:
        return self._min_word_count

    @classmethod
    def set_min_word_count(cls, value: int) -> None:
        try:
            if is_positive_integer(value) and is_less_than(value, cls._max_word_count):
                cls._min_word_count = value
        except ValidationError as e:
            raise ValidationError(e)
        except ValueError as e:
            raise ValidationError(e)

    @property
    def max_word_count(self) -> int:
        return self._max_word_count

    @classmethod
    def set_max_word_count(cls, value: int) -> None:
        try:
            if is_positive_integer(value) and is_greater_than(
                value, cls._min_word_count
            ):
                cls._max_word_count = value
        except ValidationError as e:
            raise ValidationError(e)
        except ValueError as e:
            raise ValidationError(e)

    def _populate_password_prep(self, password_length: int) -> None:
        """
        Populate the _password_prep list with randomly selected words.

        This method selects random words based on the specified cumulative password
        length. Each chosen word has an additional space appended to it. To ensure
        that the final password does not end with an empty space, the collective
        password length is incremented by one.

        The last empty space will be removed in the final password preparation step,
        resulting in a passphrase of the desired length.

        :param collective_pw_length: The desired length of the passphrase, which
                                    must be validated against the minimum and
                                    maximum length constraints.
        :type collective_pw_length: int

        :return: None
        """

        while password_length > 0:
            wrd = self._pick_a_random_word(password_length)
            if len(wrd) == password_length - 1:
                continue
            elif password_length == len(wrd):
                self._password_prep.append(wrd)
                break
            else:
                wrd += " "
                self._password_prep.append(wrd)
                password_length -= len(wrd)

    def _get_last_item_index(self) -> int:
        """
        Retrieve the index of the last word in the password preparation list.

        :return: The index of the last word in the `_password_prep` list.
        :rtype: int
        """
        return len(self._password_prep) - 1

    def _final_password_prep(self) -> None:
        """
        Finalize the password preparation by removing trailing whitespace.

        :return: None
        """
        self._password_prep[self._get_last_item_index()] = self._password_prep[
            self._get_last_item_index()
        ]

    def _get_words(self, count):
        self._password_prep.extend(random.sample(self.words, k=count))

    def generate(self, password_length: int, use_word_count: bool = True) -> str:
        """
        Generate a randomized passphrase of a specified length.

        If `use_word_count` is set to True, the passphrase will be generated
        based on the number of words specified by `password_length`. If set to
        False, the method generates a passphrase based on the specified
        character length.

        :param password_length: The desired length of the passphrase, which determines
                        how many words or characters will be included in the generated
                        passphrase.
        :type password_length: int

        :param use_word_count: A boolean flag that indicates whether the passphrase
                               should be generated based on a word count (if True)
                               or a character count (if False).
        :type use_word_count: bool, optional (default is True)

        :return: The generated randomized passphrase.
        :rtype: str
        """
        if use_word_count:
            self.validate_input(
                password_length, self._min_word_count, self._max_word_count
            )
            self._password_prep.clear()
            self._get_words(password_length)
            return " ".join(self._password_prep)
        else:
            self.validate_input(password_length)
            self._password_prep.clear()
            self._populate_password_prep(password_length)
            self._final_password_prep()
            return self._get()
