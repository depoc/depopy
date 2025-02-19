from depoc.objects.base import DepocObject
from depoc.resources.methods import Retrieve


class User(Retrieve):
    ''' This object represents the current authenticated user '''
    
    OBJECT_NAME: str = 'user'
    OBJECT_ENDPOINT: str = 'me'

    id: str
    ''' Unique identifier of the user. '''
    name: str
    ''' Full name of the user. '''
    email: str
    ''' User's email address. '''
    username: str
    ''' Unique username of the user. '''
    is_active: bool
    ''' Indicates whether the user account is active. '''
    is_staff: bool
    ''' Indicates whether the user has staff privileges. '''
    is_superuser: bool
    ''' Indicates whether the user has superuser privileges. '''
    last_login: str
    ''' Timestamp of the user's last login. '''
    date_joined: str
    ''' Timestamp of when the user registered in Depoc. '''

    @classmethod
    def get(cls, resource_id = None) -> DepocObject:
        data = super().get(resource_id)
        return User(data=data.get(cls.OBJECT_NAME))
