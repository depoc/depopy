from depoc.resources.base import Resource
    

class Retrieve(Resource):
    @classmethod
    def all(cls) -> 'Resource':
        url = cls.class_url()
        return cls.request('GET', url)
