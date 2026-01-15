import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from leviathan_ui import (
    InmersiveSplash, 
    InmojiTrx, 
    WipeWindow, 
    CustomTitleBar
)

class MiAppPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(900, 550)
        
        # 1. WipeWindow: Polished Mode (Rounded glass with shadow)
        WipeWindow.create()\
            .set_mode("ghostBlur")\
            .set_background("auto")\
            .set_radius(10)\
            .apply(self)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 2. CustomTitleBar: Windows 11 Style (Botones SVG e integración de acento)
        self.title_bar = CustomTitleBar(self, title="LEVIATHAN ENGINE V2.0")
        layout.addWidget(self.title_bar)
        
        
        content = QWidget()
        content_lay = QVBoxLayout(content)
        content_lay.setAlignment(Qt.AlignCenter)
        
        label = QLabel("Test de Leviathan-UI: ghostBlur Mode")
        label.setStyleSheet("color: white; font-size: 24px; font-weight: bold; font-family: 'Segoe UI';")
        content_lay.addWidget(label, alignment=Qt.AlignCenter)
        
        self.btn = QPushButton("Cerrar app")
        self.btn.setFixedSize(280, 50)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.08);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """)
        content_lay.addWidget(self.btn, alignment=Qt.AlignCenter)
        layout.addWidget(content, 1)

        self.btn.clicked.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 3. InmojiTrx: Icono Premium
    InmojiTrx("🐉").apply(app)
    
    # 4. Definimos el Splash de Entrada (Modo Adaptive: no tapa el taskbar)
    # Soporta frases personalizadas de inicio
    mi_app = MiAppPrincipal()
    
    splash = InmersiveSplash(title="Iniciando...", logo="🐉", color="auto")\
        .set_mode("adaptive")\
        .set_phrases([
            "Verificando integridad del núcleo...",
            "Sincronizando con base de datos...",
            "Leviathan Engine listo para ejecución."
        ])\
        .on_finish(mi_app.show)\
        .attach_to_window(mi_app, exit_phrases=[
            "Desconectando nodos del sistema...",
            "Vaciando buffer de memoria...",
            "Protocolo de salida completado."
        ])
    
    # ¡Despegue!
    splash.start()
    
    sys.exit(app.exec_())
