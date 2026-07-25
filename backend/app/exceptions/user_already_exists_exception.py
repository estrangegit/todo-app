class UserAlreadyExistsException(Exception):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists")