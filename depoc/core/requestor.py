import requests

from depoc.utils._error import APIError

from typing import Any, Dict, Optional, Literal


class Requestor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}

    def request(
        self,
        method: Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        response = requests.request(
            method,
            endpoint,
            json=params,
            headers=self.headers
        )

        if response.status_code == 404:
            raise APIError('Not found', 404)

        data = response.json()

        if 'error' in data:
            message = data.get('error').get('message')
            status = data.get('error').get('status')
            raise APIError(message, status)
        
        response.raise_for_status()
    
        return data
