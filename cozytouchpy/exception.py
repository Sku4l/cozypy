class CozytouchException(Exception):
    pass


class AuthentificationFailed(CozytouchException):
    pass


class HttpRequestFailed(CozytouchException):
    pass
