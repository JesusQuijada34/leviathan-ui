# 🌊 Leviathan-UI: Framework Premium para PyQt6 (v1.0.5)

**Leviathan-UI** es un framework profesional para crear aplicaciones de escritorio con el aspecto moderno de **Windows 11** usando Python y PyQt6.

> **Lanzamiento 1.0.5** — Correcciones de compatibilidad PyQt6, scripts de demo funcionales, y mejoras visuales en controles.

## 📚 Documentación

Este repositorio incluye documentación estructurada en `docs/`:

- `docs/overview.md` — visión general del framework.
- `docs/faq.md` — respuestas a preguntas frecuentes.
- `docs/dev-community-post.md` — post listo para publicar en comunidades de desarrolladores.
- `docs/index.md` — índice de documentación.

---
## 🚀 Publicación en PyPI

Para publicar en PyPI necesitas un **token de acceso** de PyPI (no tu contraseña). El flujo correcto es:

1. Crear el token en tu cuenta de PyPI.
2. Guardarlo localmente en `~/.pypirc` o usar `twine upload --non-interactive -u __token__ -p <TOKEN> dist/*`.
3. Asegurar que el paquete es compatible instalando la rueda:

```bash
python -m pip install dist/leviathan_ui-1.0.5-py3-none-any.whl
```

4. Subir con twine:

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
```

> No incluyas el token en el repositorio. Usa `.pypirc.example` como plantilla.

---

## 🚀 ¿Qué hay de nuevo? (v1.0.5)

### 🐛 Correcciones
- **Compatibilidad PyQt6 completa**: Todos los scripts actualizados a sintaxis moderna (`Qt.AlignmentFlag`, `app.exec()`)
- **Scripts de demo 100% funcionales**: `ghost`, `ghostBlur`, `polished`, `dialogBox` ejecutan sin errores
- **TitleBar transparente**: Mejor integración visual con ventanas personalizadas

### 📚 Mejoras
- Documentación FAQ completa
- README reorganizado con ejemplos claros
- Changelog actualizado con todas las correcciones

Hemos mejorado el framework para que sea más fácil de usar en todo el mundo:

### 📦 Paquetes Python listos para usar
*   **Ruedas (`.whl`) disponibles**: ahora el proyecto está preparado para generar distribuciones wheel con `python -m build --wheel`.
*   **Empaquetado moderno**: compatibilidad con PyQt6 y mejores metadatos en `pyproject.toml`.

### 🌍 Tu programa en cualquier idioma
Ahora es mucho más fácil que tu aplicación hable el idioma de tus usuarios:
*   **Detección automática:** El sistema detecta solo si tu computadora está en español, inglés, u otros idiomas.
*   **Soporte global:** Incluye paquetes para más de 10 regiones (Español, Inglés, Chino, Japonés, etc.).
*   **A prueba de errores:** Si el sistema no encuentra tu idioma, te avisará de forma clara en lugar de fallar.

### 🎨 Instalación más visual y sencilla
El proceso de instalación ahora es más amigable:
*   **Pantalla de bienvenida:** Verás una ventana de carga moderna al iniciar.
*   **Iconos dinámicos:** Dibujos animados que te guían en cada paso.
*   **Instalación local:** Puedes instalar el framework directamente desde los archivos descargados sin complicaciones.

---

## 🛠 Guía de Instalación Paso a Paso

No necesitas usar comandos complejos. Hemos creado un **asistente visual** que hará todo por ti:

1.  Abre la carpeta del proyecto en tu computadora.
2.  Abre una terminal o consola de comandos.
3.  Escribe el siguiente código y presiona **Enter**:

```bash
python leviathan-ui.py
```

*Esto abrirá una ventana que te guiará paso a paso, igual que cuando instalas cualquier otro programa en Windows.*

---

## 🎯 Ejemplo Rápido

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from leviathan_ui import CustomTitleBar, WipeWindow

class MiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 550)
        
        # Aplicar efecto GhostBlur
        WipeWindow.create().set_mode("ghostBlur").set_radius(10).apply(self)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra de título personalizada
        self.title_bar = CustomTitleBar(self, title="Mi Aplicación")
        layout.addWidget(self.title_bar)
        
        # Contenido
        content = QLabel("¡Hola Mundo con Leviathan-UI!")
        content.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec())
```

---

## 📦 Scripts de Demo Incluidos

Prueba los diferentes estilos visuales:

```bash
python lvthnUi.ghost.py      # Efecto Ghost transparente
python lvthnUi.ghostBlur.py   # Efecto Ghost con desenfoque
python lvthnUi.polished.py    # Estilo pulido con sombras
python lvthnUI.dialogBox.py   # Diálogos personalizados
```
