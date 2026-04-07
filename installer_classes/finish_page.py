# -*- coding: utf-8 -*-
"""
finish_page.py - Página final de instalación completada
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from installer_classes.i18n_manager import I18nManager

i18n = I18nManager()


class FinishPage(QWidget):
    """Página final mostrando éxito de la instalación"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Icono de éxito
        icon = QLabel("✓")
        icon.setFont(QFont("Segoe UI", 72))
        icon.setStyleSheet("color: #4CAF50; background: transparent;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)
        
        # Título
        title = QLabel(i18n.get("finish_title"))
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel(i18n.get("finish_subtitle"))
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #aaaaaa; background: transparent;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Info de lo instalado
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: rgba(76, 175, 80, 0.1);
                border: 1px solid rgba(76, 175, 80, 0.3);
                border-radius: 12px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        info_text = QLabel(
            "📦 Leviathan-UI v1.0.4\n"
            "🐍 Python Package\n"
            "✅ Instalación verificada"
        )
        info_text.setFont(QFont("Consolas", 11))
        info_text.setStyleSheet("color: #4CAF50; background: transparent; padding: 20px;")
        info_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        layout.addStretch()
        
        # Mensaje final
        desc = QLabel(i18n.get("finish_desc"))
        desc.setFont(QFont("Segoe UI", 11))
        desc.setStyleSheet("color: #cccccc; background: transparent;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
