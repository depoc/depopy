from depoc import BASE_URL
from depoc.objects.base import DepocObject
from depoc.core.requestor import Requestor

from typing import Literal, Optional, Dict, Any


class Resource(DepocObject):
    _requestor: Requestor

    def __init__(
            self,
            requestor: Optional[Requestor] = None,
            data: Optional[Dict[str, Any]] = None,
        ):
        super().__init__(data)
        cls = self.__class__
        cls._requestor = requestor

    @classmethod
    def class_url(cls) -> str:
        if cls == Resource:
            raise NotImplementedError(
                'Resource is an abstract class. You should perform '
                'actions on its subclasses (e.g. Customer, Products)'
            )
        return f'{BASE_URL}/{cls.OBJECT_ENDPOINT}'

    @classmethod
    def request(
        cls,
        method: Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return cls._requestor.request(method, endpoint, params)
