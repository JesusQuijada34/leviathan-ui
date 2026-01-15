# Leviathan UI

**Premium UI Framework for PyQt5 with Windows 11 Aesthetics**

A modern, feature-rich UI framework that brings Windows 11's beautiful design language to your PyQt5 applications.

## ✨ Features

- **🪟 WipeWindow**: Three stunning window modes
  - `polished`: Solid background with shadows and rounded corners
  - `ghost`: Fully transparent overlay mode
  - `ghostBlur`: Acrylic/frosted glass blur effect (Windows 10/11)

- **🌊 InmersiveSplash**: Professional splash screen system
  - Adaptive mode (respects taskbar) and fullscreen mode
  - Custom phrases for startup and exit
  - Smooth fade animations
  - Automatic lifecycle management

- **🎨 CustomTitleBar**: Windows 11 style title bar
  - Native SVG-drawn window controls
  - System accent color integration
  - Smooth drag and maximize/minimize

- **🎭 InmojiTrx**: High-quality icon generation
  - Convert emojis to multi-resolution ICO files
  - Support for PNG/ICO images
  - Perfect taskbar rendering

## 📦 Installation

```bash
pip install leviathan-ui
```

Or install from wheel:
```bash
pip install leviathan_ui-1.0.0-py3-none-any.whl
```

## 🚀 Quick Start

```python
from PyQt5.QtWidgets import QApplication, QWidget
from leviathan_ui import WipeWindow, InmersiveSplash, CustomTitleBar, InmojiTrx

app = QApplication([])

# Create your main window
window = QWidget()
window.resize(800, 600)

# Apply blur effect
WipeWindow.create()\
    .set_mode("ghostBlur")\
    .set_radius(15)\
    .apply(window)

# Add custom title bar
title_bar = CustomTitleBar(window, title="My App")

# Set app icon
InmojiTrx("🚀").apply(app)

# Create splash screen
splash = InmersiveSplash.create()\
    .set_mode("adaptive")\
    .set_phrases(["Loading modules...", "Ready!"])\
    .on_finish(window.show)\
    .start()

app.exec_()
```

## 📖 Documentation

### WipeWindow

```python
WipeWindow.create()\
    .set_mode("polished")      # "polished", "ghost", or "ghostBlur"
    .set_background("auto")     # "auto" or hex color "#RRGGBB"
    .set_radius(20)             # Corner radius in pixels
    .set_blur(30)               # Blur intensity (ghostBlur mode only)
    .apply(widget)
```

### InmersiveSplash

```python
InmersiveSplash.create()\
    .set_mode("adaptive")       # "adaptive" or "full"
    .set_color("auto")          # "auto" or hex color
    .set_phrases([...])         # List of status messages
    .on_finish(callback)        # Function to call when done
    .attach_to_window(win, exit_phrases=[...])  # Auto exit splash
    .start()
```

### CustomTitleBar

```python
title_bar = CustomTitleBar(
    parent=window,
    title="My Application",
    icon="🎨"
)
```

### InmojiTrx

```python
# From emoji
InmojiTrx("🐉").apply(app)

# From image file
InmojiTrx("icon.png").apply(app)
```

## 🎯 Requirements

- Python 3.8+
- PyQt5 >= 5.15.0
- Pillow >= 9.0.0
- Windows 10/11 (for blur effects)

## 📄 License

MIT License - feel free to use in your projects!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⭐ Credits

Created by Jesus Quijada
