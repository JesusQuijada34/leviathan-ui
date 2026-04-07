# -*- coding: utf-8 -*-
"""
utils.py - Funciones utilitarias del instalador
"""

import socket


def check_internet_connection():
    """Verifica si hay conexión a internet probando conexión a PyPI"""
    try:
        socket.create_connection(("pypi.org", 443), timeout=3)
        return True
    except OSError:
        return False
