# -*- coding: utf-8 -*-
"""
install_worker.py - Worker thread para la instalación del paquete
"""

import sys
import subprocess
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

from installer_classes.i18n_manager import I18nManager
from installer_classes.utils import check_internet_connection

i18n = I18nManager()


class InstallWorker(QThread):
    """Worker thread que ejecuta la instalación sin bloquear la UI"""
    
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    log = pyqtSignal(str, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, options):
        super().__init__()
        self.options = options
        self.python_exe = sys.executable
        
    def run(self):
        """Ejecuta el proceso de instalación"""
        try:
            success = self._install()
            self.finished.emit(success, "")
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def _run_command(self, cmd, desc, progress_val):
        """Ejecuta un comando de subprocess y reporta progreso"""
        self.status.emit(desc)
        self.log.emit(f"> {' '.join(cmd)}", desc)
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, startupinfo=startupinfo
        )
        
        output = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                output.append(line.strip())
                self.log.emit('\n'.join(output[-5:]), desc)
        
        if process.returncode != 0:
            raise Exception(f"\n".join(output[-10:]))
        
        self.progress.emit(progress_val)
    
    def _install(self):
        """Proceso completo de instalación"""
        # 1. Dependencias base (0-20%)
        if self.options.get('upgrade_deps', True):
            self._run_command(
                [self.python_exe, "-m", "pip", "install", "PyQt6", "Pillow", "--upgrade"],
                i18n.get("install_deps"), 20
            )
        else:
            self.progress.emit(20)
        
        # 2. Instalar leviathan-ui (20-80%)
        install_mode = self.options.get('install_mode', 'local')
        
        if install_mode == 'local':
            dist_dir = Path("dist")
            whl_files = list(dist_dir.glob("*.whl")) if dist_dir.exists() else []
            
            if not whl_files:
                raise Exception(i18n.get("error_no_whl"))
            
            for idx, whl in enumerate(whl_files):
                progress = 20 + int((idx + 1) / len(whl_files) * 60)
                force = ["--force-reinstall"] if self.options.get('force', False) else []
                self._run_command(
                    [self.python_exe, "-m", "pip", "install", str(whl)] + force,
                    f"Instalando {whl.name}...", progress
                )
        else:
            # Remoto desde PyPI
            if not check_internet_connection():
                raise Exception(i18n.get("error_no_internet"))
            
            self._run_command(
                [self.python_exe, "-m", "pip", "install", "leviathan-ui", "--upgrade"],
                i18n.get("install_package"), 80
            )
        
        # 3. Crear atajos si se solicitaron (80-95%)
        if self.options.get('desktop_shortcut', False):
            self._create_shortcut("desktop")
        if self.options.get('startmenu_shortcut', False):
            self._create_shortcut("startmenu")
        
        self.progress.emit(95)
        
        # 4. Verificación final (95-100%)
        self._run_command(
            [self.python_exe, "-c", "import leviathan_ui; print('OK')"],
            i18n.get("install_finish"), 100
        )
        
        return True
    
    def _create_shortcut(self, location):
        """Crear accesos directos de demostración"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            if location == "desktop":
                path = winshell.desktop()
            else:
                path = winshell.programs()
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(Path(path) / "Leviathan-UI Demo.lnk"))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = "-c \"from leviathan_ui import InmersiveSplash; print('Demo')\""
            shortcut.WorkingDirectory = str(Path.home())
            shortcut.IconLocation = sys.executable
            shortcut.save()
        except:
            pass  # Opcional, no crítico
