# 📝 Historial de Cambios - Leviathan-UI

## [1.0.6] - 2026-04-07: Instalador Profesional Estilo NSIS

### 🚀 Nuevo Instalador Leviathan-UI Setup
*   **UI completamente rediseñada**: Instalador profesional estilo NSIS con banners y transiciones pulidas.
*   **Pantalla de bienvenida con banner vertical**: Usa `assets/splash_setup.png` como banner lateral izquierdo (estilo instaladores clásicos).
*   **Pantalla de opciones avanzadas**: Checkboxes para modo de instalación (local/remoto), accesos directos (desktop/menú inicio), y opciones avanzadas (force reinstall, upgrade deps).
*   **Pantalla de instalación con banner superior**: Usa `assets/splash.png` como banner superior durante la instalación.
*   **Prevención de múltiples instancias**: Usa `QSharedMemory` para evitar que se ejecuten múltiples instaladores simultáneamente.
*   **Manejo robusto de errores**: Validaciones de conexión a internet, existencia de archivos `.whl`, y logging detallado de la instalación.
*   **Worker thread para instalación**: La instalación se ejecuta en un `QThread` separado para no bloquear la UI.
*   **Barra de progreso animada**: Progreso visual con estados de instalación claros.

### 🐛 Correcciones
*   Instalador ahora maneja correctamente modo local (sin internet) y remoto (con internet).
*   Validaciones previas antes de iniciar la instalación.
*   Mejor manejo de errores de pip con logging visible.

---

## [1.0.5] - 2026-04-06: Correcciones de Compatibilidad PyQt6 y Scripts de Demo

### 🐛 Errores arreglados
*   **Compatibilidad PyQt6 completa**: Corregidos todos los `Qt.AlignCenter` → `Qt.AlignmentFlag.AlignCenter`.
*   **API deprecada de locale**: Reemplazado `locale.getdefaultlocale()` (deprecado en Python 3.11+) con `locale.getlocale()` compatible.
*   **Método exec() moderno**: Todos los `app.exec_()` cambiados a `app.exec()` (sintaxis PyQt6).
*   **Scripts de demo funcionales**: `lvthnUi.ghost.py`, `lvthnUi.ghostBlur.py`, `lvthnUi.polished.py`, `lvthnUI.dialogBox.py` ahora ejecutan sin errores.

### ✨ Mejoras visuales
*   **TitleBar transparente**: La `CustomTitleBar` ahora usa `background-color: transparent` para mejor integración visual.
*   **Fondos transparentes en controles**: Corrección de QSS en `packagemaker` para eliminar fondos opacos `#121822` detrás de labels y radio buttons.

### 📚 Documentación
*   README actualizado con nueva versión y mejor estructura.
*   FAQ completo añadido con respuestas a problemas comunes.

---

## [1.0.4] - 2026-04-05: PyQt6, empaquetado de ruedas y documentación completa

### 🚀 Mejoras principales
*   Migración total a **PyQt6** para compatibilidad con las últimas herramientas de Qt.
*   Construcción de paquetes **wheel** para distribución más simple en entornos Python.
*   Nueva documentación para desarrolladores, FAQ y guía de publicación.
*   Nueva plantilla `.env` y `.gitignore` modernizado para facilitar el desarrollo local.

### 🧠 Experiencia de desarrollo
*   Documentación reorganizada en `docs/` con **Overview**, **FAQ** y un **post listo para la comunidad**.
*   Instrucciones claras para crear el paquete y publicar la versión.
*   Mejoras de consistencia en el README para proyectos y colaboradores.

---

## [1.0.3] - 2026-01-23: Soporte Multi-idioma y Mejoras Visuales

### 🌍 Soporte para muchos idiomas (i18n)
*   **Nueva carpeta de traducciones**: Ahora los textos están separados en una carpeta llamada `lang/`. Esto hace que sea muy fácil añadir nuevos idiomas en el futuro.
*   **Disponible en todo el mundo**: ¡Ahora puedes usar la aplicación en casi cualquier idioma! Hemos añadido soporte para Chino, Japonés, Ruso, Alemán, Francés, Portugués y muchas variantes de Español.
*   **Detección automática**: El programa es inteligente: detecta qué idioma usas en tu computadora y se configura solo para que no tengas que cambiar nada.

### 🎨 Un instalador más bonito (Setup)
*   **Dibujos animados (SVG)**: Hemos añadido iconos que se mueven durante la instalación para que el proceso sea más entretenido y visual.
*   **Pantalla de bienvenida**: Ahora, al abrir el instalador, verás una pantalla de carga moderna (Splash Screen) antes de empezar.
*   **Efecto de cristal (GhostBlur)**: El instalador ahora tiene un fondo elegante, transparente y borroso, parecido al estilo de Windows moderno.

### 📦 Mejoras internas
*   **Instalación automática**: Hemos mejorado la forma en la que el programa instala sus archivos internos para que sea más rápido y falle menos.

---

## [1.0.2] - 2026-01-17: Mejoras Visuales Básicas
*   **Nueva barra de carga**: Añadimos una barra de progreso personalizada (`LeviathanProgressBar`).
*   **Mejores iconos**: Ahora es más fácil poner imágenes y dibujos dentro de los botones y menús del programa.
