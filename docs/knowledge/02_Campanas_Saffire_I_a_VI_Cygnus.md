---
type: domain-analysis
facility: "Cygnus Spacecraft"
investigations: [PSI-98, PSI-101, PSI-102, PSI-103, PSI-104, PSI-105]
tags: [nasa/cygnus, saffire, habitat-lunar, ml-training]
---

# Campanas Saffire I a VI (Vehiculo Cygnus)

Las seis misiones **Saffire** (*Spacecraft Fire Experiment*) ejecutaron incendios controlados a gran escala dentro de vehiculos de carga **Cygnus** tras desacoplarse de la ISS. Son el puente directo entre ensayos milimetricos en laboratorio (`BASS`, `FLEX`) y incendios reales en cabinas habitables.

---

## 1. Inventario y Contenido del Repositorio

| Investigacion | Escala y Combustibles | Variables Atmosfericas | Aporte Principal al Proyecto |
| :--- | :--- | :--- | :--- |
| [[PSI-98_SAFFIRE-I]] | Panel SIBAL $0.4 \times 0.94\text{ m}$ ($11.41\text{ GB}$); tabla de 13 cols | $21\%\text{ O}_2$, $14.7\text{ psi}$, flujo $20\text{ cm/s}$ | Linea base de propagacion a escala real y calibracion de camaras duales. |
| [[PSI-101_SAFFIRE-II]] | 9 muestras: PMMA plano/ranurado, SIBAL, Nomex, silicona | Flujo concurrente y opuesto | Comparativa directa entre polimeros inflamables y textiles resistentes (`Nomex`). |
| [[PSI-102_SAFFIRE-III]] | Panel grande SIBAL repetido a mayor ventilacion | Flujo alto de $30\text{ cm/s}$ | Demuestra que aumentar ventilacion acelera el frente de llama concurrente. |
| [[PSI-103_SAFFIRE-IV]] | Multiples materiales en atmosfera enriquecida | $30\text{–}34\%\text{ O}_2$, baja presion | Primera validacion a gran escala de riesgo de ignicion en atmosferas Artemis. |
| [[PSI-104_SAFFIRE-V]] | Tejido SIBAL y polimeros de cabina | $\sim 8.2\text{ psi}$ ($56.5\text{ kPa}$), $30\text{–}34\%\text{ O}_2$ | Referencia de certificacion normativa para **habitats lunares y rovers**. |
| [[PSI-105_SAFFIRE-VI]] | Multiples muestras con perfil quimico completo | Seguimiento de $\text{CO}$, $\text{HF}$, $\text{HCl}$ | Define limites toxicos de humo y sobrepresion antes de activar `CONTENCION`. |

---

## 2. Como Se Usa en Entrenamiento ML/DL

1. **Modelo 1 ([[M1_RandomForest_GBR_Inflamabilidad]]):**
   - `Saffire-I` a `Saffire-V` aportan corridas de alta concentracion de oxigeno ($30\text{–}34\%\text{ O}_2$) y baja presion ($8.2\text{ psi}$), donde un modelo entrenado solo con datos de la ISS ($21\%\text{ O}_2$) subestimaria la velocidad de propagacion $V_f$.
   - Columnas utilizadas: `Material`, `Sample Thickness (cm)`, `Air Flow (cm/s)`, `Percent O2`, `Flow Direction` y `Burn Time (s)`.
2. **Modelo 2 ([[M2_CNN_ONNX_DecisionTree_FSM]]):**
   - En **Google Colab**, extraemos secuencias representativas de camara de `Saffire-I` y `Saffire-III` para entrenar la clase `3: Propagacion Abierta` de `flame_cnn.onnx`.
   - `Saffire-VI` fija los umbrales de `co_ppm` y gases acidos que disparan el `DecisionTreeClassifier`.
3. **Modelo 3 ([[M3_PCA_KMeans_TFIDF_TOPSIS]]):**
   - Las notas ISA-Tab de `Saffire-IV/V/VI` dominan los criterios `habitat` y `spinoff` dentro de `TopsisMultiCriteriaRanker`.

---

## 3. Roles y Objetivos

- **Objetivos cubiertos:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]].
- **Dominio:** [[Rol_Combinado_Sinergia]] (`Saffire-I/II/IV`), [[Rol_Mecatronica_y_Control]] (`Saffire-III` control de flujo) y [[Rol_Gestion_Industrial]] (`Saffire-V/VI` estandares lunares y toxicologia FMEA).
