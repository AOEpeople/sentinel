from sentinel.config.config_repository import ConfigRepository
from sentinel.oidc.token import Token


class TokenRepository:
    backend = None

    def __init__(self):
        self.backend = ConfigRepository()

    def set(self, token: "Token"):
        self.backend.set(token)

    def get(self) -> "Token":
        return self.backend.get(Token)

    def exists(self) -> bool:
        return self.backend.exists(Token)
