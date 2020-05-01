# -*- coding:utf-8 -*-
"""Provides authentification and row access to Cozytouch modules."""
name = "cozytouchpy"
__version__ = "1.6.1"

from .client import CozytouchClient
from .exception import CozytouchException, AuthentificationFailed, HttpRequestFailed
