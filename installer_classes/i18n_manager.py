# -*- coding: utf-8 -*-
"""
i18n_manager.py - Sistema de internacionalización del instalador
"""

class I18nManager:
    """Gestor de internacionalización simplificado"""
    
    def __init__(self):
        self.lang_data = {
            # Español por defecto
            "welcome_title": "Bienvenido al Instalador de Leviathan-UI",
            "welcome_subtitle": "Este asistente instalará Leviathan-UI v1.0.4 en tu sistema.",
            "welcome_desc": "Leviathan-UI es un framework premium de PyQt6 para crear aplicaciones modernas con estilo Windows 11.",
            "options_title": "Opciones de Instalación",
            "options_subtitle": "Personaliza la instalación según tus necesidades:",
            "opt_install_mode": "Modo de instalación:",
            "opt_local": "Local (desde archivos .whl en dist/)",
            "opt_remote": "Remoto (desde PyPI - requiere internet)",
            "opt_shortcuts": "Crear accesos directos:",
            "opt_desktop": "En el escritorio",
            "opt_startmenu": "En el menú de inicio",
            "opt_advanced": "Opciones avanzadas:",
            "opt_force": "Forzar reinstalación",
            "opt_upgrade": "Actualizar dependencias",
            "install_title": "Instalando Leviathan-UI",
            "install_subtitle": "Por favor espera mientras se instala el framework...",
            "install_preparing": "Preparando instalación...",
            "install_deps": "Instalando dependencias...",
            "install_package": "Instalando paquete...",
            "install_finish": "Finalizando...",
            "finish_title": "Instalación Completada",
            "finish_subtitle": "Leviathan-UI v1.0.4 se ha instalado correctamente.",
            "finish_desc": "Puedes comenzar a usar el framework inmediatamente.",
            "btn_next": "Siguiente",
            "btn_back": "Atrás",
            "btn_cancel": "Cancelar",
            "btn_install": "Instalar",
            "btn_finish": "Finalizar",
            "btn_close": "Cerrar",
            "error_title": "Error de Instalación",
            "error_no_whl": "No se encontraron archivos .whl en dist/\nSelecciona modo remoto o compila el paquete primero.",
            "error_no_internet": "No hay conexión a internet\nSelecciona modo local o verifica tu conexión.",
            "error_install": "Falló la instalación. Revisa el log para más detalles.",
            "single_instance": "El instalador ya está en ejecución.",
        }
        
    def get(self, key, default=""):
        """Obtener texto traducido por clave"""
        return self.lang_data.get(key, default)
