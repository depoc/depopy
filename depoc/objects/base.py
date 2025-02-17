import json

from typing import Optional, Dict, Any


class ObjectBase:
    OBJECT_NAME: str
    OBJECT_ENDPOINT: str

    def __init__(
            self,
            data: Optional[Dict[str, Any]] = None,
        ):
        self._data = data or {}
        self._modified_fields = set()

    def __setattr__(self, k: str, v: Any) -> None:        
        if k.startswith("_"):
            super().__setattr__(k, v)
        else:
            self._data[k] = v
            self._modified_fields.add(k)

    def __getattr__(self, k: str) -> Any:
        if k in self._data:
            return self._data[k]
        raise AttributeError(f"{k} not found in DepocObject.")
    
    def __delattr__(self, k: str) -> Any:
        if k[0] == '_' or k in self.__dict__:
            return super().__delattr__(k)
        else:
            del self[k]

    def __repr__(self) -> str:
        return f"DepocObject({json.dumps(self._data, indent=2)})"

    def to_dict(self) -> Dict[str, Any]:
        return self._data.copy()

    def to_json(self) -> str:
        return json.dumps(self._data, indent=2)

    def get_modified_fields(self) -> Dict[str, Any]:
        return {k: self._data[k] for k in self._modified_fields}
