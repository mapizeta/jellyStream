"""
Estilos Winamp para la interfaz gráfica
Este archivo contiene todos los estilos CSS para recrear la apariencia clásica de Winamp
"""

from PyQt5.QtWidgets import QPushButton, QListWidget, QFrame, QProgressBar, QLabel, QLineEdit, QSlider

# Estilos principales
WINAMP_MAIN_STYLE = """
QMainWindow {
    background-color: #2b2b2b;
    color: #ffffff;
}
"""

WINAMP_FRAME_STYLE = """
QFrame {
    background-color: #2b2b2b;
    border: 2px solid #404040;
    border-radius: 3px;
    color: #ffffff;
}
"""

WINAMP_BUTTON_STYLE = """
QPushButton {
    background-color: #404040;
    border: 1px solid #606060;
    border-radius: 2px;
    color: #ffffff;
    padding: 4px 8px;
    font-size: 9px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #505050;
    border: 1px solid #707070;
}
QPushButton:pressed {
    background-color: #303030;
    border: 1px solid #505050;
}
QPushButton:disabled {
    background-color: #2a2a2a;
    border: 1px solid #404040;
    color: #666666;
}
"""

WINAMP_LIST_STYLE = """
QListWidget {
    background-color: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 2px;
    color: #ffffff;
    font-size: 9px;
    selection-background-color: #404040;
    selection-color: #ffffff;
}
QListWidget::item {
    padding: 2px 4px;
    border-bottom: 1px solid #2a2a2a;
}
QListWidget::item:selected {
    background-color: #404040;
}
QListWidget::item:hover {
    background-color: #303030;
}
"""

WINAMP_PROGRESS_STYLE = """
QProgressBar {
    border: 1px solid #404040;
    border-radius: 2px;
    text-align: center;
    background-color: #1a1a1a;
    color: #ffffff;
    font-size: 8px;
}
QProgressBar::chunk {
    background-color: #00ff00;
    border-radius: 1px;
}
"""

WINAMP_LABEL_STYLE = """
QLabel {
    color: #ffffff;
    font-size: 9px;
    font-weight: bold;
}
"""

WINAMP_LINEEDIT_STYLE = """
QLineEdit {
    background-color: #1a1a1a;
    border: 1px solid #404040;
    color: #ffffff;
    padding: 2px 4px;
    font-size: 9px;
}
"""

WINAMP_SLIDER_STYLE = """
QSlider::groove:horizontal {
    border: 1px solid #404040;
    height: 8px;
    background: #1a1a1a;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #00ff00;
    border: 1px solid #ffffff;
    width: 12px;
    margin: -2px 0;
    border-radius: 6px;
}
"""

# Estilos específicos para diferentes widgets
INFO_LABEL_STYLE = """
QLabel {
    background-color: #1a1a1a;
    border: 1px solid #404040;
    padding: 4px;
    font-size: 10px;
    color: #ffffff;
}
"""

VISUALIZER_STYLE = """
background-color: #000000; 
border: 1px solid #404040;
"""

def apply_winamp_style(widget, style_type="default"):
    """
    Aplica estilos Winamp a un widget específico
    
    Args:
        widget: El widget al que aplicar el estilo
        style_type: Tipo de estilo a aplicar ("button", "list", "frame", etc.)
    """
    style_map = {
        "button": WINAMP_BUTTON_STYLE,
        "list": WINAMP_LIST_STYLE,
        "frame": WINAMP_FRAME_STYLE,
        "progress": WINAMP_PROGRESS_STYLE,
        "label": WINAMP_LABEL_STYLE,
        "lineedit": WINAMP_LINEEDIT_STYLE,
        "slider": WINAMP_SLIDER_STYLE,
        "info_label": INFO_LABEL_STYLE,
        "visualizer": VISUALIZER_STYLE,
        "main": WINAMP_MAIN_STYLE
    }
    
    if style_type in style_map:
        widget.setStyleSheet(style_map[style_type])

def apply_winamp_theme_to_window(window):
    """
    Aplica el tema Winamp completo a una ventana
    
    Args:
        window: La ventana principal a la que aplicar el tema
    """
    # Aplicar estilo principal
    window.setStyleSheet(WINAMP_MAIN_STYLE)
    
    # Buscar y aplicar estilos a widgets específicos
    for child in window.findChildren(QPushButton):
        apply_winamp_style(child, "button")
    
    for child in window.findChildren(QListWidget):
        apply_winamp_style(child, "list")
    
    for child in window.findChildren(QFrame):
        apply_winamp_style(child, "frame")
    
    for child in window.findChildren(QProgressBar):
        apply_winamp_style(child, "progress")
    
    for child in window.findChildren(QLabel):
        apply_winamp_style(child, "label")
    
    for child in window.findChildren(QLineEdit):
        apply_winamp_style(child, "lineedit")
    
    for child in window.findChildren(QSlider):
        apply_winamp_style(child, "slider")

# Colores de la paleta Winamp
WINAMP_COLORS = {
    "background": "#2b2b2b",
    "dark_background": "#1a1a1a",
    "border": "#404040",
    "text": "#ffffff",
    "disabled_text": "#666666",
    "accent": "#00ff00",
    "button_hover": "#505050",
    "button_pressed": "#303030"
}

# Configuración de fuentes
WINAMP_FONTS = {
    "small": "9px",
    "medium": "10px",
    "large": "12px"
} 