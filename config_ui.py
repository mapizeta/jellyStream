# Configuración para la versión con archivos .ui
# Este archivo contiene configuraciones para personalizar el comportamiento del reproductor

# Configuración de la interfaz
INTERFACE_CONFIG = {
    "window_title": "Reproductor Jellyfin - Estilo Winamp",
    "window_size": (1000, 700),
    "theme": "winamp",
    "auto_connect": True,
    "show_visualizer": True,
    "enable_high_dpi": True
}

# Configuración de estilos
STYLE_CONFIG = {
    "apply_winamp_theme": True,
    "custom_colors": {
        "background": "#2b2b2b",
        "dark_background": "#1a1a1a",
        "border": "#404040",
        "text": "#ffffff",
        "accent": "#00ff00"
    },
    "font_sizes": {
        "small": "9px",
        "medium": "10px",
        "large": "12px"
    }
}

# Configuración de funcionalidad
FEATURE_CONFIG = {
    "enable_visualizer": True,
    "enable_search": True,
    "enable_shuffle": True,
    "auto_play_next": True,
    "show_progress_bar": True,
    "enable_volume_control": True,
    "enable_balance_control": True
}

# Configuración de reproducción
PLAYBACK_CONFIG = {
    "default_volume": 100,
    "default_balance": 0,
    "auto_advance": True,
    "fade_duration": 0.5,
    "cache_duration": 1.5
}

# Configuración de la interfaz de usuario
UI_CONFIG = {
    "show_album_art": False,  # Futura funcionalidad
    "show_lyrics": False,      # Futura funcionalidad
    "enable_dark_mode": True,
    "enable_animations": True,
    "show_tooltips": True
}

def get_config():
    """
    Retorna la configuración completa
    """
    return {
        "interface": INTERFACE_CONFIG,
        "style": STYLE_CONFIG,
        "features": FEATURE_CONFIG,
        "playback": PLAYBACK_CONFIG,
        "ui": UI_CONFIG
    }

def update_config(section, key, value):
    """
    Actualiza una configuración específica
    
    Args:
        section: Sección de configuración ('interface', 'style', etc.)
        key: Clave a actualizar
        value: Nuevo valor
    """
    if section == "interface" and key in INTERFACE_CONFIG:
        INTERFACE_CONFIG[key] = value
    elif section == "style" and key in STYLE_CONFIG:
        STYLE_CONFIG[key] = value
    elif section == "features" and key in FEATURE_CONFIG:
        FEATURE_CONFIG[key] = value
    elif section == "playback" and key in PLAYBACK_CONFIG:
        PLAYBACK_CONFIG[key] = value
    elif section == "ui" and key in UI_CONFIG:
        UI_CONFIG[key] = value
    else:
        raise ValueError(f"Configuración no válida: {section}.{key}")

def apply_config_to_window(window):
    """
    Aplica la configuración a una ventana del reproductor
    
    Args:
        window: Instancia de ReproductorJellyfinUI
    """
    # Aplicar configuración de interfaz
    if INTERFACE_CONFIG.get("window_title"):
        window.setWindowTitle(INTERFACE_CONFIG["window_title"])
    
    if INTERFACE_CONFIG.get("window_size"):
        window.resize(*INTERFACE_CONFIG["window_size"])
    
    # Aplicar configuración de reproducción
    if hasattr(window, 'volumeSlider'):
        window.volumeSlider.setValue(PLAYBACK_CONFIG.get("default_volume", 100))
    
    if hasattr(window, 'balanceSlider'):
        window.balanceSlider.setValue(PLAYBACK_CONFIG.get("default_balance", 0))
    
    # Aplicar configuración de funcionalidad
    if hasattr(window, 'visualizer'):
        window.visualizer.setVisible(FEATURE_CONFIG.get("enable_visualizer", True))
    
    if hasattr(window, 'progressBar'):
        window.progressBar.setVisible(FEATURE_CONFIG.get("show_progress_bar", True)) 