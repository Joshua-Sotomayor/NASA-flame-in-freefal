---
type: domain-analysis
facility: "ISS-CIR / ISS-MSG"
investigations: [PSI-146, PSI-147, PSI-153, PSI-154, PSI-126, PSI-129]
tags: [nasa/acme, soot, e-field, smoke-point, same, daft]
---

# Llamas Gaseosas, Hollin, Punto de Humo y Campos Electricos

Este grupo cubre deteccion temprana de aerosoles, estabilidad aerodinamica de llama y supresion electrohidrodinamica sin fluidos consumibles.

---

## 1. Investigaciones del Bloque y Datos Clave

| Investigacion | Variables y Sensorica | Relevancia Ingenieril |
| :--- | :--- | :--- |
| [[PSI-146_ACME-Flame-Design]] | Camaras $\text{OH}^*/\text{CH}^*$, flujo estequiometrico en etileno/metano | Produce **llamas esfericas azules limpias sin hollin** (clase `1` en nuestra CNN `flame_cnn.onnx`). |
| [[PSI-147_ACME-s-Flame]] | Radiometros y medicion de diametro esferico hasta extincion | Calibra el umbral exacto de **extincion radiativa** para validar el limite inferior de $\text{Da}$ en `M1`. |
| [[PSI-153_ACME-CLD-Flame]] | Extincion laser de hollin ($635\text{ nm}$), camaras visibles | Distingue llamas laminares productoras de hollin amarillo frente a llamas azules limpias en la CNN. |
| [[PSI-154_ACME-E-FIELD]] | Electrodos de malla a $\pm 10\text{ kV}$, corriente ionica, video | Viento ionico que aplana/suprime llamas y emula gravedad parcial; alternativa tecnologica en supresion `O3`/`O4`. |
| [[PSI-126_SLICE]] | Altura de desprendimiento (*liftoff*) y punto de soplado (*blowout*) | Fija la velocidad de flujo superior donde la llama se desprende o apaga ($\text{Da}$ critico superior). |
| [[PSI-129_SPICE]] (+ `SAME/DAFT`) | Boquillas $0.7\text{–}2.0\text{ mm}$, punto de humo + particulas $<0.1\,\mu\text{m}$ | Demuestra que en $0g$ las particulas de humo se aglomeran y cambian la respuesta de detectores de ionizacion vs opticos. |

---

## 2. Aplicacion Directa al Entrenamiento y Control

1. **Rama Tabular del Detector Temprano (`sensor_tree.joblib`):**
   - `SPICE` junto con `SAME/DAFT` y `Spinoff Node 9407` calibran la regla `submicron_aerosol > 18.0 -> PRE_ALERTA` para detectar pirólisis de cables antes de que aparezca llama visible en la camara.
2. **Clasificador Optico (`flame_cnn.onnx`):**
   - `ACME Flame Design` y `ACME CLD` definen las firmas visuales de llama esferica simetrica frente a llama difusiva luminosa con hollin.
3. **Evaluacion Comparativa de Supresion (`GovernanceAndSpinoffService`):**
   - `ACME E-FIELD` entra en el arbol de decision de supresion como metodo activo sin agotamiento de agente (junto a `PFE` de niebla fina y $\text{CO}_2$).

---

## 3. Roles y Objetivos

- **Objetivos:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]].
- **Dominios:** Liderado por [[Rol_Mecatronica_y_Control]], con sinergia industrial en [[PSI-129_SPICE]] (`[[Rol_Combinado_Sinergia]]`).
