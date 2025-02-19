from typing import Optional


class APIError(Exception):
    def __init__(
            self,
            message: str,
            status: Optional[int] = None,
        ):
        super().__init__(message, status)
        self.message = message
        self.status = status
