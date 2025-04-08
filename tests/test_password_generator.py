import pytest

from passbrew.exceptions import ValidationError
from passbrew.generators.base_generator import BasePasswordGenerator
from passbrew.generators.user_friendly import UserFriendlyPasswordGenerator


@pytest.fixture
def generator():
    return BasePasswordGenerator()


@pytest.fixture
def friendly_password():
    return UserFriendlyPasswordGenerator()


class TestSetMinLength:
    def test_set_min_length_valid_int(self, generator):
        generator.set_min_length(20)
        assert generator.min_length == 20

    def test_set_min_length_invalid_int(self, generator):
        with pytest.raises(ValidationError):
            generator.set_min_length(-1)

    def test_set_min_length_str(self, generator):
        with pytest.raises(ValidationError):
            generator.set_min_length("str")

    def test_set_min_length_float(self, generator):
        with pytest.raises(ValidationError):
            generator.set_min_length(20.0)

    def test_set_min_length_exceeds_max_length(self, generator):
        with pytest.raises(ValidationError):
            generator.set_min_length(100)


class TestSetMaxLength:
    def test_set_max_length_valid_int(self, generator):
        generator.set_max_length(30)
        assert generator.max_length == 30

    def test_set_max_length_invalid_int(self, generator):
        with pytest.raises(ValidationError):
            generator.set_max_length(20)

    def test_set_max_length_negative_int(self, generator):
        with pytest.raises(ValidationError):
            generator.set_max_length(-1)

    def test_set_max_length_str(self, generator):
        with pytest.raises(ValidationError):
            generator.set_max_length("str")

    def test_set_max_length_float(self, generator):
        with pytest.raises(ValidationError):
            generator.set_max_length(20.0)

    def test_set_max_length_exceeds_max_length(self, generator):
        with pytest.raises(ValidationError):
            generator.set_max_length(1)
