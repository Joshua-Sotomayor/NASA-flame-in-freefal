# Guía de Despliegue Todo-en-Uno: Render Free + UptimeRobot (`$0 USD`)

> Estrategia de producción para **AERO-IGNIS SI (`M-12`)**: publicar la API FastAPI, el dashboard estático (`frontend/`) y los modelos verificados por `SHA-256` dentro de un único servicio web en **Render** (`512 MB RAM`), mantenido activo con **UptimeRobot** (`$0 USD`).

---

## 1. Arquitectura Elegida y Justificación Técnica

1. **Un solo origen HTTPS en Render (`https://<tu-app>.onrender.com`):**
   - `backend/main.py` ya sirve el frontend (`/`, `/styles.css`, `/app.js`, `/GeistPixel-Square.woff2`, `/assets/museum/*`) y los 6 endpoints `/api/v1/*`.
   - Evita configurar CORS entre dos dominios y respeta `Content-Security-Policy: default-src 'self'` de forma nativa.
2. **Ahorro de RAM para el límite gratuito de 512 MB (`requirements/base.txt`):**
   - Los pesos entrenados en `artifacts/models/` ocupan **~370 KB** en disco (`flammability_rf.joblib`, `burntime_gbr.joblib`, `flame_cnn.onnx`, `sensor_tree.joblib`, `psi_tfidf_kmeans.joblib` + `manifest.sha256.json`).
   - En ejecución, el servidor usa `onnxruntime` y `scikit-learn` sin importar `torch`, `onnx` ni `pandas`. Por eso `requirements.txt` (`-r requirements/base.txt`) excluye PyTorch (`~2.5 GB` en Linux) y conserva un arranque ligero debajo del tope de `512 MB`.
3. **Compatibilidad con UptimeRobot Free (`HEAD` + `GET`) y Proxy (`X-Forwarded-For`):**
   - `/api/v1/health` y `/` aceptan explícitamente `GET` y `HEAD` (`200 OK`), evitando respuestas `405 Method Not Allowed` en monitores HTTP(s) gratuitos.
   - `PayloadAndRateLimitMiddleware` extrae el primer salto de `X-Forwarded-For` para aislar la cuota de tasa de cada visitante detrás del balanceador de Render.

---

## 2. Pasos para Desplegar en Render (`$0 USD`)

### Opción A — Blueprint automático (`render.yaml`, recomendada)
1. Ingresa a [dashboard.render.com](https://dashboard.render.com/) con la cuenta vinculada a GitHub.
2. Selecciona **New + $\rightarrow$ Blueprint**.
3. Elige el repositorio `Joshua-Sotomayor/NASA-flame-in-freefal` (rama `main`).
4. Render detectará [render.yaml](../render.yaml) automáticamente (`name: aero-ignis-si`, `plan: free`, `healthCheckPath: /api/v1/health`). Haz clic en **Apply**.

### Opción B — Web Service manual (si prefieres crearlo paso a paso)
1. En Render haz clic en **New + $\rightarrow$ Web Service** y conecta el repositorio (`Branch: main`, `Runtime: Python 3`).
2. Configura exactamente estos campos:
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1`
   - **Health Check Path:** `/api/v1/health`
   - **Instance Type:** `Free` (`$0/month`)
3. En **Environment Variables**, agrega:
   - `PYTHON_VERSION` = `3.12.7`
   - `WEB_CONCURRENCY` = `1`
4. Espera a que el log muestre `Application startup complete` y verifica estas dos URLs en navegador o modo incógnito:
   - `https://<tu-app>.onrender.com/api/v1/health` $\rightarrow$ `{"status":"ok","models_verified_sha256":true,"psi_count":24}`
   - `https://<tu-app>.onrender.com/` $\rightarrow$ Dashboard **NASA + ENREDADOS** con `0` errores en consola.

---

## 3. Mantener el Servicio Despierto con UptimeRobot (`$0 USD`)

Render Free suspende el contenedor tras **15 minutos** sin tráfico entrante (reactivarlo toma `~30–50 s`). Para evitar el *cold start* durante la evaluación del jurado:

1. Entra a [uptimerobot.com](https://uptimerobot.com/) (plan **Free**, `$0 USD`).
2. Haz clic en **+ Add New Monitor**:
   - **Monitor Type:** `HTTP(s)`
   - **Friendly Name:** `AERO-IGNIS SI - Render Health`
   - **URL (or IP):** `https://<tu-app>.onrender.com/api/v1/health`
   - **Monitoring Interval:** `Every 5 minutes`
3. Guarda el monitor. Como `/api/v1/health` soporta peticiones `HEAD` y `GET`, UptimeRobot recibirá `HTTP 200` cada 5 minutos (`< 15 min` de inactividad) sin consumir cuota de rutas ML (`bucket="general"`, 1 petición cada 5 min frente a límite de `60 req/min`).

---

## 4. Nota Opcional sobre Netlify

Si más adelante decidieran separar el frontend estático en CDN manteniendo el backend en Render, [netlify.toml](../netlify.toml) ya incluye el proxy `/api/*` y las cabeceras OWASP. Para habilitar CORS desde un dominio externo concreto en Render, definir la variable de entorno:

- `ALLOWED_ORIGINS` = `https://<tu-sitio>.netlify.app`
