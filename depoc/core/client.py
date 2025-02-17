from depoc.core.requestor import Requestor
from depoc.objects.user import User


class DepocClient(object):
    def __init__(
        self,
        api_key: str,
    ):
        self.requestor = Requestor(api_key)

        # top-level services
        self.user = User(self.requestor)
