# -*- coding: utf-8 -*-
"""
options_page.py - Página de opciones de instalación
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from installer_classes.i18n_manager import I18nManager
from installer_classes.utils import check_internet_connection

i18n = I18nManager()


class OptionsPage(QWidget):
    """Página de opciones con checkboxes para personalizar la instalación"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #121822; border: none;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        # Título
        title = QLabel(i18n.get("options_title"))
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(title)

        subtitle = QLabel(i18n.get("options_subtitle"))
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #aaaaaa; background: transparent;")
        layout.addWidget(subtitle)

        # Frame de opciones
        options_frame = QFrame()
        options_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.03);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(15, 15, 15, 15)
        options_layout.setSpacing(12)
        
        # Modo de instalación
        mode_label = QLabel(i18n.get("opt_install_mode"))
        mode_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        mode_label.setStyleSheet("color: #ff5722; background: transparent;")
        options_layout.addWidget(mode_label)
        
        self.radio_local = QCheckBox(i18n.get("opt_local"))
        self.radio_local.setChecked(True)
        self.radio_local.setFont(QFont("Segoe UI", 11))
        self.radio_local.setStyleSheet("""
            QCheckBox { color: white; spacing: 10px; }
            QCheckBox::indicator { width: 20px; height: 20px; border-radius: 10px; border: 2px solid #666; }
            QCheckBox::indicator:checked { background: #ff5722; border-color: #ff5722; }
        """)
        self.radio_local.toggled.connect(self.on_mode_changed)
        options_layout.addWidget(self.radio_local)
        
        self.radio_remote = QCheckBox(i18n.get("opt_remote"))
        self.radio_remote.setFont(QFont("Segoe UI", 11))
        self.radio_remote.setStyleSheet("""
            QCheckBox { color: white; spacing: 10px; }
            QCheckBox::indicator { width: 20px; height: 20px; border-radius: 10px; border: 2px solid #666; }
            QCheckBox::indicator:checked { background: #0078d4; border-color: #0078d4; }
        """)
        self.radio_remote.toggled.connect(self.on_mode_changed)
        options_layout.addWidget(self.radio_remote)
        
        # Estado de conexión
        self.connection_status = QLabel("Verificando conexión...")
        self.connection_status.setFont(QFont("Segoe UI", 10))
        self.connection_status.setStyleSheet("color: #888888; background: transparent; padding-left: 30px;")
        options_layout.addWidget(self.connection_status)
        
        QTimer.singleShot(100, self.check_connection)
        
        # Separador compacto
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background: rgba(255,255,255,0.1); max-height: 1px;")
        options_layout.addWidget(line)
        
        # Accesos directos
        shortcuts_label = QLabel(i18n.get("opt_shortcuts"))
        shortcuts_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        shortcuts_label.setStyleSheet("color: #ff5722; background: transparent;")
        options_layout.addWidget(shortcuts_label)
        
        self.chk_desktop = QCheckBox(i18n.get("opt_desktop"))
        self.chk_desktop.setChecked(False)
        self.chk_desktop.setFont(QFont("Segoe UI", 11))
        self.chk_desktop.setStyleSheet("""
            QCheckBox { color: #cccccc; spacing: 8px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 3px; border: 2px solid #666; }
            QCheckBox::indicator:checked { background: #4CAF50; border-color: #4CAF50; }
        """)
        options_layout.addWidget(self.chk_desktop)
        
        self.chk_startmenu = QCheckBox(i18n.get("opt_startmenu"))
        self.chk_startmenu.setChecked(True)
        self.chk_startmenu.setFont(QFont("Segoe UI", 11))
        self.chk_startmenu.setStyleSheet("""
            QCheckBox { color: #cccccc; spacing: 8px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 3px; border: 2px solid #666; }
            QCheckBox::indicator:checked { background: #4CAF50; border-color: #4CAF50; }
        """)
        options_layout.addWidget(self.chk_startmenu)

        # Separador compacto
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background: rgba(255,255,255,0.1); max-height: 1px;")
        options_layout.addWidget(line2)

        # Opciones avanzadas
        adv_label = QLabel(i18n.get("opt_advanced"))
        adv_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        adv_label.setStyleSheet("color: #ff5722; background: transparent;")
        options_layout.addWidget(adv_label)
        
        self.chk_force = QCheckBox(i18n.get("opt_force"))
        self.chk_force.setFont(QFont("Segoe UI", 11))
        self.chk_force.setStyleSheet("""
            QCheckBox { color: #cccccc; spacing: 8px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 3px; border: 2px solid #666; }
            QCheckBox::indicator:checked { background: #ff9800; border-color: #ff9800; }
        """)
        options_layout.addWidget(self.chk_force)
        
        self.chk_upgrade = QCheckBox(i18n.get("opt_upgrade"))
        self.chk_upgrade.setChecked(True)
        self.chk_upgrade.setFont(QFont("Segoe UI", 11))
        self.chk_upgrade.setStyleSheet("""
            QCheckBox { color: #cccccc; spacing: 8px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 3px; border: 2px solid #666; }
            QCheckBox::indicator:checked { background: #ff9800; border-color: #ff9800; }
        """)
        options_layout.addWidget(self.chk_upgrade)

        layout.addWidget(options_frame)
    
    def on_mode_changed(self):
        """Gestiona el cambio de modo de instalación"""
        sender = self.sender()
        if sender == self.radio_local and self.radio_local.isChecked():
            self.radio_remote.setChecked(False)
        elif sender == self.radio_remote and self.radio_remote.isChecked():
            self.radio_local.setChecked(False)
        
        if not self.radio_local.isChecked() and not self.radio_remote.isChecked():
            sender.setChecked(True)
    
    def check_connection(self):
        """Verifica la conexión a internet y actualiza UI"""
        if check_internet_connection():
            self.connection_status.setText("✓ Conexión a internet disponible")
            self.connection_status.setStyleSheet("color: #4CAF50; background: transparent; padding-left: 30px;")
        else:
            self.connection_status.setText("✗ No hay conexión a internet - Modo remoto no disponible")
            self.connection_status.setStyleSheet("color: #f44336; background: transparent; padding-left: 30px;")
            if self.radio_remote.isChecked():
                self.radio_local.setChecked(True)
                self.radio_remote.setEnabled(False)
    
    def get_options(self):
        """Retorna las opciones seleccionadas como diccionario"""
        return {
            'install_mode': 'remote' if self.radio_remote.isChecked() else 'local',
            'desktop_shortcut': self.chk_desktop.isChecked(),
            'startmenu_shortcut': self.chk_startmenu.isChecked(),
            'force': self.chk_force.isChecked(),
            'upgrade_deps': self.chk_upgrade.isChecked(),
        }
