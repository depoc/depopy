from depoc.resources.methods import Retrieve
from depoc.objects.owner import OwnerObject


class Owner(Retrieve[OwnerObject]):
    obj = OwnerObject
    endpoint = 'owner'
    label = 'owner'
