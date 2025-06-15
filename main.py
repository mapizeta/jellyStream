#!/usr/bin/env python3
"""
Reproductor de música Jellyfin
==============================

Aplicación para reproducir música desde un servidor Jellyfin usando PyQt5 y VLC.
Versión con interfaz basada en archivos .ui para mejor mantenimiento.

Uso:
    python main.py

Configuración:
    Modifica las variables en jellyfin_api.py para configurar tu servidor Jellyfin.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication
from reproductor_gui_ui import ReproductorJellyfinUI
from jellyfin_api import DEFAULT_CONFIG

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    missing_deps = []
    
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")
    
    try:
        import vlc
    except ImportError:
        missing_deps.append("python-vlc")
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    if missing_deps:
        print("❌ Faltan las siguientes dependencias:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstala las dependencias con:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    
    return True

def show_config_info():
    """Muestra información sobre la configuración actual"""
    print("🎵 Reproductor Jellyfin - Versión UI")
    print("=" * 40)
    print(f"Servidor: {DEFAULT_CONFIG['JELLYFIN_URL']}")
    print(f"Usuario ID: {DEFAULT_CONFIG['USER_ID']}")
    print(f"API Key: {DEFAULT_CONFIG['API_KEY'][:8]}...")
    print("Interfaz: Archivos .ui (Qt Designer)")
    print("=" * 40)

def main():
    """Función principal de la aplicación"""
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Mostrar información de configuración
    show_config_info()
    
    # Establecer atributos de Qt antes de crear QApplication
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Crear aplicación
    app = QApplication(sys.argv)
    app.setApplicationName("Reproductor Jellyfin")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Jellyfin Player")
    
    # Configurar estilo
    app.setStyle('Fusion')
    
    try:
        # Crear y mostrar la ventana principal
        gui = ReproductorJellyfinUI()
        gui.show()
        
        # Ejecutar la aplicación
        return app.exec_()
        
    except Exception as e:
        QMessageBox.critical(None, "Error Fatal", 
                           f"Error al iniciar la aplicación:\n{str(e)}")
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 