class UserDoesNotExist(Exception):
    """
    Raises when user not found
    """
    pass


class NotValidCredentials(Exception):
    """
    Raises when passed not valid password
    """
    pass


class UsernameIsTaken(Exception):
    """
    Raises when user is trying to register with busy username
    """
    pass


class TokenExpired(Exception):
    """
    Raises when jwt token is expired
    """
    pass
