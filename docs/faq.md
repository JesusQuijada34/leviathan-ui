# FAQ - Leviathan UI

## ¿Por qué se migró a PyQt6?
PyQt6 trae compatibilidad con las últimas versiones de Qt y permite aprovechar nuevas APIs de renderizado y widgets. Además, la migración mejora la compatibilidad con herramientas de empaquetado modernas.

## ¿Cómo construyo las ruedas (`.whl`)?
1. Instala `build`:

```bash
python -m pip install --upgrade build
```

2. Genera el wheel:

```bash
python -m build --wheel --outdir dist
```

3. El archivo resultante estará en `dist/`.

## ¿Qué hace `.env`?
El archivo `.env` se usa para configurar variables locales del proyecto sin subirlas a Git. En este repositorio se incluyen valores de ejemplo como `APP_VERSION`, `PYTHONPATH` y `DEFAULT_LOCALE`.

## ¿Dónde está la documentación del proyecto?
La documentación principal está en `docs/`:
- `docs/overview.md`: visión general del framework.
- `docs/faq.md`: preguntas frecuentes.
- `docs/dev-community-post.md`: anuncio para la comunidad de desarrolladores.

## ¿Cómo contribuyo?
1. Crea un issue con tu propuesta.
2. Haz un fork y trabaja en una rama con nombre descriptivo.
3. Envía un PR con cambios claros y documentación actualizada.

## 🐛 Errores Comunes y Soluciones

### Error: `AttributeError: module 'PyQt6.QtCore' has no attribute 'AlignCenter'`

**Solución**: Usa `Qt.AlignmentFlag.AlignCenter` en lugar de `Qt.AlignCenter`.

### Error: `AttributeError: 'QApplication' object has no attribute 'exec_'`

**Solución**: Usa `app.exec()` en lugar de `app.exec_()`.

### Error: `AttributeError: module 'locale' has no attribute 'getdefaultlocale'`

**Solución**: Actualiza a Leviathan-UI v1.0.5+ que usa `locale.getlocale()` compatible con Python 3.11+.

## ¿Qué versiones soporta este repositorio?
Leviathan UI está diseñado para Python 3.8+ y usa `PyQt6>=6.5.0`.
