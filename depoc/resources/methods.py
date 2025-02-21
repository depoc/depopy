from typing import Any

from .base import T, APIResource


class Create(APIResource[T]):
    @classmethod
    def create(cls, params: dict[str, Any]) -> T:
        url = cls.endpoint
        response = cls.requestor.request('POST', url, params)
        return cls._convert_to_object(response)


class Retrieve(APIResource[T]):
    @classmethod
    def get(cls, resource_id: str | None = None) -> T:
        url = f'{cls.endpoint}/{resource_id}' if resource_id else cls.endpoint
        response = cls.requestor.request('GET', url)
        return cls._convert_to_object(response)


class Update(APIResource[T]):
    @classmethod
    def update(
        cls,
        params: dict[str, Any],
        resource_id: str | None = None,
    ) -> T:
        url = f'{cls.endpoint}/{resource_id}' if resource_id else cls.endpoint
        response = cls.requestor.request('PATCH', url, params)
        return cls._convert_to_object(response)


class Delete(APIResource[T]):
    @classmethod
    def delete(cls, resource_id: str | None = None) -> T:
        url = f'{cls.endpoint}/{resource_id}' if resource_id else cls.endpoint
        response = cls.requestor.request('DELETE', url)
        return cls._convert_to_object(response)
