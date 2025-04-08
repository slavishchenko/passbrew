import secrets

from passbrew.generators.base_generator import BasePasswordGenerator
from passbrew.validators import validate_length


class ComputerFriendlyPassword(BasePasswordGenerator):
    """
    Refactor this later.
    """

    def get(self, length: int) -> str:
        if validate_length(length, self.min_length, self.max_length):
            return secrets.token_urlsafe(length)
