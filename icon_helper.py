"""
Helper para manejar íconos del tema y proporcionar fallbacks
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
import os

class IconHelper:
    """Clase para manejar íconos del tema y fallbacks"""
    
    # Mapeo de nombres de íconos del tema a nombres de archivo de respaldo
    ICON_MAPPING = {
        "media-playback-start": "play.png",
        "media-playback-pause": "pause.png", 
        "media-playback-stop": "stop.png",
        "media-skip-forward": "next.png",
        "media-skip-backward": "previous.png",
        "media-playback-pause": "pause.png",
        "media-play": "play.png"
    }
    
    @staticmethod
    def get_icon(theme_name, fallback_path="icons"):
        """
        Obtiene un ícono del tema o usa un fallback
        
        Args:
            theme_name: Nombre del ícono del tema
            fallback_path: Ruta donde buscar íconos de respaldo
            
        Returns:
            QIcon: El ícono encontrado o un ícono vacío
        """
        # Intentar obtener del tema primero
        icon = QIcon.fromTheme(theme_name)
        
        if not icon.isNull():
            return icon
        
        # Si no está disponible en el tema, buscar archivo de respaldo
        fallback_file = IconHelper.ICON_MAPPING.get(theme_name)
        if fallback_file:
            fallback_path_full = os.path.join(fallback_path, fallback_file)
            if os.path.exists(fallback_path_full):
                return QIcon(fallback_path_full)
        
        # Si no hay fallback, devolver ícono vacío
        return QIcon()
    
    @staticmethod
    def apply_theme_icons_to_window(window):
        """
        Aplica íconos del tema a todos los botones de una ventana
        
        Args:
            window: La ventana principal
        """
        # Mapeo de nombres de botones a íconos del tema
        button_icons = {
            "playButton": "media-playback-start",
            "pauseButton": "media-playback-pause", 
            "stopButton": "media-playback-stop",
            "nextButton": "media-skip-forward",
            "prevButton": "media-skip-backward",
            "refreshButton": "view-refresh",
            "minimizeButton": "window-minimize"
        }
        
        for button_name, icon_name in button_icons.items():
            if hasattr(window, button_name):
                button = getattr(window, button_name)
                if isinstance(button, QPushButton):
                    icon = IconHelper.get_icon(icon_name)
                    if not icon.isNull():
                        button.setIcon(icon)
                        # Si el botón tiene texto, ocultarlo para mostrar solo el ícono
                        if button.text() in ["▶", "⏸", "⏹", "⏭", "⏮", "🔄", "_"]:
                            button.setText("")
    
    @staticmethod
    def check_theme_availability():
        """
        Verifica qué íconos del tema están disponibles
        
        Returns:
            dict: Diccionario con el estado de cada ícono
        """
        availability = {}
        test_icons = [
            "media-playback-start",
            "media-playback-pause", 
            "media-playback-stop",
            "media-skip-forward",
            "media-skip-backward",
            "view-refresh",
            "window-minimize"
        ]
        
        for icon_name in test_icons:
            icon = QIcon.fromTheme(icon_name)
            availability[icon_name] = not icon.isNull()
        
        return availability

def print_icon_status():
    """Imprime el estado de los íconos del tema"""
    availability = IconHelper.check_theme_availability()
    
    print("📋 Estado de íconos del tema:")
    for icon_name, available in availability.items():
        status = "✅" if available else "❌"
        print(f"  {status} {icon_name}")
    
    return availability 