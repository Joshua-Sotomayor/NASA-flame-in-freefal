---
type: ml-model
model_id: M1
artifacts: [flammability_rf.joblib, burntime_gbr.joblib]
tags: [nasa/ml, random-forest, gradient-boosting, shap]
---

# Modelo 1: RandomForestClassifier + GradientBoostingRegressor (`FlammabilityPredictor`)

Pipeline tabular que combina ecuaciones adimensionales ($	ext{Da}$, $	ext{Pe}$, $V_f$) con modelos ensamblados entrenados sobre `BASS-II (PSI-25)` y `Saffire I-VI`.

## Entradas y Entrenamiento
- Entrenamiento rapido CPU local (`backend/train_models.py`) y afinamiento con datos OSDR completos en [[08_Plan_Entrenamiento_ML_DL_y_Google_Colab]].
- Variables: `Percent O2`, `Pressure (atm)`, `Air Flow (cm/s)`, `Sample Thickness (cm)`, `Material`, `Flow Direction`.
- Salida explicable: probabilidad de extincion, `Burn Time (s)`, $V_f$ y `feature_importances_` auditable.

## Conexiones
- Cumple [[O2_Prediccion_Inflamabilidad_Habitats]] y apoya [[O4_Spinoffs_Terrestres_y_Forense]]
- Liderado por [[Rol_Combinado_Sinergia]]
