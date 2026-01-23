
import sys
import os
import time
import subprocess
import threading
import json
import locale
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QStackedWidget, QFrame, 
                             QCheckBox, QTextEdit, QScrollArea)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtSvg import QSvgWidget

from leviathan_ui.wipeWindow import WipeWindow
from leviathan_ui.title_bar import CustomTitleBar, get_accent_color
from leviathan_ui.dialogs import LeviathanDialog
from leviathan_ui.progress_bar import LeviathanProgressBar
from leviathan_ui.splash import InmersiveSplash

# --- Sistema de i18n ---
class I18nManager:
    def __init__(self):
        self.lang_data = {}
        self.load_language()

    def load_language(self):
        try:
            # 1. Detectar idioma del SO
            try:
                # Intentar getdefaultlocale() primero (mejor para Windows)
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", DeprecationWarning)
                    lang_tuple = locale.getdefaultlocale()
                default_locale = lang_tuple[0] if lang_tuple and lang_tuple[0] else None
                
                # Fallback a getlocale() si getdefaultlocale() falla
                if not default_locale:
                    lang_tuple = locale.getlocale()
                    default_locale = lang_tuple[0] if lang_tuple[0] else "en_US"
            except:
                default_locale = "en_US"

            
            lang_code = default_locale.replace("_", "-")
            lang_path = os.path.join("lang", f"{lang_code}.lv-lng")

            # 2. Intento de carga del idioma detectado
            if not os.path.exists(lang_path):
                # Fallback parcial: si no existe es-AR, intentar con cualquier 'es'
                prefix = lang_code.split("-")[0]
                available_langs = [f for f in os.listdir("lang") if f.startswith(prefix) and f.endswith(".lv-lng")]
                if available_langs:
                    lang_path = os.path.join("lang", available_langs[0])

            # 3. MÁXIMO FALLBACK: Si sigue sin existir, usar English (en-US) por defecto
            if not os.path.exists(lang_path):
                lang_path = os.path.join("lang", "en-US.lv-lng")

            # 4. Carga final
            if os.path.exists(lang_path):
                with open(lang_path, "r", encoding="utf-8") as f:
                    self.lang_data = json.load(f)
            else:
                # Caso extremo: ni el fallback existe
                print("Critical Error: No language pack or fallback found.")
                sys.exit(1)
        except Exception as e:
            print(f"I18n Error: {e}")
            sys.exit(1)


    def get(self, key, default=""):
        return self.lang_data.get(key, default)

i18n = I18nManager()

# --- Señales ---
class InstallerSignals(QObject):
    log_updated = pyqtSignal(str, str)
    progress_updated = pyqtSignal(int)
    install_finished = pyqtSignal()
    announcements_loaded = pyqtSignal(str)

# --- Páginas del Instalador ---
class PageBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 10, 50, 20)
        self.layout.setSpacing(10)
        
        # Aplicar fuente Segoe UI (Windows 11 style)
        self.setFont(QFont("Segoe UI", 10))

    def add_svg_icon(self, svg_path):
        if os.path.exists(svg_path):
            svg_widget = QSvgWidget(svg_path)
            svg_widget.setFixedSize(80, 80)
            self.layout.addWidget(svg_widget, alignment=Qt.AlignCenter)
            return svg_widget
        return None

class WelcomePage(PageBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.add_svg_icon("assets/info.svg")
        
        title = QLabel(i18n.get("welcome_title"))
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        desc = QLabel(i18n.get("welcome_desc"))
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 11))
        desc.setStyleSheet("color: #dddddd; background: transparent; line-height: 1.4;")
        
        origin = QLabel(i18n.get("welcome_origin"))
        origin.setWordWrap(True)
        origin.setFont(QFont("Segoe UI", 10))
        origin.setStyleSheet("color: #aaaaaa; background: rgba(255,255,255,0.06); padding: 15px; border-radius: 10px;")
        
        self.layout.addWidget(title, alignment=Qt.AlignCenter)
        self.layout.addSpacing(5)
        self.layout.addWidget(desc, alignment=Qt.AlignCenter)
        self.layout.addSpacing(15)
        self.layout.addWidget(origin)
        self.layout.addStretch()

class LicensePage(PageBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        title = QLabel(i18n.get("license_title"))
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        desc = QLabel(i18n.get("license_desc"))
        desc.setFont(QFont("Segoe UI", 10))
        desc.setStyleSheet("color: #cccccc; background: transparent;")
        
        # Área de texto con scroll para la licencia
        self.license_text = QTextEdit()
        self.license_text.setReadOnly(True)
        self.license_text.setFont(QFont("Consolas", 9))
        self.license_text.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.4);
                color: #e0e0e0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 10px;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        
        # Cargar licencia desde archivo
        try:
            with open("LICENSE", "r", encoding="utf-8") as f:
                license_content = f.read()
            self.license_text.setPlainText(license_content)
        except:
            self.license_text.setPlainText("MIT License\n\nCopyright (c) 2026 Jesus Quijada\n\n[License file not found]")
        
        # Checkbox de aceptación
        self.accept_checkbox = QCheckBox(i18n.get("license_accept"))
        self.accept_checkbox.setFont(QFont("Segoe UI", 10))
        self.accept_checkbox.setFocusPolicy(Qt.NoFocus)
        self.accept_checkbox.setCursor(Qt.PointingHandCursor)
        self.accept_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                background: rgba(0, 0, 0, 0.3);
            }
            QCheckBox::indicator:checked {
                background: #0078d4;
                border-color: #0078d4;
            }
        """)
        
        self.layout.addWidget(title)
        self.layout.addWidget(desc)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.license_text)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.accept_checkbox)
        self.layout.addStretch()

class ComponentsPage(PageBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        title = QLabel(i18n.get("comp_title"))
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        comp_frame = QFrame()
        comp_frame.setStyleSheet("background: rgba(255,255,255,0.03); border-radius: 12px; padding: 10px;")
        comp_lay = QVBoxLayout(comp_frame)
        
        # Lista simplificada de componentes
        comps = ["💠 WipeWindow", "🚥 CustomTitleBar", "✨ InmojiTrx", "📊 LeviathanProgressBar"]
        for c in comps:
            lbl = QLabel(c)
            lbl.setFont(QFont("Segoe UI", 11))
            lbl.setStyleSheet("color: #bbbbbb; margin-bottom: 2px;")
            comp_lay.addWidget(lbl)
            
        self.layout.addWidget(title)
        self.layout.addWidget(comp_frame)
        self.layout.addStretch()

class AnnouncementsPage(PageBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Sección de anuncios
        announcements_title = QLabel(i18n.get("announcements_title"))
        announcements_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        announcements_title.setStyleSheet("color: white; background: transparent;")
        
        self.announcements_label = QLabel(i18n.get("announcements_loading"))
        self.announcements_label.setWordWrap(True)
        self.announcements_label.setFont(QFont("Segoe UI", 11))
        self.announcements_label.setStyleSheet("""
            color: #eeeeee; 
            background: rgba(0, 120, 212, 0.15); 
            padding: 20px; 
            border-radius: 12px;
            border-left: 4px solid #0078d4;
        """)
        self.announcements_label.setMinimumHeight(200)
            
        self.layout.addWidget(announcements_title, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.announcements_label)
        self.layout.addStretch()
    
    def update_announcements(self, text):
        self.announcements_label.setText(text)

class InstallPage(PageBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.add_svg_icon("assets/install.svg")
        
        title = QLabel(i18n.get("install_title"))
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        self.log_area = QLabel(i18n.get("install_preparing"))
        self.log_area.setWordWrap(True)
        self.log_area.setFont(QFont("Consolas", 10))
        self.log_area.setStyleSheet("color: #00ff00; background: #0c0c0c; padding: 15px; border-radius: 8px;")
        self.log_area.setMinimumHeight(120)
        
        self.explanation = QLabel(i18n.get("install_explanation"))
        self.explanation.setWordWrap(True)
        self.explanation.setFont(QFont("Segoe UI", 10))
        self.explanation.setStyleSheet("color: #999999; font-style: italic; background: transparent;")
        
        self.layout.addWidget(title)
        self.layout.addWidget(self.log_area)
        self.layout.addWidget(self.explanation)
        self.layout.addStretch()

    def update_log(self, log, explanation):
        self.log_area.setText(log)
        self.explanation.setText(f"<b>{i18n.get('btn_next')}...</b> {explanation}")

class FinalPage(PageBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.add_svg_icon("assets/finished.svg")
        
        title = QLabel(i18n.get("finish_title"))
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        msg = QLabel(i18n.get("finish_desc"))
        msg.setFont(QFont("Segoe UI", 12))
        msg.setStyleSheet("color: #cccccc; background: transparent;")
        
        tip = QLabel(i18n.get("finish_tip"))
        tip.setFont(QFont("Segoe UI", 10))
        tip.setStyleSheet("color: #aaaaaa; background: rgba(46, 204, 113, 0.1); padding: 10px; border-radius: 8px;")
        
        self.layout.addStretch()
        self.layout.addWidget(title, alignment=Qt.AlignCenter)
        self.layout.addWidget(msg, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(tip, alignment=Qt.AlignCenter)
        self.layout.addStretch()

# --- Ventana Principal del Instalador ---
class LeviathanInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(720, 540)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        
        # 1. Efecto GhostBlur (v1.0.3 estándar)
        WipeWindow.create().set_mode("ghostBlur").set_blur(40).set_radius(22).apply(self)
        self._accent = get_accent_color()
        
        # 2. UI
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self, title=f"Leviathan UI v1.0.3 Setup", icon="app/app-icon.ico", hide_max=True)
        self.title_bar.setStyleSheet("background: transparent;")
        self.root_layout.addWidget(self.title_bar)
        
        self.page_container = QStackedWidget()
        self.root_layout.addWidget(self.page_container)
        
        self.signals = InstallerSignals()
        
        self.pages = [WelcomePage(), LicensePage(), ComponentsPage(), AnnouncementsPage(), InstallPage(), FinalPage()]
        for p in self.pages:
            self.page_container.addWidget(p)
            
        # Bottom Bar
        self.bottom_bar = QWidget()
        self.bottom_bar.setFixedHeight(90)
        self.bottom_layout = QVBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(50, 0, 50, 10)
        
        self.progress_bar = LeviathanProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.value = 0
        self.progress_bar.setFixedHeight(6)
        
        # Inicialmente ocultar la barra de progreso
        self.progress_bar.setVisible(False)
        
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.progress_bar)
        
        btn_layout = QHBoxLayout()
        self.btn_next = QPushButton(i18n.get("btn_begin"))
        self.btn_next.setFixedSize(150, 36)
        self.btn_next.setFocusPolicy(Qt.NoFocus)
        self.btn_next.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.btn_next.setCursor(Qt.PointingHandCursor)
        self.apply_btn_style()
        self.btn_next.clicked.connect(self.handle_next)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_next)
        self.bottom_layout.addLayout(btn_layout)

        
        self.root_layout.addWidget(self.bottom_bar)
        self._current_step = 0
        
        self.signals.log_updated.connect(self.pages[4].update_log)
        self.signals.progress_updated.connect(self.update_progress)
        self.signals.install_finished.connect(self.on_install_completed)
        self.signals.announcements_loaded.connect(self.pages[3].update_announcements)
        
        # Cargar anuncios en segundo plano
        threading.Thread(target=self.load_announcements, daemon=True).start()

    def apply_btn_style(self, enabled=True):
        color = self._accent if enabled else "#555555"
        self.btn_next.setStyleSheet(f"""
            QPushButton {{
                background: {color}; 
                color: white; 
                border-radius: 6px; 
                border: none;
            }}
            QPushButton:hover {{
                background: {self.lighten_color(color, 1.1)};
            }}
            QPushButton:pressed {{
                background: {self.lighten_color(color, 0.9)};
            }}
        """)
        self.btn_next.setEnabled(enabled)
    
    def lighten_color(self, hex_color, factor):
        """Aclara u oscurece un color hexadecimal"""
        try:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color

    def show_confirmation_dialog(self, title, message):
        """Muestra un diálogo de confirmación usando LeviathanDialog"""
        self.dialog_result = None
        
        def on_response(btn_text):
            self.dialog_result = btn_text
        
        LeviathanDialog.launch(
            parent=self,
            title=title,
            message=message,
            mode="warning",
            buttons=[i18n.get("btn_no"), i18n.get("btn_yes")],
            callback=on_response
        )
        
        # Esperar a que el usuario responda
        while self.dialog_result is None:
            QApplication.processEvents()
            time.sleep(0.01)
        
        return self.dialog_result == i18n.get("btn_yes")
    
    def show_warning_dialog(self, title, message):
        """Muestra un diálogo de advertencia"""
        LeviathanDialog.launch(
            parent=self,
            title=title,
            message=message,
            mode="warning",
            buttons=[i18n.get("btn_accept")]
        )

    def handle_next(self):
        if self._current_step == 0:
            # Welcome -> License
            self._current_step += 1
            self.animate_page(self._current_step)
            self.btn_next.setText(i18n.get("btn_next"))
            self.show_progress_bar_animated()
            
        elif self._current_step == 1:
            # License -> Components (validar aceptación)
            if not self.pages[1].accept_checkbox.isChecked():
                self.show_warning_dialog(i18n.get("license_title"), i18n.get("license_required"))
                return
            
            self._current_step += 1
            self.animate_page(self._current_step)
            self.update_progress(40)
            
        elif self._current_step == 2:
            # Components -> Announcements
            self._current_step += 1
            self.animate_page(self._current_step)
            self.update_progress(60)

        elif self._current_step == 3:
            # Announcements -> Install (confirmar)
            if self.show_confirmation_dialog(
                i18n.get("install_confirm_title"), 
                i18n.get("install_confirm_desc")
            ):
                self._current_step += 1
                self.animate_page(self._current_step)
                self.apply_btn_style(False)
                self.btn_next.setText(i18n.get("btn_installing"))
                self.set_progress_marquee(True)
                threading.Thread(target=self.run_install_sync, daemon=True).start()
            
        elif self._current_step == 4:
            # Install -> Finish (automático, no debería llegar aquí)
            pass
            
        elif self._current_step == 5:
            # Finish -> Close
            self.close()

    def show_progress_bar_animated(self):
        """Muestra la barra de progreso con animación slide-up"""
        self.progress_bar.setVisible(True)
        self.progress_bar.value = 20
        
        # Animación de deslizamiento desde abajo
        self.progress_anim = QPropertyAnimation(self.progress_bar, b"geometry")
        self.progress_anim.setDuration(400)
        
        start_geo = self.progress_bar.geometry()
        start_geo.moveTop(start_geo.top() + 30)
        end_geo = self.progress_bar.geometry()
        
        self.progress_anim.setStartValue(start_geo)
        self.progress_anim.setEndValue(end_geo)
        self.progress_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.progress_anim.start()

    def update_progress(self, value):
        """Actualiza el valor de la barra de progreso"""
        self.progress_bar.value = value

    def set_progress_marquee(self, enabled):
        """Activa/desactiva el modo marquee de la barra de progreso"""
        if enabled:
            # Usar el método nativo de LeviathanProgressBar
            self.progress_bar.setMarquee(True)
        else:
            # Modo normal
            self.progress_bar.setMarquee(False)
            self.progress_bar.setRange(0, 100)

    def animate_page(self, index):
        new_page = self.page_container.widget(index)
        self.page_container.setCurrentIndex(index)
        self.anim = QPropertyAnimation(new_page, b"pos")
        self.anim.setDuration(550)
        self.anim.setStartValue(QPoint(self.width(), 0))
        self.anim.setEndValue(QPoint(0, 0))
        self.anim.setEasingCurve(QEasingCurve.OutQuart)
        self.anim.start()

    def on_install_completed(self):
        self.set_progress_marquee(False)
        self.progress_bar.value = 100
        self.apply_btn_style(True)
        self.btn_next.setText(i18n.get("btn_finish"))
        self._current_step = 5
        self.animate_page(self._current_step)

    def load_announcements(self):
        """Carga anuncios desde una API (simulado)"""
        try:
            # Simular carga de anuncios (puedes cambiar esto por una API real)
            time.sleep(2)
            
            # Ejemplo: Intentar cargar desde GitHub releases o similar
            # url = "https://api.github.com/repos/usuario/leviathan-ui/releases/latest"
            # response = requests.get(url, timeout=5)
            # if response.status_code == 200:
            #     data = response.json()
            #     announcement = f"🎉 Nueva versión disponible: {data['tag_name']}\n{data['body'][:100]}..."
            # else:
            #     raise Exception("API no disponible")
            
            # Por ahora, mensaje estático
            announcement = "🚀 Leviathan UI v1.0.3 está aquí!\n\n✨ Nuevas características:\n• Soporte mejorado para Windows 11\n• Animaciones más fluidas\n• Mejor rendimiento"
            
            self.signals.announcements_loaded.emit(announcement)
        except Exception as e:
            self.signals.announcements_loaded.emit(i18n.get("announcements_error"))

    def _run_command(self, cmd_args, description, progress_target):
        self.signals.log_updated.emit(f"> Executing: {' '.join(cmd_args)}", description)
        
        # Windows: Hide console window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        process = subprocess.Popen(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            startupinfo=startupinfo
        )
        
        output_accum = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                clean_line = line.strip()
                if clean_line:
                    output_accum.append(clean_line)
                    # Emit last few lines to keep UI responsive but not flooded
                    display_log = "\n".join(output_accum[-8:]) 
                    self.signals.log_updated.emit(display_log, description)
        
        if process.returncode != 0:
            full_log = "\n".join(output_accum)
            raise Exception(f"Process failed (Exit Code {process.returncode}):\n{full_log}")
            
        self.signals.progress_updated.emit(progress_target)

    def run_install_sync(self):
        try:
            python_exe = sys.executable
            
            # 1. Base Dependencies
            self._run_command(
                [python_exe, "-m", "pip", "install", "PyQt5", "Pillow", "--upgrade"],
                i18n.get("install_preparing") + " (PyQt5, Pillow)",
                30
            )
            
            # 2. Local Distributions
            dist_dir = "dist"
            if os.path.exists(dist_dir) and os.listdir(dist_dir):
                whl_files = [f for f in os.listdir(dist_dir) if f.endswith(".whl")]
                if whl_files:
                    for idx, whl in enumerate(whl_files):
                        progress = 30 + int((idx + 1) / len(whl_files) * 40) # Up to 70%
                        whl_path = os.path.join(dist_dir, whl)
                        self._run_command(
                            [python_exe, "-m", "pip", "install", whl_path, "--force-reinstall"],
                            f"Installing local package: {whl}",
                            progress
                        )
                else:
                    self.signals.log_updated.emit("No .whl files found in dist/. Skipping local install.", "Checking local dist")
                    self.signals.progress_updated.emit(70)
            else:
                 # Fallback: Try installing leviathan-ui from PyPI if no local dist
                self._run_command(
                    [python_exe, "-m", "pip", "install", "leviathan-ui", "--upgrade"],
                    "Installing Leviathan UI from PyPI (Online Mode)",
                    70
                )

            # 3. Final Configuration
            time.sleep(1) # Grace period
            self.signals.progress_updated.emit(100)
            self.signals.log_updated.emit("All tasks finished successfully.\nDevice ready.", "Finalization")
            self.signals.install_finished.emit()
            
        except Exception as e:
            error_msg = f"❌ INSTALLATION FAILED:\n{str(e)}"
            self.signals.log_updated.emit(error_msg, "CRITICAL ERROR")
            # Set progress to 0 to indicate failure visually (red bar logic could be added)
            self.signals.progress_updated.emit(0)



if __name__ == "__main__":
    # Módulo 2: Splash Screen UWP al iniciar SETUP
    app = QApplication(sys.argv)
    
    # Crear carpeta app e icono si no existen para que el splash no falle
    if not os.path.exists("app"): os.makedirs("app")
    icon_p = "app/app-icon.ico"
    if not os.path.exists(icon_p): # Generar dummy si no está
        with open(icon_p, "wb") as f: f.write(b"") 

    # Configurar splash con color del sistema y duración de 3 segundos
    splash = InmersiveSplash(splash_type="UWP", logo=os.path.abspath(icon_p), color="auto")
    
    def start_installer():
        window = LeviathanInstaller()
        window.show()

    splash.on_finish(start_installer)
    splash.launch()
    
    sys.exit(app.exec_())
