# -*- coding: utf-8 -*-
"""
i18n_manager.py - Sistema de internacionalización del instalador
Soporta: Español (es), English (en), Português (pt), Français (fr), Deutsch (de)
"""

import locale
import os


class I18nManager:
    """Gestor de internacionalización con soporte multi-idioma"""
    
    SUPPORTED_LANGS = ['es', 'en', 'pt', 'fr', 'de']
    
    def __init__(self, lang=None):
        self.current_lang = lang or self._detect_system_lang()
        self.translations = self._load_translations()
        self.lang_data = self.translations.get(self.current_lang, self.translations['es'])
        
    def _detect_system_lang(self) -> str:
        """Detecta el idioma del sistema operativo"""
        try:
            system_lang = locale.getdefaultlocale()[0]
            if system_lang:
                lang_code = system_lang[:2].lower()
                if lang_code in self.SUPPORTED_LANGS:
                    return lang_code
        except:
            pass
        return 'es'  # Default español
    
    def _load_translations(self) -> dict:
        """Carga todas las traducciones disponibles"""
        return {
            'es': self._get_spanish(),
            'en': self._get_english(),
            'pt': self._get_portuguese(),
            'fr': self._get_french(),
            'de': self._get_german(),
        }
    
    def _get_spanish(self) -> dict:
        return {
            "welcome_title": "Bienvenido al Instalador de Leviathan-UI",
            "welcome_subtitle": "Este asistente instalará Leviathan-UI v1.0.5 en tu sistema.",
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
            "finish_subtitle": "Leviathan-UI v1.0.5 se ha instalado correctamente.",
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
    
    def _get_english(self) -> dict:
        return {
            "welcome_title": "Welcome to Leviathan-UI Installer",
            "welcome_subtitle": "This wizard will install Leviathan-UI v1.0.5 on your system.",
            "welcome_desc": "Leviathan-UI is a premium PyQt6 framework for creating modern Windows 11 style applications.",
            "options_title": "Installation Options",
            "options_subtitle": "Customize the installation according to your needs:",
            "opt_install_mode": "Installation mode:",
            "opt_local": "Local (from .whl files in dist/)",
            "opt_remote": "Remote (from PyPI - requires internet)",
            "opt_shortcuts": "Create shortcuts:",
            "opt_desktop": "On desktop",
            "opt_startmenu": "In start menu",
            "opt_advanced": "Advanced options:",
            "opt_force": "Force reinstallation",
            "opt_upgrade": "Upgrade dependencies",
            "install_title": "Installing Leviathan-UI",
            "install_subtitle": "Please wait while the framework is being installed...",
            "install_preparing": "Preparing installation...",
            "install_deps": "Installing dependencies...",
            "install_package": "Installing package...",
            "install_finish": "Finalizing...",
            "finish_title": "Installation Complete",
            "finish_subtitle": "Leviathan-UI v1.0.5 has been successfully installed.",
            "finish_desc": "You can start using the framework immediately.",
            "btn_next": "Next",
            "btn_back": "Back",
            "btn_cancel": "Cancel",
            "btn_install": "Install",
            "btn_finish": "Finish",
            "btn_close": "Close",
            "error_title": "Installation Error",
            "error_no_whl": "No .whl files found in dist/\nSelect remote mode or build the package first.",
            "error_no_internet": "No internet connection\nSelect local mode or check your connection.",
            "error_install": "Installation failed. Check the log for details.",
            "single_instance": "The installer is already running.",
        }
    
    def _get_portuguese(self) -> dict:
        return {
            "welcome_title": "Bem-vindo ao Instalador Leviathan-UI",
            "welcome_subtitle": "Este assistente instalará Leviathan-UI v1.0.5 no seu sistema.",
            "welcome_desc": "Leviathan-UI é um framework premium PyQt6 para criar aplicações modernas com estilo Windows 11.",
            "options_title": "Opções de Instalação",
            "options_subtitle": "Personalize a instalação de acordo com suas necessidades:",
            "opt_install_mode": "Modo de instalação:",
            "opt_local": "Local (de arquivos .whl em dist/)",
            "opt_remote": "Remoto (do PyPI - requer internet)",
            "opt_shortcuts": "Criar atalhos:",
            "opt_desktop": "Na área de trabalho",
            "opt_startmenu": "No menu iniciar",
            "opt_advanced": "Opções avançadas:",
            "opt_force": "Forçar reinstalação",
            "opt_upgrade": "Atualizar dependências",
            "install_title": "Instalando Leviathan-UI",
            "install_subtitle": "Por favor aguarde enquanto o framework é instalado...",
            "install_preparing": "Preparando instalação...",
            "install_deps": "Instalando dependências...",
            "install_package": "Instalando pacote...",
            "install_finish": "Finalizando...",
            "finish_title": "Instalação Completa",
            "finish_subtitle": "Leviathan-UI v1.0.5 foi instalado com sucesso.",
            "finish_desc": "Você pode começar a usar o framework imediatamente.",
            "btn_next": "Próximo",
            "btn_back": "Voltar",
            "btn_cancel": "Cancelar",
            "btn_install": "Instalar",
            "btn_finish": "Finalizar",
            "btn_close": "Fechar",
            "error_title": "Erro de Instalação",
            "error_no_whl": "Nenhum arquivo .whl encontrado em dist/\nSelecione modo remoto ou compile o pacote primeiro.",
            "error_no_internet": "Sem conexão com a internet\nSelecione modo local ou verifique sua conexão.",
            "error_install": "Falha na instalação. Verifique o log para detalhes.",
            "single_instance": "O instalador já está em execução.",
        }
    
    def _get_french(self) -> dict:
        return {
            "welcome_title": "Bienvenue dans l'Installateur Leviathan-UI",
            "welcome_subtitle": "Cet assistant installera Leviathan-UI v1.0.5 sur votre système.",
            "welcome_desc": "Leviathan-UI est un framework PyQt6 premium pour créer des applications modernes avec style Windows 11.",
            "options_title": "Options d'Installation",
            "options_subtitle": "Personnalisez l'installation selon vos besoins:",
            "opt_install_mode": "Mode d'installation:",
            "opt_local": "Local (depuis fichiers .whl dans dist/)",
            "opt_remote": "Remote (depuis PyPI - nécessite internet)",
            "opt_shortcuts": "Créer raccourcis:",
            "opt_desktop": "Sur le bureau",
            "opt_startmenu": "Dans le menu démarrer",
            "opt_advanced": "Options avancées:",
            "opt_force": "Forcer réinstallation",
            "opt_upgrade": "Mettre à jour dépendances",
            "install_title": "Installation Leviathan-UI",
            "install_subtitle": "Veuillez attendre pendant l'installation du framework...",
            "install_preparing": "Préparation de l'installation...",
            "install_deps": "Installation des dépendances...",
            "install_package": "Installation du paquet...",
            "install_finish": "Finalisation...",
            "finish_title": "Installation Terminée",
            "finish_subtitle": "Leviathan-UI v1.0.5 a été installé avec succès.",
            "finish_desc": "Vous pouvez commencer à utiliser le framework immédiatement.",
            "btn_next": "Suivant",
            "btn_back": "Retour",
            "btn_cancel": "Annuler",
            "btn_install": "Installer",
            "btn_finish": "Terminer",
            "btn_close": "Fermer",
            "error_title": "Erreur d'Installation",
            "error_no_whl": "Aucun fichier .whl trouvé dans dist/\nSélectionnez mode remote ou compilez d'abord.",
            "error_no_internet": "Pas de connexion internet\nSélectionnez mode local ou vérifiez votre connexion.",
            "error_install": "Installation échouée. Vérifiez le log pour détails.",
            "single_instance": "L'installateur est déjà en cours d'exécution.",
        }
    
    def _get_german(self) -> dict:
        return {
            "welcome_title": "Willkommen beim Leviathan-UI Installer",
            "welcome_subtitle": "Dieser Assistent installiert Leviathan-UI v1.0.5 auf Ihrem System.",
            "welcome_desc": "Leviathan-UI ist ein Premium PyQt6 Framework für moderne Windows 11 Stil Anwendungen.",
            "options_title": "Installationsoptionen",
            "options_subtitle": "Passen Sie die Installation an Ihre Bedürfnisse an:",
            "opt_install_mode": "Installationsmodus:",
            "opt_local": "Lokal (aus .whl Dateien in dist/)",
            "opt_remote": "Remote (von PyPI - benötigt Internet)",
            "opt_shortcuts": "Verknüpfungen erstellen:",
            "opt_desktop": "Auf Desktop",
            "opt_startmenu": "Im Startmenü",
            "opt_advanced": "Erweiterte Optionen:",
            "opt_force": "Neuinstallation erzwingen",
            "opt_upgrade": "Abhängigkeiten aktualisieren",
            "install_title": "Leviathan-UI wird installiert",
            "install_subtitle": "Bitte warten Sie während das Framework installiert wird...",
            "install_preparing": "Installation wird vorbereitet...",
            "install_deps": "Abhängigkeiten werden installiert...",
            "install_package": "Paket wird installiert...",
            "install_finish": "Finalisierung...",
            "finish_title": "Installation Abgeschlossen",
            "finish_subtitle": "Leviathan-UI v1.0.5 wurde erfolgreich installiert.",
            "finish_desc": "Sie können das Framework sofort verwenden.",
            "btn_next": "Weiter",
            "btn_back": "Zurück",
            "btn_cancel": "Abbrechen",
            "btn_install": "Installieren",
            "btn_finish": "Beenden",
            "btn_close": "Schließen",
            "error_title": "Installationsfehler",
            "error_no_whl": "Keine .whl Dateien in dist/ gefunden\nWählen Sie Remote-Modus oder erstellen Sie das Paket.",
            "error_no_internet": "Keine Internetverbindung\nWählen Sie Lokal-Modus oder prüfen Sie Ihre Verbindung.",
            "error_install": "Installation fehlgeschlagen. Prüfen Sie das Log für Details.",
            "single_instance": "Der Installer läuft bereits.",
        }
    
    def get(self, key: str, default: str = "") -> str:
        """Obtener texto traducido por clave
        
        Args:
            key: Clave de traducción
            default: Valor por defecto si no existe
            
        Returns:
            Texto traducido o valor por defecto
        """
        try:
            return self.lang_data.get(key, default)
        except Exception:
            return default
    
    def set_language(self, lang: str) -> bool:
        """Cambiar idioma activo
        
        Args:
            lang: Código de idioma (es, en, pt, fr, de)
            
        Returns:
            True si el cambio fue exitoso, False en caso contrario
        """
        try:
            if lang in self.SUPPORTED_LANGS:
                self.current_lang = lang
                self.lang_data = self.translations[lang]
                return True
            return False
        except Exception:
            return False
    
    def get_supported_languages(self) -> list:
        """Retorna lista de idiomas soportados"""
        return self.SUPPORTED_LANGS.copy()
