from requests import request, Response

from depoc import BASE_URL


class Connection:
    def __init__(
            self,
            username: str,
            password: str,
    ):
        self.username = username
        self.password = password
        self.access_token = self.get_access_token(self.username, self.password)
    
    def get_access_token(self, username: str, password: str):
        method = 'POST'
        url: str = BASE_URL + '/token'
        login: dict[str, str] = {'username': username, 'password': password}
        response: Response = request(method, url, data=login)
        
        data: dict[str, str] = response.json()

        if response.status_code == 200:
            access_token = data.get('access', '')
            return access_token

        return data
