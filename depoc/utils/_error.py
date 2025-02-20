class APIError(Exception):
    def __init__(
            self,
            message: str,
            status: int,
        ):
        super().__init__(message, status)
        self.message = message
        self.status = status
