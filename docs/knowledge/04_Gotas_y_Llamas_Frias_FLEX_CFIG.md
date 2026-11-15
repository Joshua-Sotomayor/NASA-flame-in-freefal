---
type: domain-analysis
facility: "ISS-CIR (MDCA)"
investigations: [PSI-24, PSI-27, PSI-78, PSI-79, PSI-138]
tags: [nasa/droplets, cool-flames, flex, cfi-g, dl-cnn]
---

# Gotas Liquidas y Llamas Frias (FLEX, FLEX-2J, MDCA-FLEX-ICE, CFI-G)

Las investigaciones de gotas y gases en el **Combustion Integrated Rack (CIR)** revelaron fenomenos invisibles al ojo humano que invalidan los detectores opticos convencionales.

---

## 1. Hallazgos Cientificos y Variables del Repositorio

| Investigacion | Combustibles y Configuracion | Fenomeno Critico y Dato Util |
| :--- | :--- | :--- |
| [[PSI-24_FLEX]] | Gotas de heptano, metanol, decano ($2\text{–}5\text{ mm}$) en MDCA | **Descubrio llamas frias ($500\text{–}800\text{ K}$):** tras extinguirse la llama caliente, la gota continua oxidandose casi invisible en UV $\text{OH}^*$ ($310\text{ nm}$) y puede reencenderse. |
| [[PSI-27_FLEX-2]] | Pares de gotas y atmosferas diluidas ($\text{N}_2, \text{CO}_2, \text{He}, \text{Xe}$) | Cuantifica concentraciones limite de diluyente para apagar llamas calientes y frias sin intoxicar la cabina. |
| [[PSI-78_FLEX-2J]] | Arreglos lineales y planos de gotas (NASA-JAXA) | Velocidad de propagacion por salto termico entre gotas vecinas (*array flame spread*). |
| [[PSI-79_MDCA-FLEX-ICE]] | Gotas bicomponentes (ASI Italia) | Evaporacion diferencial y microexplosiones cuando cambian las fracciones de mezcla liquida. |
| [[PSI-138_CFI-G]] | Butano, propano y DME gaseoso hasta $85\%\text{ O}_2$ | Llamas frias difusivas en fase gaseosa (*inside-out flames*) gobernadas por cinetica de coeficiente de temperatura negativo (NTC). |

---

## 2. Como Alimentan el Deep Learning y la FSM

1. **Etiquetado de la CNN (`flame_cnn.onnx` — [[M2_CNN_ONNX_DecisionTree_FSM]]):**
   - `FLEX` y `CFI-G` aportan las firmas opticas de **baja luminancia y corona debil UV/termica** que forman la clase **`2: Llama Fria NTC`**, separandola de `0: Nominal` y de `1: Llama Esferica Azul 0g`.
   - En **Google Colab**, aplicamos *data augmentation* rotacional de $360^\circ$ (valido fisicamente por la simetria esferica en $0g$) para multiplicar las muestras de entrenamiento sin sobreajuste.
2. **Regla de Enclavamiento en `DeterministicFsmController`:**
   - Si la CNN clasifica `Llama Fria NTC`, la FSM **bloquea el retorno automatico a `NORMAL`** aunque la camara visible no muestre llama naranja brillante; exige verificacion de enfriamiento termico ($\Delta T/\Delta t \le 0$).
3. **Generalizacion en `M1` y Comparador de Supresores:**
   - `FLEX-2J` y `MDCA-FLEX-ICE` aportan casos de gotas multiples y mezclas a `M1` y parametros de dilucion inerte frente a niebla fina `PFE`.

---

## 3. Roles y Objetivos

- **Objetivos:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]].
- **Dominios:** [[Rol_Combinado_Sinergia]] (`FLEX`, `FLEX-2`) y [[Rol_Mecatronica_y_Control]] (`FLEX-2J`, `MDCA-FLEX-ICE`, `CFI-G`).
