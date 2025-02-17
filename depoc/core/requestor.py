import requests

from typing import Any, Dict, Optional, Union, Literal


class Requestor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}

    def request(
        self,
        method: Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], None]:
        try:
            response = requests.request(
                method,
                endpoint,
                json=params,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'API request failed: {e}')
            return None
