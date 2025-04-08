import pytest

from passbrew.exceptions import ExceedsMaximumLength, ValidationError
from passbrew.generators.passphrase import PassphraseGenerator


@pytest.fixture
def passphrase():
    return PassphraseGenerator()


def test_passphrase_set_min_word_count_valid(passphrase):
    passphrase.set_min_word_count(5)
    assert passphrase.min_word_count == 5


def test_passphrase_set_min_word_count_greater_than_max(passphrase):
    with pytest.raises(ExceedsMaximumLength):
        passphrase.set_min_word_count(13)


def test_passphrase_set_max_word_count_valid(passphrase):
    passphrase.set_max_word_count(15)
    assert passphrase.max_word_count == 15


def test_passphrase_set_max_word_count_less_than_min(passphrase):
    with pytest.raises(ValidationError):
        passphrase.set_max_word_count(3)


class TestGenerateUseWordCount:
    def test_passphrase_generate_valid_word_count(self, passphrase):
        pwd = passphrase.generate(5)
        assert len(pwd.split()) == 5

    def test_passphrase_generate_less_than_min_count(self, passphrase):
        with pytest.raises(ValidationError):
            passphrase.generate(2)

    def test_passphrase_generate_more_than_max_count(self, passphrase):
        with pytest.raises(ValidationError):
            passphrase.generate(100)


class TestGenerateUseChars:
    def test_passphrase_generate_valid(self, passphrase):
        pwd = passphrase.generate(20, use_word_count=False)
        assert len(pwd) == 20

    def test_pasphrase_generate_with_string(self, passphrase):
        with pytest.raises(ValidationError):
            passphrase.generate("str", use_word_count=False)

    def test_pasphrase_generate_with_negative_number(self, passphrase):
        with pytest.raises(ValidationError):
            passphrase.generate(-1, use_word_count=False)

    def test_pasphrase_generate_with_0(self, passphrase):
        with pytest.raises(ValidationError):
            passphrase.generate(0, use_word_count=False)

    def test_generate_less_than_min_length(self, passphrase):
        with pytest.raises(ValidationError):
            passphrase.generate(2, use_word_count=False)

    def test_generate_greater_than_max_length(self, passphrase):
        with pytest.raises(ValidationError):
            passphrase.generate(100, use_word_count=False)

    def test_generate_large_num_of_passwords(self, passphrase):
        passwords = []
        for _ in range(50):
            pwd = passphrase.generate(20, use_word_count=False)
            passwords.append(pwd)
        assert len(passwords) == 50
        for p in passwords:
            assert len(p) == 20
