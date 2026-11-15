# Dependencias y Ejecución Local (AERO-IGNIS)

## 1. Instalación de paquetes

Desde la raíz del proyecto (`NASA/`):

```powershell
# Dependencias ligeras de producción e inferencia (Render 512 MB RAM, sin torch)
pip install -r requirements.txt

# O entorno completo para desarrollo, reentrenamiento PyTorch y suite pytest
pip install -r requirements/dev.txt
```

> Nota de despliegue: En producción (`requirements.txt` -> `requirements/base.txt`), el servidor ejecuta inferencia de `flame_cnn.onnx` mediante `onnxruntime` con pesos verificados por `SHA-256`, evitando instalar `torch` para mantenerse holgado dentro de los `512 MB` de RAM gratuitos en Render.

## 2. Arranque del servidor web

Se admiten dos formas de ejecución equivalentes:

```powershell
# Opción A: desde la carpeta raíz del repositorio
py backend/main.py

# Opción B: directamente desde la carpeta backend/
cd backend
py main.py
```

También puede iniciarse con recarga en desarrollo mediante Uvicorn desde la raíz:

```powershell
py -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Una vez activo, abrir en el navegador: `http://127.0.0.1:8000/`.
