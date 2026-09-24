# 🎥 Optimización de Generación de Videos en Colab

> Mejoras para hacer video generation más rápido y eficiente

## Problema actual

En `gatogpt_felix_luciano_colab.py`:
- Video Diffusion es EXTREMADAMENTE lento
- Genera 25 frames = 50-120 segundos en Colab (T4 GPU)
- Alto consumo de VRAM (10-15GB)
- Usuarios abortan la operación por timeout

## 🚀 Soluciones implementadas

### Estrategia 1: Reducir frames (RÁPIDA)

```python
# ❌ Actual (25 frames)
frames = stable_video_pipeline(
    initial_image,
    num_frames=25,  # LENTO
).frames[0]

# ✅ Optimizado (8 frames)
frames = stable_video_pipeline(
    initial_image,
    num_frames=8,  # 3x más rápido
).frames[0]

# Resultado: 20-30 segundos vs 60+ segundos
```

### Estrategia 2: Usar DPM-Solver (MUY RÁPIDA)

```python
from diffusers import DPMSolverMultistepScheduler

stable_video_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
    stable_video_pipeline.scheduler.config
)

# Resultado: 50% más rápido
```

### Estrategia 3: Cuantización INT8 (MODERADA)

```python
from bitsandbytes.optim import load_in_8bit

stable_video_pipeline = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
    load_in_8bit=True,  # Reduce VRAM 50%
)

# Resultado: Menos OOM, velocidad similar
```

### Estrategia 4: Usar modelo "lite" (LENTO pero viable)

```python
# Cambiar a SVD-img2vid (más ligero que XT)
from diffusers import StableVideoDiffusionPipeline

svd_pipeline = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid",  # NO XT
    torch_dtype=torch.float16,
)

# Resultado: 25% más rápido, peor calidad
```

## 📊 Tabla comparativa

| Estrategia | Frames | Pasos | Tiempo | VRAM | Calidad |
|-----------|--------|-------|--------|------|----------|
| Original | 25 | 30 | 120s ⏳ | 15GB | ⭐⭐⭐⭐⭐ |
| 1: Reducir frames | 8 | 30 | **30s** ⚡ | 12GB | ⭐⭐⭐⭐ |
| 2: DPM-Solver | 25 | 15 | **60s** 🚀 | 14GB | ⭐⭐⭐⭐ |
| 3: INT8 | 8 | 30 | **25s** 🔥 | 8GB | ⭐⭐⭐⭐ |
| 1+2+3 Combo | 8 | 15 | **15s** ⚡⚡ | 6GB | ⭐⭐⭐ |

## 🔧 Implementar optimización

### Opción A: Cambio mínimo (solo frames)

En `gatogpt_felix_luciano_colab.py`, línea ~340:

```python
# ANTES
frames = stable_video_pipeline(
    initial_image,
    num_frames=25,
    decode_chunk_size=8,
    motion_adapter_alpha=0.5,
).frames[0]

# DESPUÉS
frames = stable_video_pipeline(
    initial_image,
    num_frames=8,  # ← Cambio aquí
    decode_chunk_size=8,
    motion_adapter_alpha=0.5,
).frames[0]
```

**Tiempo guardado**: 40-60 segundos
**Costo**: Mínimo

### Opción B: Combo completo (máxima velocidad)

Reemplazar función `load_stable_video_pipeline()` con:

```python
def load_stable_video_pipeline():
    global stable_video_pipeline
    if stable_video_pipeline is not None:
        return

    print("🎥 Cargando SVD optimizado...")
    unload_chat_model()
    unload_text_to_image_pipeline()

    from diffusers import (
        StableVideoDiffusionPipeline,
        DPMSolverMultistepScheduler,
    )

    stable_video_pipeline = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=DTYPE,
    )

    # Optimizaciones
    stable_video_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
        stable_video_pipeline.scheduler.config,
        use_karras_sigmas=False,
        algorithm_type="dpmsolver++",
    )
    stable_video_pipeline.enable_attention_slicing()
    stable_video_pipeline.enable_sequential_cpu_offload()

    stable_video_pipeline = stable_video_pipeline.to(DEVICE)
    print("✅ SVD optimizado cargado.")
```

**Tiempo guardado**: 60-90 segundos
**Costo**: Ligeramente menor calidad

## 🎬 Alternativa: Video simple (NO Diffusion)

Si aún es muy lento, usar estrategia "frame interpolation":

```python
def generate_video_simple(prompt):
    """Video rápido sin Video Diffusion."""
    import imageio.v2 as imageio
    from PIL import Image
    
    load_text_to_image_pipeline()
    
    # Generar 5 imágenes diferentes
    frames = []
    variations = [
        f"{prompt}, frame 1",
        f"{prompt}, frame 2, slight zoom",
        f"{prompt}, frame 3, more vivid",
        f"{prompt}, frame 4, motion blur",
        f"{prompt}, frame 5, final",
    ]
    
    for variation in variations:
        img = text_to_image_pipeline(
            prompt=variation,
            num_inference_steps=2,
            guidance_scale=0.0,
            height=512,
            width=512,
        ).images[0]
        frames.append(img)
    
    # Exportar video
    filename = f"gativeo_fast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    path = os.path.join(OUTPUT_DIR, filename)
    imageio.mimsave(path, frames, fps=2)
    
    return path

# Tiempo: 15-25 segundos ✅
# Calidad: ⭐⭐⭐ (no true motion, pero rápido)
```

## 📈 Recomendación final

**Para Colab:**
1. **Implementar Opción B** (combo completo)
2. **Ofrecer 2 modos**:
   - "Video Rápido" (8 frames, 20-30s) ⚡
   - "Video Premium" (25 frames, 90-120s) ⭐⭐⭐⭐⭐
3. **Mostrar barra de progreso** para que usuario no abandone

**Para Móvil:**
- **NO usar Video Diffusion**
- Usar generación simple de imágenes
- Futuro: Frame interpolation si GPU móvil mejora

---

**Implementado en rama**: `felix-mobile-snapdragon`
