from typing import Generic, TypeVar, Type

from depoc.core.requestor import Requestor
from depoc.objects.base import DepocObject

T = TypeVar('T', bound=DepocObject)


class APIResource(Generic[T]):
    requestor: 'Requestor' = Requestor()
    endpoint: str
    obj: Type[T]
    label: str

    @classmethod
    def _convert_to_object(cls, data) -> T:
        if not cls.obj:
            raise ValueError('obj class not defined for this resource')
        return cls.obj(data.get(cls.label))
