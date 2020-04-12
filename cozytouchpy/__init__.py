# -*- coding:utf-8 -*-
'''
Provides authentification and row access to Cozytouch modules.
'''
name = 'cozytouchpy'
__version__ = '1.4.1'
__all__ = ["cozytouchpy"]

from .client import CozytouchClient
from .exception import CozytouchException
