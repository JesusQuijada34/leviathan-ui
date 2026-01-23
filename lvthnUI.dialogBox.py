import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from leviathan_ui import WipeWindow, CustomTitleBar, LeviathanDialog, InmojiTrx

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leviathan UI - Dialog Test")
        self.resize(1000, 600)
        
        # Estilo de ventana con Blur
        WipeWindow.create().set_mode("ghostBlur").set_radius(20).apply(self)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_bar = CustomTitleBar(self, title="LEVIATHAN ENGINE V2.1")
        layout.addWidget(self.title_bar)
        
        content = QWidget()
        content_lay = QVBoxLayout(content)
        content_lay.setAlignment(Qt.AlignCenter)
        content_lay.setSpacing(20)
        
        label = QLabel("PRUEBA DE COMPONENTES DE MENSAJE")
        label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        content_lay.addWidget(label)
        
        # Botones para diferentes tipos de dialogo
        modes = [
            ("INFO", "info", ["OK"]), 
            ("SUCCESS", "success", ["GENIAL"]), 
            ("WARNING", "warning", ["IGNORAR", "REINTENTAR"]), 
            ("ERROR", "error", ["CERRAR"]),
            ("PREGUNTA", "info", ["NO", "SÍ"])
        ]
        
        for name, mode, btns in modes:
            btn = QPushButton(f"MOSTRAR {name}")
            btn.setFixedSize(250, 45)
            # Conectamos para usar nuestra nueva librería
            btn.clicked.connect(lambda checked, m=mode, b=btns: self.open_dialog(m, b))
            
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.08);
                    color: white;
                    border: 1px solid rgba(255,255,255,0.15);
                    border-radius: 10px;
                    font-weight: 500;
                    font-family: 'Segoe UI';
                }
                QPushButton:hover {
                    background-color: white;
                    color: black;
                }
            """)
            content_lay.addWidget(btn)
            
        layout.addWidget(content, 1)

    def open_dialog(self, mode, buttons):
        def on_action(result):
            print(f"🔹 LeviathanDialog: El usuario seleccionó -> {result}")

        LeviathanDialog.launch(
            parent=self, 
            title=f"Sistema Leviathan - {mode.upper()}", 
            message=f"Esta es una demostración del componente de diálogo en modo '{mode}'. "
                    "¿Deseas continuar con la operación actual utilizando los nuevos botones dinámicos?",
            mode=mode,
            buttons=buttons,
            callback=on_action
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Sincronizamos el icono con el ID de la app para la barra de tareas
    icon_path = os.path.join("app", "lvthnUI.dialogBox-icon.ico")
    icon = InmojiTrx(icon_path).apply(app)
    
    ventana = MiVentana()
    # Aplicamos el icono también a la ventana (vital para frameless)
    ventana.setWindowIcon(icon)
    ventana.show()
    
    sys.exit(app.exec_())
