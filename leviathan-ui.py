#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leviathan-UI Professional Setup v1.0.5
Instalador pulido estilo NSIS con banners, opciones avanzadas, 
y manejo robusto de instalación remota/local.
"""

import sys
import os
import subprocess
import threading
import json
import time
import locale
import socket
import ctypes
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QFrame, QCheckBox, QTextEdit,
    QProgressBar, QMessageBox, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal, QObject, QThread, QSize, QTimer, QSharedMemory, QSystemSemaphore
from PyQt6.QtGui import QFont, QColor, QPixmap, QPainter, QLinearGradient

# Importar leviathan-ui
from leviathan_ui.wipeWindow import WipeWindow
from leviathan_ui.title_bar import CustomTitleBar, get_accent_color
from leviathan_ui.progress_bar import LeviathanProgressBar

# --- Sistema de i18n simplificado ---
class I18nManager:
    def __init__(self):
        self.lang_data = {
            # Español por defecto
            "welcome_title": "Bienvenido al Instalador de Leviathan-UI",
            "welcome_subtitle": "Este asistente instalará Leviathan-UI v1.0.5 en tu sistema.",
            "welcome_desc": "Leviathan-UI es un framework premium de PyQt6 para crear aplicaciones modernas con estilo Windows 11.",
            "options_title": "Opciones de Instalación",
            "options_subtitle": "Personaliza la instalación según tus necesidades:",
            "opt_install_mode": "Modo de instalación:",
            "opt_local": "Local (desde archivos .whl en dist/)",
            "opt_remote": "Remoto (desde PyPI - requiere internet)",
            "opt_shortcuts": "Crear accesos directos:",
            "opt_desktop": "En el escritorio",
            "opt_startmenu": "En el menú de inicio",
            "opt_advanced": "Opciones avanzadas:",
            "opt_force": "Forzar reinstalación",
            "opt_upgrade": "Actualizar dependencias",
            "install_title": "Instalando Leviathan-UI",
            "install_subtitle": "Por favor espera mientras se instala el framework...",
            "install_preparing": "Preparando instalación...",
            "install_deps": "Instalando dependencias...",
            "install_package": "Instalando paquete...",
            "install_finish": "Finalizando...",
            "finish_title": "Instalación Completada",
            "finish_subtitle": "Leviathan-UI v1.0.5 se ha instalado correctamente.",
            "finish_desc": "Puedes comenzar a usar el framework inmediatamente.",
            "btn_next": "Siguiente",
            "btn_back": "Atrás",
            "btn_cancel": "Cancelar",
            "btn_install": "Instalar",
            "btn_finish": "Finalizar",
            "btn_close": "Cerrar",
            "error_title": "Error de Instalación",
            "error_no_whl": "No se encontraron archivos .whl en dist/\nSelecciona modo remoto o compila el paquete primero.",
            "error_no_internet": "No hay conexión a internet\nSelecciona modo local o verifica tu conexión.",
            "error_install": "Falló la instalación. Revisa el log para más detalles.",
            "single_instance": "El instalador ya está en ejecución.",
        }
        
    def get(self, key, default=""):
        return self.lang_data.get(key, default)

i18n = I18nManager()

# --- Señales ---
class InstallerSignals(QObject):
    log_updated = pyqtSignal(str, str)
    progress_updated = pyqtSignal(int)
    install_finished = pyqtSignal(bool, str)
    status_changed = pyqtSignal(str)

# --- Verificar conexión a internet ---
def check_internet_connection():
    try:
        socket.create_connection(("pypi.org", 443), timeout=3)
        return True
    except OSError:
        return False

# --- Prevenir múltiples instancias ---
class SingleInstanceChecker:
    def __init__(self, key="leviathan_ui_setup_105"):
        self.key = key
        self.shared_memory = QSharedMemory(key)
        self.semaphore = QSystemSemaphore(key + "_sem", 1)
        
    def is_running(self):
        if self.shared_memory.attach():
            return True
        return not self.shared_memory.create(1)
    
    def release(self):
        self.shared_memory.detach()

# --- Worker de instalación ---
class InstallWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    log = pyqtSignal(str, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, options):
        super().__init__()
        self.options = options
        self.python_exe = sys.executable
        
    def run(self):
        try:
            success = self._install()
            self.finished.emit(success, "")
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def _run_command(self, cmd, desc, progress_val):
        self.status.emit(desc)
        self.log.emit(f"> {' '.join(cmd)}", desc)
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, startupinfo=startupinfo
        )
        
        output = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                output.append(line.strip())
                self.log.emit('\n'.join(output[-5:]), desc)
        
        if process.returncode != 0:
            raise Exception(f"\n".join(output[-10:]))
        
        self.progress.emit(progress_val)
    
    def _install(self):
        # 1. Dependencias base (0-20%)
        if self.options.get('upgrade_deps', True):
            self._run_command(
                [self.python_exe, "-m", "pip", "install", "PyQt6", "Pillow", "--upgrade"],
                i18n.get("install_deps"), 20
            )
        else:
            self.progress.emit(20)
        
        # 2. Instalar leviathan-ui (20-80%)
        install_mode = self.options.get('install_mode', 'local')
        
        if install_mode == 'local':
            dist_dir = Path("dist")
            whl_files = list(dist_dir.glob("*.whl")) if dist_dir.exists() else []
            
            if not whl_files:
                raise Exception(i18n.get("error_no_whl"))
            
            for idx, whl in enumerate(whl_files):
                progress = 20 + int((idx + 1) / len(whl_files) * 60)
                force = ["--force-reinstall"] if self.options.get('force', False) else []
                self._run_command(
                    [self.python_exe, "-m", "pip", "install", str(whl)] + force,
                    f"Instalando {whl.name}...", progress
                )
        else:
            # Remoto desde PyPI
            if not check_internet_connection():
                raise Exception(i18n.get("error_no_internet"))
            
            self._run_command(
                [self.python_exe, "-m", "pip", "install", "leviathan-ui", "--upgrade"],
                i18n.get("install_package"), 80
            )
        
        # 3. Crear atajos si se solicitaron (80-95%)
        if self.options.get('desktop_shortcut', False):
            self._create_shortcut("desktop")
        if self.options.get('startmenu_shortcut', False):
            self._create_shortcut("startmenu")
        
        self.progress.emit(95)
        
        # 4. Verificación final (95-100%)
        self._run_command(
            [self.python_exe, "-c", "import leviathan_ui; print('OK')"],
            i18n.get("install_finish"), 100
        )
        
        return True
    
    def _create_shortcut(self, location):
        """Crear accesos directos de demostración"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            if location == "desktop":
                path = winshell.desktop()
            else:
                path = winshell.programs()
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(Path(path) / "Leviathan-UI Demo.lnk"))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = "-c \"from leviathan_ui import InmersiveSplash; print('Demo')\""
            shortcut.WorkingDirectory = str(Path.home())
            shortcut.IconLocation = sys.executable
            shortcut.save()
        except:
            pass  # Opcional, no crítico

# --- Páginas del instalador ---

class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Banner vertical izquierdo (splash_setup.png)
        self.banner = QLabel()
        self.banner.setFixedWidth(164)
        self.banner.setScaledContents(True)
        banner_pixmap = QPixmap("assets/splash_setup.png")
        if not banner_pixmap.isNull():
            self.banner.setPixmap(banner_pixmap)
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
        version_info = QLabel("Versión: 1.0.5 | Python 3.8+ | PyQt6 6.5+")
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

class OptionsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(25)
        
        # Título
        title = QLabel(i18n.get("options_title"))
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(title)
        
        subtitle = QLabel(i18n.get("options_subtitle"))
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #aaaaaa; background: transparent;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
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
        options_layout.setContentsMargins(25, 25, 25, 25)
        options_layout.setSpacing(20)
        
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
        
        options_layout.addSpacing(15)
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background: rgba(255,255,255,0.1); max-height: 1px;")
        options_layout.addWidget(line)
        options_layout.addSpacing(10)
        
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
        
        options_layout.addSpacing(15)
        
        # Separador
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background: rgba(255,255,255,0.1); max-height: 1px;")
        options_layout.addWidget(line2)
        options_layout.addSpacing(10)
        
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
        layout.addStretch()
    
    def on_mode_changed(self):
        sender = self.sender()
        if sender == self.radio_local and self.radio_local.isChecked():
            self.radio_remote.setChecked(False)
        elif sender == self.radio_remote and self.radio_remote.isChecked():
            self.radio_local.setChecked(False)
        
        if not self.radio_local.isChecked() and not self.radio_remote.isChecked():
            sender.setChecked(True)
    
    def check_connection(self):
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
        return {
            'install_mode': 'remote' if self.radio_remote.isChecked() else 'local',
            'desktop_shortcut': self.chk_desktop.isChecked(),
            'startmenu_shortcut': self.chk_startmenu.isChecked(),
            'force': self.chk_force.isChecked(),
            'upgrade_deps': self.chk_upgrade.isChecked(),
        }

class InstallPage(QWidget):
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
        self.worker = InstallWorker(options)
        self.worker.progress.connect(self.on_progress)
        self.worker.status.connect(self.on_status)
        self.worker.log.connect(self.on_log)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
    
    def on_progress(self, value):
        self.progress.value = value
    
    def on_status(self, text):
        self.status_label.setText(text)
    
    def on_log(self, log, desc):
        self.log_area.setText(log)
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )
    
    def on_finished(self, success, error_msg):
        if success:
            self.status_label.setText("✓ Instalación completada")
            self.status_label.setStyleSheet("color: #4CAF50; background: transparent;")
        else:
            self.status_label.setText("✗ " + i18n.get("error_title"))
            self.status_label.setStyleSheet("color: #f44336; background: transparent;")
            self.log_area.append(f"\n❌ ERROR:\n{error_msg}")

class FinishPage(QWidget):
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
            "📦 Leviathan-UI v1.0.5\n"
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

# --- Ventana principal del instalador ---
class LeviathanSetup(QWidget):
    def __init__(self):
        super().__init__()
        
        # Prevenir múltiples instancias
        self.instance_checker = SingleInstanceChecker()
        if self.instance_checker.is_running():
            QMessageBox.warning(None, "Instalador en ejecución", i18n.get("single_instance"))
            sys.exit(1)
        
        self.setWindowTitle("Leviathan-UI Setup")
        self.resize(800, 520)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Aplicar efecto visual
        WipeWindow.create().set_mode("ghostBlur").set_radius(8).apply(self)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de título
        self.title_bar = CustomTitleBar(self, title="Leviathan-UI v1.0.5 Setup", hide_max=True)
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
        if self.current_page > 0:
            self.current_page -= 1
            self.animate_page_transition(self.current_page)
            self.update_buttons()
    
    def animate_page_transition(self, index):
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
        if hasattr(self, 'instance_checker'):
            self.instance_checker.release()
        event.accept()

# --- Main ---
if __name__ == "__main__":
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
        print("Leviathan-UI Setup v1.0.5")
        sys.exit(0)
    
    window = LeviathanSetup()
    window.show()
    
    sys.exit(app.exec())
