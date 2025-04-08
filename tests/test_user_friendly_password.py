import pytest

from passbrew.exceptions import ValidationError
from passbrew.generators.user_friendly import UserFriendlyPasswordGenerator


@pytest.fixture
def friendly_password():
    return UserFriendlyPasswordGenerator()


class TestSetCharAmount:
    def test_set_char_amount_valid(self, friendly_password):
        friendly_password.set_char_amount(2)
        assert friendly_password.char_amount == 2

    def test_set_char_amount_0(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.set_char_amount(0)

    def test_set_char_amount_too_many(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.set_char_amount(100)


class TestSetNumAmount:
    def test_set_num_amount_valid(self, friendly_password):
        friendly_password.set_num_amount(2)
        assert friendly_password.num_amount == 2

    def test_set_num_amount_0(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.set_num_amount(0)

    def test_set_num_amount_too_many(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.set_num_amount(100)


class TestSetSpaceAmount:
    def test_set_empty_space_amount_valid(self, friendly_password):
        friendly_password.set_empty_space_amount(2)
        assert friendly_password.empty_space_amount == 2

    def test_set_empty_space_amount_0(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.set_empty_space_amount(0)

    def test_set_empty_space_amount_too_many(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.set_empty_space_amount(100)


class TestGetExtraCharsAmount:
    def test_extra_chars_amount_valid(self, friendly_password):
        friendly_password.get_extra_chars_amnt(2, 2, 2)
        assert friendly_password.get_extra_chars_amnt() == 6

    def test_extra_chars_amount_too_many_chars(self, friendly_password):
        with pytest.raises(ValueError):
            friendly_password.get_extra_chars_amnt(char_amount=50, password_length=40)

    def test_extra_chars_amount_too_many_everything(self, friendly_password):
        with pytest.raises(ValueError):
            friendly_password.get_extra_chars_amnt(
                char_amount=50,
                num_amount=50,
                empty_space_amount=50,
            )


def test_effective_password_length(friendly_password):
    friendly_password.set_char_amount(1)
    friendly_password.set_num_amount(1)
    friendly_password.set_empty_space_amount(1)
    assert friendly_password._get_effective_password_length(20) == 17


class TestPickRandomWord:
    def test_pick_random_word_valid_length(self, friendly_password):
        word = friendly_password._pick_a_random_word(5)
        assert len(word) <= 5

    def test_pick_random_word_invalid_length(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password._pick_a_random_word(0)

    def test_pick_random_word_length_is_str(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password._pick_a_random_word("str")


class TestGenerate:
    def test_generate_valid_input(self, friendly_password):
        pwd = friendly_password.generate(20)
        assert len(pwd) == 20

    def test_generate_less_than_min_length(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.generate(2)

    def test_generate_greater_than_max_length(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.generate(100)

    def test_generate_with_a_string(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.generate("str")

    def test_generate_negative_num(self, friendly_password):
        with pytest.raises(ValidationError):
            friendly_password.generate(-1)

    def test_generate_large_num_of_passwords(self, friendly_password):
        passwords = []
        for _ in range(50):
            pwd = friendly_password.generate(20)
            passwords.append(pwd)
        assert len(passwords) == 50
