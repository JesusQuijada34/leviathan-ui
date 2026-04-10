# 📝 Changelog - Leviathan-UI

## [1.0.5] - 2026-04-09: Setup Refinement & UI Polish

### 🎨 Instalador Profesional - Mejoras Visuales
*   **Splash Screen Integrado**: Ahora el splash es parte de la ventana principal (modo APPX), mostrando el logo y título mientras carga.
*   **Indicador de Página**: 4 dots visuales que muestran el progreso del setup (● ● ● ●).
*   **Navegación Mejorada**: Botones "Atrás", "Siguiente" y "Cancelar" con estilo consistente.
*   **Transiciones Automáticas**: Al completar la instalación, avanza automáticamente a la página final.

### 🐛 Correcciones Críticas
*   **Navegación Entre Páginas**: Solucionado problema donde el botón "Siguiente" no cambiaba de página.
*   **Bordes Azules Eliminados**: Todos los widgets ahora usan fondo oscuro sólido (#121822) en lugar de transparencia que mostraba el azul de Windows.
*   **Banner sin Distorsión**: El banner superior de instalación mantiene su aspect ratio correctamente.
*   **PyQt6 API**: Corrección de `QEasingCurve.OutQuad` → `QEasingCurve.Type.OutQuad`.

### 📐 Layout Compacto
*   Ventana reducida a 720×480px (más compacta y profesional).
*   Espaciado reducido entre controles para eliminar espacio desperdiciado.
*   Tamaños de fuente optimizados para mejor legibilidad.

---

## [1.0.4] - 2026-04-07: Professional Installer, PyQt6 & Documentation

### 🚀 Nuevo Instalador Leviathan-UI Setup
*   **UI completamente rediseñada**: Instalador profesional estilo NSIS con banners y transiciones pulidas.
*   **Pantalla de bienvenida con banner vertical**: Usa `assets/splash_setup.png` como banner lateral izquierdo.
*   **Pantalla de opciones avanzadas**: Checkboxes para modo de instalación (local/remoto), accesos directos, y opciones avanzadas.
*   **Pantalla de instalación con banner superior**: Usa `assets/splash.png` como banner superior durante la instalación.
*   **Prevención de múltiples instancias**: Usa `QSharedMemory` para evitar múltiples instaladores simultáneos.
*   **Worker thread para instalación**: Ejecución en `QThread` separado sin bloquear UI.

### 🐛 Correcciones PyQt6
*   **Compatibilidad PyQt6 completa**: `Qt.AlignCenter` → `Qt.AlignmentFlag.AlignCenter`.
*   **API deprecada de locale**: `locale.getdefaultlocale()` → `locale.getlocale()` (Python 3.11+).
*   **Método exec() moderno**: `app.exec_()` → `app.exec()`.
*   **Scripts de demo funcionales**: Todos los demos ahora ejecutan sin errores.

### ✨ Mejoras visuales
*   **TitleBar transparente**: `CustomTitleBar` con `background-color: transparent`.
*   **Fondos transparentes en controles**: Corrección de QSS en `packagemaker`.

### 📚 Documentación
*   README actualizado con nueva versión y mejor estructura.
*   FAQ completo añadido con respuestas a problemas comunes.
*   Clases del instalador separadas en `installer_classes/`.

---

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
