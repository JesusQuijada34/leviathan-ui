# 🚀 Leviathan-UI v1.0.5 – Instalador Profesional con Navegación Wizard

Hola comunidad de desarrolladores Python,

Hoy presentamos **Leviathan-UI v1.0.5**, una actualización enfocada en ofrecer una experiencia de instalación profesional comparable a instaladores NSIS o InstallShield, pero completamente en Python con PyQt6.

---

## ✨ Lo Nuevo en v1.0.5

### 🎯 Navegación Wizard de 4 Pasos
El instalador ahora presenta una interfaz clara y profesional:
1. **Bienvenida** – Banner vertical + introducción al framework
2. **Opciones** – Personalización de instalación (modo local/remoto, accesos directos)
3. **Instalación** – Progreso en tiempo real con logs de salida
4. **Finalizado** – Confirmación visual de éxito

**Indicador de progreso visual**: 4 dots (● ● ● ●) que muestran la página actual con color naranja (#ff5722).

### 🖼️ Splash Screen Integrado (Modo APPX)
- Splash integrado en la ventana principal (no ventana separada)
- Muestra logo, título y subtítulo animados
- Fade-out suave de 600ms revela la interfaz
- Barra de título siempre visible

### � Layout Compacto Profesional
- **Tamaño optimizado**: 720×480px (compacto y centrado)
- **Sin espacio desperdiciado**: Eliminados todos los `addStretch()` innecesarios
- **Fuentes refinadas**: Jerarquía visual clara con tamaños optimizados
- **Controles compactos**: Botones 75×28px, barra inferior 50px

### 🐛 Correcciones Importantes
- **Fondos sólidos**: Eliminados bordes azules de Windows con #121822 uniforme
- **Navegación fluida**: Cambio instantáneo entre páginas
- **PyQt6 API moderna**: Uso correcto de `QEasingCurve.Type.OutQuad`
- **Splash transparente**: No bloquea eventos del mouse

---

## 🎨 ¿Qué es Leviathan-UI?

Framework profesional para crear aplicaciones de escritorio con estilo Windows 11:

| Componente | Descripción |
|------------|-------------|
| `CustomTitleBar` | Barra de título frameless con botones animados |
| `WipeWindow` | Efectos visuales: polished, ghostBlur, ghost |
| `InmersiveSplash` | Splash screens con animaciones suaves |
| `LeviathanProgressBar` | Barras de progreso estilo moderno |
| `LeviathanDialog` | Diálogos modales con overlay |

---

## 🚀 Instalación Rápida

### Opción 1: Instalador GUI (Recomendado)
```bash
git clone https://github.com/tuusuario/leviathan-ui.git
cd leviathan-ui
python leviathan-ui.py
```

### Opción 2: pip install
```bash
pip install leviathan-ui
```

---

## 💡 Ejemplo de Uso

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from leviathan_ui import CustomTitleBar, WipeWindow

class MiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 550)
        
        # Aplicar efecto visual moderno
        WipeWindow.create().set_mode("polished").set_radius(8).apply(self)
        
        # Layout sin márgenes
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra de título personalizada
        self.title_bar = CustomTitleBar(self, title="Mi Aplicación", hide_max=False)
        layout.addWidget(self.title_bar)
        
        # Contenido
        content = QLabel("¡Hola con Leviathan-UI!")
        content.setStyleSheet("color: white; font-size: 24px; background: transparent;")
        layout.addWidget(content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec())
```

---

## 🛠️ Casos de Uso

- **Instaladores de software**: Wizard de múltiples pasos con progreso
- **Aplicaciones enterprise**: Look profesional consistente
- **Herramientas de desarrollo**: IDEs con interface moderna
- **Dashboards**: Paneles de control visualmente atractivos

---

## 📚 Recursos

- **GitHub**: [github.com/tuusuario/leviathan-ui](https://github.com/tuusuario/leviathan-ui)
- **Documentación**: `docs/overview.md`, `FAQ.md`, `CHANGELOG.md`
- **Ejemplos**: Scripts demo `lvthnUi.*.py` incluidos
- **PyPI**: `pip install leviathan-ui`

---

## 🤝 Contribuciones

Buscamos colaboradores en:
- Nuevos efectos visuales (WipeWindow modes)
- Componentes de UI adicionales
- Mejoras de documentación
- Soporte para Linux/macOS mejorado

---

## 📝 Changelog Resumido

| Versión | Fecha | Cambios Clave |
|---------|-------|---------------|
| v1.0.5 | 2026-04-09 | Instalador wizard, splash integrado, UI compacta |
| v1.0.4 | 2026-04-07 | PyQt6 completo, empaquetado wheel, i18n 10+ idiomas |
| v1.0.3 | 2026-01-23 | Soporte multi-idioma, instalador con SVG animados |

---

**¿Preguntas o feedback?** Déjalos en los comentarios o abre un issue en GitHub.

¡Feliz desarrollo! 🐉�

#python #pyqt6 #gui #windows11 #desktop #framework #installer
