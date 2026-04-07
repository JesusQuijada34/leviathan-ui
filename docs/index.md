# Leviathan UI - Documentación

Bienvenido a la documentación de Leviathan UI.

## Archivos principales

- `overview.md` — visión general del framework.
- `faq.md` — preguntas frecuentes.
- `dev-community-post.md` — anuncio para compartir en la comunidad.

## Publicación en PyPI

El proyecto está configurado para generar una rueda Python con:

```bash
python -m pip install --upgrade build
python -m build --wheel --outdir dist
```

Para subir a PyPI se recomienda usar `twine` y un token de API en lugar de contraseña.

## Compatibilidad garantizada

- `PyQt6>=6.5.0`
- `Pillow>=9.0.0`
- `Python >= 3.8`

## Archivos importantes

- `pyproject.toml` — metadata y requisitos del paquete.
- `.env` — configuración local de desarrollo.
- `.gitignore` — archivos que no deben versionarse.
- `.pypirc.example` — plantilla para PyPI token.
