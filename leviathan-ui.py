#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leviathan-UI Professional Setup v1.0.4
Instalador pulido estilo NSIS con banners, opciones avanzadas, 
y manejo robusto de instalación remota/local.

Las clases están separadas en el directorio class/ para mejor organización.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from installer_classes import LeviathanSetup


def main():
    """Punto de entrada principal del instalador"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Fusión oscuro
    app.setStyleSheet("""
        QToolTip {
            background: #1a1a2e;
            color: white;
            border: 1px solid #333;
            padding: 5px;
        }
    """)
    
    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("Leviathan-UI Setup v1.0.4")
        sys.exit(0)
    
    window = LeviathanSetup()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
