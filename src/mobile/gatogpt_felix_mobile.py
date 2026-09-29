# -*- coding: utf-8 -*-
"""
🐱 GatoGPT Félix - Versión Mobile para Snapdragon 8 Gen2

Este archivo es un wrapper para compatibilidad hacia atrás.
El código principal ahora está en src/mobile/main.py

Para ejecutar la app móvil, usa:
    python src/mobile/main.py

O simplemente:
    python -m src.mobile.main
"""

import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Redirigir a main.py
if __name__ == "__main__":
    print("⚠️ Este archivo es un wrapper. Redirigiendo a src/mobile/main.py...")
    print("Para ejecutar directamente, usa: python src/mobile/main.py")
    
    # Ejecutar main.py
    from src.mobile.main import FelixMobileApp, FelixConsole, KIVY_AVAILABLE
    
    if KIVY_AVAILABLE:
        try:
            FelixMobileApp().run()
        except Exception as e:
            print(f"❌ Error al ejecutar Kivy: {e}")
            print("Falling back a modo consola...")
            FelixConsole().run()
    else:
        FelixConsole().run()
