import pytest

from passbrew.errors import ValidationError
from passbrew.utils import filter_list


@pytest.fixture
def lst():
    return ["cat", "dog", "lion"]


class TestFilterList:
    def test_filter_list(self, lst):
        filtered = filter_list(lst, 4)
        assert len(filtered) == 3

    def test_filter_list_invalid_length(self, lst):
        assert len(filter_list(lst, 2)) == 0

    def test_filter_list_invalid_list(
        self,
    ):
        with pytest.raises(TypeError, match="Input should be a list of string"):
            filter_list([1, 2, 3], 3)

    def test_filter_list_max_length_str(self, lst):
        with pytest.raises(ValidationError, match="Invalid input type"):
            filter_list(lst, "one")

    def test_filter_list_max_length_negative(self, lst):
        with pytest.raises(
            ValidationError,
            match="The input must be a positive number. Please provide a valid positive number.",
        ):
            filter_list(lst, -1)
