#!/usr/bin/env python3
"""
Script para crear íconos simples usando caracteres Unicode
Estos íconos se usarán como fallback cuando los íconos del tema no estén disponibles
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(text, filename, size=(24, 24), bg_color=(64, 64, 64), text_color=(255, 255, 255)):
    """
    Crea un ícono simple con texto
    
    Args:
        text: Texto a mostrar en el ícono
        filename: Nombre del archivo a guardar
        size: Tamaño del ícono (ancho, alto)
        bg_color: Color de fondo (R, G, B)
        text_color: Color del texto (R, G, B)
    """
    # Crear imagen
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Intentar usar una fuente del sistema, o usar la predeterminada
    try:
        # En Windows, intentar usar Segoe UI
        font = ImageFont.truetype("segoeui.ttf", 16)
    except:
        try:
            # Alternativa: Arial
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            # Última opción: fuente predeterminada
            font = ImageFont.load_default()
    
    # Calcular posición del texto para centrarlo
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Dibujar texto
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Guardar imagen
    img.save(filename, 'PNG')
    print(f"✅ Creado: {filename}")

def main():
    """Función principal"""
    print("🎨 Creando íconos de respaldo...")
    
    # Crear directorio icons si no existe
    if not os.path.exists('icons'):
        os.makedirs('icons')
        print("📁 Creado directorio 'icons'")
    
    # Definir íconos a crear
    icons = {
        'play.png': '▶',
        'pause.png': '⏸',
        'stop.png': '⏹',
        'next.png': '⏭',
        'previous.png': '⏮',
        'refresh.png': '🔄',
        'minimize.png': '−'
    }
    
    # Crear cada ícono
    for filename, symbol in icons.items():
        filepath = os.path.join('icons', filename)
        create_icon(symbol, filepath)
    
    print("\n🎉 ¡Íconos creados exitosamente!")
    print("📁 Los íconos están en la carpeta 'icons/'")
    print("🔄 Ejecuta la aplicación para ver los íconos en acción")

if __name__ == "__main__":
    main() 