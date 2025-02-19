from depoc.objects.base import DepocObject
from depoc.resources.methods import Retrieve, Update


class Owner(Retrieve, Update):
    """ This object represents the owner of the business """

    OBJECT_NAME: str = 'owner'
    OBJECT_ENDPOINT: str = 'owner'

    id: str
    ''' Unique identifier of the owner. '''
    name: str
    ''' Full name of the owner. '''
    email: str
    ''' Owner's email address. '''
    phone: str
    ''' Owner's phone number '''
    
    @classmethod
    def get(cls, resource_id = None) -> DepocObject:
        data = super().get(resource_id)
        return Owner(data=data.get(cls.OBJECT_NAME))

    @classmethod
    def update(cls, resource_id = None, params = None) -> DepocObject:
        data = super().update(resource_id, params)
        return Owner(data=data)
