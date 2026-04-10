# -*- coding: utf-8 -*-
"""
welcome_page.py - Página de bienvenida del instalador
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
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
        self.setStyleSheet("background-color: #121822; border: none;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Banner vertical izquierdo (splash_setup.png) - tamaño fijo proporcional
        self.banner = QLabel()
        self.banner.setFixedWidth(140)
        self.banner.setFixedHeight(340)  # Altura fija proporcional al contenido
        self.banner.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self._banner_pixmap = QPixmap("assets/splash_setup.png")
        if not self._banner_pixmap.isNull():
            self._update_banner_pixmap()
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
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)
        
        # Logo o icono
        logo = QLabel("🐉")
        logo.setStyleSheet("font-size: 48px; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_layout.addWidget(logo)

        # Título
        title = QLabel(i18n.get("welcome_title"))
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        title.setWordWrap(True)
        content_layout.addWidget(title)

        # Subtítulo
        subtitle = QLabel(i18n.get("welcome_subtitle"))
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #aaaaaa; background: transparent;")
        subtitle.setWordWrap(True)
        content_layout.addWidget(subtitle)

        # Descripción
        desc = QLabel(i18n.get("welcome_desc"))
        desc.setFont(QFont("Segoe UI", 10))
        desc.setStyleSheet("color: #cccccc; background: transparent; line-height: 1.4;")
        desc.setWordWrap(True)
        content_layout.addWidget(desc)
        
        # Info de versión
        version_info = QLabel("Versión: 1.0.5 | Python 3.8+ | PyQt6 6.5+")
        version_info.setFont(QFont("Segoe UI", 10))
        version_info.setStyleSheet("color: #666666; background: transparent;")
        content_layout.addWidget(version_info)

        # Requisitos (sin stretch antes, para que la ventana se ajuste al contenido)
        reqs = QLabel("✓ Requiere conexión a internet para modo remoto\n✓ Python 3.8 o superior\n✓ Windows 10/11 recomendado")
        reqs.setFont(QFont("Segoe UI", 10))
        reqs.setStyleSheet("color: #888888; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px;")
        content_layout.addWidget(reqs)

        layout.addWidget(content, 1)

    def _update_banner_pixmap(self):
        """Escala el pixmap al tamaño fijo del banner"""
        if self._banner_pixmap.isNull():
            return
        scaled = self._banner_pixmap.scaled(
            140, 340,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.banner.setPixmap(scaled)
