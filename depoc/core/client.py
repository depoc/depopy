from depoc.core.requestor import Requestor
from depoc.objects.user import User
from depoc.objects.owner import Owner


class DepocClient(object):
    def __init__(
        self,
        api_key: str,
    ):
        self.requestor = Requestor(api_key)

        self.me = User(self.requestor)
        self.owner = Owner(self.requestor)
