#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leviathan-ui.py - Entry point principal de Leviathan-UI v1.0.5
SetupDialogs - Sistema de instaladores profesionales
"""

import sys
import os
import re
from pathlib import Path

# Asegurar que el directorio actual está en el path para imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer, Qt
    
    from leviathan_ui.splash import InmersiveSplash
    from installer_classes.leviathan_setup import LeviathanSetup
    from leviathan_ui import __version__
except ImportError as e:
    print(f"❌ Error: Dependencia faltante - {e}")
    print("   Asegúrate de tener instalado: pip install PyQt6 Pillow")
    sys.exit(1)

def show_version():
    """Mostrar versión"""
    print("🐉 Leviathan-UI v1.0.5")
    print("   SetupDialogs - Sistema de instaladores profesionales")
    print("   2024 Jesus Quijada - MIT License")
    sys.exit(0)

def launch_gui():
    """Lanzar instalador GUI de leviathan-ui con splash integrado"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QToolTip {
            background: #1a1a2e;
            color: white;
            border: 1px solid #333;
            padding: 5px;
        }
    """)

    # Crear ventana principal con splash integrado
    window = LeviathanSetup()

    # Crear splash en modo APPX (embedded) - se integra en la ventana principal
    splash = InmersiveSplash(
        title="Leviathan-UI",
        subtitle="v1.0.5 Setup",
        logo="app/app-icon.ico",
        color="#1a1a2e",
        accent_color="#00d4aa",
        splash_type="APPX",
        show_progress=False  # Deshabilitar marquee progress bar
    )

    # Adjuntar splash al contenedor de contenido
    # El splash cubre solo el área de páginas, dejando visible titlebar y buttonbar
    splash.attach_to_main_window(window, window.content_container)

    # Mostrar ventana (el splash está encima como overlay)
    window.show()

    # Desvanecer splash después de 2.5 segundos
    def finish_splash():
        splash.finish_loading(0)  # Inicia fade out inmediatamente

    QTimer.singleShot(2500, finish_splash)

    return app.exec()

def parse_legacy_args(args):
    parsed = {}
    
    for arg in args:
        # Pattern: key="value" o key='value' o key=value
        match = re.match(r'^(\w+)=(["\']?)(.+?)\2$', arg)
        if match:
            key, _, value = match.groups()
            parsed[key] = value
        elif arg.startswith('--'):
            # Pattern: --key=value
            if '=' in arg:
                key, value = arg[2:].split('=', 1)
                parsed[key] = value
            else:
                parsed[arg[2:]] = True
        elif not arg.startswith('-'):
            # Positional command
            parsed['_command'] = arg
    
    return parsed

def show_error_dialog(title, message):
    """Muestra un error incluso si PyQt6 no está disponible"""
    try:
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()
    except:
        print(f"\n{'='*50}")
        print(f"ERROR: {title}")
        print(f"{'='*50}")
        print(message)
        print(f"{'='*50}\n")
    
def main():
    """Punto de entrada principal con manejo global de excepciones"""
    try:
        args = sys.argv[1:]
        
        if not args:
            # Sin argumentos: lanzar GUI
            sys.exit(launch_gui())
        
        # --version o -v
        if '--version' in args or '-v' in args:
            show_version()
        
        # Parsear argumentos legacy
        parsed = parse_legacy_args(args)
        
        command = parsed.get('_command') or parsed.get('configure')
        
        # Si no hay comando claro, mostrar ayuda
        if not command:
            from leviathan_ui.cli import LeviathanCLI
            cli = LeviathanCLI()
            return cli.run(['--help'])
        
        # Determinar qué comando ejecutar
        cli_args = []
        
        if command in ('configure', 'activepath', 'showStatus', 'start', 'precompile', 'compile', 'packageStart'):
            from leviathan_ui.cli import LeviathanCLI
            cli = LeviathanCLI()
            
            if command == 'configure':
                cli_args = ['configure']
                name = parsed.get('configure') or parsed.get('name', 'MiInstalador')
                cli_args.append(name)
                if 'requires' in parsed:
                    cli_args.extend(['--requires', parsed['requires']])
                if 'gpumode' in parsed:
                    cli_args.extend(['--gpumode', parsed['gpumode']])
            
            elif command == 'precompile':
                cli_args = ['precompile']
                if 'file' in parsed:
                    cli_args.append(parsed['file'])
                else:
                    cli_args.append('setup.ls')
            
            elif command == 'compile':
                cli_args = ['compile']
                if 'file' in parsed:
                    cli_args.append(parsed['file'])
                else:
                    cli_args.append('setup.lsx')
                if 'icon' in parsed:
                    cli_args.extend(['--icon', parsed['icon']])
            
            elif command == 'packageStart':
                cli_args = ['pack']
                if 'file' in parsed:
                    cli_args.append(parsed['file'])
            
            else:
                # Comandos legacy sin argumentos
                cli_map = {
                    'activepath': 'install',
                    'showStatus': 'status', 
                    'start': 'run'
                }
                cli_args = [cli_map.get(command, command)]
            
            return cli.run(cli_args)
        else:
            # Comando desconocido o nombre de proyecto
            from leviathan_ui.cli import LeviathanCLI
            cli = LeviathanCLI()
            cli_args = ['configure', command]
            return cli.run(cli_args)
    
    except KeyboardInterrupt:
        print("\n⚠️  Operación cancelada por el usuario")
        return 130
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        try:
            show_error_dialog("Error Crítico", error_msg)
        except:
            print(f"\n{'='*50}")
            print(f"ERROR CRÍTICO: {error_msg}")
            print(f"{'='*50}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
