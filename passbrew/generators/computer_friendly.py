import secrets

from passbrew.generators.base_generator import BasePasswordGenerator
from passbrew.validation import validate_length


class ComputerFriendlyPasswordGenerator(BasePasswordGenerator):
    """
    Refactor this later.
    """

    def get(self, length: int) -> str:
        if validate_length(length, self.min_length, self.max_length):
            return secrets.token_urlsafe(length)
