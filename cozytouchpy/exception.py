"""Class for exception."""


class CozytouchException(Exception):
    """Default exception."""

    pass


class AuthentificationFailed(CozytouchException):
    """Authentification failed."""

    pass


class HttpRequestFailed(CozytouchException):
    """Http requestion failed."""

    pass
