from __future__ import division
import time


class Token:
    EXPIRE_BUFFER = 30  # mark access token as expired if the ttl is less than 10s
    access_token: str = ""
    refresh_token: str = ""
    id_token: str = ""
    expires_in: int = 0
    expires_at: int = 0

    def __init__(self, access_token: str, refresh_token: str = None, id_token: str = None, expires_in: int = None,
                 expires_at: int = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_in = expires_in
        self.expires_at = expires_at

    def is_expired(self) -> bool:
        now = time.time()
        if now > self.expires_at - self.EXPIRE_BUFFER:
            return True
        return False

    def renew_expires_at_from_now(self):
        self.expires_at = int(time.time()) + self.expires_in
