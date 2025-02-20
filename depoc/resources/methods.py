from .base import T, APIResource


class Retrieve(APIResource[T]):
    @classmethod
    def get(cls, resource_id: str | None = None) -> T:
        url = f'{cls.endpoint}/{resource_id}' if resource_id else cls.endpoint
        response = cls.requestor.request('GET', url)
        return cls._convert_to_object(response)
