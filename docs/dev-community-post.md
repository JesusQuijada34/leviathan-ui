# Publicación para la comunidad de desarrolladores

## Leviathan UI 1.0.4 – Ahora con PyQt6 y empaquetado wheel

Hola comunidad,

Hoy lanzamos **Leviathan UI 1.0.4**, una versión pensada para desarrolladores que necesitan una interfaz moderna y una distribución más fácil en Python.

### Lo más destacado

- 🔧 Migración completa a **PyQt6**
- 📦 Soporte para generar **ruedas (`.whl`)**
- 📚 Documentación nueva en `docs/`
- 🧩 Template `.env` para desarrollo local
- 🧾 Changelog actualizado y control de versiones claro

### Por qué te interesa

Si trabajas con apps Python y quieres un look profesional tipo Windows 11, este framework te ofrece:
- barra de título personalizada
- efectos de vidrio y blur
- diálogos modernos con overlay
- controles de progreso visuales
- generación automática de iconos desde emojis o imágenes

### Cómo usarlo

```bash
git clone https://github.com/JesusQuijada34/leviathan-ui.git
cd leviathan-ui
python -m pip install --upgrade build
python -m build --wheel --outdir dist
```

### Dónde encontrar la documentación
- `docs/overview.md` — visión general del proyecto
- `docs/faq.md` — preguntas frecuentes
- `docs/dev-community-post.md` — este post listo para compartir

### Llamado a la acción
Si te interesa, prueba el paquete y comparte tus pantallas. También estamos abiertos a PRs para nuevos efectos, componentes de UI y mejoras de documentación.

¡Gracias y feliz desarrollo! 👾
