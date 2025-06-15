# Configuración de Qt Creator para PyQt5

## Pasos para evitar errores de sintaxis:

### 1. **Configurar versión de Qt en Qt Creator:**
1. Abre Qt Creator
2. Ve a **Tools** → **Options** → **Kits**
3. En la pestaña **Qt Versions**, asegúrate de que esté seleccionada una versión de Qt 5.x
4. En **Kits**, verifica que el kit activo use Qt 5.x

### 2. **Configurar el proyecto:**
1. En Qt Creator, ve a **Projects** (panel izquierdo)
2. Selecciona tu kit de Qt 5.x
3. En **Build Settings**, asegúrate de que use Qt 5.x

### 3. **Configurar el archivo .ui:**
1. Abre `main_window.ui` en Qt Creator
2. En el panel **Property Editor** (derecha)
3. Para cada QFrame, en la propiedad **frameShape**:
   - Selecciona **Box** (no **QFrame::Shape::Box**)
   - Selecciona **NoFrame** (no **QFrame::Shape::NoFrame**)
4. Para **frameShadow**:
   - Selecciona **Raised** (no **QFrame::Shadow::Raised**)
5. Para **orientation** en QSlider:
   - Selecciona **Horizontal** (no **Qt::Orientation::Horizontal**)
6. Para **alignment** en QLabel:
   - Selecciona **AlignCenter** (no **Qt::AlignmentFlag::AlignCenter**)

### 4. **Guardar configuración:**
- Guarda el archivo .ui
- Los cambios se aplicarán automáticamente

## Alternativa: Script de corrección automática

Si prefieres no cambiar la configuración, puedes usar este script después de cada edición:

```bash
python fix_qt_syntax.py
```

El script corregirá automáticamente todas las referencias de Qt6 a Qt5. 