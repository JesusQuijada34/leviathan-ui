# -*- coding: utf-8 -*-
"""
leviathan_setup.py - Ventana principal del instalador
Mejorado con soporte multi-resolución y DPI awareness
"""

import sys
import ctypes
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QGuiApplication, QScreen

from leviathan_ui.wipeWindow import WipeWindow
from leviathan_ui.title_bar import CustomTitleBar

from installer_classes.i18n_manager import I18nManager
from installer_classes.single_instance_checker import SingleInstanceChecker
from installer_classes.welcome_page import WelcomePage
from installer_classes.options_page import OptionsPage
from installer_classes.install_page import InstallPage
from installer_classes.finish_page import FinishPage
from installer_classes.utils import check_internet_connection

i18n = I18nManager()


class LeviathanSetup(QWidget):
    """Ventana principal del instalador profesional Leviathan-UI
    
    Características:
    - Soporte multi-resolución (1080p, 1440p, 4K, ultrawide)
    - DPI awareness para pantallas de alta densidad
    - Límites inteligentes de tamaño según resolución
    """
    
    def __init__(self):
        super().__init__()
        
        # Prevenir múltiples instancias
        self.instance_checker = SingleInstanceChecker()
        if self.instance_checker.is_running():
            QMessageBox.warning(None, "Instalador en ejecución", i18n.get("single_instance"))
            sys.exit(1)
        
        self.setWindowTitle("Leviathan-UI Setup")
        
        # Enable DPI awareness on Windows
        if sys.platform == "win32":
            try:
                # DPI awareness for proper scaling on high-DPI displays
                ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware
            except:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except:
                    pass
        
        # Obtener pantalla principal y datos de DPI
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # Calcular DPI scale factor
        dpi = screen.logicalDotsPerInch()
        self.dpi_scale = dpi / 96.0  # 96 DPI is standard
        
        # Tamaño base compacto, se ajustará al contenido real
        base_width = 720
        base_height = 480

        # Ajustar ligeramente por DPI (evitar que sea muy pequeño en 4K)
        if self.dpi_scale > 1.5:  # 4K o pantallas muy densas
            base_width = 850
            base_height = 550

        # Asegurar que no exceda la pantalla disponible
        window_width = min(base_width, int(screen_width * 0.85))
        window_height = min(base_height, int(screen_height * 0.85))

        # Usar tamaño inicial pero permitir ajuste al contenido
        self.resize(window_width, window_height)
        self.setMinimumSize(600, 420)  # Tamaño mínimo absoluto
        
        # Centrar en pantalla
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.move(x, y)
        # Ventana frameless pero maximizable
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinMaxButtonsHint)
        self.setStyleSheet("background-color: #121822; border: none;")

        # Aplicar efecto visual - polished es más estable que ghostBlur
        WipeWindow.create().set_mode("polished").set_radius(8).apply(self)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Barra de título (siempre visible, no cubierta por splash)
        self.title_bar = CustomTitleBar(self, title="Leviathan-UI v1.0.5 Setup", hide_max=False)
        self.title_bar.setStyleSheet("background-color: transparent; border: none;")
        main_layout.addWidget(self.title_bar)

        # Contenedor de contenido (área donde el splash hará overlay)
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background-color: #121822; border: none;")
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Contenedor de páginas
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background-color: #121822; border: none;")

        # Crear páginas
        self.page_welcome = WelcomePage()
        self.page_options = OptionsPage()
        self.page_install = InstallPage()
        self.page_finish = FinishPage()

        self.pages.addWidget(self.page_welcome)  # 0
        self.pages.addWidget(self.page_options)   # 1
        self.pages.addWidget(self.page_install)   # 2
        self.pages.addWidget(self.page_finish)    # 3

        # Conectar señal de instalación terminada para ir a página final
        self.page_install.finished.connect(self.on_install_finished)

        content_layout.addWidget(self.pages, 1)
        main_layout.addWidget(self.content_container, 1)

        # Barra de botones (siempre visible, no cubierta por splash)
        self.button_bar = QWidget()
        self.button_bar.setFixedHeight(50)
        self.button_bar.setStyleSheet("background: rgba(0,0,0,0.2); border-top: 1px solid rgba(255,255,255,0.1);")

        btn_layout = QHBoxLayout(self.button_bar)
        btn_layout.setContentsMargins(15, 10, 15, 10)
        btn_layout.setSpacing(10)
        
        self.btn_cancel = QPushButton(i18n.get("btn_cancel"))
        self.btn_cancel.setFixedSize(75, 28)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #aaaaaa;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.1); color: white; }
        """)
        self.btn_cancel.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_cancel)
        
        btn_layout.addStretch()

        # Indicador de página (dots)
        self.page_indicator = QWidget()
        self.page_indicator.setFixedWidth(80)
        indicator_layout = QHBoxLayout(self.page_indicator)
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        indicator_layout.setSpacing(6)
        indicator_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.page_dots = []
        for i in range(4):
            dot = QLabel("●")
            dot.setFont(QFont("Segoe UI", 8))
            dot.setStyleSheet("color: #555555; background: transparent;")
            self.page_dots.append(dot)
            indicator_layout.addWidget(dot)

        btn_layout.addWidget(self.page_indicator)
        btn_layout.addStretch()

        self.btn_back = QPushButton(i18n.get("btn_back"))
        self.btn_back.setFixedSize(75, 28)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.1); }
            QPushButton:disabled { color: #666666; border-color: #333333; }
        """)
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setEnabled(False)
        btn_layout.addWidget(self.btn_back)
        
        self.btn_next = QPushButton(i18n.get("btn_next"))
        self.btn_next.setFixedSize(90, 28)
        self.btn_next.setStyleSheet("""
            QPushButton {
                background: #ff5722;
                color: white;
                border: none;
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background: #ff7043; }
            QPushButton:disabled { background: #333333; color: #666666; }
        """)
        self.btn_next.clicked.connect(self.go_next)
        btn_layout.addWidget(self.btn_next)
        
        main_layout.addWidget(self.button_bar)
        
        self.current_page = 0
        self.update_buttons()
    
    def update_buttons(self):
        """Actualiza el estado de los botones según la página actual"""
        self.btn_back.setEnabled(self.current_page > 0 and self.current_page < 3)

        # Actualizar indicador de página (dots)
        for i, dot in enumerate(self.page_dots):
            if i == self.current_page:
                dot.setStyleSheet("color: #ff5722; background: transparent;")  # Activo: naranja
            else:
                dot.setStyleSheet("color: #555555; background: transparent;")  # Inactivo: gris

        if self.current_page == 0:
            self.btn_next.setText(i18n.get("btn_next"))
        elif self.current_page == 1:
            self.btn_next.setText(i18n.get("btn_install"))
        elif self.current_page == 2:
            self.btn_next.setEnabled(False)
            self.btn_cancel.setEnabled(False)
        elif self.current_page == 3:
            self.btn_next.setText(i18n.get("btn_finish"))
            self.btn_next.setEnabled(True)
            self.btn_cancel.setText(i18n.get("btn_close"))
    
    def go_next(self):
        """Navega a la siguiente página o finaliza"""
        if self.current_page == 3:
            self.close()
            return
        
        if self.current_page == 1:
            # Ir a instalación
            options = self.page_options.get_options()
            
            # Validaciones
            if options['install_mode'] == 'local':
                if not list(Path("dist").glob("*.whl")):
                    QMessageBox.warning(self, "Error", i18n.get("error_no_whl"))
                    return
            else:
                if not check_internet_connection():
                    QMessageBox.warning(self, "Error", i18n.get("error_no_internet"))
                    return
            
            self.current_page = 2
            self.animate_page_transition(2)
            self.update_buttons()
            self.page_install.start_installation(options)
            return
        
        self.current_page += 1
        self.animate_page_transition(self.current_page)
        self.update_buttons()
    
    def go_back(self):
        """Vuelve a la página anterior"""
        if self.current_page > 0:
            self.current_page -= 1
            self.animate_page_transition(self.current_page)
            self.update_buttons()
    
    def animate_page_transition(self, index):
        """Transición simple entre páginas"""
        self.pages.setCurrentIndex(index)

    def on_install_finished(self, success, error_msg):
        """Maneja cuando la instalación termina - cambia a página final"""
        self.current_page = 3
        self.animate_page_transition(3)
        self.update_buttons()

    def closeEvent(self, event):
        """Libera recursos al cerrar"""
        if hasattr(self, 'instance_checker'):
            self.instance_checker.release()
        event.accept()
