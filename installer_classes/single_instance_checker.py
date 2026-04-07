# -*- coding: utf-8 -*-
"""
single_instance_checker.py - Prevención de múltiples instancias del instalador
"""

from PyQt6.QtCore import QSharedMemory, QSystemSemaphore


class SingleInstanceChecker:
    """Verifica que solo haya una instancia del instalador en ejecución"""
    
    def __init__(self, key="leviathan_ui_setup_105"):
        self.key = key
        self.shared_memory = QSharedMemory(key)
        self.semaphore = QSystemSemaphore(key + "_sem", 1)
        
    def is_running(self):
        """Retorna True si ya hay una instancia en ejecución"""
        if self.shared_memory.attach():
            return True
        return not self.shared_memory.create(1)
    
    def release(self):
        """Libera los recursos de memoria compartida"""
        self.shared_memory.detach()
