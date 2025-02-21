from depoc.core.requestor import Requestor
from depoc.core.client import DepocClient
from depoc.core.auth import Connection

from depoc.services.user import User
from depoc.services.owner import Owner
from depoc.services.accounts import Accounts


token: str | None = None

# Constants
BASE_URL: str = 'https://api.depoc.com.br'
