from depoc.services.user import User
from depoc.services.owner import Owner


class DepocClient:
    def __init__(self, token: str | None = None):
        self._token = token
        
        # top-level services
        self.me = User()
        self.owner = Owner()
