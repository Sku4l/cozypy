"""Class for exception."""


class CozytouchException(Exception):
    """Default exception."""


class AuthentificationFailed(CozytouchException):
    """Authentification failed."""


class HttpRequestFailed(CozytouchException):
    """Http requestion failed."""
