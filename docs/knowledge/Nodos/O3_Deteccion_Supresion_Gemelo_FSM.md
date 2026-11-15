---
type: objective
objective_id: O3
domain: Mecatronica y Control
tags: [nasa/objective, fsm, cnn, onnx, suppression]
---

# Objetivo 3: Deteccion Temprana, Supresion y Gemelo Digital con FSM

Ejecutar en tiempo real web un Gemelo Digital del ducto `Saffire/CIR` mediante fusion multimodal (`CNN .onnx` + `DecisionTreeClassifier`) y control determinista `NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA`.

## Conexiones Clave
- Modelo principal: [[M2_CNN_ONNX_DecisionTree_FSM]]
- Datasets criticos: [[PSI-24_FLEX]], [[PSI-138_CFI-G]], [[PSI-110_MSC]], [[PSI-129_SPICE]], [[PSI-146_ACME-Flame-Design]], [[PSI-154_ACME-E-FIELD]], [[PSI-102_SAFFIRE-III]], [[PSI-105_SAFFIRE-VI]]
- Rol lider: [[Rol_Mecatronica_y_Control]]
