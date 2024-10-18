class UserDoesNotExist(Exception):
    pass


class NotValidCredentials(Exception):
    pass


class UsernameIsTaken(Exception):
    pass


class TokenExpired(Exception):
    pass


class BarcodeAlreadyExistExc(Exception):
    ...
