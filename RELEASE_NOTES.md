# 🚀 Notas de Publicación - Leviathan-UI v1.0.5

Esta versión se enfoca en refinamiento del instalador profesional, navegación fluida y pulido visual.

## ✨ Novedades en 1.0.5

### 🎯 Navegación Wizard Profesional
El instalador ahora presenta una experiencia de 4 pasos tipo NSIS:
1. **Bienvenida** - Banner vertical + introducción
2. **Opciones** - Checkboxes para personalizar instalación
3. **Instalación** - Progreso en tiempo real con logs
4. **Finalizado** - Confirmación de éxito

- **Indicador Visual**: 4 dots (● ● ● ●) muestran el progreso actual
- **Botones de Navegación**: Atrás/Siguiente/Cancelar con estados dinámicos
- **Transición Automática**: Al terminar la instalación, avanza directo a "Finalizado"

### 🖼️ Splash Screen Integrado (Modo APPX)
- El splash ahora es parte de la ventana principal (no ventana separada)
- Muestra logo `app/app-icon.ico` + título "Leviathan-UI" + subtítulo versión
- Fade-out suave de 600ms revelando la interfaz principal
- Barra de título visible durante todo el proceso

### 📐 Layout Compacto y Profesional
- **Tamaño optimizado**: 720×480px (anterior 70% pantalla era excesivo)
- **Sin espacio desperdiciado**: Eliminados todos `addStretch()` innecesarios
- **Fuentes refinadas**: Títulos 20px (era 26px), subtítulos 11px (era 14px)
- **Controles compactos**: Botones 75×28px, barra inferior 50px altura

### 🐛 Correcciones Críticas
- **Navegación**: Solucionado `QEasingCurve.Type.OutQuad` (PyQt6 API)
- **Fondos uniformes**: Todos los widgets usan #121822 sólido (sin azul Windows)
- **Banners**: Aspect ratio preservado al redimensionar
- **Eventos**: Splash transparente a clicks (`WA_TransparentForMouseEvents`)

---

## Historial de Versiones

### v1.0.4 (2026-04-07)
- Migración completa a **PyQt6**
- Generación de paquete wheel
- Documentación en `docs/`
- Soporte multilingüe integral (10+ idiomas)
- Efecto GhostBlur estándar

### v1.0.3 (2026-01-23)
- Soporte multi-idioma (i18n)
- Pantalla de bienvenida SVG
- Instalación automática mejorada

---

## 🌈 Soporte Multilingüe Integral (i18n)
Leviathan UI ahora rompe las barreras idiomáticas. No se trata solo de traducciones, sino de una adaptación completa de componentes para soportar diversas regiones, asegurando que las interfaces sean coherentes y accesibles globalmente:
- **Iberoamérica**: Soporte completo para variantes regionales (es-AR, es-MX, es-ES).
- **Asia-Pacífico**: Optimización de tipografías y espaciado para caracteres complejos (zh-CN, ja-JP, ko-KR).
- **Europa Occidental**: Localización estándar para (en-US, fr-FR, de-DE, it-IT, pt-BR, tr-TR).
- **Eurasia y MENA**: Soporte inicial para alfabetos cirílicos y preparativos para layouts RTL (ar-SA, ru-RU).

## 🎨 Instalador Dinámico y Experiencia Visual
El proceso de configuración inicial ha dejado de ser una simple terminal para convertirse en una experiencia inmersiva:
- **SVGs Animados de Alta Fidelidad**: Feedback visual en tiempo real durante la extracción de paquetes y configuración de dependencias.
- **Estandarización GosthBlur**: Hemos portado el efecto de cristal (Glassmorphism) desde la rama experimental v1.1. Este estilo visual ahora es el estándar nativo para el instalador y los componentes de sistema, ofreciendo una estética moderna y ligera.

## 🏗️ Optimización de Distribución y Despliegue
Hemos refinado la arquitectura de salida para entornos profesionales:
- **Gestión de `dist/`**: El núcleo ahora prioriza la lectura de archivos pre-compilados en la carpeta de distribución, reduciendo los tiempos de carga en producción.
- **Modo Offline**: Mejoras significativas en el reconocimiento de assets locales, permitiendo despliegues en redes privadas o entornos controlados sin dependencia de CDNs externas.

## 🛠️ Mejoras Menores y Estabilidad
- Corregido un error de renderizado en contenedores con `overflow: hidden` bajo el efecto GosthBlur.
- Optimización del peso del paquete base en un 12% gracias a la limpieza de metadatos i18n redundantes.

---
### ¿Cómo actualizar?
Ejecuta el comando de actualización en tu terminal:
```bash
leviathan-ui update
```

¡Gracias por ser parte de la evolución de Leviathan UI! 🐉
