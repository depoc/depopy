from depoc.resources.methods import Retrieve


class User(Retrieve):
    """ This object represents the authenticated user of your business """
    
    OBJECT_NAME: str = 'user'
    OBJECT_ENDPOINT: str = 'me'

    id: str
    name: str
    email: str
    username: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    last_login: str
    date_joined: str

    @classmethod
    def all(cls):
        data = super().all()
        return User(data=data)
