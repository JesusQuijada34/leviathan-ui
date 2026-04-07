# Leviathan UI - Visión general

Leviathan UI es un framework de interfaz moderna para aplicaciones Python que provee:

- Estilo Windows 11 con título personalizado y controles propios.
- Efectos de vidrio y blur mediante `WipeWindow`.
- Diálogos modernos con `LeviathanDialog`.
- Barra de progreso animada con `LeviathanProgressBar`.
- Iconos generados automáticamente con `InmojiTrx`.

## Arquitectura

El código principal está en la carpeta `leviathan_ui/`:

- `title_bar.py`: Barra de título con botones de ventana y acento dinámico.
- `wipeWindow.py`: Gestión de apariencia transparente, blur y efectos de ventana.
- `dialogs.py`: Dialogos modales con overlay, animaciones y botones estilizados.
- `progress_bar.py`: Barra de progreso nativa con modo estándar y marquee.
- `splash.py`: Pantalla de bienvenida y splash screen personalizable.
- `lightsOff.py`: Efectos glow para controles interactivos.
- `inmojiTrx.py`: Generación de iconos desde emojis o archivos de imagen.

## Instalación y uso

1. Clona el repositorio:

```bash
git clone https://github.com/JesusQuijada34/leviathan-ui.git
cd leviathan-ui
```

2. Crea un entorno virtual y activa Python 3.8+.

3. Instala dependencias:

```bash
python -m pip install -r requirements.txt
```

4. O genera un paquete wheel:

```bash
python -m pip install --upgrade build
python -m build --wheel --outdir dist
```

## Desarrollo

- Usa `.env` para variables locales.
- Evita subir `dist/`, `build/`, `*.egg-info/` y entornos virtuales.
- Documentación adicional y FAQ están en `docs/`.
