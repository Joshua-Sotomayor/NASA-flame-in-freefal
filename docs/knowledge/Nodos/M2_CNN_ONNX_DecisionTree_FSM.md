---
type: dl-model
model_id: M2
artifacts: [flame_cnn.onnx, sensor_tree.joblib]
tags: [nasa/dl, pytorch, onnx, fsm, decision-tree]
---

# Modelo 2: CNN PyTorch (ONNX) + DecisionTreeClassifier + FSM Determinista

Arquitectura de ejecucion determinista y visualizacion explicable para el Gemelo Digital del ducto `Saffire/CIR`.

## Entrenamiento e Inferencia
- Rama optica: CNN entrenada en **Google Colab T4 GPU** (`notebooks/AERO_IGNIS_Colab_Training.ipynb`) con frames representativos de [[PSI-25_BASS-II]], [[PSI-24_FLEX]], [[PSI-146_ACME-Flame-Design]] y [[PSI-98_SAFFIRE-I]], exportada a `flame_cnn.onnx` (<15 MB) con digest `SHA-256`.
- Clases opticas: `0: Nominal`, `1: Llama Esferica Azul 0g`, `2: Llama Fria NTC`, `3: Propagacion Abierta`.
- Rama tabular: `DecisionTreeClassifier` sobre $\Delta T/\Delta t$, `CO (ppm)`, aerosol submicrónico ($<0.1\,\mu\text{m}$) y flujo de aire, exponiendo la regla exacta activada.
- Seguridad: `DeterministicFsmController` con histéresis e interlock de pérdida serial (`comm_ok=False -> FALLA_SEGURA`).

## Conexiones
- Cumple [[O3_Deteccion_Supresion_Gemelo_FSM]]
- Verificado por [[09_Estrategia_TDD_y_Redaccion_Writing_Craft]]
- Liderado por [[Rol_Mecatronica_y_Control]]
