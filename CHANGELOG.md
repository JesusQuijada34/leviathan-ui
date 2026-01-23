# 📝 Historial de Cambios - Leviathan-UI

## [1.0.3] - 2026-01-23: Sistema i18n y Setup SVG

### 🏗️ Internacionalización (i18n)
*   **Nueva Carpeta `lang/`**: Implementación de archivos de idioma `.lv-lng` basados en JSON.
*   **Soporte Global**: Añadidos paquetes de idioma para Árabe, Chino, Japonés, Coreano, Ruso, Turco, Alemán, Francés, Italiano, Portugués y diversas regiones de Español.
*   **Lógica de Carga Segura**: El sistema ahora detecta el idioma del SO y valida la existencia del pack antes de iniciar.

### 🎨 Experiencia de Instalación (Setup)
*   **Iconos SVG**: Integración de SVGs animados para los pasos de Información, Instalación y Finalización.
*   **Splash UWP en Setup**: El instalador ahora utiliza el sistema KJ302 para mostrar un splash screen moderno al iniciar.
*   **Modo GhostBlur**: El instalador utiliza el efecto de cristal esmerilado por defecto.

### 📦 Distribución
*   **Soporte `.whl`**: El instalador automatiza la carga de paquetes desde la carpeta `dist/`.

---

## [1.0.2] - 2026-01-17: Mejoras de UI Base
*   Introducción de `LeviathanProgressBar` y soporte mejorado para iconos de imagen en componentes.
