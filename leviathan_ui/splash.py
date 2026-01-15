import sys
import os
import random
import difflib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush

# Importamos el capturador de acento desde la librería hermana
from .title_bar import get_accent_color

class InmersiveSplash(QWidget):
    """
    🌊 InmersiveSplash: Ciclo de vida completo del Bot.
    Modos: 
    - adaptive: Ocupa toda la pantalla respetando la barra de tareas.
    - full: Ocupa absolutamente toda la pantalla (Kiosk).
    """
    def __init__(self, title="Sincronizando...", logo="🐉", color="auto", is_exit=False):
        super().__init__()
        self.is_exit = is_exit
        self._title = title
        self._logo = logo
        self._color_cfg = color
        self._mode = "adaptive"
        self._phrases = []
        self._callback = None
        
        # Flags de ventana
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_mode(self, mode):
        """'adaptive' o 'full'."""
        self._mode = mode
        return self

    def set_phrases(self, phrases):
        """Lista de strings que se mostrarán durante la carga."""
        self._phrases = phrases
        return self

    def on_finish(self, callback):
        self._callback = callback
        return self

    def launch(self):
        # 1. Ajuste de Pantalla
        desktop = QDesktopWidget()
        if self._mode == "adaptive":
            geom = desktop.availableGeometry() # Respeta Taskbar
        else:
            geom = desktop.screenGeometry() # Full Kiosk
            
        self.setGeometry(geom)
        
        # 2. Color de Fondo
        self._final_color = get_accent_color() if self._color_cfg == "auto" else self._color_cfg
        
        # 3. UI
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        
        self.logo_lbl = QLabel(self._logo)
        self.logo_lbl.setFont(QFont("Segoe UI Variable Display", 120))
        self.logo_lbl.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.logo_lbl, alignment=Qt.AlignCenter)
        
        self.pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        self.pbar.setFixedWidth(int(self.width() * 0.4))
        self.pbar.setFixedHeight(6)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet("QProgressBar { background: rgba(0,0,0,0.1); border-radius: 3px; } QProgressBar::chunk { background: white; border-radius: 3px; }")
        layout.addWidget(self.pbar, alignment=Qt.AlignCenter)
        
        self.status_lbl = QLabel(self._title)
        self.status_lbl.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 18px; font-weight: 600; background: transparent;")
        layout.addWidget(self.status_lbl, alignment=Qt.AlignCenter)
        
        # 4. Animación de Entrada
        self.setWindowOpacity(0)
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(800)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()
        
        # 5. Lógica de Pasos
        self._current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_progress)
        self.timer.start(800) 
        
        self.show()
        return self

    def _update_progress(self):
        if not self._phrases:
            self._phrases = ["Analizando datos...", "Sincronizando...", "Preparando interfaz..."]
            
        if self._current_step < len(self._phrases):
            msg = self._phrases[self._current_step]
            prog = int(((self._current_step + 1) / len(self._phrases)) * 100)
            self.status_lbl.setText(msg)
            self.pbar.setValue(prog)
            self._current_step += 1
        else:
            self.timer.stop()
            QTimer.singleShot(600, self._close_splash)

    def _close_splash(self):
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(600)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self._finalize)
        self.fade_out.start()

    def _finalize(self):
        self.close()
        if self.is_exit:
            QApplication.instance().quit()
        elif self._callback:
            self._callback()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor(self._final_color))

    def attach_to_window(self, window, exit_phrases=None):
        """Registra el splash de salida automáticamente."""
        QApplication.instance().setQuitOnLastWindowClosed(False)
        phrases = exit_phrases or ["Cerrando sesiones...", "Guardando logs...", "Leviathan fuera."]
        
        def on_close(event):
            InmersiveSplash(title="Saliendo...", logo=self._logo, color=self._color_cfg, is_exit=True)\
                .set_mode(self._mode)\
                .set_phrases(phrases)\
                .launch()
            event.accept()
            
        window.closeEvent = on_close
        return self

    def start(self): return self.launch()
    @staticmethod
    def create(): return InmersiveSplash()
