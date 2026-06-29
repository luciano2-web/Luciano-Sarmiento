# 🐱 GatoGPT Félix Mobile - Snapdragon 8 Gen2

**Chat local con IA en tu móvil. Sin internet, sin API, solo Félix y tú.**

## 📱 Soportado en

- ✅ **Android 12+** con Snapdragon 8 Gen2
- ✅ **iOS 15+** (experimental)
- ✅ **Computadora local** (Windows, macOS, Linux)

## 🚀 Inicio Rápido

### Opción 1: Computadora Local (Más fácil)

```bash
# 1. Clonar repo
git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
cd Luciano-Sarmiento
git checkout felix-mobile-snapdragon

# 2. Crear virtual env
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements_mobile.txt

# 4. Ejecutar
python gatogpt_felix_mobile.py
```

### Opción 2: Android (Complejo)

Necesitas:
- Python 3.9+
- Buildozer o python-for-android
- NDK de Android

```bash
# Instalar buildozer
pip install buildozer cython

# Generar spec
buildozer android debug

# Esperar compilación (15-30 min)
```

## 🎯 Comandos

### Chat Normal
```
🐾 Tú: ¿Cuál es el capital de Francia?
🐱 Félix: París, por supuesto. Allí hay gatos muy sofisticados. 🐾
```

### Generar Imagen
```
🐾 Tú: @gatimage un gato estudiando matemáticas
🐱 Félix: Generando imagen... (30-60 segundos)
✅ Imagen guardada en: ./felix_outputs/images/gatimage_20240115_143025.png
```

### Limpiar Chat
```
🐾 Tú: clear
✨ Chat limpiado.
```

### Salir
```
🐾 Tú: quit
🐱 Félix: ¡Hasta luego, Luciano! Ronronea... 🐾
```

## ⚙️ Optimizaciones para Snapdragon 8 Gen2

### 1. **Cuantización INT8**
- Reduce tamaño del modelo en 4x
- Pérdida mínima de calidad
- Uso de RAM: ~1.5GB vs 6GB sin cuantizar

### 2. **Modelos Ultra-Ligeros**
- **Chat**: Microsoft Phi-2 (2.7B) en lugar de 7B+
- **Imagen**: SSD-1B (1B) en lugar de 5B+

### 3. **Gestión Inteligente de Memoria**
- Descargar modelos de imagen después de usarlos
- Mantener modelo de chat en RAM (lo usas más)
- Garbage collection automático

### 4. **Resolución Reducida**
- Imágenes 256x256 (vs 512x512)
- Tokens limitados a 150 palabras
- Pasos de generación mínimos

## 📊 Benchmarks en Snapdragon 8 Gen2

| Tarea | Tiempo | RAM Pico | Notas |
|-------|--------|---------|-------|
| Carga inicial | 8-10s | 500MB | Primera vez descarga modelos |
| Chat (150 tokens) | 1.5-2s | 2.5GB | Rápido, modelo en RAM |
| Gen. Imagen (256x256) | 40-60s | 3.5GB | Limitado por GPU Adreno |
| Limpieza después | <1s | 500MB | Descarga modelo imagen |

## 🔧 Configuración Avanzada

Edita `felix_mobile_config.yaml`:

```yaml
models:
  chat:
    model_id: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Aún más ligero
  image:
    resolution: [256, 256]  # Reducir más si es necesario
    steps: 1  # Mínimo (borroso pero súper rápido)
```

## 🐛 Solución de Problemas

### "Out of Memory"
```bash
# Reducir resolución en config
resolution: [224, 224]

# O usar modelo de chat aún más ligero
model_id: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

### "Modelo descarga muy lentamente"
- Usa WiFi 5GHz
- Primera descarga es lenta (~2-5GB)
- Luego se cachea localmente

### "Imagen borrosa o extraña"
- Aumentar `steps` en config (pero será más lento)
- Usar prompt más descriptivo
- Ejemplo: `@gatimage un gato adorable, cute, ilustración bonita`

## 📁 Estructura de Archivos

```
Luciano-Sarmiento/
├── gatogpt_felix_mobile.py      ← Main app
├── requirements_mobile.txt       ← Dependencias
├── felix_mobile_config.yaml     ← Configuración
├── README_MOBILE.md             ← Este archivo
├── felix_outputs/               ← Imágenes generadas
│   └── images/
└── felix_models/                ← Cache de modelos descargados
```

## 🎨 Personalización de Félix

Edita `FELIX_SYSTEM_PROMPT` en `gatogpt_felix_mobile.py`:

```python
FELIX_SYSTEM_PROMPT = """
Eres Félix, un gato muy especial para [TU NOMBRE].
Tienes personalidad única, eres inteligente y juguetón.
Responde siempre en [IDIOMA] de forma corta y clara.
"""
```

## 📈 Mejoras Futuras

- [ ] Modo offline completo (sin descargar modelos)
- [ ] Voz (text-to-speech)
- [ ] Más comandos (@gatmusic, @gatdance)
- [ ] Interfaz gráfica mejorada (Kivy + Material Design)
- [ ] Sincronización en la nube opcional

## 📝 Licencia

MIT - Usa libremente

## 🤝 Contribuciones

¿Ideas para optimizar Félix? 
- Fork este repo
- Crea rama: `git checkout -b mejora/nueva-feature`
- Commit: `git commit -m "feat: descripción"`
- Push: `git push origin mejora/nueva-feature`
- Abre Pull Request

---

**Hecho con ❤️ para Luciano y su Snapdragon 8 Gen2**

🐱 *Félix te espera. Ronronea... 🐾*
