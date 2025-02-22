from typing import Any

from .base import T, APIResource


class Create(APIResource[T]):
    @classmethod
    def create(cls, params: dict[str, Any]) -> T:
        response = cls.requestor.request('POST', cls.endpoint, params)
        return cls._convert_to_object(response)


class Retrieve(APIResource[T]):
    @classmethod
    def get(cls, resource_id: str | None = None) -> T:
        endpoint = f'{cls.endpoint}/{resource_id}' if resource_id else cls.endpoint
        response = cls.requestor.request('GET', endpoint)
        return cls._convert_to_object(response)
    
    @classmethod
    def all(cls, *, limit: int | None = None, page: int | None = None) -> T:
        endpoint = f'{cls.endpoint}?page={page}' if page else cls.endpoint
        response = cls.requestor.request('GET', endpoint)
        return cls._paginate(response, limit)


class Update(APIResource[T]):
    @classmethod
    def update(cls, params: dict[str, Any], resource_id: str | None = None) -> T:
        endpoint = f'{cls.endpoint}/{resource_id}' if resource_id else cls.endpoint
        response = cls.requestor.request('PATCH', endpoint, params)
        return cls._convert_to_object(response)


class Delete(APIResource[T]):
    @classmethod
    def delete(cls, resource_id: str | None = None) -> T:
        endpoint = f'{cls.endpoint}/{resource_id}' if resource_id else cls.endpoint
        response = cls.requestor.request('DELETE', endpoint)
        return cls._convert_to_object(response)
