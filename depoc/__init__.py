from depoc.core.requestor import Requestor
from depoc.core.client import DepocClient
from depoc.core.auth import Connection

from depoc.services.user import User
from depoc.services.owner import Owner
from depoc.services.account import Account
from depoc.services.business import Business
from depoc.services.customer import Customer


token: str | None = None

# Constants
BASE_URL: str = 'http://127.0.0.1:8000'
