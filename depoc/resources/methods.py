from typing import Optional, Dict, Any

from depoc.resources.base import Resource


class List(Resource):
    @classmethod
    def all(cls) -> Dict[str, Any]:
        url = cls.class_url()
        return cls.request('GET', url)


class Retrieve(Resource):
    @classmethod
    def get(cls, resource_id: Optional[str] = None) -> Dict[str, Any]:
        if resource_id:
            url = f'{cls.class_url()}/{resource_id}'
        else:
            url = cls.class_url()

        return cls.request('GET', url)


class Update(Resource):
    @classmethod
    def update(
        cls,
        resource_id: Optional[str] = None,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        url = cls.class_url()
        return cls.request('PATCH', url, params=params)
