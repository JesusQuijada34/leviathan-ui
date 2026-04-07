# -*- coding: utf-8 -*-
"""
leviathan_setup.py - Ventana principal del instalador
"""

import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QGuiApplication

from leviathan_ui.wipeWindow import WipeWindow
from leviathan_ui.title_bar import CustomTitleBar

from installer_classes.i18n_manager import I18nManager
from installer_classes.single_instance_checker import SingleInstanceChecker
from installer_classes.welcome_page import WelcomePage
from installer_classes.options_page import OptionsPage
from installer_classes.install_page import InstallPage
from installer_classes.finish_page import FinishPage
from installer_classes.utils import check_internet_connection
from pathlib import Path

i18n = I18nManager()


class LeviathanSetup(QWidget):
    """Ventana principal del instalador profesional Leviathan-UI"""
    
    def __init__(self):
        super().__init__()
        
        # Prevenir múltiples instancias
        self.instance_checker = SingleInstanceChecker()
        if self.instance_checker.is_running():
            QMessageBox.warning(None, "Instalador en ejecución", i18n.get("single_instance"))
            sys.exit(1)
        
        self.setWindowTitle("Leviathan-UI Setup")
        
        # Calcular tamaño basado en resolución de pantalla -50px=x, -30px=y
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # Aplicar offset y asegurar tamaño mínimo razonable
        window_width = max(screen_width - 50, 800)
        window_height = max(screen_height - 30, 520)
        
        self.resize(window_width, window_height)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Aplicar efecto visual
        WipeWindow.create().set_mode("ghostBlur").set_radius(8).apply(self)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de título
        self.title_bar = CustomTitleBar(self, title="Leviathan-UI v1.0.4 Setup", hide_max=True)
        self.title_bar.setStyleSheet("background-color: transparent; border: none;")
        main_layout.addWidget(self.title_bar)
        
        # Contenedor de páginas
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background: transparent;")
        
        # Crear páginas
        self.page_welcome = WelcomePage()
        self.page_options = OptionsPage()
        self.page_install = InstallPage()
        self.page_finish = FinishPage()
        
        self.pages.addWidget(self.page_welcome)  # 0
        self.pages.addWidget(self.page_options)   # 1
        self.pages.addWidget(self.page_install)   # 2
        self.pages.addWidget(self.page_finish)    # 3
        
        main_layout.addWidget(self.pages, 1)
        
        # Barra de botones
        self.button_bar = QWidget()
        self.button_bar.setFixedHeight(70)
        self.button_bar.setStyleSheet("background: rgba(0,0,0,0.2); border-top: 1px solid rgba(255,255,255,0.1);")
        
        btn_layout = QHBoxLayout(self.button_bar)
        btn_layout.setContentsMargins(20, 15, 20, 15)
        btn_layout.setSpacing(15)
        
        self.btn_cancel = QPushButton(i18n.get("btn_cancel"))
        self.btn_cancel.setFixedSize(100, 38)
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
        
        self.btn_back = QPushButton(i18n.get("btn_back"))
        self.btn_back.setFixedSize(100, 38)
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
        self.btn_next.setFixedSize(120, 38)
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
        """Animación de transición entre páginas"""
        current_widget = self.pages.currentWidget()
        
        anim = QPropertyAnimation(current_widget, b"pos")
        anim.setDuration(300)
        anim.setStartValue(QPoint(0, 0))
        anim.setEndValue(QPoint(-50, 0))
        anim.setEasingCurve(QEasingCurve.OutQuad)
        
        def on_finished():
            self.pages.setCurrentIndex(index)
            new_widget = self.pages.currentWidget()
            new_widget.move(50, 0)
            
            anim2 = QPropertyAnimation(new_widget, b"pos")
            anim2.setDuration(300)
            anim2.setStartValue(QPoint(50, 0))
            anim2.setEndValue(QPoint(0, 0))
            anim2.setEasingCurve(QEasingCurve.OutQuad)
            anim2.start()
        
        anim.finished.connect(on_finished)
        anim.start()
    
    def closeEvent(self, event):
        """Libera recursos al cerrar"""
        if hasattr(self, 'instance_checker'):
            self.instance_checker.release()
        event.accept()
