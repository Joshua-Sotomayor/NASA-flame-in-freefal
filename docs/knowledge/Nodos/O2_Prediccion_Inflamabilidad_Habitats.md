---
type: objective
objective_id: O2
domain: Combinado
tags: [nasa/objective, flammability, artemis, lunar-habitat]
---

# Objetivo 2: Prediccion de Inflamabilidad y Extincion en Habitats

Predecir si un material o atmosfera se auto-extingue (`Extinguished: Yes/No`), su tiempo de quemado (`Burn Time`) y su tasa de propagacion $V_f$ en la ISS ($21\%\text{ O}_2, 14.7\text{ psi}$), habitats lunares ($34\%\text{ O}_2, 8.2\text{ psi}$) y trajes EVA ($100\%\text{ O}_2, 4.3\text{ psi}$).

## Conexiones Clave
- Modelo principal: [[M1_RandomForest_GBR_Inflamabilidad]]
- Datasets nucleares: [[PSI-25_BASS-II]], [[PSI-26_BASS]], [[PSI-98_SAFFIRE-I]], [[PSI-103_SAFFIRE-IV]], [[PSI-104_SAFFIRE-V]], [[PSI-109_NCA]], [[PSI-132_BRE]]
- Rol responsable: [[Rol_Combinado_Sinergia]] y [[Rol_Mecatronica_y_Control]]
