# 🎵 Reproductor Jellyfin

Un reproductor de música moderno que se conecta a tu servidor Jellyfin para reproducir música de forma fácil y elegante. **Versión 2.0 con interfaz basada en archivos .ui para mejor mantenimiento y personalización.**

## ✨ Características

- **Conexión directa a Jellyfin**: Reproduce música directamente desde tu servidor Jellyfin
- **Interfaz moderna**: Diseño limpio y fácil de usar con PyQt5
- **Arquitectura modular**: Interfaz separada en archivos .ui para fácil edición
- **Estilo Winamp clásico**: Apariencia retro con colores y diseño clásico
- **Lista de álbumes**: Navega por todos tus álbumes de música
- **Búsqueda en tiempo real**: Encuentra álbumes rápidamente
- **Reproducción en cola**: Agrega canciones individuales o álbumes completos
- **Controles de reproducción**: Play, pause, siguiente, anterior, stop
- **Barra de progreso**: Visualiza el progreso de la canción actual
- **Visualizador**: Simulación de visualizador de espectro estilo Winamp
- **Información detallada**: Muestra título, artista, duración y más

## 🚀 Instalación

### Requisitos previos

- Python 3.7 o superior
- VLC Media Player instalado en tu sistema
- Un servidor Jellyfin funcionando
- Qt Designer (opcional, para editar la interfaz)

### Instalación de dependencias

1. Clona o descarga este repositorio
2. Instala las dependencias de Python:

```bash
pip install -r requirements.txt
```

O instala manualmente:


### Configuración

1. Abre el archivo `jellyfin_api.py`
2. Modifica las siguientes variables con tu configuración:

```python
DEFAULT_CONFIG = {
    "JELLYFIN_URL": "http://tu-servidor-jellyfin:8096",  # URL de tu servidor
    "API_KEY": "tu-api-key-aqui",                        # Tu API key de Jellyfin
    "USER_ID": "tu-user-id-aqui"                         # Tu ID de usuario
}
```

#### Cómo obtener tu API Key y User ID:

1. **API Key**: Ve a tu servidor Jellyfin → Dashboard → API Keys → Crear nueva API key
2. **User ID**: Ve a tu perfil de usuario en Jellyfin y copia el ID de la URL

## 🎮 Uso

### Ejecutar la aplicación

```bash
python main.py
```

O directamente:

```bash
python reproductor_gui_ui.py
```

### Cómo usar la aplicación

1. **Conectar**: La aplicación se conectará automáticamente a tu servidor Jellyfin
2. **Navegar**: Usa el panel izquierdo para navegar por tus álbumes
3. **Buscar**: Escribe en el campo de búsqueda para filtrar álbumes
4. **Seleccionar**: Haz clic en un álbum para ver sus canciones
5. **Reproducir**: 
   - Doble clic en una canción para reproducirla inmediatamente
   - Usa "Agregar todo el álbum" para agregar todas las canciones a la cola
6. **Controlar**: Usa los botones de control para manejar la reproducción

## 📁 Estructura del proyecto

```
reproductor/
├── main.py                    # Archivo principal de la aplicación
├── jellyfin_api.py           # Clase para manejar la API de Jellyfin
├── reproductor_gui_ui.py     # Implementación con archivos .ui
├── main_window.ui            # Archivo de interfaz principal
├── winamp_styles.py          # Estilos CSS para apariencia Winamp
├── requirements.txt          # Dependencias de Python
├── README.md                 # Este archivo
├── README_UI.md              # Documentación específica de la versión .ui
├── ejemplo_uso_ui.py         # Ejemplos de uso de la nueva interfaz
└── migrar_a_ui.py            # Script de migración desde versión original
```

## 🎨 Personalización

### Modificar la interfaz

1. Abre `main_window.ui` en Qt Designer
2. Realiza los cambios deseados
3. Guarda el archivo
4. Ejecuta la aplicación para ver los cambios

### Personalizar estilos

Edita `winamp_styles.py` para cambiar colores, fuentes y apariencia:

```python
# Cambiar color de fondo
WINAMP_COLORS["background"] = "#1a1a1a"

# Cambiar tamaño de fuente
WINAMP_FONTS["small"] = "10px"
```

### Aplicar estilos personalizados

```python
from winamp_styles import apply_winamp_theme_to_window
apply_winamp_theme_to_window(window)
```

## 🔧 Funcionalidades técnicas

### API de Jellyfin (`jellyfin_api.py`)

- **Conexión segura**: Manejo de sesiones y headers de autenticación
- **Listado de álbumes**: Obtiene todos los álbumes de música
- **Búsqueda**: Filtra álbumes por nombre o artista
- **Información de canciones**: Obtiene detalles completos de cada canción
- **URLs de streaming**: Genera URLs para reproducir música

### Interfaz gráfica (`reproductor_gui_ui.py`)

- **Arquitectura modular**: Interfaz separada en archivos .ui
- **Diseño responsive**: Se adapta a diferentes tamaños de ventana
- **Hilos de trabajo**: Carga datos sin bloquear la interfaz
- **Búsqueda en tiempo real**: Filtra resultados mientras escribes
- **Controles de reproducción**: Interfaz completa para manejar música
- **Visualizador**: Simulación de espectro de audio
- **Manejo de errores**: Mensajes informativos para problemas de conexión

### Estilos Winamp (`winamp_styles.py`)

- **Paleta de colores**: Colores clásicos de Winamp
- **Estilos CSS**: Definiciones de apariencia para todos los widgets
- **Funciones de aplicación**: Métodos para aplicar estilos dinámicamente
- **Configuración de fuentes**: Tamaños y estilos de texto

## 🐛 Solución de problemas

### Error de conexión con Jellyfin

1. Verifica que tu servidor Jellyfin esté funcionando
2. Confirma que la URL, API key y User ID sean correctos
3. Asegúrate de que el puerto 8096 esté abierto
4. Verifica que tu firewall no bloquee la conexión

### Error de VLC

1. Asegúrate de tener VLC Media Player instalado
2. Verifica que `python-vlc` esté instalado correctamente
3. En Windows, asegúrate de que VLC esté en el PATH del sistema

### Problemas con archivos .ui

1. Verifica que `main_window.ui` esté en el mismo directorio
2. Asegúrate de que PyQt5 esté instalado correctamente
3. Usa Qt Designer para verificar que el archivo .ui sea válido

### Problemas de reproducción

1. Verifica tu conexión a internet
2. Confirma que los archivos de música estén disponibles en Jellyfin
3. Revisa que las URLs de streaming sean accesibles

## 🔄 Migración desde versión anterior

Si tienes código que usa la versión anterior:

```python
# Antes
from reproductor_gui import ReproductorJellyfin
window = ReproductorJellyfin()

# Después
from reproductor_gui_ui import ReproductorJellyfinUI
window = ReproductorJellyfinUI()
```

Ejecuta `python migrar_a_ui.py` para obtener ayuda detallada con la migración.

## 📝 Notas adicionales

- La aplicación usa VLC como motor de reproducción para mejor compatibilidad
- El caché de red está configurado para 1.5 segundos para mejor rendimiento
- Las canciones se reproducen automáticamente en secuencia
- Puedes agregar múltiples álbumes a la cola de reproducción
- La interfaz se puede editar visualmente con Qt Designer
- Los estilos están separados para fácil personalización

## 🤝 Contribuciones

Si encuentras algún problema o tienes sugerencias de mejora, no dudes en crear un issue o enviar un pull request.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT. 