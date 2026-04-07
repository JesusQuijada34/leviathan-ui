# -*- coding: utf-8 -*-
"""
welcome_page.py - Página de bienvenida del instalador
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from installer_classes.i18n_manager import I18nManager

i18n = I18nManager()


class WelcomePage(QWidget):
    """Página inicial con banner vertical y mensaje de bienvenida"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Banner vertical izquierdo (splash_setup.png) - recortado y centrado
        self.banner = QLabel()
        self.banner.setFixedWidth(164)
        self.banner.setFixedHeight(520)  # Altura fija para match con ventana
        self.banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_pixmap = QPixmap("assets/splash_setup.png")
        if not banner_pixmap.isNull():
            # Escalar manteniendo aspect ratio, luego centrar
            scaled = banner_pixmap.scaled(164, 520, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.banner.setPixmap(scaled)
            self.banner.setStyleSheet("background: transparent;")
        else:
            # Fallback: gradiente
            self.banner.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1a1a2e, stop:1 #16213e);
            """)
        
        layout.addWidget(self.banner)
        
        # Contenido derecho
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)
        
        # Logo o icono
        logo = QLabel("🐉")
        logo.setStyleSheet("font-size: 64px; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_layout.addWidget(logo)
        
        # Título
        title = QLabel(i18n.get("welcome_title"))
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        title.setWordWrap(True)
        content_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel(i18n.get("welcome_subtitle"))
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #aaaaaa; background: transparent;")
        subtitle.setWordWrap(True)
        content_layout.addWidget(subtitle)
        
        # Descripción
        desc = QLabel(i18n.get("welcome_desc"))
        desc.setFont(QFont("Segoe UI", 11))
        desc.setStyleSheet("color: #cccccc; background: transparent; line-height: 1.5;")
        desc.setWordWrap(True)
        content_layout.addWidget(desc)
        
        # Info de versión
        version_info = QLabel("Versión: 1.0.4 | Python 3.8+ | PyQt6 6.5+")
        version_info.setFont(QFont("Segoe UI", 10))
        version_info.setStyleSheet("color: #666666; background: transparent;")
        content_layout.addWidget(version_info)
        
        content_layout.addStretch()
        
        # Requisitos
        reqs = QLabel("✓ Requiere conexión a internet para modo remoto\n✓ Python 3.8 o superior\n✓ Windows 10/11 recomendado")
        reqs.setFont(QFont("Segoe UI", 10))
        reqs.setStyleSheet("color: #888888; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;")
        content_layout.addWidget(reqs)
        
        layout.addWidget(content, 1)
