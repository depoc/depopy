from depoc import BASE_URL
from depoc.objects.base import ObjectBase
from depoc.core.requestor import Requestor

from typing import Literal, Optional, Dict, Any

class Resource(ObjectBase):
    _requestor: Requestor

    def __init__(
            self,
            requestor: Optional[Requestor] = None,
            data: Optional[Dict[str, Any]] = None,
            id: Optional[str] = None,
        ):
        super().__init__(data)
        cls = self.__class__
        cls._requestor = requestor
        self._id = id

    @classmethod
    def class_url(cls) -> str:
        if cls == Resource:
            raise NotImplementedError(
                'Resource is an abstract class. You should perform '
                'actions on its subclasses (e.g. Customer, Products)'
            )
        return f'{BASE_URL}/{cls.OBJECT_ENDPOINT}'

    def instance_url(self) -> str:
        if not self.id:
            raise ValueError('Instance url requires an ID.')
        return f'{self.class_url()}/{self.id}'

    @classmethod
    def request(
        cls,
        method: Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> 'ObjectBase':
        data = cls._requestor.request(method, endpoint, params)[cls.OBJECT_NAME]
        post_data = {}
        
        for key, value in data.items():
            if isinstance(value, dict):
                post_data.update(value)
            else:
                post_data[key] = value

        return post_data
