# 🚀 Notas de Publicación - Leviathan-UI v1.0.4

Esta versión de Leviathan UI se enfoca en compatibilidad, empaquetado y documentación para desarrolladores.

## Cambios clave en 1.0.4

- Migración completa a **PyQt6**.
- Generación de paquete wheel (`dist/leviathan_ui-1.0.4-py3-none-any.whl`).
- Documentación nueva en `docs/` y guía de publicación a PyPI.
- `.env` de ejemplo para desarrollar con variables locales.
- `pyproject.toml` actualizado con metadata de paquete y dependencias.
- `details.xml` actualizado para reflejar el nuevo nombre y versión.

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
