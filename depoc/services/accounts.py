from depoc.resources.methods import Update, Delete
from depoc.objects.accounts import AccountsObject


class Accounts(Update[AccountsObject], Delete[AccountsObject]):
    obj = AccountsObject
    endpoint = 'accounts'
    label = 'user'
