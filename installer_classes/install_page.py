# -*- coding: utf-8 -*-
"""
install_page.py - Página de progreso de instalación
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtGui import QFont, QPixmap

from leviathan_ui.progress_bar import LeviathanProgressBar
from installer_classes.i18n_manager import I18nManager
from installer_classes.install_worker import InstallWorker

i18n = I18nManager()


class InstallPage(QWidget):
    """Página de instalación con progreso y log de salida"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.worker = None
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Banner superior (splash.png)
        self.banner = QLabel()
        self.banner.setFixedHeight(120)
        self.banner.setScaledContents(True)
        banner_pixmap = QPixmap("assets/splash.png")
        if not banner_pixmap.isNull():
            self.banner.setPixmap(banner_pixmap)
        else:
            self.banner.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1a1a2e, stop:1 #16213e);
            """)
        layout.addWidget(self.banner)
        
        # Contenido
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(50, 30, 50, 30)
        content_layout.setSpacing(20)
        
        # Título
        title = QLabel(i18n.get("install_title"))
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        content_layout.addWidget(title)
        
        subtitle = QLabel(i18n.get("install_subtitle"))
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #aaaaaa; background: transparent;")
        content_layout.addWidget(subtitle)
        
        content_layout.addSpacing(20)
        
        # Barra de progreso
        self.progress = LeviathanProgressBar()
        self.progress.setFixedHeight(8)
        content_layout.addWidget(self.progress)
        
        # Label de estado
        self.status_label = QLabel(i18n.get("install_preparing"))
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet("color: #ff5722; background: transparent;")
        content_layout.addWidget(self.status_label)
        
        content_layout.addSpacing(15)
        
        # Área de log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFont(QFont("Consolas", 9))
        self.log_area.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.5);
                color: #00ff00;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        self.log_area.setFixedHeight(200)
        content_layout.addWidget(self.log_area)
        
        layout.addWidget(content, 1)
    
    def start_installation(self, options):
        """Inicia el worker de instalación con las opciones seleccionadas"""
        self.worker = InstallWorker(options)
        self.worker.progress.connect(self.on_progress)
        self.worker.status.connect(self.on_status)
        self.worker.log.connect(self.on_log)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
    
    def on_progress(self, value):
        """Actualiza la barra de progreso"""
        self.progress.value = value
    
    def on_status(self, text):
        """Actualiza el texto de estado"""
        self.status_label.setText(text)
    
    def on_log(self, log, desc):
        """Actualiza el área de log"""
        self.log_area.setText(log)
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )
    
    def on_finished(self, success, error_msg):
        """Maneja la finalización de la instalación"""
        if success:
            self.status_label.setText("✓ Instalación completada")
            self.status_label.setStyleSheet("color: #4CAF50; background: transparent;")
        else:
            self.status_label.setText("✗ " + i18n.get("error_title"))
            self.status_label.setStyleSheet("color: #f44336; background: transparent;")
            self.log_area.append(f"\n❌ ERROR:\n{error_msg}")
