# 🐱 GatoGPT Félix - Proyecto Unificado

Chat local estilo ChatGPT con personalidad felina, optimizado para Colab y Android.

## Estructura

```
gatogpt-felix/
├── README.md
├── colab/
│   └── gatogpt_felix_colab.py      # Versión Google Colab
├── mobile/
│   ├── gatogpt_felix_mobile.py     # Versión Android/iOS (Kivy)
│   ├── buildozer.spec              # Config Buildozer APK
│   └── requirements_mobile.txt
├── web/
│   └── gatogpt_felix_web.py        # Versión web (Gradio)
├── core/
│   ├── __init__.py
│   ├── personality.py              # Personalidad de Félix
│   ├── chat_engine.py              # Motor de chat unificado
│   ├── image_gen.py                # Generación de imágenes
│   └── utils.py                    # Utilidades
└── docs/
    └── OPTIMIZACIONES.md
```

## Versiones

### 1. Google Colab (Python)
- Chat local con Qwen3-0.6B
- Imagen: SD-Turbo local
- Video simple: secuencia de imágenes
- Interfaz Gradio

### 2. Mobile (Kivy)
- Modelo: TinyLlama 1.1B (más ligero que phi-2)
- Interfaz nativa Android/iOS
- APK compilable con Buildozer

### 3. Web (Gradio)
- Versión deployable
- Compatible con Spaces de Hugging Face

## Instalación

```bash
# Colab
!pip install transformers accelerate torch diffusers gradio pillow imageio

# Mobile
pip install -r mobile/requirements_mobile.txt
```
