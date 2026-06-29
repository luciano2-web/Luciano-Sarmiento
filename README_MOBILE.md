# 🐱 GatoGPT Félix - Versión Snapdragon 8 Gen 2

> Chat inteligente con generación de imágenes **100% local** para tu móvil Snapdragon 8 Gen 2.

## 📋 Requisitos

### Hardware
- **Dispositivo**: Snapdragon 8 Gen 2 (OnePlus 12, Xiaomi 14, etc.)
- **RAM**: Mínimo 8GB (12GB recomendado)
- **Almacenamiento**: 10GB libre para modelos + salida
- **GPU**: Adreno 8 Gen 2 (recomendado usar CPU primero)

### Software
- Python 3.9 o superior
- Android 12+ (usando Termux o similar) o iOS con Pythonista
- pip actualizado

## 🚀 Instalación

### Opción 1: En Termux (Android)

```bash
# 1. Instalar Termux desde F-Droid (gratis)
# 2. Abrir Termux y ejecutar:

pkg update && pkg upgrade -y
pkg install python3 python3-dev clang -y

# 3. Clonar repositorio
git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
cd Luciano-Sarmiento
git checkout felix-mobile-snapdragon

# 4. Crear entorno virtual
python3 -m venv venv_felix
source venv_felix/bin/activate

# 5. Instalar dependencias
pip install --upgrade pip
pip install -r requirements_mobile.txt

# ⚠️ NOTA: Esto descargará 5-8GB
# Conectar a WiFi y esperar 30-60 minutos
```

### Opción 2: En iOS (Pythonista)

1. Descargar [Pythonista 3](https://apps.apple.com/app/pythonista-3/id1357750361) ($9.99)
2. Ejecutar:
   ```python
   import requests
   code = requests.get("https://raw.githubusercontent.com/luciano2-web/Luciano-Sarmiento/felix-mobile-snapdragon/gatogpt_felix_mobile.py").text
   exec(code)
   ```
3. Las dependencias deben instalarse automáticamente

## 📱 Uso

### Ejecutar la app

```bash
python3 gatogpt_felix_mobile.py
```

**Primera ejecución**:
- ⏳ Descargará ~2GB de modelos (5-10 minutos)
- 🔋 Consumirá mucho CPU/GPU
- 📈 Después, cada inicio es rápido

### Comandos

| Comando | Descripción | Tiempo |
|---------|-------------|--------|
| `Hola Félix` | Chat normal | 2-5s |
| `¿Cuál es 2+2?` | Pregunta matemática | 3-8s |
| `@gatimage un gato genio` | Generar imagen | 30-60s |
| `@gatimage` | Imagen aleatoria | 30-60s |

### Ejemplos de chat

```
TÚ: Hola Félix
🐱 Félix: ¡Miau! Hola, soy Félix, tu asistente felino. 
¿Qué necesitas hoy? 🐾

TÚ: Ayúdame a estudiar fracciones
🐱 Félix: Claro, prrr. Una fracción es una parte de un todo.
Por ejemplo: 1/2 es la mitad de algo. ¿Quieres más ejemplos? 🎓

TÚ: @gatimage un gato estudiando matemáticas en la biblioteca
🐱 Félix: ¡Miau! Generé una imagen. 🐾
🖼️ ~/gatogpt_mobile_outputs/gatimage_20241201_153045.png
```

## ⚡ Optimizaciones para Snapdragon 8 Gen 2

### Modelos ultra-ligeros
- **Chat**: Microsoft Phi-2 (2.7B) - 5GB descargado, 3GB en memoria
- **Imagen**: Segmind SSD-1B (832M) - 2GB descargado, 1.5GB en memoria

### Técnicas implementadas
1. **INT8 Quantization** - Reduce tamaño 75%
2. **Lazy Loading** - Carga modelos bajo demanda
3. **Memory Offloading** - Carga CPU↔GPU automática
4. **Attention Slicing** - Reduce picos de RAM
5. **VAE Tiling** - Procesa imagen en bloques

### Rendimiento esperado

| Tarea | Tiempo | RAM |
|-------|--------|-----|
| Chat simple | 3-8s | 4-5GB |
| Chat complejo | 8-15s | 5-6GB |
| Imagen (primera) | 40-60s | 6-8GB |
| Imagen (siguiente) | 35-50s | 6-7GB |

## 🔧 Configuración

Editar `felix_mobile_config.yaml` para personalizar:

```yaml
models:
  chat:
    id: "gpt2"  # Cambiar a gpt2 si RAM < 6GB
    max_tokens: 50  # Reducir para más velocidad
  image:
    steps: 10  # Menos pasos = más rápido
    resolution: 384  # Menor resolución = menos RAM
```

## 🐛 Troubleshooting

### "Out of Memory" (OOM)
```bash
# Cambiar a modelo más ligero
sed -i 's/microsoft\/phi-2/gpt2/g' gatogpt_felix_mobile.py
```

### App se congela
```bash
# Reducir pasos de imagen
sed -i 's/num_inference_steps=15/num_inference_steps=8/g' gatogpt_felix_mobile.py
```

### Descarga muy lenta
```bash
# Usar espejo de Hugging Face
export HF_ENDPOINT=https://hf-mirror.com
python3 gatogpt_felix_mobile.py
```

### GPU no se detecta
```python
import torch
print(torch.cuda.is_available())  # Debe ser True
print(torch.cuda.get_device_name())  # Debe ser Adreno
```

## 📊 Comparación: Colab vs Móvil

| Métrica | Colab T4 | Snapdragon 8 Gen 2 |
|---------|----------|--------------------|
| Chat (5 tokens/s) | **1-2s** ⚡ | 3-8s ✅ |
| Imagen (2 pasos) | **5-10s** ⚡ | 35-60s ✅ |
| Costo/mes | **$9.99** 💰 | **Gratis** 🎉 |
| Privacidad | Nube ☁️ | Local 🔒 |
| Always-on | No | **Sí** ✅ |

## 🎯 Próximas mejoras

- [ ] Soporte GPU Adreno nativo (ahora usa CPU)
- [ ] Caché de imágenes generadas
- [ ] Integración con WhatsApp/Telegram
- [ ] Voz (text-to-speech)
- [ ] Fine-tuning de Félix con datos personales
- [ ] Versión iOS nativa (SwiftUI)

## 📚 Recursos

- [Documentación PyTorch Mobile](https://pytorch.org/mobile/home/)
- [Hugging Face Optimized Models](https://huggingface.co/models?other=mobile)
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Termux Wiki](https://wiki.termux.com/)

## 📄 Licencia

MIT License - Siéntete libre de usar, modificar y distribuir.

## 🙋 Soporte

¿Problemas? Abre un [issue en GitHub](https://github.com/luciano2-web/Luciano-Sarmiento/issues)

---

**Hecho con ❤️ y ronroneos por Luciano**

🐱 *"El futuro es local, rápido y felino."* 🐾
