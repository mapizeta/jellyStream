#!/usr/bin/env python3
"""
Script para corregir automáticamente la sintaxis de Qt6 a Qt5 en archivos .ui
Ejecuta este script después de editar archivos .ui en Qt Creator
"""

import os
import sys
import re

def fix_qt_syntax(file_path):
    """
    Corrige la sintaxis de Qt6 a Qt5 en un archivo .ui
    
    Args:
        file_path: Ruta al archivo .ui
    """
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return False
    
    print(f"🔧 Corrigiendo sintaxis en: {file_path}")
    
    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mapeo de correcciones
    corrections = {
        # QFrame
        r'QFrame::Shape::Box': 'QFrame::Box',
        r'QFrame::Shape::NoFrame': 'QFrame::NoFrame',
        r'QFrame::Shadow::Raised': 'QFrame::Raised',
        r'QFrame::Shadow::Sunken': 'QFrame::Sunken',
        r'QFrame::Shadow::Plain': 'QFrame::Plain',
        
        # Qt Orientation
        r'Qt::Orientation::Horizontal': 'Qt::Horizontal',
        r'Qt::Orientation::Vertical': 'Qt::Vertical',
        
        # Qt Alignment
        r'Qt::AlignmentFlag::AlignCenter': 'Qt::AlignCenter',
        r'Qt::AlignmentFlag::AlignLeft': 'Qt::AlignLeft',
        r'Qt::AlignmentFlag::AlignRight': 'Qt::AlignRight',
        r'Qt::AlignmentFlag::AlignTop': 'Qt::AlignTop',
        r'Qt::AlignmentFlag::AlignBottom': 'Qt::AlignBottom',
        r'Qt::AlignmentFlag::AlignVCenter': 'Qt::AlignVCenter',
        r'Qt::AlignmentFlag::AlignHCenter': 'Qt::AlignHCenter',
        
        # Qt Window Flags
        r'Qt::WindowType::Window': 'Qt::Window',
        r'Qt::WindowType::Dialog': 'Qt::Dialog',
        r'Qt::WindowType::Tool': 'Qt::Tool',
        
        # QSlider
        r'QSlider::TickPosition::TicksAbove': 'QSlider::TicksAbove',
        r'QSlider::TickPosition::TicksBelow': 'QSlider::TicksBelow',
        r'QSlider::TickPosition::TicksBothSides': 'QSlider::TicksBothSides',
        r'QSlider::TickPosition::NoTicks': 'QSlider::NoTicks',
        
        # QComboBox
        r'QComboBox::InsertPolicy::InsertAtTop': 'QComboBox::InsertAtTop',
        r'QComboBox::InsertPolicy::InsertAtBottom': 'QComboBox::InsertAtBottom',
        r'QComboBox::InsertPolicy::InsertAtCurrent': 'QComboBox::InsertAtCurrent',
        r'QComboBox::InsertPolicy::InsertAfterCurrent': 'QComboBox::InsertAfterCurrent',
        r'QComboBox::InsertPolicy::InsertBeforeCurrent': 'QComboBox::InsertBeforeCurrent',
        r'QComboBox::InsertPolicy::InsertAlphabetically': 'QComboBox::InsertAlphabetically',
        
        # QTabWidget
        r'QTabWidget::TabPosition::North': 'QTabWidget::North',
        r'QTabWidget::TabPosition::South': 'QTabWidget::South',
        r'QTabWidget::TabPosition::East': 'QTabWidget::East',
        r'QTabWidget::TabPosition::West': 'QTabWidget::West',
        
        # QTabBar
        r'QTabBar::Shape::RoundedNorth': 'QTabBar::RoundedNorth',
        r'QTabBar::Shape::RoundedSouth': 'QTabBar::RoundedSouth',
        r'QTabBar::Shape::RoundedEast': 'QTabBar::RoundedEast',
        r'QTabBar::Shape::RoundedWest': 'QTabBar::RoundedWest',
        r'QTabBar::Shape::TriangularNorth': 'QTabBar::TriangularNorth',
        r'QTabBar::Shape::TriangularSouth': 'QTabBar::TriangularSouth',
        r'QTabBar::Shape::TriangularEast': 'QTabBar::TriangularEast',
        r'QTabBar::Shape::TriangularWest': 'QTabBar::TriangularWest',
    }
    
    # Aplicar correcciones
    changes_made = 0
    for old_pattern, new_pattern in corrections.items():
        matches = re.findall(old_pattern, content)
        if matches:
            content = re.sub(old_pattern, new_pattern, content)
            changes_made += len(matches)
            print(f"  ✅ Corregido: {old_pattern} → {new_pattern} ({len(matches)} ocurrencias)")
    
    # Guardar el archivo corregido
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Se corrigieron {changes_made} referencias de Qt6 a Qt5")
        return True
    else:
        print("ℹ️  No se encontraron referencias de Qt6 para corregir")
        return False

def main():
    """Función principal"""
    print("🔧 Corrector de sintaxis Qt6 → Qt5")
    print("=" * 40)
    
    # Buscar archivos .ui en el directorio actual
    ui_files = [f for f in os.listdir('.') if f.endswith('.ui')]
    
    if not ui_files:
        print("❌ No se encontraron archivos .ui en el directorio actual")
        return
    
    print(f"📁 Archivos .ui encontrados: {', '.join(ui_files)}")
    print()
    
    # Corregir cada archivo
    for ui_file in ui_files:
        fix_qt_syntax(ui_file)
        print()
    
    print("🎉 Proceso completado!")
    print("💡 Para evitar este problema en el futuro:")
    print("   1. Configura Qt Creator para usar Qt 5.x")
    print("   2. O ejecuta este script después de cada edición")
    print("   3. Consulta qt_creator_config.md para más detalles")

if __name__ == "__main__":
    main() 