# Reproductor Jellyfin - Interfaz con Archivos .ui

Este proyecto ha sido convertido para usar archivos .ui de Qt Designer, manteniendo toda la funcionalidad del reproductor original pero con una estructura más modular y fácil de mantener.

## Archivos de la Interfaz

### Archivos .ui
- `main_window.ui` - Ventana principal con toda la interfaz
- `winamp_styles.py` - Estilos CSS para recrear la apariencia de Winamp

### Archivos Python
- `reproductor_gui_ui.py` - Implementación que carga la interfaz desde el archivo .ui
- `reproductor_gui.py` - Implementación original (mantenida como referencia)

## Ventajas de usar archivos .ui

1. **Separación de diseño y lógica**: La interfaz se define en archivos .ui independientes
2. **Fácil edición visual**: Se puede usar Qt Designer para modificar la interfaz
3. **Reutilización**: Los archivos .ui se pueden reutilizar en otros proyectos
4. **Mantenimiento**: Es más fácil mantener y modificar la interfaz
5. **Colaboración**: Los diseñadores pueden trabajar en los archivos .ui sin tocar código

## Cómo usar la nueva interfaz

### Ejecutar el reproductor
```bash
python reproductor_gui_ui.py
```

### Modificar la interfaz
1. Abre `main_window.ui` en Qt Designer
2. Realiza los cambios deseados
3. Guarda el archivo
4. Ejecuta el reproductor para ver los cambios

### Aplicar estilos personalizados
Los estilos Winamp están definidos en `winamp_styles.py` y se pueden aplicar usando:

```python
from winamp_styles import apply_winamp_theme_to_window

# Aplicar tema completo
apply_winamp_theme_to_window(window)

# O aplicar estilos específicos
from winamp_styles import apply_winamp_style
apply_winamp_style(button_widget, "button")
```

## Estructura de la Interfaz

La interfaz está organizada en tres paneles principales:

### Panel Izquierdo
- **Controles principales**: Botones de reproducción, barra de progreso
- **Lista de álbumes**: Búsqueda y visualización de álbumes

### Panel Central
- **Información**: Detalles del álbum y canción actual
- **Controles de audio**: Volumen y balance
- **Acciones**: Botones para manejar álbumes y cola

### Panel Derecho
- **Lista de canciones**: Canciones del álbum seleccionado
- **Cola de reproducción**: Lista de canciones en cola

## Personalización

### Modificar estilos
Edita `winamp_styles.py` para cambiar colores, fuentes y apariencia:

```python
# Cambiar color de fondo
WINAMP_COLORS["background"] = "#1a1a1a"

# Cambiar tamaño de fuente
WINAMP_FONTS["small"] = "10px"
```

### Agregar nuevos widgets
1. Abre `main_window.ui` en Qt Designer
2. Agrega el nuevo widget
3. Dale un nombre único (objectName)
4. Conecta las señales en `reproductor_gui_ui.py`

### Agregar nuevas funcionalidades
1. Implementa la lógica en `reproductor_gui_ui.py`
2. Conecta las señales de los widgets
3. Actualiza la interfaz según sea necesario

## Requisitos

- Python 3.6+
- PyQt5
- python-vlc
- Qt Designer (para editar archivos .ui)

## Instalación

```bash
pip install PyQt5 python-vlc
```

## Diferencias con la versión original

| Aspecto | Versión Original | Versión .ui |
|---------|------------------|-------------|
| Definición de interfaz | Código Python | Archivos .ui |
| Edición de interfaz | Modificar código | Qt Designer |
| Separación de responsabilidades | Mezclada | Clara |
| Mantenimiento | Más complejo | Más simple |
| Reutilización | Limitada | Alta |

## Migración desde la versión original

Si tienes código que usa la versión original:

1. Reemplaza las importaciones:
   ```python
   # Antes
   from reproductor_gui import ReproductorJellyfin
   
   # Después
   from reproductor_gui_ui import ReproductorJellyfinUI
   ```

2. Actualiza la creación de la ventana:
   ```python
   # Antes
   window = ReproductorJellyfin()
   
   # Después
   window = ReproductorJellyfinUI()
   ```

3. Los nombres de los widgets pueden haber cambiado, consulta `main_window.ui` para los nombres actuales.

## Solución de problemas

### Error al cargar archivo .ui
- Asegúrate de que `main_window.ui` esté en el mismo directorio
- Verifica que PyQt5 esté instalado correctamente

### Estilos no se aplican
- Verifica que `winamp_styles.py` esté en el mismo directorio
- Asegúrate de que los nombres de los widgets coincidan

### Funcionalidad faltante
- Compara `reproductor_gui.py` con `reproductor_gui_ui.py`
- Verifica que todas las señales estén conectadas

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Modifica los archivos .ui según sea necesario
4. Actualiza la documentación
5. Envía un pull request

## Licencia

Este proyecto mantiene la misma licencia que el proyecto original. 