# Guía de Instalación y Uso - Windows

## 🚀 Instalación Rápida

### Paso 1: Instalar Dependencias
1. Haz doble clic en `instalar_dependencias.bat`
2. Espera a que se instalen todas las dependencias
3. Se crearán automáticamente los íconos de respaldo

### Paso 2: Crear Acceso Directo (Opcional)
1. Haz doble clic en `crear_acceso_directo.bat`
2. Se creará un acceso directo en tu escritorio
3. Ahora puedes ejecutar la app desde el escritorio

### Paso 3: Ejecutar la Aplicación
- **Opción A**: Haz doble clic en `ejecutar_reproductor.bat`
- **Opción B**: Haz doble clic en el acceso directo del escritorio
- **Opción C**: Ejecuta `python main.py` desde la línea de comandos

## 📁 Archivos .bat Incluidos

### `instalar_dependencias.bat`
- Instala Python si no está instalado
- Instala todas las dependencias necesarias
- Crea los íconos de respaldo automáticamente
- **Usar solo la primera vez**

### `ejecutar_reproductor.bat`
- Verifica que todo esté instalado correctamente
- Ejecuta correcciones automáticas si es necesario
- Inicia la aplicación
- **Usar cada vez que quieras ejecutar la app**

### `crear_acceso_directo.bat`
- Crea un acceso directo en el escritorio
- Permite ejecutar la app con un doble clic
- **Usar solo una vez para crear el acceso directo**

## 🔧 Solución de Problemas

### Error: "Python no está instalado"
1. Descarga Python desde https://python.org
2. Instálalo marcando "Add Python to PATH"
3. Ejecuta `instalar_dependencias.bat` nuevamente

### Error: "No se encuentra main.py"
- Asegúrate de ejecutar los archivos .bat desde la carpeta del proyecto
- No muevas los archivos .bat fuera de la carpeta

### Error: "Fallo al instalar dependencias"
1. Verifica tu conexión a internet
2. Ejecuta `pip install --upgrade pip`
3. Ejecuta `instalar_dependencias.bat` nuevamente

### La aplicación no se inicia
1. Ejecuta `python main.py` desde la línea de comandos
2. Revisa los mensajes de error
3. Verifica que VLC esté instalado en tu sistema

## 📋 Requisitos del Sistema

- **Windows 10/11** (probado en Windows 10)
- **Python 3.7+** (se instala automáticamente si es necesario)
- **VLC Media Player** (descargar desde https://vlc.org)
- **Conexión a internet** (para instalar dependencias)

## 🎯 Configuración de Jellyfin

Antes de usar la aplicación, edita `jellyfin_api.py` y configura:
- URL de tu servidor Jellyfin
- API Key
- User ID

## 🎨 Personalización

### Cambiar íconos
1. Reemplaza los archivos en la carpeta `icons/`
2. Usa archivos PNG de 24x24 píxeles
3. Mantén los nombres: `play.png`, `pause.png`, etc.

### Editar interfaz
1. Abre `main_window.ui` en Qt Designer
2. Haz los cambios deseados
3. Ejecuta `python fix_qt_syntax.py` para corregir sintaxis
4. Ejecuta la aplicación

## 📞 Soporte

Si tienes problemas:
1. Revisa los mensajes de error en la consola
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que VLC esté instalado
4. Consulta la documentación en `README.md`

## 🚀 Comandos Avanzados

### Ejecutar desde línea de comandos
```cmd
python main.py
```

### Instalar dependencias manualmente
```cmd
pip install -r requirements.txt
```

### Crear íconos manualmente
```cmd
python create_icons.py
```

### Corregir sintaxis de Qt
```cmd
python fix_qt_syntax.py
``` 