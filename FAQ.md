# ❓ Preguntas Frecuentes - Leviathan-UI

## 🔧 Instalación y Setup

### ¿Cómo instalo Leviathan-UI?
**Opción 1: Instalador GUI (Recomendado)**
```bash
python leviathan-ui.py
```
Este comando abre el instalador visual con 4 pasos claros: Bienvenida → Opciones → Instalación → Finalizado.

**Opción 2: pip install**
```bash
pip install leviathan-ui
```

### ¿Qué requisitos necesito?
- **Python**: 3.8 o superior
- **PyQt6**: 6.5+ (se instala automáticamente)
- **Sistema**: Windows 10/11 recomendado (Linux/macOS compatible)

### ¿Puedo instalar sin internet?
Sí. El instalador soporta modo **Local** que usa archivos `.whl` en la carpeta `dist/`. Solo selecciona "Local" en las opciones de instalación.

---

## 🎨 Uso del Framework

### ¿Cómo aplicar efectos visuales a mi ventana?
```python
from leviathan_ui import WipeWindow

# Modos disponibles:
WipeWindow.create().set_mode("polished").set_radius(8).apply(window)   # Estilo refinado
WipeWindow.create().set_mode("ghostBlur").set_radius(10).apply(window)    # Efecto cristal
WipeWindow.create().set_mode("ghost").set_radius(8).apply(window)        # Transparente
```

### ¿Cómo agrego una barra de título personalizada?
```python
from leviathan_ui import CustomTitleBar

self.title_bar = CustomTitleBar(
    self, 
    title="Mi Aplicación", 
    icon="path/to/icon.ico",  # Opcional
    hide_max=False            # Mostrar botón maximizar
)
layout.addWidget(self.title_bar)
```

### ¿Cómo hago mi ventana redimensionable con frameless?
```python
self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinMaxButtonsHint)
self.setMinimumSize(600, 400)  # Tamaño mínimo
```

---

## 🐛 Solución de Problemas

### "AttributeError: type object 'QEasingCurve' has no attribute 'OutQuad'"
**Solución**: En PyQt6, usa `QEasingCurve.Type.OutQuad` en lugar de `QEasingCurve.OutQuad`.

### La ventana muestra bordes azules/celeste de Windows
**Solución**: Establece fondo sólido oscuro en todos los widgets:
```python
widget.setStyleSheet("background-color: #121822; border: none;")
```

### El splash screen bloquea los clicks
**Solución**: Configura transparencia para eventos del mouse:
```python
splash.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
```

### El instalador no avanza de página
**Causa**: La señal `finished` del worker thread no está conectada.
**Solución**: Conecta la señal en tu ventana principal:
```python
self.page_install.finished.connect(self.on_install_finished)
```

---

## 📦 Empaquetado y Distribución

### ¿Cómo creo un instalador ejecutable?
Usa PyInstaller con el hook incluido:
```bash
pyinstaller --onefile --windowed leviathan-ui.py
```

### ¿Cómo publico en PyPI?
1. Genera distribución wheel: `python -m build --wheel`
2. Sube con twine: `python -m twine upload dist/*`

### ¿Cómo cambio el idioma del instalador?
El instalador detecta automáticamente el idioma del sistema. Para forzar un idioma, edita `lang/` y configura `i18n_manager.py`.

---

## 💡 Mejores Prácticas

### Estructura recomendada para páginas del instalador
```
installer_classes/
├── leviathan_setup.py      # Ventana principal con navegación
├── welcome_page.py         # Página 1: Bienvenida
├── options_page.py         # Página 2: Opciones
├── install_page.py         # Página 3: Progreso
├── finish_page.py          # Página 4: Finalizado
└── i18n_manager.py         # Gestión de idiomas
```

### Patrón para navegación wizard
```python
def go_next(self):
    if self.current_page == 1:  # Opciones → Instalación
        options = self.page_options.get_options()
        self.page_install.start_installation(options)
    self.current_page += 1
    self.pages.setCurrentIndex(self.current_page)
    self.update_buttons()
```

---

## 🔗 Integraciones

### Uso con Packagemaker
Leviathan-UI es la base visual de [Packagemaker](https://github.com/tuusuario/packagemaker). Ambos proyectos comparten:
- `CustomTitleBar` - Barra de título unificada
- `WipeWindow` - Efectos visuales consistentes
- Paleta de colores #121822 (fondo) / #ff5722 (acento)

### Compatibilidad con otros frameworks
Leviathan-UI es compatible con:
- **PyQt6** / **PySide6**: Usa la misma sintaxis de señales
- **Qt Designer**: Exporta archivos `.ui` y aplica efectos después
- **FBS (Fman Build System)**: Funciona con empaquetado FBS

---

## 📞 Soporte

¿No encuentras tu respuesta?
- Abre un [Issue en GitHub](../../issues)
- Consulta la documentación en `docs/overview.md`
- Revisa los scripts de demo: `lvthnUi.*.py`

---

**Última actualización**: 2026-04-09 | **Versión**: 1.0.5
