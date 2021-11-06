from dataclasses import dataclass
import datetime

@dataclass
class KayoAuthToken:
    token: str
    token_expires_in: int
    refresh_token: str
    token_created_at: datetime.datetime

    @property
    def token_expires_at(self) -> datetime.datetime:
        return self.token_created_at + datetime.timedelta(seconds=self.token_expires_in)

    @property
    def is_token_expired(self) -> bool:
        # If 30seconds until token expires, its time to refresh it
        return (datetime.datetime.now()+ datetime.timedelta(seconds=30)) > self.token_expires_at